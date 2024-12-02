from dataclasses import dataclass
from abc import abstractmethod, ABC
from typing_extensions import Self


class _Step(ABC):
    """A step is one movement of a foot relative to its current position."""
    @abstractmethod
    def reversed(self) -> "_Step":
        pass

    @abstractmethod
    def mirrored(self) -> Self:
        pass

    @abstractmethod
    def accept(self, visitor: "_StepVisitor"):
        """Visitor pattern for step objects."""
        pass

    def __neg__(self) -> Self:
        return self.reversed()


@dataclass
class Move(_Step):
    forward: int
    rightward: int

    def __add__(self, other: "Move") -> "Move":
        return Move(forward=self.forward + other.forward,
                    rightward=self.rightward + other.rightward)

    def reversed(self) -> "Move":
        return Move(forward=-self.forward, rightward=-self.rightward)

    def mirrored(self) -> Self:
        return Move(forward=self.forward, rightward=-self.rightward)

    def accept(self, visitor: "_StepVisitor"):
        return visitor.visit_Move(self)


@dataclass
class Turn(_Step):
    degrees: int

    def __add__(self, other: "Turn") -> "Turn":
        return Turn(degrees=self.degrees + other.degrees)  # Not modulo'd because turning 360° != turning 0°.

    def reversed(self) -> "Turn":
        return Turn(degrees=-self.degrees)

    def mirrored(self) -> Self:
        return Turn(degrees=-self.degrees)

    def accept(self, visitor: "_StepVisitor"):
        return visitor.visit_Turn(self)


@dataclass
class MoveThenTurn(_Step):
    move: Move
    turn: Turn

    def reversed(self) -> "TurnThenMove":
        return TurnThenMove(self.turn.reversed(), self.move.reversed())

    def mirrored(self) -> Self:
        return MoveThenTurn(self.move.mirrored(), self.turn.mirrored())

    def accept(self, visitor: "_StepVisitor"):
        return visitor.visit_MoveThenTurn(self)


@dataclass
class TurnThenMove(_Step):
    turn: Turn
    move: Move

    def reversed(self) -> "MoveThenTurn":
        return MoveThenTurn(self.move.reversed(), self.turn.reversed())

    def mirrored(self) -> Self:
        return TurnThenMove(self.turn.mirrored(), self.move.mirrored())

    def accept(self, visitor: "_StepVisitor"):
        return visitor.visit_TurnThenMove(self)


class _StepVisitor(ABC):
    """
    Interface for visitors of _Step objects. Helps to keep more advanced implementations (e.g. coordinate transforms)
    out of the _Step classes, which are only meant for declaration of relative movements.
    """
    def visit(self, step: _Step):
        return step.accept(self)

    @abstractmethod
    def visit_Move(self, step: Move):
        pass

    @abstractmethod
    def visit_Turn(self, step: Turn):
        pass

    @abstractmethod
    def visit_MoveThenTurn(self, step: MoveThenTurn):
        pass

    @abstractmethod
    def visit_TurnThenMove(self, step: TurnThenMove):
        pass
