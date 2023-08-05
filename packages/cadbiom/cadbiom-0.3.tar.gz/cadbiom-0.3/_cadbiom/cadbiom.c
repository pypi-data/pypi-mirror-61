/*************
Python bindings for Cadbiom functions (https://gitlab.inria.fr/pvignet/cadbiom)

Copyright (c) 2016-2017, Pierre Vignet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
**********************************/

#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
//#include <iostream>
//#define CADBIOM_VERSION "0.1.0"

#define MODULE_NAME "_cadbiom"
#define MODULE_DOC "Cadbiom python C extension."

#if PY_MAJOR_VERSION == 2 && PY_MINOR_VERSION <= 5
#define PyUnicode_FromString  PyString_FromString
#endif

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#endif

#ifdef IS_PY3K
    #define IS_INT(x)  PyLong_Check(x)
    #define PYNUMBER_FROM_LONG(x)  PyLong_FromLong(x)

    #define PYSTRING_FROM_STRING  PyUnicode_FromString

    #define MODULE_INIT_FUNC(name) \
        PyMODINIT_FUNC PyInit_ ## name(void); \
        PyMODINIT_FUNC PyInit_ ## name(void)
#else
    #define IS_INT(x)  (PyInt_Check(x) || PyLong_Check(x))
    #define PYNUMBER_FROM_LONG(x)  PyInt_FromLong(x)

    #define PYSTRING_FROM_STRING  PyString_FromString

    #define MODULE_INIT_FUNC(name) \
        static PyObject *PyInit_ ## name(void); \
        PyMODINIT_FUNC init ## name(void); \
        PyMODINIT_FUNC init ## name(void) { PyInit_ ## name(); } \
        static PyObject *PyInit_ ## name(void)
#endif

#define PY_PRINTF(o) \
    PyObject_Print(o, stdout, 0); printf("\n");

int raw_get_unshift_code(int* var_num, int* shift_step);

static PyObject *outofconflerr = NULL;

PyDoc_STRVAR(get_unshift_code_doc,
"get_unshift_code(var_num, shift_step)\n\
\n\
Get the real value of the given variable in the system (remove the shift)\n\
\n\
:param var_num: DIMACS literal coding of a shifted variable x_i\n\
:param shift_step: Shift step dependant on the run\n\
:return: DIMACS literal coding of  x_0 with same value\n\
:type var_num: <int>\n\
:type shift_step: <int>\n\
:rtype: <int>"
);

static PyObject* get_unshift_code(PyObject *self, PyObject *args, PyObject *kwds)
{
    #ifndef NDEBUG
    /* Debugging code */
    printf("get unshift code\n");
    #endif

    int var_num;
    int shift_step;

    static char* kwlist[] = {"var_num", "shift_step", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "ii", kwlist,
                                     &var_num,
                                     &shift_step)) {
        return NULL;
    }

    int var_code = (abs(var_num) - 1) % shift_step + 1;

//     std::cout << "var_num: " << var_num << std::endl;
//     std::cout << "shift_step: " << shift_step << std::endl;
//     std::cout << "var_code: " << var_code << std::endl;

    // Ce test est probablement un reliquat des tests présents dans CLUnfolder
    // où shift_step est en fait shift_step_init, qui lui, peut être inférieur à shift_step
    if (var_code <= shift_step) {
        // std::cout << "result: " << var_code * ((var_num < 0) ? -1 : 1) << std::endl;
        return Py_BuildValue("i", var_code * ((var_num < 0) ? -1 : 1));
    }

    PyErr_SetString(PyExc_ValueError, "Not a DIMACS code of an initial variable.");
    return NULL;
}

int raw_get_unshift_code(int* var_num, int* shift_step)
{
    // Equivalent of get_unshift_code but in full C
    int var_code = (abs(*var_num) - 1) % *shift_step + 1;

    // std::cout << "result: " << var_code * ((*var_num < 0) ? -1 : 1) << std::endl;
    return var_code * ((*var_num < 0) ? -1 : 1);
}

static int _shift_clause(PyObject *self, PyObject *numeric_clause, PyObject *shifted_clause, int* shift_step)
{
    PyObject *numeric_clause_iterator = PyObject_GetIter(numeric_clause);
    if (numeric_clause_iterator == NULL) {
        /* propagate error */
        PyErr_SetString(PyExc_SystemError, "could not create iterator on clause");
        return 0;
    }

    PyObject *lit;
    PyObject *shifted_lit;
    Py_ssize_t i = 0;
    long lit_val = 0;
    while ((lit = PyIter_Next(numeric_clause_iterator)) != NULL) {
        #ifndef NDEBUG
        /* Debugging code */
        if (!IS_INT(lit))  {
            PyErr_SetString(PyExc_TypeError, "integer expected in list");
            Py_DECREF(numeric_clause_iterator);
            Py_DECREF(lit);
            return 0;
        }
        #endif

        // Mieux vaut rester avec des PyObject pour faire les additions ou pas ???
        lit_val = PyLong_AsLong(lit);

        if (lit_val > 0) {
            shifted_lit = PYNUMBER_FROM_LONG(lit_val + *shift_step);
        } else {
            shifted_lit = PYNUMBER_FROM_LONG(lit_val - *shift_step);
        }

        // Add shifted_lit (use SET_ITEM instead of PyList_Append)
        // => shifted_clause is a new list there will be no leak of previously inserted items
        PyList_SET_ITEM(shifted_clause, i, shifted_lit);

        i++;

        /* release reference when done */
        // Append does not steal a reference, so shifted_lit refcount = 2
        // after Py_DECREF, shifted_lit refcount = 1, but stored in the list so the pointer var can be reused
        // SET_ITEM steals a reference, so : no Py_DECREF on items !
        Py_DECREF(lit);
    }

    /* release reference when done */
    Py_DECREF(numeric_clause_iterator);

    if (PyErr_Occurred()) {
        /* propagate error */
        return 0;
    }
    return 1;
}

PyDoc_STRVAR(shift_clause_doc,
"shift_clause(numeric_clause, shift_step)\n\
Implementation of the shift operator. Shift a numeric clause in one step.\n\
\n\
Basically, `shift_step` is added to positive variables and subtracted\n\
from negative variables in `numeric_clause`.\n\
\n\
.. warning:: Before the call you MUST lock the unfolder with:\n\
\"self.__locked = True\".\n\
\n\
:param numeric_clause: DIMACS clause (list of literals)\n\
:param shift_step: Shift step dependant on the run\n\
:return: DIMACS literal coding of x_0 with same value\n\
:type numeric_clause: <list <int>>\n\
:type shift_step: <int>\n\
:rtype: <list>"
);

static PyObject* shift_clause(PyObject *self, PyObject *args, PyObject *kwds)
{
    // https://docs.python.org/2/c-api/iter.html
    #ifndef NDEBUG
    /* Debugging code */
    printf("shift clause\n");
    #endif

    int shift_step;
    PyObject *numeric_clause;

    static char* kwlist[] = {"numeric_clause", "shift_step", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "Oi", kwlist,
                                     &numeric_clause,
                                     &shift_step)) {
        return NULL;
    }

    // Declare a new list with the size of the given one
    PyObject *shifted_clause = PyList_New(PySequence_Size(numeric_clause));
    if (shifted_clause == NULL) {
        PyErr_SetString(PyExc_SystemError, "failed to create a list");
        return NULL;
    }

    // Shift clause and fill shifted_clause (new ref)
    int ret = _shift_clause(self, numeric_clause, shifted_clause, &shift_step);
    if (ret == 0 || PyErr_Occurred()) {
        /* propagate error */
        Py_XDECREF(shifted_clause);
        return PyErr_SetFromErrno(outofconflerr);
    }

    // Return list of all shifted literals
    return shifted_clause;
}

static int _forward_code(PyObject *self, PyObject *clause, PyObject **numeric_clause, PyObject *var_code_table, int* shift_step)
{

    // Get attr literals of clause object
    PyObject* literals = PyObject_GetAttrString(clause, "literals");
    if (literals == NULL) {
        PyErr_SetString(PyExc_SystemError, "failed get attribute 'literals' on clause object");
        return 0;
    }

    PyObject *literals_iterator = PyObject_GetIter(literals);
    if (literals_iterator == NULL) {
        PyErr_SetString(PyExc_SystemError, "could not create iterator on 'literals' attribute");
        return 0;
    }

    // Declare a new list with the size of 'literals'
    *numeric_clause = PyList_New(PySequence_Size(literals));
    if (*numeric_clause == NULL) {
        PyErr_SetString(PyExc_SystemError, "failed to create a list");
        return 0;
    }
    // Append does not steal a reference, so we need Py_DECREF
    // SET_ITEM steals a reference, so: no Py_DECREF on items !

    PyObject *lit;
    long lit_val;
    PyObject *lit_name;
    PyObject *lit_sign;
    PyObject *lit_name_last_char;
    PyObject *variable_value;
    PyObject *multiply_result;
    PyObject *last_char = PYSTRING_FROM_STRING("`");
    Py_ssize_t i = 0;
    Py_ssize_t name_size = 0;
    while ((lit = PyIter_Next(literals_iterator)) != NULL) {

        // get name and sign attributes of the literal in clause
        lit_name = PyObject_GetAttrString(lit, "name"); // new ref
        lit_sign = PyObject_GetAttrString(lit, "sign"); // new ref
        #ifdef IS_PY3K
        name_size = PyBytes_GET_SIZE(lit_name);
        #else
        name_size = PyString_GET_SIZE(lit_name);
        #endif
        //std::cout << "name size" << name_size << std::endl;

        // Get value corresponding to lit_name
        // Borrowed reference
        variable_value = PyDict_GetItem(var_code_table, lit_name);
        if (variable_value == NULL) {
            Py_DECREF(lit_name);
            Py_DECREF(lit_sign);
            Py_DECREF(lit);

            Py_DECREF(literals);
            Py_DECREF(literals_iterator);
            Py_DECREF(last_char);
            PyErr_SetString(PyExc_KeyError, "lit_name not found in dict");
            return 0;
        }
        // Because variable_value reference IS borrowed (owned by PyDict_GetItem)
        // we don't do Py_DECREF(variable_value);

        // Get and test last char of the name
        lit_name_last_char = PySequence_ITEM(lit_name, name_size - 1); // new ref
        // Returns -1 on error, 0 if the result is false, 1 otherwise
        if (PyObject_RichCompareBool(lit_name_last_char, last_char, Py_EQ)) {
            // If last char is '`'
            // t+1 variable

            // Add shift_step to the value corresponding to the given name
            lit_val = PyLong_AsLong(variable_value) + *shift_step;

            // Ret of PyObject_Not is: 1 if lit is false, -1 on failure
            multiply_result = (PyObject_Not(lit_sign)) ? PYNUMBER_FROM_LONG(-lit_val) : PYNUMBER_FROM_LONG(lit_val); // new ref

        } else {
            // t variable

            // Get variable_value
            lit_val = PyLong_AsLong(variable_value);

            // Ret of PyObject_Not is: 1 if lit is false, -1 on failure
            multiply_result = (PyObject_Not(lit_sign)) ? PYNUMBER_FROM_LONG(-lit_val) : PYNUMBER_FROM_LONG(lit_val); // new ref
        }

        // Because PyList_SET_ITEM steals the reference of multiply_result, we don't do Py_DECREF(multiply_result);
        PyList_SET_ITEM(*numeric_clause, i, multiply_result);

        // Note:
        // Add new lit_cod (use SET_ITEM instead of PyList_Append)
        // => numeric_clause is a new list there will be no leak of previously inserted items
        // Append does not steal a reference, so shifted_lit refcount = 2
        // after Py_DECREF, shifted_lit refcount = 1, but stored in the list so the pointer var can be reused
        // SET_ITEM steals a reference, so : no Py_DECREF on items !

        i++;

        /* release reference when done */
        Py_DECREF(lit_name);
        Py_DECREF(lit_name_last_char);
        Py_DECREF(lit_sign);
        Py_DECREF(lit);
    }

    /* release reference when done */
    Py_DECREF(literals);
    Py_DECREF(literals_iterator);
    Py_DECREF(last_char);

    if (PyErr_Occurred()) {
        /* propagate error */
        return 0;
    }
    return 1;
}

PyDoc_STRVAR(forward_code_doc,
"forward_code(clause, var_code_table, shift_step)\n\
Translation from names to num codes. The translation depends on the shift direction.\n\
\n\
Numerically code a clause with the numeric codes found in\n\
self.__var_code_table for a base variable x,\n\
and numeric_code +/- shift_step (according to the sign) for x' variable.\n\
\n\
.. note:: Future variables x' are noted \"name`\" in Literal names.\n\
    The absolute value of these variables will increase by shift_step\n\
    in the next step.\n\
\n\
:param clause: a Clause object\n\
:param var_code_table: Var code table from the model\n\
:param shift_step: Shift step dependant on the run\n\
:return: the DIMACS coding of the forward shifted clause\n\
:type clause: <list <int>>\n\
:type var_code_table: <dict>\n\
:type shift_step: <int>\n\
:rtype: <list>"
);

static PyObject* forward_code(PyObject *self, PyObject *args, PyObject *kwds)
{
    #ifndef NDEBUG
    /* Debugging code */
    printf("forward code\n");
    #endif

    int shift_step;
    PyObject *clause;
    PyObject *var_code_table;

    static char* kwlist[] = {"clause", "var_code_table", "shift_step", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOi", kwlist,
                                     &clause,
                                     &var_code_table,
                                     &shift_step)) {
        return NULL;
    }

    PyObject *numeric_clause = NULL;

    // Shift clause and fill shifted_clause (new ref)
    int ret = _forward_code(self, clause, &numeric_clause, var_code_table, &shift_step);
    if (ret == 0 || PyErr_Occurred()) {
        /* propagate error */
        Py_XDECREF(numeric_clause);
        return PyErr_SetFromErrno(outofconflerr);
    }

    // Return list of all numeric_clause
    return numeric_clause;
}

PyDoc_STRVAR(forward_init_dynamic_doc,
"forward_init_dynamic(clauses, var_code_table, shift_step, [aux_clauses])\n\
Dynamics initialisations. Set dynamic constraints for a forward one step: X1 = f(X0)\n\
\n\
Numerically code clauses with the numeric codes found in\n\
self.__var_code_table for a base variable x,\n\
and numeric_code +/- shift_step (according to the sign) for x' variable.\n\
\n\
__dynamic_constraints is a list of lists of numeric clauses (lists of ints)\n\
Each sublist of __dynamic_constraints corresponds to a step in the unfolder;\n\
the last step is the last element.\n\
\n\
.. note:: Future variables x' are noted \"name`\" in Literal names.\n\
    The absolute value of these variables will increase by shift_step\n\
    in the next step.\n\
\n\
:param clauses: List of Clause objects\n\
:param var_code_table: Var code table from the model\n\
:param shift_step: Shift step dependant on the run\n\
:param aux_clauses: List of auxiliary Clause objects\n\
:return: A list of lists of DIMACS coding of the forward shifted clauses\n\
:type clauses: <list <Clause>>\n\
:type var_code_table: <dict>\n\
:type shift_step: <int>\n\
:type aux_clauses: <list <Clause>>\n\
:rtype: <list <list <list <int>>>>"
);

static PyObject* forward_init_dynamic(PyObject *self, PyObject *args, PyObject *kwds)
{
    #ifndef NDEBUG
    /* Debugging code */
    printf("forward init dynamic\n");
    #endif

    int shift_step;
    PyObject *clauses;
    // The C variables corresponding to optional arguments should be initialized to their default value —
    // when an optional argument is not specified, PyArg_ParseTuple() does not touch the contents of the corresponding C variable(s).
    PyObject *aux_clauses = NULL;
    PyObject *var_code_table;

    static char* kwlist[] = {"clauses", "var_code_table", "shift_step", "aux_clauses", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOi|O", kwlist,
                                     &clauses,
                                     &var_code_table,
                                     &shift_step,
                                     &aux_clauses)) {
        return NULL;
    }
    if (aux_clauses == NULL) {
        aux_clauses = PyList_New(0);
        if (aux_clauses == NULL) {
            PyErr_SetString(PyExc_SystemError, "failed to create a list");
            return NULL;
        }
    }

    PyObject *numeric_clauses = PyList_New(PySequence_Size(clauses) + PySequence_Size(aux_clauses));
    if (numeric_clauses == NULL) {
        PyErr_SetString(PyExc_SystemError, "failed to create a list");
        return NULL;
    }

    // Default clauses ////////////////////////////////////////////////////////

    PyObject *clauses_iterator = PyObject_GetIter(clauses);
    if (clauses_iterator == NULL) {
        /* propagate error */
        PyErr_SetString(PyExc_SystemError, "could not create iterator on list");
        return NULL;
    }

    PyObject *clause;
    Py_ssize_t i = 0;
    PyObject *numeric_clause = NULL;
    while ((clause = PyIter_Next(clauses_iterator)) != NULL) {

        // Forward code the non numeric clause to numeric_clause (new ref)
        int ret = _forward_code(self, clause, &numeric_clause, var_code_table, &shift_step);
        if (ret == 0 || PyErr_Occurred()) {
            /* propagate error */
            Py_XDECREF(numeric_clause);
            Py_DECREF(clauses_iterator);
            Py_DECREF(clause);
            Py_DECREF(numeric_clauses);
            return PyErr_SetFromErrno(outofconflerr);
        }

        PyList_SET_ITEM(numeric_clauses, i, numeric_clause);

        /* release reference when done */
        // no DECREF on the return of forward_code, because PyList_SET_ITEM steals reference
        Py_DECREF(clause);

        i++;
    }

    /* release reference when done */
    Py_DECREF(clauses_iterator);

    // Auxiliary clauses //////////////////////////////////////////////////////

    clauses_iterator = PyObject_GetIter(aux_clauses);
    if (clauses_iterator == NULL) {
        /* propagate error */
        PyErr_SetString(PyExc_SystemError, "could not create iterator on aux list");
        return NULL;
    }

    while ((clause = PyIter_Next(clauses_iterator)) != NULL) {

        // Forward code the non numeric clause to numeric_clause (new ref)
        int ret = _forward_code(self, clause, &numeric_clause, var_code_table, &shift_step);
        if (ret == 0 || PyErr_Occurred()) {
            /* propagate error */
            Py_XDECREF(numeric_clause);
            Py_DECREF(clauses_iterator);
            Py_DECREF(clause);
            Py_DECREF(numeric_clauses);
            return PyErr_SetFromErrno(outofconflerr);
        }

        PyList_SET_ITEM(numeric_clauses, i, numeric_clause);

        /* release reference when done */
        // no DECREF on the return of forward_code, because PyList_SET_ITEM steals reference
        Py_DECREF(clause);

        i++;
    }

    /* release reference when done */
    Py_DECREF(clauses_iterator);

    // Build a list and put in it the list of numeric clauses (lists of ints).
    PyObject* dynamic_constraints = PyList_New(1);
    // NULL on failure
    PyList_SET_ITEM(dynamic_constraints, 0, numeric_clauses);

    if (PyErr_Occurred()) {
        /* propagate error */
        Py_DECREF(dynamic_constraints);
        // No decref (SET_ITEM) Py_DECREF(numeric_clauses);
        return PyErr_SetFromErrno(outofconflerr);
    }

    // Return list of all dynamic_constraints
    return dynamic_constraints;
}

PyDoc_STRVAR(shift_dimacs_clauses_doc,
"shift_dimacs_clauses(numeric_clauses, shift_step)\n\
Shift numeric clauses representing the dynamics X' = f(X,I,C)\n\
\n\
Basically, `shift_step` is added to positive variables and subtracted\n\
from negative variables in each clause in `numeric_clauses`.\n\
\n\
:param numeric_clauses: List of clauses in DIMACS format (constraints)\n\
:param shift_step: Shift step dependant on the run\n\
:return: A list of DIMACS coding of the forward shifted clause\n\
:type numeric_clauses: <list <list <int>>>\n\
:type shift_step: <int>\n\
:rtype: <list <list <int>>>"
);

static PyObject* shift_dimacs_clauses(PyObject *self, PyObject *args, PyObject *kwds)
{
    #ifndef NDEBUG
    /* Debugging code */
    printf("shift dynamic\n");
    #endif

    int shift_step;
    PyObject* numeric_clauses;

    static char* kwlist[] = {"numeric_clauses", "shift_step", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "Oi", kwlist,
                                     &numeric_clauses,
                                     &shift_step)) {
        return NULL;
    }

    if (!PySequence_Check(numeric_clauses)) {
        PyErr_SetString(PyExc_TypeError, "sequence expected");
        return NULL;
    }

    Py_ssize_t size = PySequence_Size(numeric_clauses);
    if (size == 0) {
        // Empty list, return empty list
        return PyList_New(0);
    }
    //printf("List size: %d\n", size);

    PyObject *shifted_numeric_clauses = PyList_New(PySequence_Size(numeric_clauses));
    if (shifted_numeric_clauses == NULL) {
        PyErr_SetString(PyExc_SystemError, "failed to create a list");
        return NULL;
    }

    // Iterate on last item
    PyObject *numeric_clauses_iterator = PyObject_GetIter(numeric_clauses);
    if (numeric_clauses_iterator == NULL) {
        /* propagate error */
        PyErr_SetString(PyExc_SystemError, "could not create iterator on list");
        return NULL;
    }

    PyObject *shifted_clause;
    PyObject *clause;
    Py_ssize_t i = 0;
    while ((clause = PyIter_Next(numeric_clauses_iterator)) != NULL) {

        // Declare a new list with the size of the given one
        shifted_clause = PyList_New(PySequence_Size(clause));
        if (shifted_clause == NULL) {
            PyErr_SetString(PyExc_SystemError, "failed to create a list");
            return NULL;
        }

        // Shift clause and fill shifted_clause (new ref)
        int ret = _shift_clause(self, clause, shifted_clause, &shift_step);
        if (ret == 0 || PyErr_Occurred()) {
            /* propagate error */
            Py_XDECREF(shifted_clause);
            Py_DECREF(shifted_numeric_clauses);
            Py_DECREF(numeric_clauses_iterator);
            Py_DECREF(clause);
            return PyErr_SetFromErrno(outofconflerr);
        }

        PyList_SET_ITEM(shifted_numeric_clauses, i, shifted_clause);

        /* release reference when done */
        // no DECREF on the return of shift_clause, because PyList_SET_ITEM steals reference
        Py_DECREF(clause);

        i++;
    }
    /* release reference when done */
    Py_DECREF(numeric_clauses_iterator);

    return shifted_numeric_clauses;
}

PyDoc_STRVAR(unflatten_doc,
"unflatten(solution, shift_step_init, shift_step)\n\
Transform a flat DIMACS representation of a trajectory into a list<list<int>>\n\
each sublist represents a state vector. Auxiliary variables introduced by\n\
properties compiling are ignored.\n\
\n\
:param solution: List of Clause objects (dynamic_constraints)\n\
:param shift_step_init: \n\
:param shift_step: Shift step dependant on the run\n\
:return: A list of state vectors (<list <int>>) in DIMACS format\n\
:type solution: <list <int>>\n\
:type shift_step_init: <int>\n\
:type shift_step: <int>\n\
:rtype: <list <list <int>>>"
);

static PyObject* unflatten(PyObject *self, PyObject *args, PyObject *kwds)
{
    #ifndef NDEBUG
    /* Debugging code */
    printf("unflatten\n");
    #endif

    int shift_step;
    int shift_step_init; // Attention peut être modifié à la volée si variables auxiliaires... cf __code_clause
    int var_num;
    PyObject* solution;

    static char* kwlist[] = {"solution", "shift_step_init", "shift_step", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "Oii", kwlist,
                                     &solution,
                                     &shift_step_init,
                                     &shift_step)) {
        return NULL;
    }

    size_t solution_size = PySequence_Size(solution);
    // TODO: déduction en effet d'apres le nombre de variables du systeme
    // print(shift_step_init, len(self.__solution)) (47633, 238164)
    // Len: (238164 - 47633) / 47633 = 3.9999
    // PyObject *trajectory_steps_values = PyList_New((solution_size - shift_step) / shift_step);
    PyObject *trajectory_steps_values = PyList_New(0);
    if (trajectory_steps_values == NULL) {
        PyErr_SetString(PyExc_SystemError, "failed to create a list");
        return NULL;
    }

    Py_ssize_t step = 0;
    size_t offset_step = 0;
    PyObject *unshift_code;
    PyObject *item;
    PyObject *tmp_traj;
    //PyObject *arglist;
    int i = 0;
    while ((offset_step + shift_step) < solution_size) {

        tmp_traj = PyList_New(shift_step_init);
        if (tmp_traj == NULL) {
            PyErr_SetString(PyExc_SystemError, "failed to create a list");
            Py_DECREF(trajectory_steps_values);
            return NULL;
        }

        for (i = 0; i < shift_step_init; i++) {

            // Get item of solution (int)
            // TODO: think about PyList_GET_ITEM or PyTuple_GET_ITEM (borrowed ref)
            item = PySequence_ITEM(solution, i + offset_step); // new ref
            if(item == NULL) {
                Py_DECREF(tmp_traj);
                Py_DECREF(trajectory_steps_values);
                return NULL;
            }

            // Get the real value of the given variable in the system (remove the shift)
            // Build parameters of get_unshift_code
            /*
                // Full python version with error handling on var_code value that must be <= shift_step
                // {"var_num", "shift_step", NULL};
                #ifdef IS_PY3K
                arglist = Py_BuildValue("(ii)", PyLong_AS_LONG(item), shift_step);
                #else
                arglist = Py_BuildValue("(ii)", PyInt_AS_LONG(item), shift_step);
                #endif
                Py_DECREF(item);

                unshift_code = get_unshift_code(self, arglist, NULL);
                Py_DECREF(arglist);
            */

            // Full C version without (useless?) error handling on var_code value that must be <= shift_step
            #ifdef IS_PY3K
            var_num = PyLong_AS_LONG(item);
            #else
            var_num = PyInt_AS_LONG(item);
            #endif
            Py_DECREF(item);

            // Equivalent of get_unshift_code but in full C
            unshift_code = PYNUMBER_FROM_LONG(raw_get_unshift_code(&var_num, &shift_step)); // new ref

            if(unshift_code == NULL) {
                /* Pass error back */
                Py_DECREF(tmp_traj);
                Py_DECREF(trajectory_steps_values);
                return NULL;
            }

            PyList_SET_ITEM(tmp_traj, i, unshift_code);
            // Steal: no DECREF
        }

        //PyList_SET_ITEM(trajectory_steps_values, step, tmp_traj);
        PyList_Append(trajectory_steps_values, tmp_traj);
        Py_DECREF(tmp_traj);

        step++;
        // first index of time step
        offset_step = step * shift_step;

    }

    if (PyErr_Occurred()) {
        /* propagate error */
        Py_DECREF(trajectory_steps_values);
        return PyErr_SetFromErrno(outofconflerr);
    }

    // Return list of all trajectories
    return trajectory_steps_values;
}

/*************************** Method definitions *************************/

static PyMethodDef module_methods[] = {
    {"get_unshift_code", (PyCFunction) get_unshift_code, METH_VARARGS | METH_KEYWORDS, get_unshift_code_doc},
    {"unflatten", (PyCFunction) unflatten, METH_VARARGS | METH_KEYWORDS, unflatten_doc},
    {"shift_clause", (PyCFunction) shift_clause, METH_VARARGS | METH_KEYWORDS, shift_clause_doc},
    {"shift_dimacs_clauses", (PyCFunction) shift_dimacs_clauses, METH_VARARGS | METH_KEYWORDS, shift_dimacs_clauses_doc},
    {"forward_code", (PyCFunction) forward_code, METH_VARARGS | METH_KEYWORDS, forward_code_doc},
    {"forward_init_dynamic", (PyCFunction) forward_init_dynamic, METH_VARARGS | METH_KEYWORDS, forward_init_dynamic_doc},
    {NULL, NULL, 0, NULL}     /* Sentinel - marks the end of this structure */
};

MODULE_INIT_FUNC(_cadbiom)
{
    PyObject* m;

    #ifdef IS_PY3K
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,  /* m_base */
        MODULE_NAME,            /* m_name */
        MODULE_DOC,             /* m_doc */
        -1,                     /* m_size */
        module_methods          /* m_methods */
    };

    m = PyModule_Create(&moduledef);
    #else
    m = Py_InitModule3(MODULE_NAME, module_methods, MODULE_DOC);
    #endif

    // Return NULL on Python3 and on Python2 with MODULE_INIT_FUNC macro
    // In pure Python2: return nothing.
    if (!m) {
        Py_XDECREF(m);
        return NULL;
    }

    // Add the version string
    if (PyModule_AddStringConstant(m, "__version__", CADBIOM_VERSION) == -1) {
        Py_DECREF(m);
        return NULL;
    }
    if (!(outofconflerr = PyErr_NewExceptionWithDoc("_cadbiom.InternalError", "Unsupported error.", NULL, NULL))) {
        goto error;
    }
    PyModule_AddObject(m, "OutOfConflicts",  outofconflerr);

error:
    if (PyErr_Occurred())
    {
        PyErr_SetString(PyExc_ImportError, "_cadbiom: init failed");
        Py_DECREF(m);
        return NULL;
    }
    return m;
}

int main(void)
{
    printf("Try to invoke main() for debugging !!!!\n");


    //init_cadbiom();
    PyObject *func_result = NULL;
    PyObject *arglist;

    /*
    // shift_clause([66036, -66037], 47633)
    PyObject *list = PyList_New(2);
    PyObject *list_elem = PyInt_FromLong(66036);
    PyObject *list_elem_1 = PyInt_FromLong(-66037);
    PyList_SET_ITEM(list, 0, list_elem);
    PyList_SET_ITEM(list, 1, list_elem_1);


    arglist = Py_BuildValue("(Oi)", list, 47633);
    printf("ici 2\n");
    func_result = shift_clause(NULL, arglist, NULL);
    printf("LA\n");
    Py_DECREF(arglist);
    Py_DECREF(func_result);
    Py_DECREF(list);
    */

    // get_unshift_code(50, 47633)
    arglist = Py_BuildValue("(ii)", (Py_ssize_t)50, (Py_ssize_t)47633);
    func_result = get_unshift_code(NULL, arglist, NULL);
    Py_DECREF(arglist);
    Py_DECREF(func_result);

    return EXIT_SUCCESS;
}
