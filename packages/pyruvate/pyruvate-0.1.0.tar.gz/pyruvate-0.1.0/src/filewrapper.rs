use errno::{errno};
use log::{debug, error};
use pyo3::exceptions::{TypeError};
use pyo3::prelude::*;
use pyo3::types::{PyTuple};
use std::net::{TcpStream};
use std::os::unix::io::{RawFd, AsRawFd};

use crate::pyutils::{close_pyobject, with_released_gil, PyGILState_STATE};


// This is the maximum the Linux kernel will write in a single sendfile call.
const SENDFILE_MAXSIZE: usize = 0x7ffff000;


pub struct SendFileInfo {
    pub blocksize: i64,
    pub offset: libc::off_t,
    pub fd: RawFd,
    pub done: bool
}


impl SendFileInfo {

    pub fn new(fd: RawFd, blocksize: i64) -> Self{
        Self {
            blocksize,
            offset: 0,
            fd,
            done: false
        }
    }

    // true: chunk written completely, false: there's more
    pub fn send_file(&mut self, out: &mut TcpStream) -> bool {
        debug!("Sending file");
        let count = if self.blocksize < 0 {
            SENDFILE_MAXSIZE
        } else {
            self.blocksize as usize
        };
        let res = unsafe {
            libc::sendfile(
                out.as_raw_fd(),
                self.fd,
                &mut self.offset,
                count)
        };
        match res {
            -1 => {
                error!("Could not sendfile(), errno: {}", errno());
                self.done = true
            },
            num_written if num_written < count as isize => {
                self.done = true
            },
            _ => {
                debug!("Sendfile number of bytes written: {}", res);
            }
        }
        self.done
    }

}


impl Iterator for SendFileInfo {
    type Item = Vec<u8>;

    fn next(&mut self) -> Option<Self::Item> {
        match self.done {
            true => None,
            false => Some(Vec::new())
        }
    }

}


#[pyclass(name=FileWrapper,module="pyruvate")]
pub struct FileWrapper {
    pub filelike: PyObject,
    pub sendfileinfo: SendFileInfo,
}


#[pymethods]
impl FileWrapper {

    #[new]
    #[args(args="*")]
    fn new(args: &PyTuple, py: Python) -> PyResult<Self> {
        let arglen = args.len();
        if (arglen == 0) | (arglen > 2) {
            return Err(PyErr::new::<TypeError, _>("Expected mandatory <filelike> and optional <blocksize> argument"))
        }
        let filelike = args.get_item(0).to_object(py);
        let mut blocksize = -1;
        if arglen == 2 {
            if let Ok(bs) = args.get_item(1).to_object(py).extract(py) {
                blocksize = bs;
            }
        }
        let mut fd: RawFd = -1;
        if let Ok(fdpyob) = filelike.call_method0(py, "fileno") {
            if let Ok(pyfd) = fdpyob.extract(py) {
                fd = pyfd;
            }
        };
        let sendfileinfo = SendFileInfo::new(fd, blocksize);
        Ok(
            FileWrapper {
                filelike,
                sendfileinfo
        })
    }

    fn close(&mut self, py: Python) -> PyResult<()> {
        close_pyobject(&mut self.filelike, py)
    }

}


pub trait SendFile {
    // Put this in a trait for more flexibility.
    fn send_file(&mut self, out: &mut TcpStream, gilstate: PyGILState_STATE) -> bool;
}


impl SendFile for FileWrapper {

    fn send_file(&mut self, out: &mut TcpStream, gilstate: PyGILState_STATE) -> bool {
        with_released_gil(gilstate, || {
            self.sendfileinfo.send_file(out)
        })
    }

}


impl Iterator for FileWrapper {
    type Item = Vec<u8>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.sendfileinfo.fd != -1 {
            return self.sendfileinfo.next()
        }
        let py = unsafe { Python::assume_gil_acquired() };
        match self.filelike.call_method1(py, "read", PyTuple::new(py, vec![self.sendfileinfo.blocksize])) {
            Ok(bytes) => {
                if bytes != py.None() {
                    match bytes.extract::<Vec<u8>>(py) {
                        Ok(result) => {
                            if result.len() > 0 {
                                Some(result)
                            } else { None }
                        },
                        Err(e) => {
                            debug!("Could not extract from bytes");
                            e.print_and_set_sys_last_vars(py);
                            None
                        }
                    }
                } else { None }
            },
            Err(e) => {
                debug!("Fileno: {}", self.sendfileinfo.fd);
                e.print_and_set_sys_last_vars(py);
                None
            }
        }
    }

}


#[cfg(test)]
mod tests {

    use env_logger;
    use log::{debug};
    use pyo3::exceptions::TypeError;
    use pyo3::prelude::*;
    use pyo3::types::{PyDict, PyTuple};
    use std::io::{Read, Seek, Write};
    use std::net::{TcpListener, TcpStream, SocketAddr};
    use std::os::unix::io::RawFd;
    use std::sync::mpsc::channel;
    use std::thread;
    use std::os::unix::io::{AsRawFd};
    use tempfile::NamedTempFile;

    use crate::filewrapper::{FileWrapper, SendFileInfo};

    fn init() {
        let _ = env_logger::builder().is_test(true).try_init();
    }

    #[test]
    fn test_no_fileno() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(r#"
class FL(object):

    def __init__(self):
        self.offset = 0

    def fileno(self):
        return -1

    def read(self, blocksize):
        result = b'Foo 42'[self.offset:self.offset+blocksize]
        self.offset += blocksize
        return result

f = FL()"#, None, Some(&locals)) {
            Ok(_) => {
                let filelike = locals.get_item("f").expect("Could not get file object").to_object(py);
                let fd: RawFd = filelike.call_method0(py, "fileno").expect("Could not call fileno method").extract(py).expect("Could not extract RawFd");
                let fwtype = py.get_type::<FileWrapper>();
                let bs = 2;
                let fwany = fwtype.call(PyTuple::new(py, vec![filelike, bs.to_object(py)]), None).unwrap();
                if let Ok(fw) = fwany.downcast_mut::<FileWrapper>() {
                    assert_eq!(fw.sendfileinfo.fd, fd);
                    for chunk in vec![b"Fo", b"o ", b"42"] {
                        match fw.next() {
                            Some(got) => {
                                debug!("Got: {:?}", got);
                                assert_eq!(chunk, &got[..]);
                            },
                            None => {
                                assert!(false);
                            }
                        }
                    }
                } else { assert!(false); }
            },
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_send_file() {
        init();
        let gil = Python::acquire_gil();
        let py = gil.python();
        let addr : SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let mut tmp = NamedTempFile::new().unwrap();
        let mut f = tmp.reopen().unwrap();
        f.seek(std::io::SeekFrom::Start(0)).unwrap();
        let fw = FileWrapper {
            filelike: py.None(),
            sendfileinfo: SendFileInfo::new(f.as_raw_fd(), 4)};
        tmp.write_all(b"Hello World!\n").unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 13];
            let snd = snd.clone();
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            rx.recv().unwrap();
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect");
        let mut sfi = fw.sendfileinfo;
        sfi.send_file(&mut connection);
        let mut b = got.recv().unwrap();
        debug!("send_file chunk 1: {:?}", b);
        assert_eq!(&b[..], b"Hell\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 4);
        let empty : Option<Vec<u8>> = Some(Vec::new());
        assert_eq!(sfi.next(), empty);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        debug!("send_file chunk 2: {:?}", b);
        assert_eq!(&b[..], b"o Wo\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 8);
        assert_eq!(sfi.next(), empty);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        debug!("send_file chunk 3: {:?}", b);
        assert_eq!(&b[..], b"rld!\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 12);
        assert_eq!(sfi.next(), empty);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        debug!("send_file chunk 4: {:?}", b);
        assert_eq!(&b[..], b"\n\0\0\0\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 13);
        assert_eq!(sfi.next(), None);
        tx.send(()).unwrap();
        t.join().unwrap();
    }

    #[test]
    fn test_file_wrapper_new_no_args() {
        init();
        let gil = Python::acquire_gil();
        let py = gil.python();
        let fwtype = py.get_type::<FileWrapper>();
        let empty: Vec<u8> = Vec::new();
        match fwtype.call(PyTuple::new(py, empty), None) {
            Err(e) => {
                assert!(e.is_instance::<TypeError>(py));
                // clear error from Python
                PyErr::fetch(py);
            },
            Ok(_) => assert!(false)
        }
    }
}
