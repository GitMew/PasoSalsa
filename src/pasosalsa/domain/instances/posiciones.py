from ..abstracts.patterns import *
from .movement import *


class _PosicionAbierta(Posicion):
    """
    Open position, i.e. leader and follower facing each other with enough space in between to move a foot forward each without colliding.
    """
    def leaderBaselineToFollowerBaseline(self) -> Count:
        return Count(
            left=MoveThenTurn(
                Forward + Forward + Forward + Rightward,
                Clockwise180
            ),
            right=MoveThenTurn(
                Forward + Forward + Forward + Leftward,
                Clockwise180
            )
        )
PosicionAbierta = _PosicionAbierta()


class _PosicionCerrada(Posicion):
    """
    Closed position, i.e. leader and follower facing each other with no space in between.
    """
    def leaderBaselineToFollowerBaseline(self) -> Count:
        return Count(
            left=MoveThenTurn(
                Forward + Rightward,
                Clockwise180
            ),
            right=MoveThenTurn(
                Forward + Leftward,
                Clockwise180
            )
        )
PosicionCerrada = _PosicionAbierta()


class _PosicionCaida(Posicion):
    """
    The 90° position from which 'exhibe-la' and 'di-le que no' happen.

             < FR
        ^   ^< FL
        LL  LR

    Leader facing forward, follower is on his front-right facing left.
    """
    def leaderBaselineToFollowerBaseline(self) -> Count:
        return Count(
            left=MoveThenTurn(
                Rightward + Rightward + Forward,
                CounterClockwise90
            ),
            right=MoveThenTurn(
                Rightward + Forward + Forward,
                CounterClockwise90
            )
        )
PosicionCaida = _PosicionCaida()


class _PosicionAbajo(Posicion):
    """
    I don't actually know what this is called, but it is basically the following position:

        ^   ^
        LL  LR  ^   ^
                FL  FR

    Follower is facing the same way as the leader and behind him.
    """
    def leaderBaselineToFollowerBaseline(self) -> Count:
        return Count(
            left=Rightward2 + Backward,
            right=Rightward2 + Backward
        )
PosicionAbajo = _PosicionAbajo()
