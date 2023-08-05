use log::{debug, error};
use pyo3::{PyResult, PyClassShell};
use pyo3::exceptions::{ValueError};
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyIterator, PyTuple};
use std::io::{self, Write};
use std::net::TcpStream;

use crate::filewrapper::{FileWrapper, SendFile};
use crate::globals::{WSGIGlobals};
use crate::parse::get_environ;
use crate::pyutils::{with_gil, close_pyobject, PyGILState_STATE};
use crate::request::{WSGIRequest};
use crate::startresponse::{StartResponse, WriteResponse};


pub const HTTP500: &[u8] = b"HTTP/1.1 500 Internal Server Error\r\n\r\n";


pub struct WSGIResponse<'i> {
    pub pyobject: Option<PyObject>,
    pub iter: Option<PyIterator<'i>>,
    pub start_response: Option<PyObject>,
    pub complete: bool,
    pub sendfileinfo: bool,
    pub current_chunk: Vec<u8>,
    pub pos_in_chunk: usize
}


impl <'i>WSGIResponse<'i> {

    pub fn new() -> WSGIResponse<'i> {
        WSGIResponse {
            pyobject: None,
            iter: None,
            start_response: None,
            complete: false,
            sendfileinfo: false,
            current_chunk: Vec::new(),
            pos_in_chunk: 0
        }
    }

    pub fn set_pyobject(&mut self, mut pyobject: PyObject, py: Python<'i>) -> PyResult<()> {
        let iter = match PyIterator::from_object(py, &mut pyobject) {
            Ok(pyiter) => Some(pyiter),
            Err(_) => {
                None
            }
        };
        self.iter = iter;
        if let Ok(fw) = pyobject.extract::<&FileWrapper>(py) {
            if fw.sendfileinfo.fd != -1 {
                self.sendfileinfo = true;
            }
        }
        self.pyobject = Some(pyobject);
        Ok(())
    }

    pub fn set_error(&mut self) {
        self.current_chunk = HTTP500.to_vec();
        self.complete = true;
    }

    // true: There's more. false: done
    pub fn render_next_chunk(&mut self, py: Python) -> PyResult<bool> {
        let mut bytes: Vec::<u8> =Vec::new();
        match self.iter.as_mut() {
            None => {
                // handle FileWrapper here
                if let Some(ob) = self.pyobject.as_mut() {
                    match ob.extract::<&mut FileWrapper>(py) {
                        Ok(fw) => {
                            match fw.next() {
                                Some(cont) => {
                                    bytes = cont;
                                },
                                None => {
                                    self.complete = true;
                                    return Ok(false)
                                }
                            }
                        },
                        Err(e) => {
                            // No iterator, no FileWrapper, there's nothing we can do
                            debug!("Could not extract FileWrapper: {:?}", e);
                            self.complete = true;
                            return Ok(false)
                        }
                    }
                }
            },
            Some(obj) => {
                match obj.next() {
                    None => {
                        self.complete = true;
                        return Ok(false)
                    },
                    Some(Err(e)) => return Err(e),
                    Some(Ok(any)) => {
                        match any.downcast_ref::<PyBytes>() {
                            Ok(cont) => {
                                bytes = cont.as_bytes().to_vec()
                            },
                            Err(e) => {
                                error!("Could not downcast from: {:?}, got error: {:?}", any, e);
                                self.complete = true;
                                return Ok(false)
                            }
                        }
                    },
                }
            }
        };
        match self.start_response.as_mut() {
            Some(pyob) => {
                let start_response =  pyob.extract::<&mut StartResponse>(py)?;
                // bytes might be empty, but will still write the headers
                start_response.write(&bytes[..], &mut self.current_chunk);
                if start_response.content_complete() {
                    self.complete = true;
                    return Ok(false)
                }
            },
            None => return Err(PyErr::new::<ValueError, _>("StartResponse not set"))
        }
        Ok(true)
    }

    // true: chunk written completely, false: there's more
    pub fn write_chunk(&mut self, out: &mut TcpStream, py: Python, gstate: PyGILState_STATE) -> io::Result<bool> {
        match out.write(&self.current_chunk[..]) {
            Ok(num_written) => {
                if num_written < self.current_chunk.len() {
                    error!("Chunk not completely written");
                }
                out.flush()?;
            },
            Err(err) =>
                return Err(err)
        }
        if self.sendfileinfo {
            if let Some(ob) = self.pyobject.as_mut() {
                self.complete = match ob.extract::<&mut FileWrapper>(py) {
                    Ok(fw) => {
                        fw.send_file(out, gstate)
                    }
                    Err(e) => {
                        // No iterator, no FileWrapper, there's nothing we can do here
                        debug!("Could not extract FileWrapper: {:?}", e);
                        true
                    }
                }
            }
        }
        if !self.complete {
            self.current_chunk.clear();
        }
        Ok(self.complete)
    }

}


impl <'i>Drop for WSGIResponse<'i> {

    fn drop(&mut self) {
        debug!("Dropping WSGI Response");
        if let Some(ob) = self.pyobject.as_mut() {
            with_gil(|py, _gs| {
                match close_pyobject(ob, py) {
                    Err(e) => {
                        e.print_and_set_sys_last_vars(py);
                    },
                    Ok(_) => debug!("WSGIResponse dropped successfully")
                }
            });
        }
    }
}


pub fn handle_request<'i>(application: &PyObject, globals: &WSGIGlobals, req: &WSGIRequest, py: Python<'i>) -> WSGIResponse<'i> {
    let mut resp = WSGIResponse::new();
    let req = match get_environ(req, globals, py) {
        Ok(req) => req,
        Err(e) => {
            error!("Error parsing request: {:?}", e);
            e.print_and_set_sys_last_vars(py);
            resp.set_error();
            return resp
        }
    };
    // allocate the Python object on the heap
    let sr = match PyClassShell::new_mut(py,
        StartResponse::new(req, Vec::new())) {
        Ok(ob) => ob,
        Err(e) => {
            error!("Error creating start_response: {:?}", e);
            resp.set_error();
            return resp
        }
    };
    let args = PyTuple::new(py, vec![sr.environ.clone_ref(py), sr.to_object(py)]);
    let srobj = sr.to_object(py).clone_ref(py);
    debug!("Refcounts application: {:?} start_response: {:?}, environ: {:?}", application.get_refcnt(), srobj.get_refcnt(), sr.environ.get_refcnt());
    resp.start_response = Some(srobj);
    let result = application.call1(py, args); // "Calls the object. This is equivalent to the Python expression: 'self(*args)'"
    match result {
        Ok(o) => {
            debug!("Refcount result: {:?}", o.get_refcnt());
            if let Err(e) = resp.set_pyobject(o, py) {
                debug!("Could not set Python object of response");
                e.print_and_set_sys_last_vars(py);
                resp.set_error();
            }
        },
        Err(e) => {
            e.print_and_set_sys_last_vars(py);
            resp.set_error();
        }
    }
    resp
}


#[cfg(test)]
mod tests {

    use bytes::{Bytes};
    use env_logger;
    use log::{debug, error};
    use pyo3::PyClassShell;
    use pyo3::prelude::*;
    use pyo3::types::{PyDict};
    use std::io::{Read, Write, Seek};
    use std::net::{TcpListener, TcpStream, SocketAddr};
    use std::sync::mpsc::channel;
    use std::thread;
    use std::os::unix::io::{AsRawFd};
    use tempfile::NamedTempFile;

    use crate::filewrapper::{FileWrapper, SendFileInfo};
    use crate::globals::{WSGIGlobals};
    use crate::pyutils::with_gil;
    use crate::request::{WSGIRequest};
    use crate::response::{handle_request, HTTP500, WSGIResponse};
    use crate::startresponse::{StartResponse, WriteResponse};


    fn init() {
        let _ = env_logger::builder().is_test(true).try_init();
    }

    #[test]
    fn test_create() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(r#"li = [b"Hello", b"world", b"!"]"#, None, Some(&locals)) {
            Ok(_) => {
                let pylist = locals.get_item("li").unwrap().to_object(py);
                let environ = PyDict::new(py);
                let headers = vec![
                    ("200 OK".to_string(),
                    vec![("Content-type".to_string(), "text/plain".to_string())]
                    )];
                let sr = PyClassShell::new_mut(py,
                    StartResponse::new(environ.to_object(py), headers)).unwrap();
                let mut resp = WSGIResponse::new();
                match resp.set_pyobject(pylist, py) {
                    Ok(_) => {
                        resp.start_response = Some(sr.to_object(py));
                        let mut expectedv : Vec<&[u8]> = Vec::new();
                        expectedv.push(b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\n\r\nHello");
                        expectedv.push(b"world");
                        expectedv.push(b"!");
                        for expected in expectedv {
                            match resp.render_next_chunk(py) {
                                Ok(false) => {
                                    debug!("Expected further chunks");
                                    assert!(false);
                                },
                                Err(e) => {
                                    debug!("Error encountered: {:?}", e);
                                    assert!(false);
                                },
                                Ok(true) => {
                                    debug!("current chunk: {:?}", resp.current_chunk);
                                    assert!(
                                        resp.current_chunk.iter().zip(expected.iter()).all(|(p,q)| p == q));
                                    resp.current_chunk.clear();
                                }
                            }
                        }
                        match resp.render_next_chunk(py) {
                            Ok(false) => {
                                assert!(resp.complete);
                            },
                            _ => assert!(false)
                        }
                    },
                    Err(e) => {
                        debug!("Error: {:?}", e);
                        assert!(false);
                    }
                }
            },
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_iterator() {
        // From the PEP:
        // When called by the server, the application object must return an iterable yielding zero or more bytestrings.
        // This can be accomplished in a variety of ways, such as by returning a list of bytestrings,
        // or by the application being a generator function that yields bytestrings,
        // or by the application being a class whose instances are iterable.
        // Regardless of how it is accomplished,
        // the application object must always return an iterable yielding zero or more bytestrings.
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(r#"it = iter([b'Hello', b' world', b'!'])"#, None, Some(&locals)) {
            Ok(_) => {
                let pyit = locals.get_item("it").unwrap().to_object(py);
                let environ = PyDict::new(py);
                let headers = vec![
                    ("200 OK".to_string(),
                    vec![("Content-type".to_string(), "text/plain".to_string())]
                    )];
                let sr = PyClassShell::new_mut(py,
                    StartResponse::new(environ.to_object(py), headers)).unwrap();
                let mut resp = WSGIResponse::new();
                match resp.set_pyobject(pyit, py) {
                    Ok(_) => {
                        resp.start_response = Some(sr.to_object(py));
                        let mut expected : Vec<&[u8]> = Vec::new();
                        expected.push(b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\n\r\nHello");
                        expected.push(b" world");
                        expected.push(b"!");
                        for word in expected {
                            match resp.render_next_chunk(py) {
                                Ok(false) => {
                                    debug!("Expected further chunks");
                                    assert!(false);
                                },
                                Err(e) => {
                                    debug!("Error encountered: {:?}", e);
                                    assert!(false);
                                },
                                Ok(true) => {
                                debug!("Bytes: {:?}", &resp.current_chunk[..]);
                                assert!(resp.current_chunk == word);
                                resp.current_chunk.clear();
                                }
                            }
                        }
                    },
                    Err(e) => {
                        error!("Could not create PyIterator: {:?}", e);
                        assert!(false);
                    }
                }
            },
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        };
        // 'iterable' is a list of bytestrings:
        match py.run(r#"it = [b'Hello', b'world', b'!']"#, None, Some(&locals)) {
            Ok(_) => {
                let pyit = locals.get_item("it").unwrap().to_object(py);
                let environ = PyDict::new(py);
                let headers = vec![
                    ("200 OK".to_string(),
                    vec![("Content-type".to_string(), "text/plain".to_string())]
                    )];
                let sr = PyClassShell::new_mut(py,
                    StartResponse::new(environ.to_object(py), headers)).unwrap();
                let mut resp = WSGIResponse::new();
                match resp.set_pyobject(pyit, py) {
                    Ok(_) => {
                        resp.start_response = Some(sr.to_object(py));
                        let mut expected : Vec<&[u8]> = Vec::new();
                        expected.push(b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\n\r\nHello");
                        expected.push(b"world");
                        expected.push(b"!");
                        for word in expected {
                            match resp.render_next_chunk(py) {
                                Ok(true) => {
                                    debug!("{:?}", &resp.current_chunk[..]);
                                    assert!(resp.current_chunk == word);
                                    resp.current_chunk.clear();
                                },
                                _ => assert!(false)
                            }
                        }
                    },
                    Err(e) => {
                        error!("Could not create PyIterator: {:?}", e);
                        assert!(false);
                    }
                }
            },
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_set_pyobject() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(r#"li = [b"Hello", b"world", b"!"]"#, None, Some(&locals)) {
            Ok(_) => {
                let pylist = locals.get_item("li").unwrap().to_object(py);
                let mut resp = WSGIResponse::new();
                match resp.set_pyobject(pylist, py) {
                    Ok(_) => {
                        assert!(true);
                    },
                    _ => assert!(false)
                }
            },
            _ => assert!(false)
        }
    }

    #[test]
    fn test_set_error() {
        let mut resp = WSGIResponse::new();
        resp.set_error();
        assert_eq!(&resp.current_chunk[..], HTTP500);
        assert!(resp.complete);
    }

    #[test]
    fn test_write_chunk() {
        init();
        let mut r = WSGIResponse::new();
        r.current_chunk = b"Foo 42".to_vec();
        r.complete = false;
        let addr : SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 6];
            conn.read(&mut buf).unwrap();
            snd.clone().send(buf).unwrap();
            rx.recv().unwrap();
            drop(conn);
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect to server");
        debug!("Response SendFileInfo: {:?}", r.sendfileinfo);
        with_gil(|py, gs| {
            match r.write_chunk(&mut connection, py, gs) {
                Err(e) => {
                    debug!("Error: {:?}", e);
                    assert!(false);
                },
                Ok(false) => {
                    let b = got.recv().unwrap();
                    assert!(&b[..] == b"Foo 42");
                },
                _ => assert!(false)
            }
        });
        tx.send(()).unwrap();
        t.join().unwrap();
    }

    #[test]
    fn test_write_chunk_sendfile() {
        init();
        let gil = Python::acquire_gil();
        let py = gil.python();
        let addr : SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let mut tmp = NamedTempFile::new().unwrap();
        let mut f = tmp.reopen().unwrap();
        f.seek(std::io::SeekFrom::Start(0)).unwrap();
        let fw = PyClassShell::new_mut(py,
            FileWrapper {
                filelike: py.None(),
                sendfileinfo: SendFileInfo::new(f.as_raw_fd(), 42)}).unwrap().to_object(py);
        let mut r = WSGIResponse::new();
        r.set_pyobject(fw, py).unwrap();
        r.current_chunk = b"Foo 42".to_vec();
        r.complete = true;
        r.sendfileinfo = true;
        tmp.write_all(b"Hello World!\n").unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 19];
            conn.read(&mut buf).unwrap();
            conn.read(&mut buf[6..]).unwrap();
            snd.clone().send(buf).unwrap();
            rx.recv().unwrap();
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect");
        with_gil(|py, gs| {
            match r.write_chunk(&mut connection, py, gs) {
                Err(e) => {
                    debug!("Error: {:?}", e);
                    assert!(false);
                },
                Ok(true) => {
                    let b = got.recv().unwrap();
                    debug!("write chunk with file: {:?}", b);
                    assert_eq!(&b[..], b"Foo 42Hello World!\n");
                },
                _ => assert!(false)
            }
        });
        tx.send(()).unwrap();
        t.join().unwrap();
    }

    #[test]
    fn test_handle_request() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
    start_response(status, response_headers)
    return [b"Hello world!\n"]

app = simple_app"#, None, Some(&locals));
        match app {
            Ok(_) => {
                let si = "127.0.0.1:7878".parse().unwrap();
                let sn = "/foo";
                let g = WSGIGlobals::new(si, sn, py);
                let app = locals.get_item("app").unwrap().to_object(py);
                let raw = Bytes::from(&b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n"[..]);
                let mut req = WSGIRequest::new(None);
                req.parse(raw).expect("Error parsing request");
                let mut resp = handle_request(&app, &g, &req, py);
                resp.render_next_chunk(py).unwrap();
                let expected = b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nExpires: Sat, 1 Jan 2000 00:00:00 GMT\r\n\r\nHello world!\n";
                assert!(expected.len() == resp.current_chunk.len());
                assert!(
                    resp.current_chunk.iter().zip(expected.iter()).all(|(p,q)| p == q));
            },
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_handle_request_generator() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    yield b"Hello world!\n"

app = simple_app"#, None, Some(&locals));
        match app {
            Ok(_) => {
                let si = "127.0.0.1:7878".parse().unwrap();
                let sn = "/foo";
                let g = WSGIGlobals::new(si, sn, py);
                let app = locals.get_item("app").unwrap().to_object(py);
                let raw = Bytes::from(&b"GET /foo HTTP/1.1\r\n\r\n"[..]);
                let mut req = WSGIRequest::new(None);
                req.parse(raw).expect("Error parsing request");
                let mut resp = handle_request(&app, &g, &req, py);
                resp.render_next_chunk(py).unwrap();
                let expected = b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\n\r\nHello world!\n";
                assert!(expected.len() == resp.current_chunk.len());
                assert!(
                    resp.current_chunk.iter().zip(expected.iter()).all(|(p,q)| p == q));
            },
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_handle_request_multi_chunk() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT"), ('Content-Length', 13)]
    start_response(status, response_headers)
    return [b"Hello ", b"world!\n"]

app = simple_app"#, None, Some(&locals));
        match app {
            Ok(_) => {
                let app = locals.get_item("app").unwrap().to_object(py);
                let si = "127.0.0.1:7878".parse().unwrap();
                let sn = "/foo";
                let g = WSGIGlobals::new(si, sn, py);
                let raw = Bytes::from(&b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n"[..]);
                let mut req = WSGIRequest::new(None);
                req.parse(raw).expect("Error parsing request");
                let mut resp = handle_request(&app, &g, &req, py);
                resp.render_next_chunk(py).unwrap();
                let mut expected : Vec<&[u8]> = Vec::new();
                expected.push(b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nExpires: Sat, 1 Jan 2000 00:00:00 GMT\r\nContent-Length: 13\r\n\r\nHello ");
                expected.push(b"world!\n");
                for word in expected {
                    debug!("{:?}", &resp.current_chunk[..]);
                    assert_eq!(resp.current_chunk, word);
                    resp.current_chunk.clear();
                    match resp.render_next_chunk(py) {
                        Ok(_) => {},
                        _ => assert!(false)
                    }
                }
                assert!(resp.complete);
                assert!(resp.start_response.as_mut().unwrap().extract::<&StartResponse>(py).unwrap().content_complete());
            },
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_handle_request_application_error() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
    start_response(status, response_headers)
    raise Exception("Baz")

app = simple_app"#, None, Some(&locals));
        match app {
            Ok(_) => {
                let app = locals.get_item("app").unwrap().to_object(py);
                let si = "127.0.0.1:7878".parse().unwrap();
                let sn = "/foo";
                let g = WSGIGlobals::new(si, sn, py);
                let raw = Bytes::from(&b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n"[..]);
                let mut req = WSGIRequest::new(None);
                req.parse(raw).expect("Error parsing request");
                let mut resp = handle_request(&app, &g, &req, py);
                if let Err(e) = resp.render_next_chunk(py) {
                    e.print_and_set_sys_last_vars(py);
                    assert!(false);
                }
                let expected = b"HTTP/1.1 500 Internal Server Error\r\n\r\n";
                debug!("{:?}", &resp.current_chunk[..]);
                assert!(
                    resp.current_chunk.iter().zip(expected.iter()).all(|(p,q)| p == q));
                assert!(resp.complete);
            },
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_handle_request_result_not_iterable() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
    start_response(status, response_headers)
    return None

app = simple_app"#, None, Some(&locals));
        match app {
            Ok(_) => {
                let app = locals.get_item("app").unwrap().to_object(py);
                let si = "127.0.0.1:7878".parse().unwrap();
                let sn = "/foo";
                let g = WSGIGlobals::new(si, sn, py);
                let raw = Bytes::from(&b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n"[..]);
                let mut req = WSGIRequest::new(None);
                req.parse(raw).expect("Error parsing request");
                let mut resp = handle_request(&app, &g, &req, py);
                resp.render_next_chunk(py).unwrap();
                let expected = b"HTTP/1.1 500 Internal Server Error\r\n\r\n";
                debug!("{:?}", &resp.current_chunk[..]);
                assert!(
                    resp.current_chunk.iter().zip(expected.iter()).all(|(p,q)| p == q));
                assert!(resp.complete);
            },
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

}
