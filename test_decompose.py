from vmath import Vector, Matrix, Quaternion, Transform

if __name__ == '__main__':
    xf1 = Transform(Vector(1.0, 2.0, 3.0),
                    Quaternion.from_euler_angles(Vector(1.0, 1.1, 1.2)),
                    Vector(2.0, 2.0, 2.0))

    xf2 = Transform(Vector(5.0, 2.0, -8.0),
                    Quaternion.from_euler_angles(Vector(-1.0, -2.0, 1.6)),
                    Vector(3.0, 3.0, 3.0))

    xf3 = xf1 * xf2
    print(xf1)
    print(xf2)
    print(xf3)
    xf4 = (xf1.to_matrix() * xf2.to_matrix()).decompose()
    print(xf4)
