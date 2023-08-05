use log::{debug, error};
use mio::{Token};
use pyo3::prelude::*;
use spmc::{self, Sender, Receiver};
use std::net::{SocketAddr, TcpStream};
use std::sync::mpsc::{SendError};
use threadpool::ThreadPool;

use crate::globals::{WSGIGlobals};
use crate::pyutils::{with_gil};
use crate::request::{WSGIRequest};
use crate::response::{handle_request};


const MARKER: Token = Token(0);


pub fn worker<'a>(idx: usize, server_info: SocketAddr, threadapp: PyObject, script_name: String, rcv: Receiver<(Token, (WSGIRequest, Option<TcpStream>))>) {
    let thread_globals = with_gil(|py: Python<'a>, _gs| {
        WSGIGlobals::new(server_info, script_name.as_str(), py)
    });
    loop {
        match rcv.recv() {
            Ok((token, (req, out))) => {
                if token == MARKER {
                    break
                }
                debug!("Handling request in worker {}", idx);
                match out {
                    Some(mut connection) => {
                        debug!("Using tcp stream {:?} for writing out.", connection);
                        with_gil(|py, gs| {
                            let mut resp = handle_request(&threadapp.clone_ref(py), &thread_globals, &req, py);
                            loop {
                                if !resp.complete {
                                    // i.e. no error response
                                    match resp.render_next_chunk(py) {
                                        Err(e) => {
                                            e.print_and_set_sys_last_vars(py);
                                            resp.complete = true;
                                        },
                                        Ok(_) => {}
                                    }
                                }
                                let cont = match resp.write_chunk(&mut connection, py, gs) {
                                    Ok(true) => {
                                        false
                                    },
                                    Err(e) => {
                                        error!("Todo: handle write error: {:?}", e);
                                        false
                                    }
                                    _ => {
                                        true
                                        // there's more to write, stay in loop
                                    }
                                };
                                if !cont {break}
                            }
                        });
                    },
                    None => {
                        error!("No connection to write to");
                    }
                }
            },
            Err(e) => {
                error!("Couldn't receive from queue: {:?} (sender has hung up)", e);
                break
            }
        }
    }
}

pub struct WorkerPool {
    workers: ThreadPool,
    application: PyObject,
    input: Sender<(Token, (WSGIRequest, Option<TcpStream>))>,
}


impl WorkerPool {

    pub fn new(server_info: SocketAddr, script_name: String, application: PyObject, num_workers: usize, py: Python) -> WorkerPool {
        let (input, rcv) = spmc::channel::<(Token, (WSGIRequest, Option<TcpStream>))>();
        let wp = WorkerPool {
            application: application,
            workers: ThreadPool::new(num_workers),
            input: input,
        };
        for idx in 0..num_workers {
            let rcv = rcv.clone();
            let threadapp = wp.application.clone_ref(py); // "Clone self, Calls Py_INCREF() on the ptr."
            let sn = script_name.clone();
            wp.workers.execute(move || {
                worker(idx, server_info, threadapp, sn, rcv);
            });
        }
        wp
    }

    pub fn execute(&mut self, token: Token, req: WSGIRequest, out: Option<TcpStream>) -> Result<(), SendError<(Token, (WSGIRequest, Option<TcpStream>))>> {
        self.input.send((token, (req, out)))
    }

    pub fn join(&mut self) -> Result<(), SendError<(Token, (WSGIRequest, Option<TcpStream>))>> {
        for _ in 0..self.workers.max_count() {
            self.execute(MARKER, WSGIRequest::new(None), None)?;
        }
        Ok(self.workers.join())
    }

}

#[cfg(test)]
mod tests {
    use env_logger;
    use bytes::{BytesMut};
    use log::{debug};
    use mio::{Token};
    use pyo3::ffi;
    use pyo3::prelude::*;
    use pyo3::types::{PyDict};
    use std::io::{Read};
    use std::net::{TcpListener, TcpStream, SocketAddr};
    use std::sync::mpsc::channel;
    use std::thread;

    use crate::request::{WSGIRequest};
    use crate::workers::{worker, MARKER, WorkerPool};

    fn init() {
        let _ = env_logger::builder().is_test(true).try_init();
    }

    #[test]
    fn test_worker() {
        init();
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
                let app = locals.get_item("app").unwrap().to_object(py);
                let si: SocketAddr = "127.0.0.1:0".parse().unwrap();
                let sn = "/foo";
                let server = TcpListener::bind(si).expect("Failed to bind address");
                let addr = server.local_addr().unwrap();
                let raw = BytesMut::from(&b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n"[..]);
                let raw = raw.freeze();
                let mut req = WSGIRequest::new(None);
                req.parse(raw.clone()).expect("Error parsing request");
                let token = Token(42);
                let expected = b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nExpires: Sat, 1 Jan 2000 00:00:00 GMT\r\nContent-Length: 13\r\n\r\nHello world!\n";
                let (mut input, rcv) = spmc::channel::<(Token, (WSGIRequest, Option<TcpStream>))>();
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
                let t2 = thread::spawn(move || {
                    let connection = TcpStream::connect(addr).expect("Failed to connect to server");
                    input.send((token, (req, Some(connection)))).unwrap();
                    input.send((MARKER, (WSGIRequest::new(None), None))).unwrap();
                });
                worker(23, si, app, sn.to_string(), rcv.clone());
                let b = got.recv().unwrap();
                debug!("{:?}", b);
                assert!(
                    b.iter().zip(expected.iter()).all(|(p,q)| p == q));
                tx.send(()).unwrap();
                t.join().unwrap();
                t2.join().unwrap();
            },
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_pool_simple() {
        init();
        let gil = Python::acquire_gil();
        let py = gil.python();
        let si = "127.0.0.1:0".parse().unwrap();
        let sn = "/foo";
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
                let app = locals.get_item("app").unwrap().to_object(py);
                let raw = BytesMut::from(&b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n"[..]);
                let raw = raw.freeze();
                let mut req1 = WSGIRequest::new(None);
                req1.parse(raw.clone()).expect("Error parsing request");
                let mut req2 = WSGIRequest::new(None);
                req2.parse(raw.clone()).expect("Error parsing request");
                let mut req3 = WSGIRequest::new(None);
                req3.parse(raw.clone()).expect("Error parsing request");
                let mut req4 = WSGIRequest::new(None);
                req4.parse(raw).expect("Error parsing request");
                let mut wp = WorkerPool::new(si, sn.to_string(), app, 2, py);
                let token = Token(42);
                let py_thread_state = unsafe { ffi::PyEval_SaveThread() };
                wp.execute(token, req1, None).unwrap();
                wp.execute(token, req2, None).unwrap();
                wp.execute(token, req3, None).unwrap();
                wp.execute(token, req4, None).unwrap();
                match wp.join() {
                    Ok(_) => debug!("wp joined"),
                    Err(_) => {
                        debug!("Could not join workers");
                        assert!(false);
                    }
                }
                unsafe{ ffi::PyEval_RestoreThread(py_thread_state) };
            },
            Err(e) => {
                debug!("Error encountered: {:?}", e);
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

}
