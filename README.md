# vmath
Python vector math library for 3D games.

## Usage
Main classes:
* Vector: 3D Vector.
* Matrix: 4x4 column major matrix, M1 * M2 means first apply M2, then apply M1.
* Quaternion: Quaternion for rotation.
* Transform: Transform represented as Translation-Rotation-Scale.

```python
>>> from vmath import Vector, Matrix, Quaternion, Transform
>>> v1 = Vector(1.0, 2.0, 3.0)
>>> v2 = Vector(4.0, 5.0, 6.0)
>>> v1 + v2
Vector(5.0000, 7.0000, 9.0000)

>>> q = Quaternion.from_euler_angles(Vector(0.0, 0.8, 0.0))
>>> q
Quaternion(0.9211, 0.0000, 0.3894, 0.0000)

>>> xf = Transform(v1, q, Vector(1.0, 1.0, 1.0))
>>> m = xf.to_matrix()
>>> print(m)
Matrix<0.6967, 0.0000, 0.7174, 1.0000
       0.0000, 1.0000, 0.0000, 2.0000
       -0.7174, 0.0000, 0.6967, 3.0000
       0.0000, 0.0000, 0.0000, 1.0000>

>>> m.decompose()
Transform(Vector(1.0000, 2.0000, 3.0000), Quaternion(0.9211, 0.0000, 0.3894, 0.0000), Vector(1.0000, 1.0000, 1.0000))

>>> m.transform_vector(v1)
Vector(2.8488, 2.0000, 1.3728)
>>> m.transform_point(v1)
Vector(3.8488, 4.0000, 4.3728)
```

Euler angles should be stored in Vector(pitch, yaw, roll), order yaw-pitch-roll.
Therefore the corresponding rotation matrix is M(yaw) * M(pitch) * M(roll).

## License
MIT License.
