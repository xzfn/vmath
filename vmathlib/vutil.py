
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
	# 0 / 1 \ 0
	return 1.0 - abs(t * 2.0 - 1.0)

def half_pause(t):
	# 0 - 0 / 1 - 1
	return clamp(t * 2.0 - 0.5, 0.0, 1.0)

def half_pause_ping_pong(t):
	# 0 - 0 / 1 - 1 \ 0 - 0
	return clamp(ping_pong(t) * 2.0 - 0.5, 0.0, 1.0)

def lerp_matrix(a, b, t):
	return a + (b - a).mul_scalar(t)


def alpha_ease_none(alpha, exp):
	return alpha


def alpha_ease_in(alpha, exp):
	return math.pow(alpha, exp)


def alpha_ease_out(alpha, exp):
	return 1.0 - math.pow(1.0 - alpha, exp)


def alpha_ease_in_out(alpha, exp):
	if alpha < 0.5:
		return alpha_ease_in(alpha * 2.0, exp) * 0.5
	else:
		return alpha_ease_out(alpha * 2.0 - 1.0, exp) * 0.5 + 0.5
