#include <Python.h>

#include "zbase32.h"

#define DIVIDE_ROUNDED_UP(m,n) (((m) / (n)) + ((m) % (n) > 0 ? 1 : 0))


static PyObject *
pyzbase32_ext_decode(PyObject *self, PyObject *args)
{
  unsigned char *encoded, *decoded;
  unsigned int bits, decoded_length, encoded_length;
  PyObject *result;

  if (!PyArg_ParseTuple(args,"s#I",&encoded,&encoded_length,&bits))
    return NULL;

  decoded_length = DIVIDE_ROUNDED_UP(bits,8);
  decoded = PyMem_New(unsigned char,decoded_length);

  zbase32_decode(decoded,encoded,bits);

  result = PyBytes_FromStringAndSize((char*)decoded,decoded_length);
  PyMem_Free(decoded);

  return result;
}


static PyObject *
pyzbase32_ext_encode(PyObject *self, PyObject *args)
{
  unsigned char *input, *encoded;
  unsigned int bits, encoded_length, input_length;
  PyObject *result;

  if (!PyArg_ParseTuple(args,"s#I",&input,&input_length,&bits))
    return NULL;

  encoded_length = DIVIDE_ROUNDED_UP(bits,5);
  encoded = PyMem_New(unsigned char,encoded_length);

  zbase32_encode(encoded,input,bits);

  result = PyBytes_FromStringAndSize((char*)encoded,encoded_length);
  PyMem_Free(encoded);

  return result;
}


PyMODINIT_FUNC
PyInit_ext(void)
{
  static PyMethodDef methods[] = {
    {"decode", pyzbase32_ext_decode, METH_VARARGS,
     "Decode z-base-32 encoded bytes."},
    {"encode", pyzbase32_ext_encode, METH_VARARGS,
     "Encode bytes using z-base-32."},
    {NULL, NULL, 0, NULL}
  };

  static PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "ext",
    "z-base-32 codec extension",
    -1,
    methods
  };

  return PyModule_Create(&module);
}
