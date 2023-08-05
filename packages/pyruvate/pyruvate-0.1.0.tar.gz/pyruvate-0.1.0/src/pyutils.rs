pub use pyo3::ffi::PyGILState_STATE;
use pyo3::ffi;
use pyo3::prelude::*;


#[inline]
pub fn with_gil<'a, F, R>(mut code: F) -> R
where
    F: FnMut(Python<'a>, PyGILState_STATE) -> R {
    let (gilstate, py) = unsafe {
        (ffi::PyGILState_Ensure(), Python::assume_gil_acquired())
    };
    let result = code(py, gilstate);
    unsafe { ffi::PyGILState_Release(gilstate)};
    result
}


#[inline]
pub fn with_released_gil<'a, F, R>(gilstate: PyGILState_STATE, mut code: F) -> R
where
    F: FnMut() -> R {
    unsafe { ffi::PyGILState_Release(gilstate)};
    let result = code();
    unsafe { ffi::PyGILState_Ensure() };
    result
}


pub fn close_pyobject(ob: &mut PyObject, py: Python) -> PyResult<()> {
    match ob.getattr(py, "close") {
        Ok(_) => {
            ob.call_method0(py, "close")?;
        },
        Err(_) => {}
    }
    Ok(())
}
