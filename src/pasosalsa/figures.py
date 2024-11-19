from typing import Dict, List
from typing_extensions import Self
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy


class Foot(Enum):
    LeaderLeft    = 1
    LeaderRight   = 2
    FollowerLeft  = 3
    FollowerRight = 4


class Step:
    def __init__(self, move_north: int, move_east: int, turn_degrees: int):
        self.north   = move_north
        self.east    = move_east
        self.degrees = turn_degrees

    def __add__(self, other: "Step") -> "Step":
        return Step(self.north + other.north, self.east + other.east, self.degrees + other.degrees)


class Move(Step):
    def __init__(self, north: int, east: int):
        super().__init__(north, east, 0)


class Turn(Step):
    def __init__(self, degrees: int):
        super().__init__(0, 0, degrees)


class StartingPosition(Step):
    def __init__(self, x: int, y: int, rotation: int):
        super().__init__(x, y, rotation)


InPlace  = Move(0,0)
Forward  = Move(+1,0)
Backward = Move(-1,0)
Left     = Move(0,-1)
Right    = Move(0,+1)


FeetState = Dict[Foot, StartingPosition]

@dataclass
class Checkpoint:
    steps_since_previous: List[Step]
    feet_final_position: FeetState
    hidden: bool

    def copyState(self, hidden: bool=False) -> "Checkpoint":
        return Checkpoint([], deepcopy(self.feet_final_position), hidden)


class Figura:

    def __init__(self, name: str, base: FeetState):
        self._name = name
        self._checkpoints = [Checkpoint([], base, hidden=True)]
        self.count()

    def move(self, foot: Foot, movement: Step) -> Self:
        self._lastCheckpoint().steps_since_previous.append(movement)
        self._lastCheckpoint().feet_final_position[foot] += movement

    def count(self) -> Self:
        self._addCheckpoint(self._lastCheckpoint().copyState())
        return self

    def pause(self) -> Self:
        self._addCheckpoint(self._lastCheckpoint().copyState(hidden=True))
        return self

    def _addCheckpoint(self, checkpoint: Checkpoint):
        return self._checkpoints.append(checkpoint)

    def _lastCheckpoint(self) -> Checkpoint:
        return self._checkpoints[-1]
