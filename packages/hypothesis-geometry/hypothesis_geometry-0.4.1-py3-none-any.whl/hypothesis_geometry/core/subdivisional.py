from typing import (Iterable,
                    Optional,
                    Sequence)

from reprit.base import generate_repr

from hypothesis_geometry.hints import Point
from .utils import (Orientation,
                    to_orientation)


class QuadEdge:
    """
    Based on:
        quad-edge data structure.

    Reference:
        https://en.wikipedia.org/wiki/Quad-edge
        http://www.sccg.sk/~samuelcik/dgs/quad_edge.pdf
    """
    __slots__ = ('_start', '_left_from_start', '_rotated')

    def __init__(self,
                 start: Optional[Point] = None,
                 left_from_start: Optional['QuadEdge'] = None,
                 rotated: Optional['QuadEdge'] = None) -> None:
        self._start = start
        self._left_from_start = left_from_start
        self._rotated = rotated

    @property
    def start(self) -> Point:
        """
        aka "Org" in L. Guibas and J. Stolfi notation.
        """
        return self._start

    @property
    def end(self) -> Point:
        """
        aka "Dest" in L. Guibas and J. Stolfi notation.
        """
        return self.opposite.start

    @property
    def rotated(self) -> 'QuadEdge':
        """
        aka "Rot" in L. Guibas and J. Stolfi notation.
        """
        return self._rotated

    @property
    def opposite(self) -> 'QuadEdge':
        """
        aka "Sym" in L. Guibas and J. Stolfi notation.
        """
        return self._rotated._rotated

    @property
    def left_from_start(self) -> 'QuadEdge':
        """
        aka "Onext" in L. Guibas and J. Stolfi notation.
        """
        return self._left_from_start

    @property
    def right_from_start(self) -> 'QuadEdge':
        """
        aka "Oprev" in L. Guibas and J. Stolfi notation.
        """
        return self.rotated.left_from_start.rotated

    @property
    def right_from_end(self) -> 'QuadEdge':
        """
        aka "Rprev" in L. Guibas and J. Stolfi notation.
        """
        return self.opposite.left_from_start

    @property
    def left_from_end(self) -> 'QuadEdge':
        """
        aka "Lnext" in L. Guibas and J. Stolfi notation.
        """
        return self.rotated.opposite.left_from_start.rotated

    @classmethod
    def factory(cls, start: Point, end: Point) -> 'QuadEdge':
        result, opposite = cls(start), cls(end)
        rotated, triple_rotated = cls(), cls()
        result._left_from_start = result
        opposite._left_from_start = opposite
        rotated._left_from_start = triple_rotated
        triple_rotated._left_from_start = rotated
        result._rotated = rotated
        rotated._rotated = opposite
        opposite._rotated = triple_rotated
        triple_rotated._rotated = result
        return result

    __repr__ = generate_repr(factory)

    def splice(self, other: 'QuadEdge') -> None:
        alpha = self.left_from_start.rotated
        beta = other.left_from_start.rotated
        self._left_from_start, other._left_from_start = (other.left_from_start,
                                                         self.left_from_start)
        alpha._left_from_start, beta._left_from_start = (beta.left_from_start,
                                                         alpha.left_from_start)

    def connect(self, other: 'QuadEdge') -> 'QuadEdge':
        result = QuadEdge.factory(self.end, other.start)
        result.splice(self.left_from_end)
        result.opposite.splice(other)
        return result

    def delete(self) -> None:
        self.splice(self.right_from_start)
        self.opposite.splice(self.opposite.right_from_start)

    def orientation_with(self, point: Point) -> Orientation:
        return to_orientation(self.end, self.start, point)


def to_edge_neighbours(edge: QuadEdge) -> Sequence[QuadEdge]:
    return tuple(_to_edge_neighbours(edge))


def _to_edge_neighbours(edge: QuadEdge) -> Iterable[QuadEdge]:
    candidate = edge.left_from_start
    if (edge.orientation_with(candidate.end)
            is Orientation.COUNTERCLOCKWISE):
        yield candidate
        yield candidate.right_from_end
