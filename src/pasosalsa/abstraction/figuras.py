from typing import Dict, List, Tuple
from dataclasses import dataclass

from .movement import *
from .movement import _Step

FeetState = Dict[Foot, FootPosition]


@dataclass
class Checkpoint:
    steps_since_previous: List[Tuple[Foot,_Step]]
    hidden: bool

    def copyState(self, hidden: bool=False) -> "Checkpoint":
        return Checkpoint([], hidden)


@dataclass
class Figura:
    name: str
    base: FeetState
    checkpoints: List[Checkpoint]


class BuildFigura:

    def __init__(self, name: str, base: FeetState):
        self._figure = Figura(name=name, base=base, checkpoints=[Checkpoint([], hidden=True)])
        self.count()

    def move(self, foot: Foot, movement: _Step) -> "BuildFigura":
        self._lastCheckpoint().steps_since_previous.append((foot,movement))
        return self

    def count(self) -> "BuildFigura":
        self._addCheckpoint(self._lastCheckpoint().copyState())
        return self

    def pause(self) -> "BuildFigura":
        self._lastCheckpoint().hidden = True
        return self.count()

    def finish(self) -> "Figura":
        self._figure.checkpoints.pop()
        return self._figure

    def _addCheckpoint(self, checkpoint: Checkpoint):
        return self._figure.checkpoints.append(checkpoint)

    def _lastCheckpoint(self) -> Checkpoint:
        return self._figure.checkpoints[-1]
