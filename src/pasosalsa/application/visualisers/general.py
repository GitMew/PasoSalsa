from typing import Iterable, List, Tuple, Union
from copy import deepcopy
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from ...domain.abstracts.figuras import Figura
from ...domain.abstracts.simulation import Pattern, Leader, Follower, Couple, Agent, NamedFeetStates, \
    TwoUnnamedFeetStates, NamedCountResult, Person, AbsoluteFootState


class WhichPerson(Enum):
    LEADER   = 1
    FOLLOWER = 2
    BOTH     = 3


@dataclass
class GridSpec:
    width: int
    height: int


@dataclass
class Panel:
    rendered: str
    count: int


Visualisable = Union[Pattern,Figura]


class Visualiser(ABC):

    # TODO: Implement these options.
    def __init__(self, panels_per_row: int=3, show_count_0: bool=False, loop_count_after_8: bool=False, which: WhichPerson=WhichPerson.LEADER):
        self._panels_per_row = panels_per_row
        self._mode = which

    @abstractmethod
    def _render(self, pattern_or_figura: Visualisable) -> List[Panel]:
        pass

    @abstractmethod
    def _concatenate(self, panels: List[Panel]) -> str:
        pass

    def visualise(self, pattern_or_figura: Visualisable):
        return self._concatenate(self._render(pattern_or_figura))

    def _getRenderDetails(self, pattern_or_figura: Visualisable) -> Tuple[GridSpec, NamedFeetStates, Iterable[NamedCountResult]]:
        """
        Boilerplate that any visualiser probably will want to use to iterate over the counts of a figure.
        """
        gridspec, baseline = self._normaliseGrid(pattern_or_figura)
        initial_feet = self._getInitialPosition(self._getAgent(baseline), pattern_or_figura)
        feet_and_step_iterable = self._simulate(self._getAgent(baseline), pattern_or_figura)
        return gridspec, initial_feet, feet_and_step_iterable

    def _getAgent(self, baseline: TwoUnnamedFeetStates=None) -> Agent:
        """
        Get an agent locted at the given baseline, ready to simulate patterns/figures.
        """
        if self._mode == WhichPerson.LEADER:
            return Leader(baseline)
        elif self._mode == WhichPerson.FOLLOWER:
            return Follower(baseline)
        elif self._mode == WhichPerson.BOTH:
            return Couple(baseline)
        else:
            raise ValueError(f"Impossible enum value: {self._mode}")

    def _simulate(self, simulator: Agent, pattern_or_figura: Visualisable) -> Iterable[NamedCountResult]:
        if isinstance(pattern_or_figura, Pattern):
            assert isinstance(simulator, Person)
            yield from simulator.executePattern(pattern_or_figura)
        elif isinstance(pattern_or_figura, Figura):
            yield from simulator.executeFigura(pattern_or_figura)
        else:
            raise TypeError(f"Unknown type to visualise: {type(pattern_or_figura)}")

    def _getInitialPosition(self, simulator: Agent, pattern_or_figura: Visualisable) -> NamedFeetStates:
        if isinstance(pattern_or_figura, Pattern):
            assert isinstance(simulator, Person)
            return simulator.executePatternStartingPose(pattern_or_figura)
        elif isinstance(pattern_or_figura, Figura):
            return simulator.executeFiguraStartingPose(pattern_or_figura)
        else:
            raise TypeError(f"Unknown type to visualise: {type(pattern_or_figura)}")

    def _normaliseGrid(self, pattern_or_figura: Visualisable, baseline: TwoUnnamedFeetStates=None) -> Tuple[GridSpec,TwoUnnamedFeetStates]:
        """
        Finds the smallest grid dimensions possible covered by the given figure/pattern,
        as well as how much the baseline must shift in that (0-based, right-handed) grid for the leftmost, downmost
        coordinates to be exactly 0.
        """
        xs = []
        ys = []
        for feet,_ in self._simulate(self._getAgent(baseline=baseline), pattern_or_figura):
            for position in feet.values():
                xs.append(position.x)
                ys.append(position.y)

        x_shift = min(xs)  # The minimal x should be 0, so we have to shift by -x_shift to ensure this.
        y_shift = min(ys)  # Idem for y.

        width  = max(xs) - x_shift + 1  # E.g.: if the min, max is -4, 1, then you have a 6-wide grid.
        height = max(ys) - y_shift + 1

        original_left_foot_baseline  = baseline[0] if baseline else AbsoluteFootState(0,0,90)
        original_right_foot_baseline = baseline[1] if baseline else AbsoluteFootState(1,0,90)

        return GridSpec(width,height), (
            AbsoluteFootState(original_left_foot_baseline.x - x_shift, original_left_foot_baseline.y - y_shift, original_left_foot_baseline.rotation),
            AbsoluteFootState(original_right_foot_baseline.x - x_shift, original_right_foot_baseline.y - y_shift, original_right_foot_baseline.rotation)
        )
