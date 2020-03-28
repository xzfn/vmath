
import ctypes

def matrix_to_ctype(m):
    return (ctypes.c_float * 16)(
        m.m00, m.m01, m.m02, m.m03, m.m10, m.m11, m.m12, m.m13,
        m.m20, m.m21, m.m22, m.m23, m.m30, m.m31, m.m32, m.m33)
