use slog_envlogger;
use pyo3::exceptions::{IOError};
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

use crate::filewrapper::{FileWrapper};
use crate::globals::{WSGIGlobals};
use crate::server::{Server};
use crate::startresponse::{StartResponse};


#[pyfunction]
fn serve(application: PyObject, addr: &str, num_workers: usize, py: Python::<'static>) -> PyResult<()> {
    let addr = addr.parse()?;
    let globals = WSGIGlobals::new(addr, "", py);

    match slog_envlogger::init() {
        Ok(_) => {
            match Server::new(application, &globals, num_workers, py) {
                Ok(mut server) => {
                    match server.serve() {
                        Ok(_) => Ok(()),
                        Err(_) => return Err(PyErr::new::<IOError, _>("Error encountered during event loop"))
                    }
                },
                Err(e) => return Err(PyErr::new::<IOError, _>(format!("Could not create server: {:?}", e)))
            }
        },
        Err(_) => return Err(PyErr::new::<IOError, _>("Could not setup logging"))
    }
}

#[pymodule(pyruvate)]
fn _pruvate(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<StartResponse>().expect("Could not add StartResponse class to module");
    m.add_class::<FileWrapper>().expect("Could not add FileWrapper class to module");
    m.add_wrapped(wrap_pyfunction!(serve)).expect("Could not add serve() function to module");

    Ok(())
}
