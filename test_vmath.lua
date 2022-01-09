local vmath = require('vmath')

local v1 = vmath.Vector3.new(1, 2, 3)
local v2 = vmath.Vector3.new(1, 2, 2)
print(v1 + v2)
print(v1 - v2)
print(v1 * 10)
print(10 * v1)
print(v1:cross(v2))
print(v2:dot(v1))

local v3 = v1:copy()
print(v3, v3:length(), v3:length_squared())
print(v3:normalize())
v3:normalize_self()
print(v3)

print('----')

local m = vmath.Matrix4.new()
m.m30 = 0.5
m.m31 = 1.0
print(v1)
print(m:transform_point(v1))

print('----')

local q = vmath.Quaternion.new(1.0, 0.1, 0.2, 0.3)
q:normalize_self()
print(q)
print(q:angle_axis())
print(q:inverse())
print(q:conjugate())


print('----')
print(m:to_transform())
