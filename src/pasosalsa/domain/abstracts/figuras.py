from typing import Tuple, Iterable

from .patterns import Posicion, Pattern, Count


class Figura:

    def __init__(self, name: str, posicion_at_start: Posicion, leader: Pattern, follower: Pattern):
        assert leader.duration() == follower.duration()

        self.name = name
        self.starting_posicion = posicion_at_start

        self.leader = leader
        self.follower = follower

        # Automatically impute the names of patterns if they are anonymous.
        if not self.leader.name:
            self.leader.setName(name + " (L)")
        if not self.follower.name:
            self.follower.setName(name + " (F)")

    def duration(self):
        return self.leader.duration()

    def copy(self, name: str=None) -> "Figura":
        return Figura(
            name=name or self.name,
            posicion_at_start=self.starting_posicion.copy(),
            leader=self.leader.copy(),
            follower=self.follower.copy()
        )


class BuildFigura:

    def __init__(self, name: str):
        self._name = name

    def startsIn(self, posicion: Posicion) -> "_FiguraBuilderWithStart":
        return _FiguraBuilderWithStart(name=self._name, posicion=posicion)


class _FiguraBuilderWithStart:

    def __init__(self, name: str, posicion: Posicion):
        self._name = name
        self._posicion = posicion

    def withLeader(self, pattern: Pattern) -> "_FiguraBuilderWithStartAndLeader":
        return _FiguraBuilderWithStartAndLeader(name=self._name, posicion=self._posicion, leader=pattern)

    def withFollower(self, pattern: Pattern) -> "_FiguraBuilderWithStartAndFollower":
        return _FiguraBuilderWithStartAndFollower(name=self._name, posicion=self._posicion, follower=pattern)


class _FiguraBuilderWithStartAndLeader:

    def __init__(self, name: str, posicion: Posicion, leader: Pattern):
        self._name = name
        self._posicion = posicion
        self._leader = leader

    def withFollower(self, pattern: Pattern) -> Figura:
        return Figura(
            name=self._name,
            posicion_at_start=self._posicion,
            leader=self._leader,
            follower=pattern
        )


class _FiguraBuilderWithStartAndFollower:

    def __init__(self, name: str, posicion: Posicion, follower: Pattern):
        self._name = name
        self._posicion = posicion
        self._follower = follower

    def withLeader(self, pattern: Pattern) -> Figura:
        return Figura(
            name=self._name,
            posicion_at_start=self._posicion,
            leader=pattern,
            follower=self._follower
        )
