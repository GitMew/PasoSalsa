from typing import Iterable, List, Tuple
from copy import deepcopy
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ...domain.abstracts.figuras import Figura, FeetState


@dataclass
class GridSpec:
    width: int
    height: int


@dataclass
class Panel:
    rendered: str
    count: int


class Visualiser(ABC):

    def __init__(self, panels_per_row: int=3, with_base: bool=False):  # TODO: Implement this option visualising "count 0".
        self._panels_per_row = panels_per_row

    @abstractmethod
    def _render(self, figure: Figura) -> List[Panel]:
        pass

    @abstractmethod
    def _concatenate(self, panels: List[Panel]) -> str:
        pass

    def visualise(self, figure: Figura):
        return self._concatenate(self._render(figure))

    def _simulate(self, figure: Figura, base: FeetState=None) -> Iterable[FeetState]:
        positions = deepcopy(base or figure.base)
        for checkpoint in figure.checkpoints:
            for foot, step in checkpoint.steps_since_previous:
                positions[foot] = step.updatePosition(positions[foot])
            yield deepcopy(positions)

    def _normaliseGrid(self, figure: Figura) -> Tuple[GridSpec, FeetState]:
        """
        Finds the smallest grid dimensions possible covered by the given figure,
        as well as where in that (0-based, right-handed) grid every foot must start.
        """
        xs = []
        ys = []
        for feet in self._simulate(figure, base=None):
            for position in feet.values():
                xs.append(position.x)
                ys.append(position.y)

        x_shift = min(xs)  # The minimal x should be 0, so we have to shift by -x_shift to ensure this.
        y_shift = min(ys)  # Idem for y.

        width  = max(xs) - x_shift + 1  # E.g.: if the min, max is -4, 1, then you have a 6-wide grid.
        height = max(ys) - y_shift + 1

        starting_positions = deepcopy(figure.base)
        for foot in starting_positions:
            starting_positions[foot].x -= x_shift
            starting_positions[foot].y -= y_shift

        return GridSpec(width,height), starting_positions
