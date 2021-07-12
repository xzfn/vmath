
import math

import vmath

VEC3_ZERO = vmath.Vector3(0.0, 0.0, 0.0)
VEC3_ONES = vmath.Vector3(1.0, 1.0, 1.0)

VEC3_X = vmath.Vector3(1.0, 0.0, 0.0)
VEC3_Y = vmath.Vector3(0.0, 1.0, 0.0)
VEC3_Z = vmath.Vector3(0.0, 0.0, 1.0)


def lerp(a, b, t):
	return a + (b - a) * t

def fract(f):
	return math.modf(f)[0]

def clamp(v, min_val, max_val):
	if v < min_val:
		return min_val
	if v > max_val:
		return max_val
	return v

def ping_pong(t):
	# 0 - 1 - 0
	return 1.0 - abs(t * 2.0 - 1.0)

def lerp_matrix(a, b, t):
	return a + (b - a).mul_scalar(t)
