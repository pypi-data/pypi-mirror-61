#include <Python.h>
#include "bitap.h"


static PyObject *
bitap_wrapper(PyObject *self, PyObject *args) {
  const char *text;
  const char *pattern;
  int index;

  if (!PyArg_ParseTuple(args, "ss", &pattern, &text))
    return NULL;
  index = bitap(text, pattern);

  return PyLong_FromLong(index);
}

static PyObject *
fuzzy_bitap_wrapper(PyObject *self, PyObject *args) {
  const char *text;
  const char *pattern;
  int k;
  int index;

  if (!PyArg_ParseTuple(args, "ssi", &pattern, &text, &k))
    return NULL;
  index = fuzzy_bitap(text, pattern, k);

  return PyLong_FromLong(index);
}


static PyMethodDef BitapMethods[] = {
  { "bitap", bitap_wrapper, METH_VARARGS, "Exact bitap search" },
  { "bitap_fuzzy", fuzzy_bitap_wrapper, METH_VARARGS, "Fuzzy bitap search" },
  { NULL, NULL, 0, NULL }
};

static struct PyModuleDef bitapmodule = {
    PyModuleDef_HEAD_INIT,
    "bitap",   /* name of module */
    NULL, /*bitap_doc, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    BitapMethods
};

PyMODINIT_FUNC
PyInit_bitap(void)
{
    return PyModule_Create(&bitapmodule);
}
