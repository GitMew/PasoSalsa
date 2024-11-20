from dataclasses import dataclass
from abc import abstractmethod
from enum import Enum

from math import cos, sin, radians


class Foot(Enum):
    LeaderLeft    = 1
    LeaderRight   = 2
    FollowerLeft  = 3
    FollowerRight = 4

    def __repr__(self) -> str:
        if self == Foot.LeaderLeft:
            return "LL"
        elif self == Foot.LeaderRight:
            return "LR"
        elif self == Foot.FollowerLeft:
            return "FL"
        elif self == Foot.FollowerRight:
            return "FR"


@dataclass
class FootPosition:
    x: int
    y: int
    rotation: int


class _Step:
    @abstractmethod
    def updatePosition(self, position: FootPosition) -> FootPosition:
        pass


@dataclass
class Move(_Step):
    forward: int
    rightward: int

    def __add__(self, other: "Move") -> "Move":
        return Move(forward=self.forward + other.forward,
                    rightward=self.rightward + other.rightward)

    def updatePosition(self, position: FootPosition) -> FootPosition:
        # The foot is at an angle, and the move describes a move partially along the vector subtending this angle and
        # partially along the vector orthogonal to it on the right.
        # So really, what we have is a weighted sum (weight carried by this object) of two unit vectors (deduced from the given position).
        theta = radians(position.rotation)
        unit_forward_x = cos(theta)
        unit_forward_y = sin(theta)
        unit_rightward_x = sin(theta)
        unit_rightward_y = -cos(theta)

        delta_x = unit_forward_x*self.forward + unit_rightward_x*self.rightward
        delta_y = unit_forward_y*self.forward + unit_rightward_y*self.rightward

        # FIXME: This discretisation doesn't really work for non-right-angle movements. If you step forward 1 at a 45°
        #        angle, you should land ~1.414 away in the centre of the tile diagonal to your position. Right now, you
        #        land 1 away on the diagonal, which is only 1/sqrt(2) == 0.707 in each direction, which int()s to 0 again.
        #        Of course, this is only defined for a handful of angles depending on the step size. Could allow the user
        #        to not "snap to grid" although it will be a pain to visualise. (Also, ASCII can't visualise rotations.)
        return FootPosition(x=round(position.x + delta_x), y=round(position.y + delta_y), rotation=position.rotation)


class Turn(_Step):
    def __init__(self, degrees: int):
        self.degrees = degrees

    def __add__(self, other: "Turn") -> "Turn":
        return Turn(degrees=self.degrees + other.degrees)  # Not modulo'd because turning 360° != turning 0°.

    def updatePosition(self, position: FootPosition) -> FootPosition:
        return FootPosition(position.x, position.y, (position.rotation + self.degrees) % 360)


class MoveThenTurn(_Step):
    def __init__(self, move: Move, turn: Turn):
        self.move = move
        self.turn = turn

    def updatePosition(self, position: FootPosition) -> FootPosition:
        return self.turn.updatePosition(self.move.updatePosition(position))


class TurnThenMove(_Step):
    def __init__(self, turn: Turn, move: Move):
        self.turn = turn
        self.move = move

    def updatePosition(self, position: FootPosition) -> FootPosition:
        return self.move.updatePosition(self.turn.updatePosition(position))
