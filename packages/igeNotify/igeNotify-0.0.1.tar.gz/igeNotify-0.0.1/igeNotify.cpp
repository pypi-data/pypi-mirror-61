#include <memory>
#include <Python.h>

#include "Notify.h"
#include "igeNotify_doc_en.h"

static std::shared_ptr<Notify> gNotify = nullptr;

static PyObject* notify_notify(PyObject* self, PyObject* args) {
    int id;
    char* title;
    char* message;
    unsigned long delay = 30000;
    int repeat = 0;
    int priority = 0;

    if (!PyArg_ParseTuple(args, "iss|kii", &id, &title, &message, &delay, &repeat, &priority)) {
        return NULL;
    }

    gNotify->notify(id, std::string(title), std::string(message), delay, repeat, priority);

    Py_RETURN_NONE;
}

static PyMethodDef notify_methods[] = {
    { "notify", (PyCFunction)notify_notify, METH_VARARGS, notify_doc},
    { nullptr, nullptr, 0, nullptr }
};

static PyModuleDef notify_module = {
    PyModuleDef_HEAD_INIT,
    "igeNotify",
    "Notification module",
    0,
    notify_methods
};

PyMODINIT_FUNC PyInit_igeNotify() {
    gNotify = std::make_shared<Notify>();
    return PyModule_Create(&notify_module);
}
