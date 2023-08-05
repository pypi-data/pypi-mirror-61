use log::{error};
use pyo3::prelude::*;
use std::net::{SocketAddr};


pub struct WSGIGlobals<'a> {
    pub server_info: SocketAddr,
    pub script_name: &'a str,
    pub io_module: &'a PyModule,
    pub sys_module: &'a PyModule,
    pub wsgi_module: Option<&'a PyModule>
}


impl <'a> WSGIGlobals::<'a> {

    pub fn new(server_info: SocketAddr, script_name: &'a str, py: Python<'a>) -> WSGIGlobals::<'a> {
        // XXX work around not being able to import wsgi module from tests
        let wsgi_module = match py.import("pyruvate") {
            Ok(pyruvate) => Some(pyruvate),
            Err(e) => {
                error!("Could not import WSGI module, so no FileWrapper: {:?}", e);
                None
            }
        };
        WSGIGlobals {
            server_info: server_info,
            script_name: script_name,
            io_module: py.import("io").expect("Could not import module io"),
            sys_module: py.import("sys").expect("Could not import module sys"),
            wsgi_module: wsgi_module,
        }
    }

}


#[cfg(test)]
mod tests {
    use crate::globals::WSGIGlobals;
    use log::debug;
    use pyo3::prelude::*;

    #[test]
    fn test_creation() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let si = "127.0.0.1:7878".parse().unwrap();
        let sn = "/foo";
        let pypath = py.import("sys").unwrap().get("path").unwrap();
        debug!("sys.path: {:?}", pypath);
        let got = WSGIGlobals::new(si, sn, py);
        assert!(got.server_info == si);
        assert!(got.script_name == sn);
    }

}
