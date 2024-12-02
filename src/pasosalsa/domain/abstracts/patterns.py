"""
What you need to define figure is 4 things:
    1. Name.
    2. Posicion (i.e. where the woman's feet baseline is relative to the man's).
    3. Starting pose and foot pattern for the man relative to his foot baseline.
    4. Starting pose and foot pattern for the woman relative to her foot baseline.

We define all of these in this file.
"""
from typing import Optional, List
from enum import Enum
from abc import abstractmethod, ABC
from dataclasses import dataclass

from .movement import _Step


@dataclass
class Count:
    """One movement of the left and/or right foot. Represents 1 of the 4 counts in a bar of salsa music."""
    left:  Optional[_Step] = None
    right: Optional[_Step] = None

    def isPause(self) -> bool:
        return self.left is None and self.right is None

    def __neg__(self) -> "Count":
        return Count(
            left=-self.left if self.left else None,
            right=-self.right if self.right else None
        )


class Posicion(ABC):
    """
    Describes where the follower is relative to the leader.

    Posiciones are defined assuming the leader and follower are standing feet together on their baseline. Since starting
    positions are defined starting from that baseline too, the way you get to a follower from the leader is as follows:
        - Start at leader pose.
        - Invert it to get back to the baseline.
        - Add the posicion.
        - Add the follower pose.
    """
    @abstractmethod
    def leaderBaselineToFollowerBaseline(self) -> Count:
        pass


class StartingPose(Count):
    pass


class Pattern:
    """
    A pattern is a sequence of counts describing the steps of one person.
    The counts are assumed to follow on a starting pose, which is described by the movement the person has to make from
    their baseline (feet together, pointing forward) to get there, rather than by the absolute position and orientation of the feet.
    """
    def __init__(self, start: StartingPose, counts: List[Count]):
        self.start = start
        self.counts = counts
        self.name = ""

    def duration(self) -> int:
        return len(self.counts)

    def setName(self, name: str):
        """
        Setting the name of a pattern in its constructor is optional, because usually it can be inferred from where it
        is used. For example, the name of the follower's steps in "vuelta derecha" is just "vuelta derecha (follower)".
        """
        self.name = name

    def __repr__(self):
        return (self.name if self.name else "unnamed pattern") + f" [{self.duration()}]"


class _Foot(Enum):
    LEFT  = 1
    RIGHT = 2


LeftFoot  = _Foot.LEFT
RightFoot = _Foot.RIGHT


class BuildPattern:

    def __init__(self, base: StartingPose):
        self._pattern = Pattern(base, [])
        self.count()

    def move(self, foot: _Foot, step: _Step) -> "BuildPattern":
        """Add a movement that should be done by the time the next count hits."""
        if foot == LeftFoot:
            self._pattern.counts[-1].left = step
        elif foot == RightFoot:
            self._pattern.counts[-1].right = step
        else:
            raise ValueError(f"Unknown foot: {foot}")
        return self

    def count(self) -> "BuildPattern":
        """Hit the next count. Any movements added next are to be completed after this count, not before."""
        self._pattern.counts.append(Count())
        return self

    def pause(self) -> "BuildPattern":
        """Don't register any movement since the last count. Equivalent to calling .count() except any movement done since the
           last .count() will also be deleted, just for good measure."""
        self._pattern.counts[-1] = Count()
        return self.count()

    def finish(self) -> Pattern:
        """Return the resulting pattern."""
        self._pattern.counts.pop()  # The last Count is always a work-in-progress.
        return self._pattern
