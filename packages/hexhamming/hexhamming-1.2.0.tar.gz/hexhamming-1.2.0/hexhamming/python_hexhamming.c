#include <string.h>
#include <Python.h>

///////////////////////////////////////////////////////////////
// C API
///////////////////////////////////////////////////////////////

/**
 * A 16-by-16 matrix containing the hamming distances of
 * every hex character against every other hex character.
 */
const int LOOKUP_MATRIX[16][16] = {
  { 0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4 },
  { 1, 0, 2, 1, 2, 1, 3, 2, 2, 1, 3, 2, 3, 2, 4, 3 },
  { 1, 2, 0, 1, 2, 3, 1, 2, 2, 3, 1, 2, 3, 4, 2, 3 },
  { 2, 1, 1, 0, 3, 2, 2, 1, 3, 2, 2, 1, 4, 3, 3, 2 },
  { 1, 2, 2, 3, 0, 1, 1, 2, 2, 3, 3, 4, 1, 2, 2, 3 },
  { 2, 1, 3, 2, 1, 0, 2, 1, 3, 2, 4, 3, 2, 1, 3, 2 },
  { 2, 3, 1, 2, 1, 2, 0, 1, 3, 4, 2, 3, 2, 3, 1, 2 },
  { 3, 2, 2, 1, 2, 1, 1, 0, 4, 3, 3, 2, 3, 2, 2, 1 },
  { 1, 2, 2, 3, 2, 3, 3, 4, 0, 1, 1, 2, 1, 2, 2, 3 },
  { 2, 1, 3, 2, 3, 2, 4, 3, 1, 0, 2, 1, 2, 1, 3, 2 },
  { 2, 3, 1, 2, 3, 4, 2, 3, 1, 2, 0, 1, 2, 3, 1, 2 },
  { 3, 2, 2, 1, 4, 3, 3, 2, 2, 1, 1, 0, 3, 2, 2, 1 },
  { 2, 3, 3, 4, 1, 2, 2, 3, 1, 2, 2, 3, 0, 1, 1, 2 },
  { 3, 2, 4, 3, 2, 1, 3, 2, 2, 1, 3, 2, 1, 0, 2, 1 },
  { 3, 4, 2, 3, 2, 3, 1, 2, 2, 3, 1, 2, 1, 2, 0, 1 },
  { 4, 3, 3, 2, 3, 2, 2, 1, 3, 2, 2, 1, 2, 1, 1, 0 }
};

/**
 * Returns the hamming distance of the binary between two hexadecimal strings
 *
 * @param a    hexadecimal char array
 * @param b    hexadecimal char array
 * @param a_string_length length of `a`
 * @param b_string_length length of `b`
 * @return      the number of bits different between the hexadecimal strings
 */
inline int hamming_distance(
    const char* a,
    const char* b,
    size_t a_string_length,
    size_t b_string_length
  ) {
    // if both strings are the same, short circuit
    // and return 0
    if (strcmp(a, b) == 0) {
      return 0;
    }

    int result = 0;
    int val1, val2;
    size_t i;
    for (i = 0; i < a_string_length; ++i) {
        // check to make sure all characters are valid
        // hexadecimal in both strings
        if ((a[i] > 'F' && a[i] < 'a') || (a[i] > 'f') || (a[i] > '9' && a[i] < 'A') || (a[i] < '0') ||
            (b[i] > 'F' && b[i] < 'a') || (b[i] > 'f') || (b[i] > '9' && b[i] < 'A') || (b[i] < '0')) {
            return -1;
        }

        // Convert the hex ascii char to its actual hexadecimal value
        // e.g., '0' = 0, 'A' = 10, etc.
        // Note: this is case INSENSITIVE
        val1 = (a[i] > '9') ? (a[i] &~ 0x20) - 'A' + 10: (a[i] - '0');
        val2 = (b[i] > '9') ? (b[i] &~ 0x20) - 'A' + 10: (b[i] - '0');

        result += LOOKUP_MATRIX[val1][val2];
    }

    return result;
}

/**
 * Returns true if hexstrings are within a Hamming distance;
 * otherwise, returns false (stops early)
 *
 * @param a    hexadecimal char array
 * @param b    hexadecimal char array
 * @param a_string_length length of `a`
 * @param b_string_length length of `b`
 * @param max_dist maximum allowable hamming distance
 * @return      whether or not the strings are within some
 *              predefined hamming distance; -1 means an error has occurred
 */
inline int check_hexstrings_within_dist(
    const char* a,
    const char* b,
    size_t a_string_length,
    size_t b_string_length,
    size_t max_dist
  ) {
    // if both strings are the same, short circuit
    // and return 0
    if (strcmp(a, b) == 0) {
      return 1;
    }

    size_t result = 0;
    int val1, val2;
    size_t i;
    for (i = 0; i < a_string_length; ++i) {
        // check to make sure all characters are valid
        // hexadecimal in both strings
        if ((a[i] > 'F' && a[i] < 'a') || (a[i] > 'f') || (a[i] > '9' && a[i] < 'A') || (a[i] < '0') ||
            (b[i] > 'F' && b[i] < 'a') || (b[i] > 'f') || (b[i] > '9' && b[i] < 'A') || (b[i] < '0')) {
            return -1;
        }

        // Convert the hex ascii char to its actual hexadecimal value
        // e.g., '0' = 0, 'A' = 10, etc.
        // Note: this is case INSENSITIVE
        val1 = (a[i] > '9') ? (a[i] &~ 0x20) - 'A' + 10: (a[i] - '0');
        val2 = (b[i] > '9') ? (b[i] &~ 0x20) - 'A' + 10: (b[i] - '0');

        result += LOOKUP_MATRIX[val1][val2];
        if (result > max_dist) {
            return 0;
        }
    }

    return 1;
}

/**
 * Python interface for `hamming_distance`
 *
 * @param self      Python `self` object
 * @param args      Python arguments for `hamming_distance` interface
 *                  - `string1` -- hex string
 *                  - `string2` -- hex string
 * @returns         the integer hamming distance between the binary
 */
static PyObject * hamming_distance_wrapper(PyObject *self, PyObject *args) {
    char *input_s1;
    char *input_s2;

    // get the two strings from `args`
    // if they are incorrect types (i.e., not 's'), this will raise
    // a ValueError
    if (!PyArg_ParseTuple(args, "ss", &input_s1, &input_s2)) {
        PyErr_SetString(
            PyExc_ValueError,
            "error occurred while parsing arguments"
        );
        return NULL;
    }

    // if either c-string is NULL, can't move on, so raise
    if (input_s1 == NULL || input_s2 == NULL) {
        PyErr_SetString(PyExc_ValueError, "one or no strings provided!");
        return NULL;
    }

    size_t input_s1_len = strlen(input_s1);
    size_t input_s2_len = strlen(input_s2);

    if (input_s1_len != input_s2_len) {
        PyErr_SetString(PyExc_ValueError, "strings are NOT the same length");
        return NULL;
    }

    // at this point, we can safely proceed with
    // our `hamming_distance` computation
    int dist = hamming_distance(input_s1, input_s2, input_s1_len, input_s2_len);
    if (dist == -1) {
      // this should only happen if the strings contain
      // invalid hexadecimal characters
      PyErr_SetString(PyExc_ValueError, "hex string contains invalid char");
      return NULL;
    } else {
      // put the unsigned int into a Python Int object
      // and return back to the caller!
      return Py_BuildValue("I", dist);
    }
}

/**
 * Python interface for `check_hexstrings_within_dist`
 *
 * @param self      Python `self` object
 * @param args      Python arguments for `check_hexstrings_within_dist` interface
 *                  - `string1` -- hex string
 *                  - `string2` -- hex string
 * @returns         
 */
static PyObject * check_hexstrings_within_dist_wrapper(PyObject *self, PyObject *args) {
    char *input_s1;
    char *input_s2;
    unsigned int max_dist;

    // get the two strings from `args`
    // if they are incorrect types (i.e., not 's'), this will raise
    // a ValueError
    if (!PyArg_ParseTuple(args, "ssI", &input_s1, &input_s2, &max_dist)) {
        PyErr_SetString(
            PyExc_ValueError,
            "error occurred while parsing arguments"
        );
        return NULL;
    }

    // if either c-string is NULL, can't move on, so raise
    if (input_s1 == NULL || input_s2 == NULL) {
        PyErr_SetString(PyExc_ValueError, "one or no strings provided!");
        return NULL;
    }

    size_t input_s1_len = strlen(input_s1);
    size_t input_s2_len = strlen(input_s2);

    if (input_s1_len != input_s2_len) {
        PyErr_SetString(PyExc_ValueError, "strings are NOT the same length");
        return NULL;
    }

    if ((int)max_dist < 0) {
        PyErr_SetString(PyExc_ValueError, "`max_dist` must be >0");
        return NULL;
    }

    if (max_dist > input_s1_len) {
        return Py_BuildValue("O", Py_True);
    }

    // at this point, we can safely proceed with
    // our `hamming_distance` computation
    int result = check_hexstrings_within_dist(
        input_s1,
        input_s2,
        input_s1_len,
        input_s2_len,
        max_dist
    );
    if (result == -1) {
      // this should only happen if the strings contain
      // invalid hexadecimal characters
      PyErr_SetString(PyExc_ValueError, "hex string contains invalid char");
      return NULL;
    } else {
      // put the unsigned int into a Python Int object
      // and return back to the caller!
      return Py_BuildValue("O", result == 1 ? Py_True : Py_False);
    }
}

///////////////////////////////////////////////////////////////
// Docstrings
///////////////////////////////////////////////////////////////
static char hamming_docstring[] =
    "Calculate the hamming distance of two strings\n\n"
    "This is equivalent to\n\n"
    "    bin(int(a, 16) ^ int(b, 16)).count('1')\n\n"
    "with the only difference being it was written in C and optimized\n"
    "using a lookup table of pre-calculated hexadecimal hamming distances.\n"
    ":param a: hexadecimal string\n"
    ":type a: str\n"
    ":param b: hexadecimal string\n"
    ":type b: str\n"
    ":returns: the hamming distance between the bits of two hexadecimal strings\n"
    ":rtype: int\n"
    ":raises ValueError: if either string doesn't exist, "
    "if the strings are different lengths, or if the strings aren't valid hex";

static char check_hexstrings_within_dist_docstring[] =
    "Check if the hex strings are within a specified Hamming Distance\n\n"
    "This is equivalent to\n\n"
    "    bin(int(a, 16) ^ int(b, 16)).count('1') < max_dist \n\n"
    "with the only difference being it was written in C and optimized\n"
    "using a lookup table of pre-calculated hexadecimal hamming distances.\n"
    ":param a: hexadecimal string\n"
    ":type a: str\n"
    ":param b: hexadecimal string\n"
    ":type b: str\n"
    ":param max_dist: maximum allowable Hamming Distance\n"
    ":type max_dist: int\n"
    ":returns: whether or not the two hex strings are within `max_dist`\n"
    ":rtype: int\n"
    ":raises ValueError: if either string doesn't exist, "
    "if the strings are different lengths, or if the strings aren't valid hex";

static char CompareDocstring[] =
    "Module for calculating hamming distance of two hexadecimal strings";

///////////////////////////////////////////////////////////////
// Python C-extension Initialization
///////////////////////////////////////////////////////////////
static PyMethodDef CompareMethods[] = {
    {"hamming_distance", hamming_distance_wrapper, METH_VARARGS, hamming_docstring},
    {"check_hexstrings_within_dist", check_hexstrings_within_dist_wrapper, METH_VARARGS, check_hexstrings_within_dist_docstring},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef hexhammingdef = {
        PyModuleDef_HEAD_INIT,
        "hexhamming",
        CompareDocstring,
        -1,
        CompareMethods,
        NULL
};

#define INITERROR return NULL

PyMODINIT_FUNC
PyInit_hexhamming(void)

#else
#define INITERROR return

PyMODINIT_FUNC
inithexhamming(void)
#endif

{
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&hexhammingdef);
#else
    PyObject *module = Py_InitModule3("hexhamming", CompareMethods, CompareDocstring);
#endif
    if (PyModule_AddStringConstant(module, "__version__", "1.2.0")) {
        Py_XDECREF(module);
        INITERROR;
    }
    if (module == NULL) {
        INITERROR;
    }

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
