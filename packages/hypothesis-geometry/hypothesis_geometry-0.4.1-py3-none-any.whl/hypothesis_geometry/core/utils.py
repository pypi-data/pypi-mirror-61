from enum import (IntEnum,
                  unique)
from itertools import chain
from numbers import Real
from typing import (Iterator,
                    List,
                    Sequence,
                    TypeVar)

from robust import parallelogram
from robust.hints import Point as RealPoint

from hypothesis_geometry.hints import (Contour,
                                       Point)

Domain = TypeVar('Domain')


def to_sign(value: Real) -> int:
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


flatten = chain.from_iterable


def split(sequence: Sequence[Domain],
          *,
          size: int = 2) -> List[Sequence[Domain]]:
    step, offset = divmod(len(sequence), size)
    return [sequence[number * step + min(number, offset):
                     (number + 1) * step + min(number + 1, offset)]
            for number in range(size)]


@unique
class Orientation(IntEnum):
    CLOCKWISE = -1
    COLLINEAR = 0
    COUNTERCLOCKWISE = 1


def to_orientation(first_ray_point: Point,
                   vertex: Point,
                   second_ray_point: Point) -> Orientation:
    if not _is_real_point(vertex):
        first_ray_point, vertex, second_ray_point = (
            _to_real_point(first_ray_point), _to_real_point(vertex),
            _to_real_point(second_ray_point))
    return Orientation(to_sign(parallelogram.signed_area(
            vertex, first_ray_point, vertex, second_ray_point)))


def to_orientations(contour: Contour) -> Iterator[Orientation]:
    return (to_orientation(contour[index - 1], contour[index],
                           contour[(index + 1) % len(contour)])
            for index in range(len(contour)))


def _is_real_point(point: Point) -> bool:
    x, y = point
    return isinstance(x, Real) and isinstance(y, Real)


def _to_real_point(point: Point) -> RealPoint:
    x, y = point
    return float(x), float(y)
