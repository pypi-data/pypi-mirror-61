use bytes::{Bytes, BytesMut};
use log::{debug, error};
use mio::net::{TcpStream, TcpListener};
use mio::{Events, Interest, Poll, Token};
use pyo3::ffi;
use pyo3::prelude::*;
use std::collections::{HashMap, HashSet};
use std::error;
use std::io::{self, Read, Write};
use std::net;
use std::os::unix::io::{FromRawFd, IntoRawFd};
use std::time::Duration;

use crate::globals::{WSGIGlobals};
use crate::request::{WSGIRequest};
use crate::response::{HTTP500};
use crate::workers::{WorkerPool};


pub const SERVER: Token = Token(0);
const READBUFSIZE: usize = 16384;
const POLL_TIMEOUT: u64 = 100;


type Result<T> = std::result::Result<T, Box<dyn error::Error>>;


pub fn next(current: &mut Token) -> Token {
    let next = current.0;
    current.0 += 1;
    Token(next)
}


pub fn handle_read_event(
    connection: &mut dyn Read) -> io::Result<Bytes> {
    let mut received_data = BytesMut::with_capacity(READBUFSIZE);

    loop {
        let mut buf = [0; READBUFSIZE];
        match connection.read(&mut buf) {
            Ok(0) => {
                // connection closed or done writing.
                debug!("received 0 bytes");
                break;
            }
            Ok(n) => {
                received_data.extend_from_slice(&buf[..n]);
            },
            // connection is not ready to perform this I/O operation.
            Err(err) if would_block(&err) => {
                debug!("Connection would block");
                break;
            },
            Err(err) if interrupted(&err) => {
                error!("Interrupted!");
                continue;
            },
            Err(err) if broken_pipe(&err) => {
                error!("Broken Pipe!");
                return Ok(received_data.freeze())
            }
            // Other errors we'll consider fatal.
            Err(err) => {
                error!("Other error!");
                return Err(err)
            },
        }
    }
    if received_data.len() == 0 {
        return Err(io::Error::new(io::ErrorKind::Other, "Empty request!"))
    }
    Ok(received_data.freeze())
}


pub fn would_block(err: &io::Error) -> bool {
    err.kind() == io::ErrorKind::WouldBlock
}


pub fn interrupted(err: &io::Error) -> bool {
    err.kind() == io::ErrorKind::Interrupted
}


pub fn broken_pipe(err: &io::Error) -> bool {
    err.kind() == io::ErrorKind::BrokenPipe
}


pub struct Server {
    poll: Poll,
    events: Events,
    listener: TcpListener,
    workers: WorkerPool,
    connections: HashMap<Token, TcpStream>,
    requests: HashMap<Token, WSGIRequest>,
    error_responses: HashSet<Token>,
}


impl <'g>Server {

    pub fn new(application: PyObject, globals: &WSGIGlobals::<'g>, num_workers: usize, py: Python) -> io::Result<Server> {
        let addr = globals.server_info;
        let workers = WorkerPool::new(
            globals.server_info,
            globals.script_name.to_string(),
            application,
            num_workers,
            py);
        let mut listener = TcpListener::bind(addr)?;
        let poll = Poll::new()?;
        poll.registry().register(&mut listener, SERVER, Interest::READABLE)?;

        Ok(Server {
            poll: poll,
            events: Events::with_capacity(1024),
            listener: listener,
            workers: workers,
            connections: HashMap::new(),
            requests: HashMap::new(),
            error_responses: HashSet::new()
        })
    }

    pub fn serve(&mut self) -> Result<()> {
        let mut unique_token = Token(SERVER.0 + 1);
        let py_thread_state = unsafe { ffi::PyEval_SaveThread() };
        loop {
            match self.poll.poll(&mut self.events, Some(Duration::from_millis(POLL_TIMEOUT))) {
                Ok(_) => {
                    for event in self.events.iter() {
                        match event.token() {
                            SERVER => {
                                loop {
                                    match self.listener.accept() {
                                        Ok((mut connection, _)) => {
                                            let token = next(&mut unique_token);

                                            self.poll.registry().register(
                                                &mut connection,
                                                token,
                                                Interest::READABLE)?;

                                            self.connections.insert(token, connection);
                                        },
                                        Err(_) => break
                                    }
                                }
                            },
                            token if event.is_readable() => {
                                match self.connections.get_mut(&token) {
                                    Some(connection) => {
                                        match handle_read_event(connection) {
                                            Ok(raw) => {
                                                if !self.requests.contains_key(&token) {
                                                    let peer_addr = match connection.peer_addr() {
                                                        Ok(addr) => Some(addr),
                                                        Err(e) => {
                                                            debug!("Error encountered {:?}", e);
                                                            None
                                                        }
                                                    };
                                                    self.requests.insert(token, WSGIRequest::new(peer_addr));
                                                }
                                                if let Some(req) = self.requests.get_mut(&token) {
                                                    match req.parse(raw) {
                                                        Ok(_) => {
                                                            if req.complete {
                                                                debug!("request complete");
                                                                match self.requests.remove(&token) {
                                                                    Some(req) => {
                                                                        let mut connection = self.connections.remove(&token).unwrap();
                                                                        self.poll.registry().deregister(&mut connection)?;
                                                                        let newconn = unsafe {net::TcpStream::from_raw_fd(connection.into_raw_fd())};
                                                                        newconn.set_nonblocking(false)?;
                                                                        if let Err(e) = self.workers.execute(token, req, Some(newconn)) {
                                                                            error!("Could not relay request to worker: {}",e);
                                                                        }
                                                                    },
                                                                    None => {}
                                                                }
                                                            }
                                                        },
                                                        Err(e) => {
                                                            error!("Could not parse request: {:?}", e);
                                                            self.error_responses.insert(token);
                                                            self.poll.registry().reregister(
                                                                connection,
                                                                token,
                                                                Interest::WRITABLE)?;
                                                        }
                                                    }
                                                } else { error!("no such token {:?}", token) }
                                            },
                                            Err(e) => error!("Error encountered: {:?}", e)
                                        };
                                    },
                                    None => {
                                        error!("No such connection: {:?}",token);
                                    }
                                }
                            },
                            token if event.is_writable() => {
                                if self.error_responses.contains(&token) {
                                    match self.connections.get_mut(&token) {
                                        Some(connection) => {
                                            connection.write(HTTP500)?;
                                            self.connections.remove(&token);
                                            self.error_responses.remove(&token);
                                        },
                                        None => {
                                            error!("Writable: no such connection: {:?}", token);
                                        }
                                    }
                                }
                            },
                            _ => ()
                        }
                    }
                },
                Err(e) => {
                    error!("Error processing poll events: {:?}", e);
                    self.workers.join()?;
                    unsafe { ffi::PyEval_RestoreThread(py_thread_state) };
                }
            }
        }
    }

}


#[cfg(test)]
mod tests {

    use env_logger;
    use log::{debug};
    use mio::{Token};
    use pyo3::prelude::*;
    use pyo3::types::{PyDict};
    use std::io::{self, Read};
    use std::ops::{Range};

    use crate::globals::{WSGIGlobals};
    use crate::server::{next, broken_pipe, handle_read_event, interrupted, would_block, Server};


    struct StreamMock {
        pub data: Vec<u8>,
        pos: usize,
        error: Option<io::ErrorKind>,
    }

    impl StreamMock {

        pub fn new(data: Vec<u8>) -> StreamMock {
            StreamMock {
                data: data,
                pos: 0,
                error: None
            }
        }

        pub fn read_slice(&mut self, range: Range<usize>, buf: &mut [u8]) -> usize {
            self.pos = range.start;
            let start = range.start;
            let num_bytes = range.end - self.pos;
            for idx in range {
                let offset = idx - start;
                match self.data.get(idx) {
                    Some(d) => {
                        buf[offset] = *d;
                        self.pos = self.pos + 1;
                    },
                    None => return offset
                }
            }
            num_bytes
        }

    }

    impl Read for StreamMock {

        fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
            match self.error {
                None => {
                    let num_bytes = self.read_slice(0..10, buf);
                    self.error = Some(io::ErrorKind::WouldBlock);
                    Ok(num_bytes)
                },
                Some(errkind) if errkind == io::ErrorKind::WouldBlock => {
                    self.error = Some(io::ErrorKind::Interrupted);
                    return Err(io::Error::new(errkind, "bar"))
                },
                Some(errkind) if errkind == io::ErrorKind::Interrupted => {
                    if self.pos < 15 {
                        return Ok(self.read_slice(10..15, buf))
                    }
                    self.error = Some(io::ErrorKind::BrokenPipe);
                    return Err(io::Error::new(errkind, "baz"))
                },
                Some(errkind) if errkind == io::ErrorKind::BrokenPipe => {
                    if self.pos < 20 {
                        return Ok(self.read_slice(15..20, buf))
                    }
                    self.error = Some(io::ErrorKind::Other);
                    return Err(io::Error::new(errkind, "foo"))
                },
                Some(errkind) if errkind == io::ErrorKind::Other => {
                    if self.pos < 25 {
                        return Ok(self.read_slice(20..25, buf))
                    }
                    return Err(io::Error::new(errkind, "bam !"))
                },
                _ => return Ok(0)
            }
        }

    }

    fn init() {
        let _ = env_logger::builder().is_test(true).try_init();
    }

    #[test]
    fn test_next() {
        let mut start = Token(0);
        for idx in 0..6 {
            let got = next(&mut start);
            assert_eq!(Token(idx), got);
            assert_eq!(start.0, idx+1);
        }
    }

    #[test]
    fn test_handle_read_event() {
        init();
        let mut s = StreamMock::new(b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n".to_vec());
        // read until WouldBlock
        match handle_read_event(&mut s) {
            Ok(got) => {
                debug!("Got (after WouldBlock): {:?}", &got[..]);
                assert_eq!(&got[..], b"GET /foo42");
            },
            Err(e) => {
                debug!("Error: {:?}", e);
                assert!(false);
            }
        }
        // read until BrokenPipe
        match handle_read_event(&mut s) {
            Ok(got) => {
                debug!("Got (after Interrupted, BrokenPipe): {:?}", &got[..]);
                assert_eq!(&got[..], b"?bar=baz H");
            },
            Err(e) => {
                debug!("Error: {:?}", e);
                assert!(false);
            }
        }
        // read until Other Error
        match handle_read_event(&mut s) {
            Ok(got) => {
                debug!("Got (after other error): {:?}", &got[..]);
                assert!(false);
            },
            Err(e) => {
                debug!("Error: {:?}", e);
                assert_eq!(e.kind(), io::ErrorKind::Other);
            }
        }
    }

    #[test]
    fn test_would_block() {
        let wbe = io::Error::new(io::ErrorKind::WouldBlock, "foo");
        assert!(would_block(&wbe));
        let nwbe = io::Error::new(io::ErrorKind::Other, "foo");
        assert!(!would_block(&nwbe));
    }

    #[test]
    fn test_interrupted() {
        let ie = io::Error::new(io::ErrorKind::Interrupted, "foo");
        assert!(interrupted(&ie));
        let nie = io::Error::new(io::ErrorKind::Other, "foo");
        assert!(!interrupted(&nie));
    }

    #[test]
    fn test_broken_pipe() {
        let bpe = io::Error::new(io::ErrorKind::BrokenPipe, "foo");
        assert!(broken_pipe(&bpe));
        let nbpe = io::Error::new(io::ErrorKind::Other, "foo");
        assert!(!broken_pipe(&nbpe));
    }

    #[test]
    fn test_create_server() {
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
                let si = "127.0.0.1:0".parse().unwrap();
                let sn = "/foo";
                let g = WSGIGlobals::new(si, sn, py);
                let app = locals.get_item("app").unwrap().to_object(py);
                match Server::new(app, &g, 2, py) {
                    Ok(got) => {
                    },
                    Err(e) => {
                        debug!("Error when creating Server: {:?}", e);
                        assert!(false);
                    }
                }
            },
            _ => assert!(false)
        }
    }

    #[test]
    #[ignore]
    fn test_server_serve() {
        unimplemented!("Missing test");
    }

}
