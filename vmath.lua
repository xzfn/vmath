-- vector math

-- locals

local Vector3
local Matrix4
local Quaternion
local Transform

-- Vector3

Vector3 = {}
Vector3.__index = Vector3

function Vector3.new(x, y, z)
	local self = setmetatable({}, Vector3)
	self.x = x or 0.0
	self.y = y or 0.0
	self.z = z or 0.0
	return self
end

function Vector3.length(self)
	return math.sqrt(self.x ^ 2 + self.y ^ 2 + self.z ^ 2)
end

function Vector3.length_squared(self)
	return self.x ^ 2 + self.y ^ 2 + self.z ^ 2
end

function Vector3.dot(self, other)
	return self.x * other.x + self.y * other.y + self.z * other.z
end

function Vector3.cross(self, other)
	local ax = self.x
	local ay = self.y
	local az = self.z
	local bx = other.x
	local by = other.y
	local bz = other.z
	return Vector3.new(ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx)
end

function Vector3.normalize_self(self)
	local length = self:length()
	if length > 0.0 then
		self.x = self.x / length
		self.y = self.y / length
		self.z = self.z / length
	else
		self.x = 1.0
		self.y = 0.0
		self.z = 0.0
	end
end

function Vector3.normalize(self)
	local v = self:copy()
	v:normalize_self()
	return v
end

function Vector3.__eq(self, other)
	return self.x == other.x and self.y == other.y and self.z == other.z
end

function Vector3.__add(self, other)
	return Vector3.new(self.x + other.x, self.y + other.y, self.z + other.z)
end

function Vector3.__mul(self, other)
	if getmetatable(self) ~= Vector3 then
		self, other = other, self
	end
	return Vector3.new(self.x * other, self.y * other, self.z * other)
end

function Vector3.__sub(self, other)
	return Vector3.new(self.x - other.x, self.y - other.y, self.z - other.z)
end

function Vector3.__unm(self)
	return Vector3.new(-self.x, -self.y, -self.z)
end

function Vector3.copy(self)
	return Vector3.new(self.x, self.y, self.z)
end

function Vector3.__tostring(self)
	return string.format('Vector3(%f, %f, %f)', self.x, self.y, self.z)
end

-- Matrix4

Matrix4 = {}
Matrix4.__index = Matrix4

function Matrix4.new(
	m00, m01, m02, m03, m10, m11, m12, m13,
	m20, m21, m22, m23, m30, m31, m32, m33
)
	local self = setmetatable({}, Matrix4)
	self.m00 = m00 or 1.0
	self.m01 = m01 or 0.0
	self.m02 = m02 or 0.0
	self.m03 = m03 or 0.0
	self.m10 = m10 or 0.0
	self.m11 = m11 or 1.0
	self.m12 = m12 or 0.0
	self.m13 = m13 or 0.0
	self.m20 = m20 or 0.0
	self.m21 = m21 or 0.0
	self.m22 = m22 or 1.0
	self.m23 = m23 or 0.0
	self.m30 = m30 or 0.0
	self.m31 = m31 or 0.0
	self.m32 = m32 or 0.0
	self.m33 = m33 or 1.0
	return self
end

function Matrix4.transform_point(self, p)
	-- ignore last row
	local x = p.x
	local y = p.y
	local z = p.z
	local nx = self.m00 * x + self.m10 * y + self.m20 * z + self.m30
	local ny = self.m01 * x + self.m11 * y + self.m21 * z + self.m31
	local nz = self.m02 * x + self.m12 * y + self.m22 * z + self.m32
	return Vector3.new(nx, ny, nz)
end

function Matrix4.transform_vector(self, v)
	-- ignore last row
	local x = v.x
	local y = v.y
	local z = v.z
	local nx = self.m00 * x + self.m10 * y + self.m20 * z
	local ny = self.m01 * x + self.m11 * y + self.m21 * z
	local nz = self.m02 * x + self.m12 * y + self.m22 * z
	return Vector3.new(nx, ny, nz)
end

function Matrix4.project_point(self, p)
	local x = p.x
	local y = p.y
	local z = p.z
	local nx = self.m00 * x + self.m10 * y + self.m20 * z + self.m30
	local ny = self.m01 * x + self.m11 * y + self.m21 * z + self.m31
	local nz = self.m02 * x + self.m12 * y + self.m22 * z + self.m32
	local nw = self.m03 * x + self.m13 * y + self.m23 * z + self.m33
	return Vector3(nx, ny, nz) * (1.0 / nw)
end

function Matrix4.inverse(self)
	-- TODO TRS only for now
	return self:to_transform():inverse():to_matrix4()
end

function Matrix4.transpose(self)
	local m00 = self.m00
	local m01 = self.m01
	local m02 = self.m02
	local m03 = self.m03
	local m10 = self.m10
	local m11 = self.m11
	local m12 = self.m12
	local m13 = self.m13
	local m20 = self.m20
	local m21 = self.m21
	local m22 = self.m22
	local m23 = self.m23
	local m30 = self.m30
	local m31 = self.m31
	local m32 = self.m32
	local m33 = self.m33
	return Matrix4.new(
		m00, m10, m20, m30,
		m01, m11, m21, m31,
		m02, m12, m22, m32,
		m03, m13, m23, m33)
end

function Matrix4.to_transform(self)
	local translation = Vector3.new(self.m30, self.m31, self.m32)
	local axis_x = Vector3.new(self.m00, self.m01, self.m02)
	local axis_y = Vector3.new(self.m10, self.m11, self.m12)
	local axis_z = Vector3.new(self.m20, self.m21, self.m22)
	local scale = Vector3.new(axis_x:length(), axis_y:length(), axis_z:length())
	axis_x:normalize_self()
	axis_y:normalize_self()
	axis_z:normalize_self()
	local rotation = Quaternion.from_matrix3({axis_x, axis_y, axis_z})
	return Transform.new(translation, rotation, scale)
end

function Matrix4.__mul(self, other)
	local am00 = self.m00
	local am01 = self.m01
	local am02 = self.m02
	local am03 = self.m03
	local am10 = self.m10
	local am11 = self.m11
	local am12 = self.m12
	local am13 = self.m13
	local am20 = self.m20
	local am21 = self.m21
	local am22 = self.m22
	local am23 = self.m23
	local am30 = self.m30
	local am31 = self.m31
	local am32 = self.m32
	local am33 = self.m33

	local bm00 = other.m00
	local bm01 = other.m01
	local bm02 = other.m02
	local bm03 = other.m03
	local bm10 = other.m10
	local bm11 = other.m11
	local bm12 = other.m12
	local bm13 = other.m13
	local bm20 = other.m20
	local bm21 = other.m21
	local bm22 = other.m22
	local bm23 = other.m23
	local bm30 = other.m30
	local bm31 = other.m31
	local bm32 = other.m32
	local bm33 = other.m33

	local cm00 = am00 * bm00 + am10 * bm01 + am20 * bm02 + am30 * bm03
	local cm01 = am01 * bm00 + am11 * bm01 + am21 * bm02 + am31 * bm03
	local cm02 = am02 * bm00 + am12 * bm01 + am22 * bm02 + am32 * bm03
	local cm03 = am03 * bm00 + am13 * bm01 + am23 * bm02 + am33 * bm03

	local cm10 = am00 * bm10 + am10 * bm11 + am20 * bm12 + am30 * bm13
	local cm11 = am01 * bm10 + am11 * bm11 + am21 * bm12 + am31 * bm13
	local cm12 = am02 * bm10 + am12 * bm11 + am22 * bm12 + am32 * bm13
	local cm13 = am03 * bm10 + am13 * bm11 + am23 * bm12 + am33 * bm13

	local cm20 = am00 * bm20 + am10 * bm21 + am20 * bm22 + am30 * bm23
	local cm21 = am01 * bm20 + am11 * bm21 + am21 * bm22 + am31 * bm23
	local cm22 = am02 * bm20 + am12 * bm21 + am22 * bm22 + am32 * bm23
	local cm23 = am03 * bm20 + am13 * bm21 + am23 * bm22 + am33 * bm23

	local cm30 = am00 * bm30 + am10 * bm31 + am20 * bm32 + am30 * bm33
	local cm31 = am01 * bm30 + am11 * bm31 + am21 * bm32 + am31 * bm33
	local cm32 = am02 * bm30 + am12 * bm31 + am22 * bm32 + am32 * bm33
	local cm33 = am03 * bm30 + am13 * bm31 + am23 * bm32 + am33 * bm33

	return Matrix4.new(cm00, cm01, cm02, cm03, cm10, cm11, cm12, cm13, cm20, cm21, cm22, cm23, cm30, cm31, cm32, cm33)
end

function Matrix4.__add(self, other)
	return Matrix4.new(
		self.m00 + other.m00, self.m01 + other.m01, self.m02 + other.m02, self.m03 + other.m03,
		self.m10 + other.m10, self.m11 + other.m11, self.m12 + other.m12, self.m13 + other.m13,
		self.m20 + other.m20, self.m21 + other.m21, self.m22 + other.m22, self.m23 + other.m23,
		self.m30 + other.m30, self.m31 + other.m31, self.m32 + other.m32, self.m33 + other.m33
	)
end

function Matrix4.__sub(self, other)
	return Matrix4.new(
		self.m00 - other.m00, self.m01 - other.m01, self.m02 - other.m02, self.m03 - other.m03,
		self.m10 - other.m10, self.m11 - other.m11, self.m12 - other.m12, self.m13 - other.m13,
		self.m20 - other.m20, self.m21 - other.m21, self.m22 - other.m22, self.m23 - other.m23,
		self.m30 - other.m30, self.m31 - other.m31, self.m32 - other.m32, self.m33 - other.m33
	)
end

function Matrix4.mul_scalar(self, s)
	return Matrix4.new(
		self.m00 * s, self.m01 * s, self.m02 * s, self.m03 * s,
		self.m10 * s, self.m11 * s, self.m12 * s, self.m13 * s,
		self.m20 * s, self.m21 * s, self.m22 * s, self.m23 * s,
		self.m30 * s, self.m31 * s, self.m32 * s, self.m33 * s
	)
end

function Matrix4.from_orthographic(left, right, bottom, top, near, far)
	local m00 = 2.0 / (right - left)
	local m11 = 2.0 / (top - bottom)
	local m22 = -2.0 / (far - near)
	local m30 = -(right + left) / (right - left)
	local m31 = -(top + bottom) / (top - bottom)
	local m32 = -near / (far - near)
	return Matrix4.new(
		m00, 0.0, 0.0, 0.0,
		0.0, m11, 0.0, 0.0,
		0.0, 0.0, m22, 0.0,
		m30, m31, m32, 1.0
	)
end

function Matrix4.from_perspective(fov, aspect, near, far)
	local tan_half_fov = math.tan(fov / 2.0)
	local m00 = 1.0 / (aspect * tan_half_fov)
	local m11 = 1.0 / tan_half_fov
	local m22 = -(far + near) / (far - near)
	local m23 = -1.0
	local m32 = -(2.0 * far * near) / (far - near)
	local m33 = 0.0
	return Matrix4.new(
		m00, 0.0, 0.0, 0.0,
		0.0, m11, 0.0, 0.0,
		0.0, 0.0, m22, m23,
		0.0, 0.0, m32, m33
	)
end

function Matrix4.copy(self)
	return Matrix4.new(
		self.m00, self.m01, self.m02, self.m03,
		self.m10, self.m11, self.m12, self.m13,
		self.m20, self.m21, self.m22, self.m23,
		self.m30, self.m31, self.m32, self.m33
	)
end

function Matrix4.__tostring(self)
	return string.format(
		'Matrix4(%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f)',
		self.m00, self.m01, self.m02, self.m03,
		self.m10, self.m11, self.m12, self.m13,
		self.m20, self.m21, self.m22, self.m23,
		self.m30, self.m31, self.m32, self.m33
	)
end

-- Quaternion

Quaternion = {}
Quaternion.__index = Quaternion

function Quaternion.new(w, x, y, z)
	local self = setmetatable({}, Quaternion)
	self.w = w or 1.0
	self.x = x or 0.0
	self.y = y or 0.0
	self.z = z or 0.0
	return self
end

function Quaternion.length(self)
	return math.sqrt(self.x ^ 2 + self.y ^ 2 + self.z ^ 2 + self.w ^ 2)
end

function Quaternion.length_squared(self)
	return self.x ^ 2 + self.y ^ 2 + self.z ^ 2 + self.w ^ 2
end

function Quaternion.normalize_self(self)
	local length = self:length()
	if length > 0.0 then
		self.w = self.w / length
		self.x = self.x / length
		self.y = self.y / length
		self.z = self.z / length
	else
		self.w = 1.0
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
	end
end

function Quaternion.normalize(self)
	local q = self:copy()
	q:normalize_self()
	return q
end

function Quaternion.slerp(self, other, t)
	local px = self.x
	local py = self.y
	local pz = self.z
	local pw = self.w
	local qx = other.x
	local qy = other.y
	local qz = other.z
	local qw = other.w
	local cos_theta = px * qx + py * qy + pz * qz + pw * qw
	if cos_theta < 0.0 then
		qx = -qx
		qy = -qy
		qz = -qz
		qw = -qw
		cos_theta = -cos_theta
	end
	local t0, t1
	if cos_theta > 0.999999 then
		t0 = 1.0 - t
		t1 = t
	else
		local angle = math.acos(cos_theta)
		local norm = 1.0 / math.sin(angle)
		t0 = math.sin((1.0 - t) * angle) * norm
		t1 = math.sin(t * angle) * norm
	end
	local x = px * t0 + qx * t1
	local y = py * t0 + qy * t1
	local z = pz * t0 + qz * t1
	local w = pw * t0 + qw * t1
	return Quaternion.new(w, x, y, z)
end

function Quaternion.conjugate(self)
	return Quaternion.new(self.w, -self.x, -self.y, -self.z)
end

function Quaternion.inverse(self)
	local x = self.x
	local y = self.y
	local z = self.z
	local w = self.w
	local rmagsqr = 1.0 / (x * x + y * y + z * z + w * w)
	return Quaternion.new(self.w * rmagsqr, -self.x * rmagsqr, -self.y * rmagsqr, -self.z * rmagsqr)
end

function Quaternion.angle_axis(self)
	local x = self.x
	local y = self.y
	local z = self.z
	local w = self.w
	local t1 = 1.0 - w * w
	if t1 <= 0.0 then
		return 0.0, Vector3.new(0.0, 0.0, 1.0)
	end
	local angle = math.atan(x * x + y * y + z * z, w) * 2.0
	local t2 = 1.0 / math.sqrt(t1)
	return angle, Vector3.new(x * t2, y * t2, z * t2)
end

function Quaternion.transform_point(self, p)
	return self:transform_vector(p)
end

function Quaternion.transform_vector(self, v)
	local vq = Quaternion(0.0, v.x, v.y, v.z)
	local q_v_qi = self * vq * self.inverse()
	return Vector3.new(q_v_qi.x, q_v_qi.y, q_v_qi.z)
end

function Quaternion.to_matrix3(self)
	local x = self.x
	local y = self.y
	local z = self.z
	local w = self.w

	local qxx = x * x
	local qyy = y * y
	local qzz = z * z
	local qxz = x * z
	local qxy = x * y
	local qyz = y * z
	local qwx = w * x
	local qwy = w * y
	local qwz = w * z

	local m00 = 1.0 - 2.0 * (qyy + qzz)
	local m01 = 2.0 * (qxy + qwz)
	local m02 = 2.0 * (qxz - qwy)

	local m10 = 2.0 * (qxy - qwz)
	local m11 = 1.0 - 2.0 * (qxx + qzz)
	local m12 = 2.0 * (qyz + qwx)

	local m20 = 2.0 * (qxz + qwy)
	local m21 = 2.0 * (qyz - qwx)
	local m22 = 1.0 - 2.0 * (qxx + qyy)

	local axis_x = Vector3.new(m00, m01, m02)
	local axis_y = Vector3.new(m10, m11, m12)
	local axis_z = Vector3.new(m20, m21, m22)
	return {axis_x, axis_y, axis_z}
end

function Quaternion.to_matrix4(self)
	local axis_x, axis_y, axis_z = self.to_matrix3()
	return Matrix4.new(
		axis_x.x, axis_x.y, axis_x.z, 0.0, axis_y.x, axis_y.y, axis_y.z, 0.0,
		axis_z.x, axis_z.y, axis_z.z, 0.0, 0.0, 0.0, 0.0, 1.0
	)
end

function Quaternion.from_angle_axis(angle, axis)
	local ha = angle * 0.5
	local s = math.sin(ha)
	local c = math.cos(ha)
	return Quaternion.new(c, axis.x * s, axis.y * s, axis.z * s)
end

function Quaternion.from_matrix3(matrix3)
	local axis_x, axis_y, axis_z = table.unpack(matrix3)
	local m00 = axis_x.x
	local m01 = axis_x.y
	local m02 = axis_x.z
	local m10 = axis_y.x
	local m11 = axis_y.y
	local m12 = axis_y.z
	local m20 = axis_z.x
	local m21 = axis_z.y
	local m22 = axis_z.z

	local fx = m00 - m11 - m22
	local fy = m11 - m00 - m22
	local fz = m22 - m00 - m11
	local fw = m00 + m11 + m22

	local bigi = 0
	local bigf = fw
	if fx > bigf then
		bigf = fx
		bigi = 1
	end
	if fy > bigf then
		bigf = fy
		bigi = 2
	end
	if fz > bigf then
		bigf = fz
		bigi = 3
	end
	local bigv = math.sqrt(bigf + 1.0) * 0.5
	local mult = 0.25 / bigv

	if bigi == 0 then
		return Quaternion.new(bigv, (m12 - m21) * mult, (m20 - m02) * mult, (m01 - m10) * mult)
	end
	if bigi == 1 then
		return Quaternion.new((m12 - m21) * mult, bigv, (m01 + m10) * mult, (m20 + m02) * mult)
	end
	if bigi == 2 then
		return Quaternion.new((m20 - m02) * mult, (m01 + m10) * mult, bigv, (m12 + m21) * mult)
	end
	if bigi == 3 then
		return Quaternion.new((m01 - m10) * mult, (m20 + m02) * mult, (m12 + m21) * mult, bigv)
	end
	return Quaternion.new()
end

function Quaternion.euler_angles(self)
	-- (pitch, yaw, roll), euler order y-x-z
	-- swap ZYX <-> YXZ from Wikipedia Conversion_between_quaternions_and_Euler_angles
	local x = self.z
	local y = self.x
	local z = self.y
	local w = self.w
	local xx = x * x
	local yy = y * y
	local zz = z * z
	local sinr_cosp = 2.0 * (w * x + y * z)
	local cosr_cosp = 1.0 - 2.0 * (xx + yy)
	local roll = math.atan(sinr_cosp, cosr_cosp)

	local sinp = 2.0 * (w * y - z * x)
	local pitch
	if math.abs(sinp) >= 1.0 then
		-- pitch = math.copysign(math.pi / 2.0, sinp)
		if sinp >= 0.0 then
			pitch = math.pi / 2.0
		else
			pitch = -math.pi / 2.0
		end
	else
		pitch = math.asin(sinp)
	end

	local siny_cosp = 2.0 * (w * z + x * y)
	local cosy_cosp = 1.0 - 2.0 * (yy + zz)
	local yaw = math.atan(siny_cosp, cosy_cosp)

	return Vector3.new(pitch, yaw, roll)
end

function Quaternion.from_euler_angles(euler_angles)
	-- (pitch, yaw, roll), euler order y-x-z
	local hpitch = euler_angles.x * 0.5
	local hyaw = euler_angles.y * 0.5
	local hroll = euler_angles.z * 0.5
	local cy = math.cos(hyaw)
	local sy = math.sin(hyaw)
	local cp = math.cos(hpitch)
	local sp = math.sin(hpitch)
	local cr = math.cos(hroll)
	local sr = math.sin(hroll)
	-- swap ZYX <-> YXZ from Wikipedia Conversion_between_quaternions_and_Euler_angles
	local w = cy * cp * cr + sy * sp * sr
	local x = cy * cp * sr - sy * sp * cr
	local y = sy * cp * sr + cy * sp * cr
	local z = sy * cp * cr - cy * sp * sr
	return Quaternion.new(w, y, z, x)
end

function Quaternion.from_from_to_rotation(va, vb)
	va = va.normalize()
	vb = vb.normalize()
	local axis = va.cross(vb).normalize()
	local angle = math.acos(va.dot(vb))
	return Quaternion.from_angle_axis(angle, axis)
end

function Quaternion.from_look_rotation(forward, up)
	-- forward becomes negative z
	local axis_z = -forward
	local axis_x = up.cross(axis_z).normalize()
	local axis_y = axis_z.cross(axis_x)
	return Quaternion.from_matrix3({axis_x, axis_y, axis_z})
end

function Quaternion.__mul(self, other)
	local px = self.x
	local py = self.y
	local pz = self.z
	local pw = self.w
	local qx = other.x
	local qy = other.y
	local qz = other.z
	local qw = other.w
	local w = pw * qw - px * qx - py * qy - pz * qz
	local x = pw * qx + px * qw + py * qz - pz * qy
	local y = pw * qy + py * qw + pz * qx - px * qz
	local z = pw * qz + pz * qw + px * qy - py * qx
	return Quaternion.new(w, x, y, z)
end

function Quaternion.copy(self)
	return Quaternion.new(self.w, self.x, self.y, self.z)
end

function Quaternion.__tostring(self)
	return string.format('Quaternion(%f, %f, %f, %f)', self.w, self.x, self.y, self.z)
end

-- Transform

Transform = {}
Transform.__index = Transform

function Transform.new(translation, rotation, scale)
	local self = setmetatable({}, Transform)
	self.translation = translation and translation:copy() or Vector3.new()
	self.rotation = rotation and rotation:copy() or Quaternion.new()
	self.scale = scale and scale:copy() or Vector3.new()
	return self
end

function Transform.transform_point(self, p)
	return self:to_matrix4():transform_point(p)
end

function Transform.transform_vector(self, v)
	return self:to_matrix4():transform_vector(v)
end

function Transform.inverse(self)
	local inv_translation = -self.translation
	local inv_rotation = self.rotation:inverse()
	local inv_scale = Vector3.new(1.0 / self.scale.x, 1.0 / self.scale.y, 1.0 / self.scale.z)
	local inv_mT = Matrix4.from_translation(inv_translation)
	local inv_mR = Matrix4.from_rotation(inv_rotation)
	local inv_mS = Matrix4.from_scale(inv_scale)
	local inv_m = inv_mS * inv_mR * inv_mT
	return inv_m:to_transform()
end

function Transform.to_matrix4(self)
	-- T * R * S
	local axis_x, axis_y, axis_z = self.rotation:to_axes()
	axis_x = axis_x * self.scale.x
	axis_y = axis_y * self.scale.y
	axis_z = axis_z * self.scale.z
	local translation = self.translation
	return Matrix4.new(axis_x.x, axis_x.y, axis_x.z, 0.0, axis_y.x, axis_y.y, axis_y.z, 0.0,
		axis_z.x, axis_z.y, axis_z.z, 0.0, translation.x, translation.y, translation.z, 1.0)
end

function Transform.__mul(self, other)
	local t1 = self.translation
	local r1 = self.rotation
	local s1 = self.scale
	local t2 = other.translation
	local r2 = other.rotation
	local s2 = other.scale
	local t3 = r1:transform_vector(Vector3.new(s1.x * t2.x, s1.y * t2.y, s1.z * t2.z)) + t1
	local r3 = r1 * r2
	local s3 = Vector3.new(s1.x * s2.x, s1.y * s2.y, s1.z * s2.z)
	return Transform.new(t3, r3, s3)
end

function Transform.copy(self)
	return Transform.new(self.translation, self.rotation, self.scale)
end

function Transform.__tostring(self)
	return string.format('Transform(%s, %s, %s)', self.translation, self.rotation, self.scale)
end


-- module


return {
	Vector3 = Vector3,
	Matrix4 = Matrix4,
	Quaternion = Quaternion,
	Transform = Transform,
}
