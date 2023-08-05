# linalg_simple

_A simple linear algebra package written in Python 3_

This is a more or less direct implementation of the **Udacity** [Linear Algebra Refresher Course](https://www.udacity.com/course/linear-algebra-refresher-course--ud953).

## Installation

**linalg_simple** is available from the Python Package Index [PyPi](https://pypi.org).
If you have Python 3 installed on your system you can use the `pip install` command:

```
pip install linalg_simple
```

## Classes

The linalg_simple package currently offers the `Vector()` class, which can directly be imported into your project with:

```python
from linalg import Vector
```

## Vector Methods

The following methods are available:

### Constructor

Arguments: int, float

```
v1 = Vector([1.5, -4.8, 3])
```

### + Method

```
v3 = v1 + v2
```

### - Method

```
v3 = v1 - v2
```

### Scalar Mutliplication

Arguments: int, float

```
v1.times_scalar(42)
```

### Magnitude

```
vector_length = v1.magnitude()
```

### Vector Normalization

```
unit_vector = v1.normalized()
```

### Dot Product

Arguments: vector object

```
dot_product = v1.dot(v2)
```

### Angle between two vectors

Arguments: vector object

```
angle = v1.angle_with(v2)
```

### Check if vector's length is zero

To avoid precision errors, you can indicate a tolerance (default: 1e-10).

```
v1.is_zero()
```

### Check if two vectors are orthogonal to each other

To avoid precision errors, you can indicate a tolerance (default: 1e-10).

Arguments: vector object, tolerance

```
v1.is_orthogonal_to(v2)
```

### Check if two vectors are parallel to each other

Arguments: vector object

```
v1.is_parallel_to(v2)
```

### Calculate projection of a vector onto a basis vector

Arguments: vector object (basis vector)

```
projection_vector = v1.component_parallel_to(v2)
```

### Calculate orthogonal component of vector

Arguments: vector object (basis vector)

```
projection_vector = v1.component_orthogonal_to(v2)
```

### Calculate Cross Product of two vectors

The vectors should be 3D (2D vectors will be augmented to 3D).

Arguments: vector object

```
crossproduct_vector = v1.cross(v2)
```

### Calculate the parallelogram spanned by two vectors

Arguments: vector object

```
area = v1.area_of_parallelogram_with(v2)
```

### Calculate area of a parallelogram spanned by two vectors

Arguments: vector object

```
area = v1.area_of_parallelogram_with(v2)
```

### Calculate area of a trinagle spanned by two vectors

Arguments: vector object

```
area = v1.area_of_triangle_with(v2)
```
