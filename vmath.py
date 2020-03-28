
import math

__all__ = ['Vector', 'Matrix', 'Quaternion', 'Transform']


class Vector(object):
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __copy__(self):
        return Vector(self.x, self.y, self.z)

    copy = __copy__

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        ax = self.x
        ay = self.y
        az = self.z
        bx = other.x
        by = other.y
        bz = other.z
        return Vector(ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx)

    def normalize(self):
        l = self.length()
        if l == 0.0:
            self.x = 1.0
            self.y = 0.0
            self.z = 0.0
        else:
            self *= 1.0 / l

    def normalized(self):
        v = self.copy()
        v.normalize()
        return v

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __mul__(self, n):
        return Vector(self.x * n, self.y * n, self.z * n)

    def __imul__(self, n):
        self.x *= n
        self.y *= n
        self.z *= n
        return self

    __rmul__ = __mul__

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __repr__(self):
        return 'Vector({:0.4f}, {:0.4f}, {:0.4f})'.format(self.x, self.y, self.z)


class Matrix(object):
    """Column major matrix.

    m00, m01, m02, m03 is the first column.
    """
    __slots__ = ('m00', 'm01', 'm02', 'm03', 'm10', 'm11', 'm12', 'm13',
                 'm20', 'm21', 'm22', 'm23', 'm30', 'm31', 'm32', 'm33')

    def __init__(self,
                 m00=1.0, m01=0.0, m02=0.0, m03=0.0, m10=0.0, m11=1.0, m12=0.0, m13=0.0,
                 m20=0.0, m21=0.0, m22=1.0, m23=0.0, m30=0.0, m31=0.0, m32=0.0, m33=1.0):
        self.m00 = m00
        self.m01 = m01
        self.m02 = m02
        self.m03 = m03
        self.m10 = m10
        self.m11 = m11
        self.m12 = m12
        self.m13 = m13
        self.m20 = m20
        self.m21 = m21
        self.m22 = m22
        self.m23 = m23
        self.m30 = m30
        self.m31 = m31
        self.m32 = m32
        self.m33 = m33

    def __mul__(self, other):
        am00 = self.m00
        am01 = self.m01
        am02 = self.m02
        am03 = self.m03
        am10 = self.m10
        am11 = self.m11
        am12 = self.m12
        am13 = self.m13
        am20 = self.m20
        am21 = self.m21
        am22 = self.m22
        am23 = self.m23
        am30 = self.m30
        am31 = self.m31
        am32 = self.m32
        am33 = self.m33

        bm00 = other.m00
        bm01 = other.m01
        bm02 = other.m02
        bm03 = other.m03
        bm10 = other.m10
        bm11 = other.m11
        bm12 = other.m12
        bm13 = other.m13
        bm20 = other.m20
        bm21 = other.m21
        bm22 = other.m22
        bm23 = other.m23
        bm30 = other.m30
        bm31 = other.m31
        bm32 = other.m32
        bm33 = other.m33

        cm00 = am00 * bm00 + am10 * bm01 + am20 * bm02 + am30 * bm03
        cm01 = am01 * bm00 + am11 * bm01 + am21 * bm02 + am31 * bm03
        cm02 = am02 * bm00 + am12 * bm01 + am22 * bm02 + am32 * bm03
        cm03 = am03 * bm00 + am13 * bm01 + am23 * bm02 + am33 * bm03

        cm10 = am00 * bm10 + am10 * bm11 + am20 * bm12 + am30 * bm13
        cm11 = am01 * bm10 + am11 * bm11 + am21 * bm12 + am31 * bm13
        cm12 = am02 * bm10 + am12 * bm11 + am22 * bm12 + am32 * bm13
        cm13 = am03 * bm10 + am13 * bm11 + am23 * bm12 + am33 * bm13

        cm20 = am00 * bm20 + am10 * bm21 + am20 * bm22 + am30 * bm23
        cm21 = am01 * bm20 + am11 * bm21 + am21 * bm22 + am31 * bm23
        cm22 = am02 * bm20 + am12 * bm21 + am22 * bm22 + am32 * bm23
        cm23 = am03 * bm20 + am13 * bm21 + am23 * bm22 + am33 * bm23

        cm30 = am00 * bm30 + am10 * bm31 + am20 * bm32 + am30 * bm33
        cm31 = am01 * bm30 + am11 * bm31 + am21 * bm32 + am31 * bm33
        cm32 = am02 * bm30 + am12 * bm31 + am22 * bm32 + am32 * bm33
        cm33 = am03 * bm30 + am13 * bm31 + am23 * bm32 + am33 * bm33

        return Matrix(cm00, cm01, cm02, cm03, cm10, cm11, cm12, cm13, cm20, cm21, cm22, cm23, cm30, cm31, cm32, cm33)

    def __repr__(self):
        return 'Matrix({:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f})'.format(
            self.m00, self.m01, self.m02, self.m03, self.m10, self.m11, self.m12, self.m13,
            self.m20, self.m21, self.m22, self.m23, self.m30, self.m31, self.m32, self.m33)

    def __str__(self):
        return 'Matrix<{:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}\n       {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}\n       {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}\n       {:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}>'.format(
            self.m00, self.m10, self.m20, self.m30,
            self.m01, self.m11, self.m21, self.m31,
            self.m02, self.m12, self.m22, self.m32,
            self.m03, self.m13, self.m23, self.m33)

    def transform_point(self, p):
        # ignore last row
        x = p.x
        y = p.y
        z = p.z
        nx = self.m00 * x + self.m10 * y + self.m20 * z + self.m30
        ny = self.m01 * x + self.m11 * y + self.m21 * z + self.m31
        nz = self.m02 * x + self.m12 * y + self.m22 * z + self.m32
        return Vector(nx, ny, nz)

    def transform_vector(self, v):
        # ignore last row
        x = v.x
        y = v.y
        z = v.z
        nx = self.m00 * x + self.m10 * y + self.m20 * z
        ny = self.m01 * x + self.m11 * y + self.m21 * z
        nz = self.m02 * x + self.m12 * y + self.m22 * z
        return Vector(nx, ny, nz)

    def project_point(self, p):
        x = p.x
        y = p.y
        z = p.z
        nx = self.m00 * x + self.m10 * y + self.m20 * z + self.m30
        ny = self.m01 * x + self.m11 * y + self.m21 * z + self.m31
        nz = self.m02 * x + self.m12 * y + self.m22 * z + self.m32
        nw = self.m03 * x + self.m13 * y + self.m23 * z + self.m33
        return Vector(nx, ny, nz) * (1.0 / nw)

    def decompose(self):
        translation = Vector(self.m30, self.m31, self.m32)
        axis_x = Vector(self.m00, self.m01, self.m02)
        axis_y = Vector(self.m10, self.m11, self.m12)
        axis_z = Vector(self.m20, self.m21, self.m22)
        scale = Vector(axis_x.length(), axis_y.length(), axis_z.length())
        axis_x.normalize()
        axis_y.normalize()
        axis_z.normalize()
        rotation = Quaternion.from_axes(axis_x, axis_y, axis_z)
        return Transform(translation, rotation, scale)

    def inversed(self):
        # TRS only
        return self.decompose().inversed().to_matrix()

    def set_translation(self, translation):
        self.m30 = translation.x
        self.m31 = translation.y
        self.m32 = translation.z

    def set_look_rotation(self, forward, up):
        # forward becomes negative z, reset scale
        axis_z = -forward
        axis_x = up.cross(axis_z).normalized()
        axis_y = axis_z.cross(axis_x)
        self.m00 = axis_x.x
        self.m01 = axis_x.y
        self.m02 = axis_x.z
        self.m10 = axis_y.x
        self.m11 = axis_y.y
        self.m12 = axis_y.z
        self.m20 = axis_z.x
        self.m21 = axis_z.y
        self.m22 = axis_z.z

    @staticmethod
    def from_translation(translation):
        return Matrix(m30=translation.x, m31=translation.y, m32=translation.z)

    @staticmethod
    def from_rotation(rotation):
        return rotation.to_matrix()

    @staticmethod
    def from_angle_axis(angle, axis):
        return Matrix.from_rotation(Quaternion.from_angle_axis(angle, axis))

    @staticmethod
    def from_scale(scale):
        return Matrix(m00=scale.x, m11=scale.y, m22=scale.z)

    @staticmethod
    def from_look_at(eye, center, up):
        forward = center - eye
        forward.normalize()
        side = forward.cross(up)
        side.normalize()
        camup = side.cross(forward)
        m00 = side.x
        m10 = side.y
        m20 = side.z
        m01 = camup.x
        m11 = camup.y
        m21 = camup.z
        m02 = -forward.x
        m12 = -forward.y
        m22 = -forward.z
        m30 = -side.dot(eye)
        m31 = -camup.dot(eye)
        m32 = forward.dot(eye)
        return Matrix(m00, m01, m02, 0.0, m10, m11, m12, 0.0, m20, m21, m22, 0.0, m30, m31, m32, 1.0)

    @staticmethod
    def from_ortho(left, right, bottom, top, near, far):
        m00 = 2.0 / (right - left)
        m11 = 2.0 / (top - bottom)
        m22 = -2.0 / (far - near)
        m30 = -(right + left) / (right - left)
        m31 = -(top + bottom) / (top - bottom)
        m32 = -near / (far - near)
        return Matrix(m00=m00, m11=m11, m22=m22, m30=m30, m31=m31, m32=m32)

    @staticmethod
    def from_perspective(fov, aspect, near, far):
        tan_half_fov = math.tan(fov / 2.0)
        m00 = 1.0 / (aspect * tan_half_fov)
        m11 = 1.0 / tan_half_fov
        m22 = -(far + near) / (far - near)
        m23 = -1.0
        m32 = -(2.0 * far * near) / (far - near)
        m33 = 0.0
        return Matrix(m00=m00, m11=m11, m22=m22, m23=m23, m32=m32, m33=m33)


class Quaternion(object):
    __slots__ = ('w', 'x', 'y', 'z')

    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __copy__(self):
        return Quaternion(self.w, self.x, self.y, self.z)

    copy = __copy__

    def __repr__(self):
        return 'Quaternion({:0.4f}, {:0.4f}, {:0.4f}, {:0.4f})'.format(self.w, self.x, self.y, self.z)

    def __mul__(self, other):
        res = self.copy()
        res *= other
        return res

    def __imul__(self, other):
        px = self.x
        py = self.y
        pz = self.z
        pw = self.w
        qx = other.x
        qy = other.y
        qz = other.z
        qw = other.w
        self.w = pw * qw - px * qx - py * qy - pz * qz
        self.x = pw * qx + px * qw + py * qz - pz * qy
        self.y = pw * qy + py * qw + pz * qx - px * qz
        self.z = pw * qz + pz * qw + px * qy - py * qx
        return self

    def slerp(self, other, t):
        px = self.x
        py = self.y
        pz = self.z
        pw = self.w
        qx = other.x
        qy = other.y
        qz = other.z
        qw = other.w
        cos_theta = px * qx + py * qy + pz * qz + pw * qw
        if cos_theta < 0.0:
            qx = -qx
            qy = -qy
            qz = -qz
            qw = -qw
            cos_theta = -cos_theta
        if cos_theta > 0.999999:
            t0 = 1.0 - t
            t1 = t
        else:
            angle = math.acos(cos_theta)
            norm = 1.0 / math.sin(angle)
            t0 = math.sin((1.0 - t) * angle) * norm
            t1 = math.sin(t * angle) * norm
        x = px * t0 + qx * t1
        y = py * t0 + qy * t1
        z = pz * t0 + qz * t1
        w = pw * t0 + qw * t1
        return Quaternion(w, x, y, z)

    def to_axes(self):
        x = self.x
        y = self.y
        z = self.z
        w = self.w

        qxx = x * x
        qyy = y * y
        qzz = z * z
        qxz = x * z
        qxy = x * y
        qyz = y * z
        qwx = w * x
        qwy = w * y
        qwz = w * z

        m00 = 1.0 - 2.0 * (qyy + qzz)
        m01 = 2.0 * (qxy + qwz)
        m02 = 2.0 * (qxz - qwy)

        m10 = 2.0 * (qxy - qwz)
        m11 = 1.0 - 2.0 * (qxx + qzz)
        m12 = 2.0 * (qyz + qwx)

        m20 = 2.0 * (qxz + qwy)
        m21 = 2.0 * (qyz - qwx)
        m22 = 1.0 - 2.0 * (qxx + qyy)

        axis_x = Vector(m00, m01, m02)
        axis_y = Vector(m10, m11, m12)
        axis_z = Vector(m20, m21, m22)
        return (axis_x, axis_y, axis_z)

    def to_matrix(self):
        axis_x, axis_y, axis_z = self.to_axes()
        return Matrix(axis_x.x, axis_x.y, axis_x.z, 0.0, axis_y.x, axis_y.y, axis_y.z, 0.0,
            axis_z.x, axis_z.y, axis_z.z, 0.0, 0.0, 0.0, 0.0, 1.0)

    def angle_axis(self):
        x = self.x
        y = self.y
        z = self.z
        w = self.w
        t1 = 1.0 - w * w
        if t1 <= 0.0:
            return (0.0, Vector(0.0, 0.0, 1.0))
        angle = math.atan2(x * x + y * y + z * z, w) * 2.0
        t2 = 1.0 / math.sqrt(t1)
        return (angle, Vector(x * t2, y * t2, z * t2))

    def euler_angles(self):
        # (pitch, yaw, roll), euler order y-x-z
        # swap ZYX <-> YXZ from Wikipedia Conversion_between_quaternions_and_Euler_angles
        x = self.z
        y = self.x
        z = self.y
        w = self.w
        xx = x * x
        yy = y * y
        zz = z * z
        sinr_cosp = 2.0 * (w * x + y * z)
        cosr_cosp = 1.0 - 2.0 * (xx + yy)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        sinp = 2.0 * (w * y - z * x)
        if abs(sinp) >= 1.0:
            pitch = math.copysign(math.pi / 2.0, sinp)
        else:
            pitch = math.asin(sinp)

        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (yy + zz)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return Vector(pitch, yaw, roll)

    def conjugated(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inversed(self):
        x = self.x
        y = self.y
        z = self.z
        w = self.w
        rmagsqr = 1.0 / (x * x + y * y + z * z + w * w)
        return Quaternion(self.w * rmagsqr, -self.x * rmagsqr, -self.y * rmagsqr, -self.z * rmagsqr)

    def transform_vector(self, v):
        vq = Quaternion(0.0, v.x, v.y, v.z)
        q_v_qi = self * vq * self.inversed()
        return Vector(q_v_qi.x, q_v_qi.y, q_v_qi.z)

    @staticmethod
    def from_euler_angles(euler_angles):
        # (pitch, yaw, roll), euler order y-x-z
        hpitch = euler_angles.x * 0.5
        hyaw = euler_angles.y * 0.5
        hroll = euler_angles.z * 0.5
        cy = math.cos(hyaw)
        sy = math.sin(hyaw)
        cp = math.cos(hpitch)
        sp = math.sin(hpitch)
        cr = math.cos(hroll)
        sr = math.sin(hroll)
        # swap ZYX <-> YXZ from Wikipedia Conversion_between_quaternions_and_Euler_angles
        w = cy * cp * cr + sy * sp * sr
        x = cy * cp * sr - sy * sp * cr
        y = sy * cp * sr + cy * sp * cr
        z = sy * cp * cr - cy * sp * sr
        return Quaternion(w, y, z, x)

    @staticmethod
    def from_angle_axis(angle, axis):
        ha = angle * 0.5
        s = math.sin(ha)
        c = math.cos(ha)
        return Quaternion(c, axis.x * s, axis.y * s, axis.z * s)

    @staticmethod
    def from_axes(axis_x, axis_y, axis_z):
        m00 = axis_x.x
        m01 = axis_x.y
        m02 = axis_x.z
        m10 = axis_y.x
        m11 = axis_y.y
        m12 = axis_y.z
        m20 = axis_z.x
        m21 = axis_z.y
        m22 = axis_z.z

        fx = m00 - m11 - m22
        fy = m11 - m00 - m22
        fz = m22 - m00 - m11
        fw = m00 + m11 + m22

        bigi = 0
        bigf = fw
        if fx > bigf:
            bigf = fx
            bigi = 1
        if fy > bigf:
            bigf = fy
            bigi = 2
        if fz > bigf:
            bigf = fz
            bigi = 3

        bigv = math.sqrt(bigf + 1.0) * 0.5
        mult = 0.25 / bigv

        if bigi == 0:
            return Quaternion(bigv, (m12 - m21) * mult, (m20 - m02) * mult, (m01 - m10) * mult)
        if bigi == 1:
            return Quaternion((m12 - m21) * mult, bigv, (m01 + m10) * mult, (m20 + m02) * mult)
        if bigi == 2:
            return Quaternion((m20 - m02) * mult, (m01 + m10) * mult, bigv, (m12 + m21) * mult)
        if bigi == 3:
            return Quaternion((m01 - m10) * mult, (m20 + m02) * mult, (m12 + m21) * mult, bigv)
        return Quaternion()

    @staticmethod
    def from_from_to_rotation(va, vb):
        axis = va.cross(vb).normalized()
        angle = math.acos(va.dot(vb))
        return Quaternion.from_angle_axis(angle, axis)

    @staticmethod
    def from_look_rotation(forward, up):
        # forward becomes negative z
        axis_z = -forward
        axis_x = up.cross(axis_z).normalized()
        axis_y = axis_z.cross(axis_x)
        return Quaternion.from_axes(axis_x, axis_y, axis_z)


class Transform(object):
    def __init__(self, translation=Vector(0.0, 0.0, 0.0), rotation=Quaternion(), scale=Vector(1.0, 1.0, 1.0)):
        self.translation = translation.copy()
        self.rotation = rotation.copy()
        self.scale = scale.copy()

    def to_matrix(self):
        # T * R * S
        axis_x, axis_y, axis_z = self.rotation.to_axes()
        axis_x *= self.scale.x
        axis_y *= self.scale.y
        axis_z *= self.scale.z
        translation = self.translation
        return Matrix(axis_x.x, axis_x.y, axis_x.z, 0.0, axis_y.x, axis_y.y, axis_y.z, 0.0,
            axis_z.x, axis_z.y, axis_z.z, 0.0, translation.x, translation.y, translation.z, 1.0)

    @staticmethod
    def from_matrix(m):
        return m.decompose()

    def transform_point(self, p):
        return self.to_matrix().transform_point(p)

    def transform_vector(self, v):
        return self.to_matrix().transform_vector(v)

    def inversed(self):
        inv_translation = -self.translation
        inv_rotation = self.rotation.inversed()
        inv_scale = Vector(1.0 / self.scale.x, 1.0 / self.scale.y, 1.0 / self.scale.z)
        inv_mT = Matrix.from_translation(inv_translation)
        inv_mR = Matrix.from_rotation(inv_rotation)
        inv_mS = Matrix.from_scale(inv_scale)
        inv_m = inv_mS * inv_mR * inv_mT
        return inv_m.decompose()

    def __mul__(self, other):
        t1 = self.translation
        r1 = self.rotation
        s1 = self.scale
        t2 = other.translation
        r2 = other.rotation
        s2 = other.scale
        t3 = r1.transform_vector(Vector(s1.x * t2.x, s1.y * t2.y, s1.z * t2.z)) + t1
        r3 = r1 * r2
        s3 = Vector(s1.x * s2.x, s1.y * s2.y, s1.z * s2.z)
        return Transform(t3, r3, s3)

    def __repr__(self):
        return 'Transform({}, {}, {})'.format(self.translation, self.rotation, self.scale)


def _test_euler(euler):
    q = Quaternion.from_euler_angles(euler)
    print('euler', euler, 'q', q)
    print('out', q.euler_angles())


def _test():
    v1 = Vector(1.0, 1.0, 1.0)
    v2 = Vector(1.0, 2.0, 3.0)
    print(v1, v2)
    print(v1 * 10)
    print(10 * v1)
    print(-v1 + v2)
    m = Matrix()
    print(m)

    print(Matrix.from_ortho(0, 800, 0, 600, -1.0, 1.0))
    print(Matrix.from_perspective(1.0, 1.6, 0.1, 1000))

    _test_euler(Vector(0.1, 0.2, 0.3))
    _test_euler(Vector(1.1, 6.0, 2.0))

    q = Quaternion.from_euler_angles(Vector(0.2, 4.0, 3.0))
    q = Quaternion.from_angle_axis(0.235, Vector(0.0, 1.0, 0.0))
    print(q.euler_angles())
    m = q.to_matrix()
    print(m)
    q2 = m.decompose().rotation
    print(q, q.euler_angles())
    print(q2, q2.euler_angles())

    print(q * q.inversed())
    print(q2 * q2.conjugated())

    t = Transform(Vector(1.0, 2.0, 3.0), Quaternion.from_euler_angles(Vector(0.3, 0.5, 0.9)), Vector(2.0, 2.0, 2.0))
    print(t)
    print(t.inversed())
    print(t * t.inversed())

    eye = Vector(0.0, 0.0, -10.0)
    at = Vector(1.0, 2.0, 3.0)
    up = Vector(0.0, 1.0, 0.0)
    m = Matrix()
    m.set_translation(eye)
    m.set_look_rotation((at - eye).normalized(), up)
    print(m)
    print(Transform(eye, Quaternion.from_look_rotation((at - eye).normalized(), up)).to_matrix())
    print('---')
    print(m.inversed())
    print(Matrix.from_look_at(eye, at, up))

if __name__ == '__main__':
    _test()
