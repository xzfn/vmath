
from vmath import Vector, Matrix, Quaternion, Transform


if __name__ == '__main__':
    pitch = 0.5
    yaw = 1.9
    roll = 0.2
    x = Vector(1.0, 0.0, 0.0)
    y = Vector(0.0, 1.0, 0.0)
    z = Vector(0.0, 0.0, 1.0)
    m_pitch_x = Matrix.from_angle_axis(pitch, x)
    m_yaw_y = Matrix.from_angle_axis(yaw, y)
    m_roll_z = Matrix.from_angle_axis(roll, z)

    # matrix multiplication order should be reversed from the euler order
    # so when euler order is yaw-pitch-roll, matrix apply order is z-x-y
    m = m_yaw_y * m_pitch_x * m_roll_z
    print(m)

    # should be the same when use Quaternion directly
    q = Quaternion.from_euler_angles(Vector(pitch, yaw, roll))
    print(q.to_matrix())
