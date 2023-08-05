use bytes::{Bytes, BytesMut};
use httparse::{self};
use log::{debug};
use pyo3::exceptions::{UnicodeDecodeError, ValueError};
use pyo3::prelude::*;
use std::net::SocketAddr;


static HTTP_COOKIE: &str = "HTTP_COOKIE";
static HTTP_HOST: &str = "HTTP_HOST";
static HTTP_USER_AGENT: &str = "HTTP_USER_AGENT";
static HTTP_ACCEPT: &str = "HTTP_ACCEPT";
static HTTP_ACCEPT_LANGUAGE: &str = "HTTP_ACCEPT_LANGUAGE";
static HTTP_ACCEPT_ENCODING: &str = "HTTP_ACCEPT_ENCODING";
static HTTP_CONNECTION: &str = "HTTP_CONNECTION";
static HTTP_UPGRADE_INSECURE_REQUESTS: &str = "HTTP_UPGRADE_INSECURE_REQUESTS";
static HTTP_DNT: &str = "HTTP_DNT";
static CONTENT_TYPE: &str = "CONTENT_TYPE";
static REQUEST_METHOD: &str = "REQUEST_METHOD";
static PATH_INFO: &str = "PATH_INFO";
static QUERY_STRING: &str = "QUERY_STRING";
static SERVER_PROTOCOL: &str = "SERVER_PROTOCOL";


pub struct WSGIRequest {
    pub body: BytesMut,
    pub complete: bool,
    pub content_length: usize,
    pub environ: Vec<(&'static str, String)>,
    pub peer_addr: Option<SocketAddr>,
    }

macro_rules! environ_set {
    ($self:expr, $key:ident, $header:expr) => {
        match String::from_utf8($header.value.to_vec()) {
            Ok(val) => $self.environ.push(($key, val)),
            Err(e) => return Err(PyErr::new::<UnicodeDecodeError, _>(format!("{:?} encountered for value: {:?}", e, $header.value)))
        }
    }
}

impl WSGIRequest {

    pub fn new(peer_addr: Option<SocketAddr>) -> WSGIRequest {
        WSGIRequest {
            body: BytesMut::new(),
            complete: false,
            content_length: 0,
            environ: Vec::new(),
            peer_addr: peer_addr,
        }
    }

    pub fn parse(&mut self, raw: Bytes) -> PyResult<()> {
        if !self.complete {
            if self.environ.len() == 0 {
                return self.parse_headers(raw)
            }
            if self.content_length == (self.body.len() + raw.len()) {
                self.complete = true;
            }
            self.body.extend_from_slice(&raw[..]);
        }
        Ok(())
    }

    pub fn parse_headers(&mut self, raw: Bytes) -> PyResult<()> {
        let mut headers = [httparse::EMPTY_HEADER; 16];
        let mut req = httparse::Request::new(&mut headers);
        match req.parse(&raw[..]) {
            Ok(res) => {
                match res {
                    httparse::Status::Partial => {
                        debug!("Partial request");
                    },
                    httparse::Status::Complete(size) => {
                        let length = raw.len();
                        if size < length {
                            self.body.extend_from_slice(&raw[size..length]);
                        } else {
                            self.complete = true;
                        }
                        for header in req.headers.iter() {
                            match header.name {
                                "Content-Length" => {
                                    if let Ok(val) = std::str::from_utf8(header.value) {
                                        if let Ok(parsedval) = val.parse() {
                                            self.content_length = parsedval;
                                            if self.content_length == self.body.len() {
                                                self.complete = true;
                                            }
                                        }
                                    }
                                },
                                "Cookie" => {
                                    environ_set!(self, HTTP_COOKIE, header);
                                },
                                "Host" => {
                                    environ_set!(self, HTTP_HOST, header);
                                },
                                "User-Agent" => {
                                    environ_set!(self, HTTP_USER_AGENT, header);
                                },
                                "Accept" => {
                                    environ_set!(self, HTTP_ACCEPT, header);
                                },
                                "Accept-Language" => {
                                    environ_set!(self, HTTP_ACCEPT_LANGUAGE, header);
                                },
                                "Accept-Encoding" => {
                                    environ_set!(self, HTTP_ACCEPT_ENCODING, header);
                                },
                                "Connection" => {
                                    environ_set!(self, HTTP_CONNECTION, header);
                                },
                                "Upgrade-Insecure-Requests" => {
                                    environ_set!(self, HTTP_UPGRADE_INSECURE_REQUESTS, header);
                                },
                                "DNT" => {
                                    environ_set!(self, HTTP_DNT, header);
                                },
                                "Content-Type" => {
                                    environ_set!(self, CONTENT_TYPE, header);
                                },
                                &_ => {}
                            }
                        }
                        match req.method {
                            Some(method) => {
                                self.environ.push((REQUEST_METHOD, method.to_string()));
                            },
                            None => {}
                        }
                        match req.path {
                            Some(path) => {
                                let parts: Vec<&str> = path.split("?").collect();
                                self.environ.push((PATH_INFO, parts[0].to_string()));
                                if parts.len() > 1 {
                                    self.environ.push((QUERY_STRING, parts[1].to_string()));
                                } else {
                                    self.environ.push((QUERY_STRING, "".to_string()));
                                }
                            },
                            None => {}
                        }
                        match req.version {
                            Some(version) => {
                                let protocol = match version {
                                    0 => "HTTP/1.0",
                                    1 => "HTTP/1.1",
                                    _ => return Err(PyErr::new::<ValueError, _>(format!("Unsupported version: {:?}", version)))
                                };
                                self.environ.push((SERVER_PROTOCOL, protocol.to_string()));
                            },
                            None => {}
                        }
                    }
                }
            },
            Err(err) => return Err(PyErr::new::<ValueError, _>(format!("Error parsing request: {:?}", err)))
        };
        Ok(())
    }

}

#[cfg(test)]
mod tests {
    use bytes::{Bytes};
    use log::{debug};

    use crate::request::{WSGIRequest};

    #[test]
    fn test_get() {
        let raw = Bytes::from(&b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n"[..]);
        let mut got = WSGIRequest::new(None);
        got.parse_headers(raw).unwrap();
        assert!(got.environ.len() == 12);
        for (name, value) in got.environ.iter() {
            match *name {
                "HTTP_COOKIE" => assert!(&value[..] == "foo_language=en;"),
                "PATH_INFO" => assert!(&value[..] == "/foo42"),
                "QUERY_STRING" => assert!(&value[..] == "bar=baz"),
                "HTTP_ACCEPT" => assert!(&value[..] == "image/webp,*/*"),
                "HTTP_ACCEPT_LANGUAGE" => assert!(&value[..] == "de-DE,en-US;q=0.7,en;q=0.3"),
                "HTTP_ACCEPT_ENCODING" => assert!(&value[..] == "gzip, deflate"),
                "HTTP_CONNECTION" => assert!(&value[..] == "keep-alive"),
                "REQUEST_METHOD" => assert!(&value[..] == "GET"),
                "HTTP_HOST" => assert!(&value[..] == "localhost:7878"),
                "HTTP_USER_AGENT" => {
                    let expected = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0";
                    assert_eq!(value, expected);
                },
                "HTTP_DNT" => assert_eq!(&value[..], "1"),
                "SERVER_PROTOCOL" => assert_eq!(&value[..], "HTTP/1.1"),
                &_ => {}
            }
        }
    }

    #[test]
    fn test_parse_body_once() {
        let raw = Bytes::from(&b"POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 27\r\n\r\nfield1=value1&field2=value2"[..]);
        let mut got = WSGIRequest::new(None);
        got.parse(raw).expect("Error parsing request");
        assert!(got.complete);
        for (name, value) in got.environ.iter() {
            match *name {
                "CONTENT_TYPE" => {
                    let expected = "application/x-www-form-urlencoded";
                    assert_eq!(value, expected);
                },
                &_ => {}
            }
        }
        assert_eq!(&got.body[..], b"field1=value1&field2=value2");
    }

    #[test]
    fn test_parse_multiple() {
        let raw1 = Bytes::from(&b"POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 41\r\n\r\nfield1=value1&field2=value2"[..]);
        let raw2 = Bytes::from(&b"&field3=value3"[..]);
        let mut got = WSGIRequest::new(None);
        got.parse(raw1).expect("Error parsing request");
        assert!(!got.complete);
        assert!(got.content_length == 41);
        got.parse(raw2).expect("Error parsing request");
        assert!(got.complete);
        assert!(got.content_length == 41);
        for (name, value) in got.environ.iter() {
            match *name {
                "CONTENT_TYPE" => {
                    let expected = "application/x-www-form-urlencoded";
                    assert_eq!(expected, value);
                },
                &_ => {}
            }
        }
        let expected = b"field1=value1&field2=value2&field3=value3";
        debug!("{:?}", got.body);
        assert!(
            got.body.iter().zip(expected.iter()).all(|(p,q)| p == q));
    }

}
