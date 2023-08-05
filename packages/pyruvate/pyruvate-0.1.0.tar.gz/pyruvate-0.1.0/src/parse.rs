use log::{debug};
use pyo3::prelude::*;
use pyo3::types::{IntoPyDict, PyString, PyTuple, PyBytes};

use crate::globals::{WSGIGlobals};
use crate::request::{WSGIRequest};


pub fn get_environ(req: &WSGIRequest, globals: &WSGIGlobals, py: Python) -> PyResult<PyObject> {
    let io = globals.io_module;
    let sys = globals.sys_module;
    let environ = req.environ.iter().map(
        |(k, v)| (k, PyString::new(py, v))).into_py_dict(py);
    environ.set_item("SERVER_NAME", format!("{}", globals.server_info.ip()))?;
    environ.set_item("SERVER_PORT", format!("{}", globals.server_info.port()))?;
    // XXX the following item needs to be set properly
    environ.set_item("SCRIPT_NAME", "")?;
    environ.set_item("REMOTE_ADDR", match req.peer_addr {
        None => "".to_string(),
        Some(addr) => format!("{}", addr.ip())
    })?;
    let input = io.call0("BytesIO")?;
    let bodylen = req.body.len();
    if bodylen > 0 {
        environ.set_item("CONTENT_LENGTH", bodylen)?;
        let body = PyBytes::new(py, &req.body[..]);
        input.call_method1("write", PyTuple::new(py, vec![body]))?;
        input.call_method1("seek", PyTuple::new(py, vec![0]))?;
    }
    environ.set_item("wsgi.input", input)?;
    environ.set_item("wsgi.errors", sys.get("stderr")?)?;
    environ.set_item("wsgi.version", (1, 0))?;
    environ.set_item("wsgi.multithread", false)?;
    environ.set_item("wsgi.multiprocess", true)?;
    environ.set_item("wsgi.run_once", false)?;
    environ.set_item("wsgi.url_scheme", "http")?;
    if let Some(wsgi) = globals.wsgi_module {
        debug!("Setting FileWrapper in environ");
        environ.set_item("wsgi.file_wrapper", wsgi.get("FileWrapper")?)?;
    }
    Ok(environ.to_object(py))
}

#[cfg(test)]
mod tests {
    use bytes::{Bytes};
    use log::{debug};
    use pyo3::prelude::*;
    use pyo3::types::{PyDict, PyString, PyBytes};
    use std::net::SocketAddr;

    use crate::globals::{WSGIGlobals};
    use crate::parse::{get_environ};
    use crate::request::{WSGIRequest};

    macro_rules! assert_header {
        ($got:ident, $py:ident, $key:literal, $value:expr) => {
            assert!($got.cast_as::<PyDict>($py).unwrap().get_item($key).unwrap().cast_as::<PyString>().unwrap().to_string().unwrap() == $value);
        }
    }

    #[test]
    fn test_environ_dict() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let si = "127.0.0.1:7878".parse().unwrap();
        let sn = "/foo";
        let g = WSGIGlobals::new(si, sn, py);
        let raw = Bytes::from(&b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n"[..]);
        let mut req = WSGIRequest::new(Some(SocketAddr::new("192.168.1.23".parse().unwrap(), 43567)));
        req.parse(raw).expect("Error parsing request");
        let got = get_environ(&req, &g, py).unwrap();
        assert_header!(got, py, "SERVER_NAME", "127.0.0.1");
        assert_header!(got, py, "SERVER_PORT", "7878");
        assert_header!(got, py, "SCRIPT_NAME", "");
        assert_header!(got, py, "REMOTE_ADDR", "192.168.1.23");
        assert_header!(got, py, "HTTP_COOKIE", "foo_language=en;");
        assert_header!(got, py, "PATH_INFO", "/foo42");
        assert_header!(got, py, "QUERY_STRING", "bar=baz");
        assert_header!(got, py, "HTTP_ACCEPT", "image/webp,*/*");
        assert_header!(got, py, "HTTP_ACCEPT_LANGUAGE", "de-DE,en-US;q=0.7,en;q=0.3");
        assert_header!(got, py, "HTTP_ACCEPT_ENCODING", "gzip, deflate");
        assert_header!(got, py, "HTTP_CONNECTION", "keep-alive");
        assert_header!(got, py, "REQUEST_METHOD", "GET");
        assert_header!(got, py, "HTTP_HOST", "localhost:7878");
        assert_header!(got, py, "HTTP_USER_AGENT", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0");
        assert_header!(got, py, "HTTP_DNT", "1");
        assert_header!(got, py, "SERVER_PROTOCOL", "HTTP/1.1");
    }

    #[test]
    fn test_post_simple_form() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let si = "127.0.0.1:7878".parse().unwrap();
        let sn = "/foo";
        let g = WSGIGlobals::new(si, sn, py);
        let raw = Bytes::from(&b"POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 27\r\n\r\nfield1=value1&field2=value2"[..]);
        let mut req = WSGIRequest::new(None);
        req.parse(raw).expect("Error parsing request");
        let got = get_environ(&req, &g, py).unwrap();
        assert_header!(got, py, "CONTENT_TYPE", "application/x-www-form-urlencoded");
        let input = got.cast_as::<PyDict>(py).unwrap().get_item("wsgi.input").unwrap().to_object(py);
        debug!("{:?}", input);
        let input = input.call_method0(py, "read").unwrap();
        debug!("{:?}", input);
        let input = input.cast_as::<PyBytes>(py).unwrap().as_bytes();
        debug!("{:?}", input);
        assert!(input == b"field1=value1&field2=value2");
    }

}
