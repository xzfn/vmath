
from vmath import Vector3
from vmathlib import vcolors

MISSING_COLOR = Vector3(1.0, 0.0, 1.0)

def named(colorname):
	return getattr(vcolors, colorname.lower(), MISSING_COLOR)
