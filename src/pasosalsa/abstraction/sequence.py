from typing import Iterable, TypeVar
from copy import deepcopy

from .figuras import Figura, FeetState, FootPosition


T = TypeVar("T")
def peek(s: Iterable[T]) -> T:
    for thing in s:
        return thing


def simulate(figure: Figura, base: FeetState=None) -> Iterable[FeetState]:
    positions = deepcopy(base or figure.base)
    for checkpoint in figure.checkpoints:
        for foot, step in checkpoint.steps_since_previous:
            positions[foot] = step.updatePosition(positions[foot])
        yield deepcopy(positions)


def translate(position: FootPosition, x: int, y: int) -> FootPosition:
    return FootPosition(position.x + x, position.y + y, position.rotation)


def rotate90(position: FootPosition, axis_x: int, axis_y: int) -> FootPosition:
    x = position.x - axis_x
    y = position.y - axis_y
    return FootPosition(-y + axis_x, x + axis_y, (position.rotation + 90) % 360)


def areEquivalentStates(state1: FeetState, state2: FeetState) -> bool:
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


def areCompatible(figura1: Figura, figura2: Figura) -> bool:
    """
    One figure is compatible with another when the end state of simulating it is equivalent to the begin state of the other.
    """
    end_state = None
    for state in simulate(figura1):
        end_state = state
    assert end_state is not None

    start_state = figura2.base
    return areEquivalentStates(end_state, start_state)


class Sequence(Figura):

    def __init__(self, name: str, *figures: Figura):
        assert len(figures) > 0

        for f1,f2 in zip(figures[:-1], figures[1:]):
            if not areCompatible(f1,f2):
                raise ValueError(f"Cannot let {f1.name} be followed by {f2.name} due to incompatible positions.")

        super().__init__(name, figures[0].base, [figures[0].checkpoints[0]] + sum(map(lambda f: f.checkpoints[1:], figures), []))

        self.subfigures = [(f.name, f.counts) for f in figures]
