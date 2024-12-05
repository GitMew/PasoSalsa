from typing import Optional

from .patterns import Count, Pattern, StartingPose, _Foot
from .figuras import Figura
from .simulation import areCompatibleFiguras, areCompatiblePatterns, Body, AbsoluteFootState, last
from .movement import MoveThenTurn, Move, Turn, _RelativeStep
from ...util.iterables import first


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
    left_foot_baseline, right_foot_baseline = AbsoluteFootState(0,0,90), AbsoluteFootState(1,0,90)
    body = Body(left_foot_baseline, right_foot_baseline)
    (left_foot,right_foot), _ = last(body.executePattern(pattern))

    # Use the difference with the original baseline as the starting move. Then swap the order of all moves and invert them.
    return Pattern(
        start=StartingPose(
            left=left_foot - left_foot_baseline,
            right=right_foot - right_foot_baseline
        ),
        counts=new_counts
    )


def LikeLeaderIn(figura: Figura) -> Pattern:
    return figura.leader.copy()


def LikeFollowerIn(figura: Figura) -> Pattern:
    return figura.follower.copy()


def WithReplacedStartByEnd(pattern: Pattern) -> Pattern:
    """
    Returns a pattern that is the same as the given pattern except it starts where the given pattern ends.
    Note: you will probably want to replace the step of the first count in that case.
    """
    left_start, right_start = AbsoluteFootState(0,0,90), AbsoluteFootState(1,0,90)  # Not start of the pattern (which we don't care about, since we will overwrite it), but start as in what .start is relative to.
    body = Body(left_start,right_start)
    (left_end, right_end), _ = last(body.executePattern(pattern))

    new_pattern = pattern.copy()
    new_pattern.start = Count(left=left_end - left_start, right=right_end - right_start)
    return new_pattern


def WithReplacedStep(pattern: Pattern, count: int, foot: _Foot, step: Optional[_RelativeStep]) -> Pattern:
    assert count <= len(pattern.counts)

    new_pattern = pattern.copy()
    new_pattern.counts[count-1].setFoot(foot, step)
    return new_pattern


def Loopable(pattern: Pattern) -> Pattern:
    """
    Replaces the starting position of the pattern, and count 1, such that the final position equals the starting
    position and count 1 lands in the same position as usual.
    """
    baseline_left, baseline_right = AbsoluteFootState(0, 0, 90), AbsoluteFootState(1, 0, 90)
    body = Body(baseline_left, baseline_right)
    absolute_position_iterable = body.executePattern(pattern)
    (left_count1, right_count1), _ = first(absolute_position_iterable)
    (left_count8, right_count8), _ = last(absolute_position_iterable)

    new_pattern = pattern.copy()
    new_pattern.start     = Count(left=left_count8 - baseline_left, right=right_count8 - baseline_right)  # .start is the difference between starting position and baseline.
    new_pattern.counts[0] = Count(left=left_count1 - left_count8,   right=right_count1 - right_count8)    # The movement you need to do on count 1 to get into the result of the old count 1 but from count 8 rather than the old starting position.
    return new_pattern
