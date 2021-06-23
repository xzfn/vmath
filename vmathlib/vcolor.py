
import colorsys

from vmath import Vector3
from vmathlib import vcolors

MISSING_COLOR = Vector3(1.0, 0.0, 1.0)

BLACK = Vector3(0.0, 0.0, 0.0)
GRAY = Vector3(0.5, 0.5, 0.5)
WHITE = Vector3(1.0, 1.0, 1.0)
RED = Vector3(1.0, 0.0, 0.0)
GREEN = Vector3(0.0, 1.0, 0.0)
BLUE = Vector3(0.0, 0.0, 1.0)
YELLOW = Vector3(1.0, 1.0, 0.0)
MAGENTA = Vector3(1.0, 0.0, 1.0)
CYAN = Vector3(0.0, 1.0, 1.0)


def named(colorname):
	return getattr(vcolors, colorname.lower(), MISSING_COLOR)

def hue(h):
	return Vector3(*colorsys.hsv_to_rgb(h, 1.0, 1.0))

def hsv(h, s, v):
	return Vector3(*colorsys.hsv_to_rgb(h, s, v))

def bounce(a, b, t):
	if t > 0.5:
		t = 1.0 - t
	t *= 2.0
	return a + (b - a) * t
