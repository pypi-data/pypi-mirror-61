use slog_scope::{error};
use pyo3::prelude::*;
use pyo3::types::{PyTuple, PyList};
use std::cmp;


static CONTENT_LENGTH_HEADER: &str = "Content-Length";


#[pyclass(name=StartResponse,module="pyruvate")]
pub struct StartResponse {
    pub environ: PyObject,
    pub headers_set: Vec<(String, Vec<(String, String)>)>,
    pub headers_sent: Vec<(String, Vec<(String, String)>)>,
    pub content_length: Option<usize>,
    pub content_bytes_written: usize,
}


pub trait WriteResponse {
    // Put this in a trait for more flexibility.
    // PyO3 can't handle some types we are using here.
    fn new(environ: PyObject, headers_set: Vec<(String, Vec<(String, String)>)>) -> StartResponse;
    fn write(&mut self, data: &[u8], output: &mut Vec<u8>);
    fn content_complete(&self) -> bool;
}


impl WriteResponse for StartResponse {

    fn new(environ: PyObject, headers_set: Vec<(String, Vec<(String, String)>)>) -> StartResponse {
        StartResponse {
            environ: environ,
            headers_set: headers_set,
            headers_sent: Vec::new(),
            content_length: None,
            content_bytes_written: 0,
        }
    }

    fn write(&mut self, data: &[u8], output: &mut Vec<u8>) {
        if self.headers_sent.len() == 0 {
            if self.headers_set.len() == 0 {
               panic!("write() before start_response()")
            }
            // Before the first output, send the stored headers
            self.headers_sent = self.headers_set.clone();
            let respinfo = self.headers_set.pop(); // headers_sent|set should have only one element
            match respinfo {
                Some(respinfo) => {
                    let response_headers : Vec<(String, String)> = respinfo.1;
                    let status: String = respinfo.0;
                    output.extend(b"HTTP/1.1 ");
                    output.extend(status.as_bytes());
                    output.extend(b"\r\n");
                    for header in response_headers.iter() {
                        let headername = &header.0;
                        output.extend(headername.as_bytes());
                        output.extend(b": ");
                        output.extend(header.1.as_bytes());
                        output.extend(b"\r\n");
                        if headername == CONTENT_LENGTH_HEADER {
                            match header.1.parse::<usize>() {
                                Ok(length) => self.content_length = Some(length),
                                Err(e) => error!("Could not parse Content-Length header: {:?}", e)
                            }
                        }
                    }
                }
                None => {
                    error!("write(): No respinfo!");
                }
            }
            output.extend(b"\r\n");
        }
        match self.content_length {
            Some(length) => {
                if length > self.content_bytes_written {
                    let num = cmp::min(length - self.content_bytes_written, data.len());
                    output.extend(&data[..num]);
                    self.content_bytes_written = self.content_bytes_written + num;
                }
            },
            None => output.extend(data)
        };
    }

    fn content_complete(&self) -> bool {
        if let Some(length) = self.content_length {
            self.content_bytes_written >= length
        } else { false }
    }

}


#[pymethods]
impl StartResponse {

    #[call]
    #[args(args="*")]
    fn __call__(&mut self, args: &PyTuple, py: Python) -> PyResult<PyObject> {
        let status = args.get_item(0);
        let response_headers : &PyList = args.get_item(1).cast_as::<PyList>()?;
        if args.len() == 3 {
            let exc_info = args.get_item(2);
            if !exc_info.is_none() {
                error!("exc_info from application: {:?}", exc_info);
            }
        }
        let mut rh = Vec::<(String, String)>::new();
        for any in response_headers {
            let tp = any.downcast_ref::<PyTuple>()?;
            rh.push((tp.get_item(0).to_string(), tp.get_item(1).to_string()));
        }
        self.headers_set = vec![(status.to_string(), rh)];
        Ok(py.None())
    }
}


#[cfg(test)]
mod tests {
    use slog::{self, Drain, o};
    use slog_scope;
    use slog_term;
    use pyo3::prelude::*;
    use pyo3::types::{PyDict, PyTuple};
    use std::io::{Read, Seek, SeekFrom};
    use tempfile::NamedTempFile;

    use crate::startresponse::{StartResponse, WriteResponse};

    #[test]
    fn test_write() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let environ = PyDict::new(py);
        let headers = vec![
            ("200 OK".to_string(),
            vec![("Content-type".to_string(), "text/plain".to_string())]
            )];
        let mut sr = StartResponse::new(environ.to_object(py), headers);
        let mut output : Vec<u8> = Vec::new();
        let data = b"Hello world!\n";
        assert!(!sr.content_complete());
        sr.write(data, &mut output);
        let expected = b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\n\r\nHello world!\n";
        assert!(
            output.iter().zip(expected.iter()).all(|(p,q)| p == q));
        assert!(!sr.content_complete());
    }

    #[test]
    fn test_honour_content_length_header() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let environ = PyDict::new(py);
        let headers = vec![
            ("200 OK".to_string(),
            vec![
                ("Content-type".to_string(), "text/plain".to_string()),
                ("Content-Length".to_string(), "5".to_string())]
            )];
        let mut sr = StartResponse::new(environ.to_object(py), headers);
        let mut output : Vec<u8> = Vec::new();
        let data = b"Hello world!\n";
        assert!(!sr.content_complete());
        sr.write(data, &mut output);
        let expected = b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-Length: 5\r\n\r\nHello";
        assert_eq!(sr.content_length, Some(5));
        assert_eq!(sr.content_bytes_written, 5);
        assert!(sr.content_complete());
        assert!(
            output.iter().zip(expected.iter()).all(|(p,q)| p == q));
    }

    #[test]
    fn test_exc_info_is_none() {
        // do not display an error message when exc_info passed
        // by application is None
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let pycode = py.run(r#"
status = '200 OK'
response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
args_with_exc_info = (status, response_headers, 'Foo')
args_exc_info_none = (status, response_headers, None) # seen with mapproxy
args_no_exc_info = (status, response_headers)
"#, None, Some(&locals));
        match pycode {
            Ok(_) => {
                let args_with_exc_info = locals.get_item("args_with_exc_info").unwrap().downcast_mut::<PyTuple>().unwrap();
                let args_exc_info_none = locals.get_item("args_exc_info_none").unwrap().downcast_mut::<PyTuple>().unwrap();
                let args_no_exc_info = locals.get_item("args_no_exc_info").unwrap().downcast_mut::<PyTuple>().unwrap();
                let environ = PyDict::new(py);
                // create logger
                let tmp = NamedTempFile::new().unwrap();
                let decorator = slog_term::PlainSyncDecorator::new(tmp.reopen().unwrap());
                let drain = slog_term::FullFormat::new(decorator).build().fuse();
                let logger = slog::Logger::root(drain, o!());
                let _guard = slog_scope::set_global_logger(logger);

                let mut sr = StartResponse::new(environ.to_object(py), Vec::new());
                match sr.__call__(args_exc_info_none, py) {
                    Ok(pynone) if pynone == py.None() => {
                        let mut errs = tmp.reopen().unwrap();
                        errs.seek(SeekFrom::Start(0)).unwrap();
                        let mut got = String::new();
                        errs.read_to_string(&mut got).unwrap();
                        assert_eq!(got.len(), 0);
                    },
                    _ => assert!(false)
                }
                match sr.__call__(args_no_exc_info, py) {
                    Ok(pynone) if pynone == py.None() => {
                        let mut errs = tmp.reopen().unwrap();
                        errs.seek(SeekFrom::Start(0)).unwrap();
                        let mut got = String::new();
                        errs.read_to_string(&mut got).unwrap();
                        assert_eq!(got.len(), 0);
                    },
                    _ => assert!(false)
                }
                match sr.__call__(args_with_exc_info, py) {
                    Ok(pynone) if pynone == py.None() => {
                        let mut errs = tmp.reopen().unwrap();
                        errs.seek(SeekFrom::Start(0)).unwrap();
                        let mut got = String::new();
                        errs.read_to_string(&mut got).unwrap();
                        assert!(got.len() > 0);
                        assert!(got.contains("Foo"));
                    },
                    _ => assert!(false)
                }
            },
            _ => assert!(false)
        }
    }

}

