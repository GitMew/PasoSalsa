from copy import deepcopy

from .patterns import Count, Pattern, StartingPose
from .figuras import Figura
from .simulation import areCompatibleFiguras, areCompatiblePatterns, Body, AbsoluteFootState, last
from .movement import MoveThenTurn, Move, Turn


class PatternSequence(Pattern):

    def __init__(self, *patterns: Pattern):
        assert len(patterns) > 0

        for p1,p2 in zip(patterns[:-1], patterns[1:]):
            if not areCompatiblePatterns(p1,p2):
                raise ValueError(f"Cannot let pattern '{p1}' be followed by '{p2}' due to incompatible end/start positions.")

        super().__init__(start=patterns[0].start, counts=sum(map(lambda p: p.counts, patterns), start=[]))


class FiguraSequence(Figura):

    def __init__(self, name: str, *figuras: Figura):
        assert len(figuras) > 0

        for f1,f2 in zip(figuras[:-1], figuras[1:]):
            if not areCompatibleFiguras(f1,f2):
                raise ValueError(f"Cannot let {f1.name} be followed by {f2.name} due to incompatible positions.")

        leader_patterns   = [f.leader for f in figuras]
        follower_patterns = [f.follower for f in figuras]
        super().__init__(name=name, posicion_at_start=figuras[0].starting_posicion,
                         leader=PatternSequence(*leader_patterns),
                         follower=PatternSequence(*follower_patterns))


def TimeReversed(pattern: Pattern, shift_pause: bool=True) -> Pattern:
    """
    Return the given pattern in reverse; the starting pose of the result is the ending pose of the given pattern, and
    the moves are in reverse order and perform the reverse movements
    E.g.: forward-inplace-leftward becomes rightward-inplace-backward.

    :param shift_pause: Since most salsa patterns have 3 active counts and 1 pause count, reversing in time means having
                        1 pause count and 3 active counts. If this argument is true, the pause at the end is not copied
                        to the start of the resulting pattern and is instead kept at the end.
    """
    new_counts = list(reversed([-c for c in pattern.counts]))
    if shift_pause and new_counts[0].isPause():
        new_counts.append(new_counts[0])
        new_counts.pop(0)

    # Compute final position of the feet after this pattern is executed starting at the baseline (0,0), (1,0).
    body = Body(AbsoluteFootState(0,0,90), AbsoluteFootState(1,0,90))
    (left_foot,right_foot), _ = last(body.executePattern(pattern))

    # Use the difference with the original baseline as the starting move. Then swap the order of all moves and invert them.
    return Pattern(
        start=StartingPose(
            left=MoveThenTurn(
                Move(forward=left_foot.y - 0, rightward=left_foot.x - 0),
                Turn(degrees=left_foot.rotation - 90)
            ),
            right=MoveThenTurn(
                Move(forward=right_foot.y - 0, rightward=right_foot.x - 1),
                Turn(degrees=right_foot.rotation - 90)
            )
        ),
        counts=new_counts
    )


def Mirror(pattern: Pattern) -> Pattern:
    """
    Return the given pattern as if you're doing it in the mirror.
    """
    return Pattern(
        start=MirrorPose(pattern.start),
        counts=[MirrorCount(c) for c in pattern.counts]
    )


def MirrorPose(pose: StartingPose) -> StartingPose:
    return StartingPose(
        left=pose.right.mirrored() if pose.right else None,
        right=pose.left.mirrored() if pose.left else None
    )


def MirrorCount(count: Count) -> Count:
    return Count(
        left=count.right.mirrored() if count.right else None,
        right=count.left.mirrored() if count.left else None
    )


def LikeLeaderIn(figura: Figura) -> Pattern:
    return deepcopy(figura.leader)


def LikeFollowerIn(figura: Figura) -> Pattern:
    return deepcopy(figura.follower)
