"""
Code related to dealing with figuras that have been anchored in space.
By default, the starting position and movement patterns in a figura are always described relative to some previous state.
In this file, we handle coordinate transformations after grounding these relative descriptions.
"""
from typing import Dict, Iterable, Tuple
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

from copy import deepcopy
from math import cos, sin, radians

from .patterns import Count, Pattern
from .movement import _StepVisitor, Move, Turn, MoveThenTurn, TurnThenMove, _RelativeStep
from .figuras import Figura
from ...util.iterables import peek, last


@dataclass
class AbsoluteFootState:
    """Absolute location (on Cartesian axes) and rotation (in degrees on the unit circle) of a foot in 2D."""
    x: int
    y: int
    rotation: int

    def isSamePlace(self, other: "AbsoluteFootState") -> bool:
        return self.x == other.x and self.y == other.y

    def getForwardUnitVector(self) -> Tuple[float,float]:
        return cos(radians(self.rotation)), sin(radians(self.rotation))

    def getRightwardUnitVector(self) -> Tuple[float,float]:
        return cos(radians(self.rotation-90)), sin(radians(self.rotation-90))

    def __sub__(self, other: "AbsoluteFootState") -> MoveThenTurn:
        # Get movement vector
        delta_x = self.x - other.x
        delta_y = self.y - other.y

        # Project it onto the relative axes
        forward_x, forward_y = self.getForwardUnitVector()
        right_x, right_y     = self.getRightwardUnitVector()

        forward_delta = delta_x*forward_x + delta_y*forward_y
        right_delta   = delta_x*right_x   + delta_y*right_y

        return MoveThenTurn(
            Move(forward=round(forward_delta), rightward=round(right_delta)),
            Turn(degrees=self.rotation - other.rotation)
        )


class NamedFoot(Enum):
    """
    Feet that distinguish between leader and follower, so that feet states can be communicated in one dictionary
    rather than two.
    """
    LeaderLeft    = 1
    LeaderRight   = 2
    FollowerLeft  = 3
    FollowerRight = 4

    def __repr__(self) -> str:
        if   self == NamedFoot.LeaderLeft:
            return "LL"
        elif self == NamedFoot.LeaderRight:
            return "LR"
        elif self == NamedFoot.FollowerLeft:
            return "FL"
        elif self == NamedFoot.FollowerRight:
            return "FR"


class SimulatedPosition(_StepVisitor):
    """
    Tracks an absolute position as it is simulated by visiting various movements.
    Since indeed every foot has its own movement, you need 4 of these simulators to simulate a figure.
    """

    def __init__(self, starting_position: AbsoluteFootState):
        self.position = starting_position

    def update(self, step: _RelativeStep):
        return self.visit(step)

    def visit_Move(self, step: Move):
        # The foot is at an angle, and the move describes a move partially along the vector subtending this angle and
        # partially along the vector orthogonal to it on the right.
        # So really, what we have is a weighted sum (weight carried by this object) of two unit vectors (deduced from the given position).
        theta = radians(self.position.rotation)
        unit_forward_x = cos(theta)
        unit_forward_y = sin(theta)
        unit_rightward_x = sin(theta)
        unit_rightward_y = -cos(theta)

        delta_x = unit_forward_x*step.forward + unit_rightward_x*step.rightward
        delta_y = unit_forward_y*step.forward + unit_rightward_y*step.rightward

        # FIXME: This discretisation doesn't really work for non-right-angle movements. If you step forward 1 at a 45°
        #        angle, you should land ~1.414 away in the centre of the tile diagonal to your position. Right now, you
        #        land 1 away on the diagonal, which is only 1/sqrt(2) == 0.707 in each direction, which int()s to 0 again.
        #        Of course, this is only defined for a handful of angles depending on the step size. Could allow the user
        #        to not "snap to grid" although it will be a pain to visualise. (Also, ASCII can't visualise rotations.)
        self.position = AbsoluteFootState(x=round(self.position.x + delta_x), y=round(self.position.y + delta_y), rotation=self.position.rotation)

    def visit_Turn(self, step: Turn):
        self.position = AbsoluteFootState(self.position.x, self.position.y, (self.position.rotation + step.degrees) % 360)

    def visit_MoveThenTurn(self, step: MoveThenTurn):
        self.visit_Move(step.move)
        self.visit_Turn(step.turn)

    def visit_TurnThenMove(self, step: TurnThenMove):
        self.visit_Turn(step.turn)
        self.visit_Move(step.move)


TwoUnnamedFeetStates = Tuple[AbsoluteFootState, AbsoluteFootState]  # State of two unnamed feet.
TwoUnnamedFeetSteps  = Tuple[_RelativeStep, _RelativeStep]  # Movement of two unnamed feet.
NamedFeetStates = Dict[NamedFoot, AbsoluteFootState]  # State of up to four named feet.
NamedFeetSteps  = Dict[NamedFoot, _RelativeStep]              # Movement of up to four named feet.
UnnamedCountResult = Tuple[TwoUnnamedFeetStates, TwoUnnamedFeetSteps]  # State and movement, each of two unnamed feet.
NamedCountResult = Tuple[NamedFeetStates, NamedFeetSteps]  # State and movement, each of any amount of named feet.


class Body:
    """
    Stores the state of two feet and updates them based on Counts, which give the movement of two feet.
    TODO: I wonder if the constructor should give so much freedom as to allow any absolute foot state.
          Don't all bodies start feet together, especially given that there are StartingPoses anyway?
    """

    def __init__(self, left_absolute_start: AbsoluteFootState, right_absolute_start: AbsoluteFootState):
        self._left_foot  = SimulatedPosition(deepcopy(left_absolute_start))
        self._right_foot = SimulatedPosition(deepcopy(right_absolute_start))
        self._first_pattern_ever = True

    def executeCount(self, count: Count) -> UnnamedCountResult:
        if count.left:
            self._left_foot.update(count.left)
        if count.right:
            self._right_foot.update(count.right)
        return (self._left_foot.position, self._right_foot.position), (count.left, count.right)

    def executePattern(self, pattern: Pattern) -> Iterable[UnnamedCountResult]:
        if self._first_pattern_ever:  # Simulate the starting stance first.
            self.executeCount(pattern.start)
            self._first_pattern_ever = False

        for count in pattern.counts:
            yield self.executeCount(count)


class Agent(ABC):
    """
    One or more people that can change state based on (i.e. act out) a Figura.

    The Agent abstraction is the bridge between Figura and Body, and between Body and dictionary-based feet states.
    The Body is a back-end that manages positions but doesn't know anything about higher-level concepts like Pattern
    and Figura. The front-ends that want to visualise feet don't know anything about lower-level separations like the
    decoupling between leaders and followers, patterns and figuras. They just know about feet and positions.

                                 Figura
                                    v
    step interpreter <-> Body <-> Agent ---> feet state dictionary
    """
    @abstractmethod
    def executeFigura(self, figura: Figura) -> Iterable[NamedCountResult]:
        pass

    @abstractmethod
    def executeFiguraStartingPose(self, figura: Figura) -> NamedFeetStates:
        pass


class Person(Agent):
    """
    A single-person Agent. Can also act out a Pattern.
    """
    def __init__(self, baseline: TwoUnnamedFeetStates=None):
        if baseline is None:
            baseline = (AbsoluteFootState(0,0,90),AbsoluteFootState(1,0,90))
        self.body = Body(*baseline)

    def executeCount(self, count: Count) -> NamedCountResult:
        return self._tagResultsWithFeet(self.body.executeCount(count))

    def executePatternStartingPose(self, pattern: Pattern) -> NamedFeetStates:
        return self.executeCount(pattern.start)[0]

    def executeFiguraStartingPose(self, figura: Figura) -> NamedFeetStates:
        return self.executePatternStartingPose(self._getPattern(figura))

    def executePattern(self, pattern: Pattern) -> Iterable[NamedCountResult]:
        for result in self.body.executePattern(pattern):
            yield self._tagResultsWithFeet(result)

    def executeFigura(self, figura: Figura) -> Iterable[Tuple[NamedFeetStates, NamedFeetSteps]]:
        yield from self.executePattern(self._getPattern(figura))

    @abstractmethod
    def _getFeetNames(self) -> Tuple[NamedFoot, NamedFoot]:
        pass

    @abstractmethod
    def _getPattern(self, figura: Figura):
        pass

    def _tagResultsWithFeet(self, result: UnnamedCountResult) -> NamedCountResult:
        left, right = self._getFeetNames()
        (left_state,right_state), (left_step,right_step) = result
        return {left: left_state, right: right_state}, \
               {left: left_step,  right: right_step}


class Leader(Person):

    def _getFeetNames(self) -> Tuple[NamedFoot, NamedFoot]:
        return NamedFoot.LeaderLeft, NamedFoot.LeaderRight

    def _getPattern(self, figura: Figura):
        return figura.leader


class Follower(Person):

    def _getFeetNames(self) -> Tuple[NamedFoot, NamedFoot]:
        return NamedFoot.FollowerLeft, NamedFoot.FollowerRight

    def _getPattern(self, figura: Figura):
        return figura.follower


class Couple(Agent):
    def __init__(self, leader_baseline: TwoUnnamedFeetStates=None):
        self.leader   = Leader(leader_baseline)
        self.follower = Follower(leader_baseline)

    def moveFollowerToBaseline(self, figura: Figura):
        self.follower.executeCount(figura.starting_posicion)

    def executeFiguraStartingPose(self, figura: Figura) -> NamedFeetStates:
        """
        Get the result of applying only the starting pose of a figura to the Couple, without any of the counts.

        Note: normally, it is not necessary to call this method. When a person's Body executes a Pattern, it will
        automatically move into the starting pose of that Pattern (assuming the Body is on its baseline).
        """
        leader_feet = self.leader.executeFiguraStartingPose(figura)
        self.moveFollowerToBaseline(figura)
        follower_feet = self.follower.executeFiguraStartingPose(figura)
        return leader_feet | follower_feet

    def executeFigura(self, figura: Figura) -> Iterable[Tuple[NamedFeetStates, NamedFeetSteps]]:
        if self.follower.body._first_pattern_ever:
            self.moveFollowerToBaseline(figura)

        for (states1,steps1), (states2,steps2) in zip(self.leader.executeFigura(figura), self.follower.executeFigura(figura)):
            yield states1 | states2, steps1 | steps2


def translate(position: AbsoluteFootState, x: int, y: int) -> AbsoluteFootState:
    return AbsoluteFootState(position.x + x, position.y + y, position.rotation)


def rotate90(position: AbsoluteFootState, axis_x: int, axis_y: int) -> AbsoluteFootState:
    x = position.x - axis_x
    y = position.y - axis_y
    return AbsoluteFootState(-y + axis_x, x + axis_y, (position.rotation + 90) % 360)


def areEquivalentStates(state1: NamedFeetStates, state2: NamedFeetStates) -> bool:
    """
    Two states are equivalent when one can be made fully equal to the other by only shifting and rotating.
    """
    # 1. Check that both states have the same feet.
    if set(state1) != set(state2):
        return False

    # 2. Choose a foot and shift that foot's position in state 2 to the position of state 1.
    #    (Could also shift both to (0,0) but then you'd have to alter both.)
    anchor_foot = peek(state1)
    anchor_position_in_1 = state1[anchor_foot]
    anchor_position_in_2 = state2[anchor_foot]
    delta_x = anchor_position_in_1.x - anchor_position_in_2.x
    delta_y = anchor_position_in_1.y - anchor_position_in_2.y

    state2 = deepcopy(state2)
    for foot in state2:
        state2[foot] = translate(state2[foot], delta_x, delta_y)

    assert state1[anchor_foot].x == state2[anchor_foot].x and state1[anchor_foot].y == state2[anchor_foot].y

    # 3. Generate all 4 rotations of state 2 and check if there's a match.
    for _ in range(4):
        if all(state1[foot] == state2[foot] for foot in state1):
            return True
        for foot in state2:
            state2[foot] = rotate90(state2[foot], anchor_position_in_1.x, anchor_position_in_1.y)
    else:
        return False


def areCompatiblePatterns(pattern1: Pattern, pattern2: Pattern) -> bool:
    """
    One pattern is compatible with another when the end state of simulating it is equivalent to the begin state of the other.
    """
    person1 = Leader((AbsoluteFootState(0, 0, 90), AbsoluteFootState(1,0,90)))
    person1_feet, _ = last(person1.executePattern(pattern1))

    person2 = Leader((AbsoluteFootState(0, 0, 90), AbsoluteFootState(1,0,90)))
    person2_feet, _ = person2.executeCount(pattern2.start)

    return areEquivalentStates(person1_feet, person2_feet)


def areCompatibleFiguras(figura1: Figura, figura2: Figura) -> bool:
    """
    One figure is compatible with another not just when the patterns of both leader and follower are each compatible,
    but when the end state of both patterns combined is compatible with the begin state of the other's patterns combined.
    This is not the same thing.
    """
    couple1 = Couple(leader_baseline=(AbsoluteFootState(0,0,90), AbsoluteFootState(1,0,90)))
    couple1_feet,_ = last(couple1.executeFigura(figura1))

    couple2 = Couple(leader_baseline=(AbsoluteFootState(0,0,90), AbsoluteFootState(1,0,90)))
    couple2_feet = couple2.executeFiguraStartingPose(figura2)

    return areEquivalentStates(couple1_feet, couple2_feet)
