import math

import numpy as np

Matrix = np.ndarray
Point = tuple[int, int]


def apply_to_point(a: Matrix, b: Point) -> Point:
    vector = np.array([b[0], b[1], 1])
    point = a @ vector
    return (round(point[0]), round(point[1]))


# Basic transformations

def translation(tx: float, ty: float) -> Matrix:
    matrix = np.eye(3)
    matrix[0,2], matrix[1,2] = tx, ty
    return matrix


def scaling(sx: float, sy: float) -> Matrix:
    matrix = np.eye(3)
    matrix[0,0], matrix[1,1] = sx, sy
    return matrix


def rotation(angle: float, clockwise: bool) -> Matrix:
    a = math.radians(-angle if clockwise else angle)
    matrix = np.eye(3)
    matrix[0,0], matrix[0,1] = math.cos(a), -math.sin(a)
    matrix[1,0], matrix[1,1] = math.sin(a), math.cos(a)
    return matrix


def shearing(shx: float, shy: float) -> Matrix:
    matrix = np.eye(3)
    matrix[0,1], matrix[1,0] = shx, shy
    return matrix


def reflection(kind: int, m: float, b: float) -> Matrix:
    matrix = np.eye(3)
    if kind == 1:
        matrix[1,1] = -1
    elif kind == 2:
        matrix[0,0] = -1
    elif kind == 3:
        matrix[0,0], matrix[1,1] = -1, -1
    elif kind == 4:
        a = math.degrees(math.atan(m))
        ref_x = reflection(1, 0, 0)
        matrix = (translation(0, b) @ rotation(a, False) @ ref_x
                  @ rotation(-a, False) @ translation(0, -b))
    return matrix


def transform_line(m: Matrix, start: Point, end: Point) -> tuple[Point, Point]:
    return apply_to_point(m, start), apply_to_point(m, end)
