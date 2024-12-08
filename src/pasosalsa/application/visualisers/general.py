from typing import Iterable, List, Tuple, Union, Optional
from copy import deepcopy
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from ...domain.instances.movement import Backward, Leftward, Clockwise90, MoveThenTurn
from ...domain.abstracts.figuras import Figura
from ...domain.abstracts.simulation import Pattern, Leader, Follower, Couple, Agent, NamedFeetStates, \
    TwoUnnamedFeetStates, NamedCountResult, Person, AbsoluteFootState, Count, NamedFoot


class WhichPerson(Enum):
    LEADER   = 1
    FOLLOWER = 2
    BOTH_FROM_LEADER   = 3
    BOTH_FROM_FOLLOWER = 4


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

    # TODO: Implement showing baselines.
    def __init__(self, which: WhichPerson, panels_per_row: int=3, loop_count_after: Optional[int]=None, show_count_0: bool=False, rotate_everything_by: int=0):
        self._mode = which
        self._rotate = rotate_everything_by
        self._panels_per_row = panels_per_row
        self._modulo_counts = loop_count_after

    @abstractmethod
    def _render(self, pattern_or_figura: Visualisable) -> List[Panel]:
        pass

    @abstractmethod
    def _concatenate(self, panels: List[Panel]) -> str:
        pass

    def visualise(self, pattern_or_figura: Visualisable):
        panels = self._render(pattern_or_figura)
        if self._modulo_counts is not None:
            for panel in panels:
                panel.count %= self._modulo_counts
        return self._concatenate(panels)

    def _getLeaderBaseline(self, pattern_or_figura: Visualisable) -> Tuple[AbsoluteFootState,AbsoluteFootState]:
        # Step 1: Get the baseline according to the visualiser mode.
        leader = Leader()
        if self._mode in {WhichPerson.LEADER, WhichPerson.FOLLOWER, WhichPerson.BOTH_FROM_LEADER}:
            first_baseline_transform = Count(left=None,right=None)
        elif self._mode == WhichPerson.BOTH_FROM_FOLLOWER:
            assert isinstance(pattern_or_figura, Figura)
            first_baseline_transform = Count(
                left=pattern_or_figura.starting_posicion.left.reversed(),
                right=pattern_or_figura.starting_posicion.right.reversed()
            )
        else:
            raise NotImplementedError

        positions, _ = leader.executeCount(first_baseline_transform)

        # Step 2: Rotate an extra amount.
        rotate_90 = Count(
            left=Clockwise90,
            right=MoveThenTurn(Backward + Leftward, Clockwise90)
        )
        for _ in range(self._rotate // 90):
            positions, _ = leader.executeCount(rotate_90)

        # Get leader feet as baseline
        return positions[NamedFoot.LeaderLeft], positions[NamedFoot.LeaderRight]

    def _getRenderDetails(self, pattern_or_figura: Visualisable) -> Tuple[GridSpec, NamedFeetStates, Iterable[NamedCountResult]]:
        """
        Boilerplate that any visualiser probably will want to use to iterate over the counts of a figure.
        """
        baseline = self._getLeaderBaseline(pattern_or_figura)
        gridspec, baseline = self._normaliseGrid(pattern_or_figura, baseline)
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
        elif self._mode == WhichPerson.BOTH_FROM_LEADER or self._mode == WhichPerson.BOTH_FROM_FOLLOWER:
            return Couple(baseline)
        else:
            raise ValueError(f"Impossible enum value: {self._mode}")

    def _simulate(self, simulator: Agent, pattern_or_figura: Visualisable) -> Iterable[NamedCountResult]:
        if isinstance(pattern_or_figura, Pattern):
            assert isinstance(simulator, Person), "You asked to visualise a single-person pattern while in two-person mode!"
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

        TODO: Since simulation doesn't output the 0th count (at least not currently), it is possible that if a grid row/column
              is only ever visited in the 0th count, the grid will be too small to show this.
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
