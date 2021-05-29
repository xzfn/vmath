#include <pybind11/pybind11.h>

#include "wrap_vmath.h"

PYBIND11_MODULE(_vmath, m) {
    wrap_vmath(m);
}
