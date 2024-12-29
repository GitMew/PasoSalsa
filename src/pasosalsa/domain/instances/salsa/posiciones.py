from ...abstracts.patterns import *
from ..movement import *


# Open position, i.e. leader and follower facing each other with enough space in between to move a foot forward each without colliding.
PosicionAbierta = Posicion(
    left=MoveThenTurn(
        Forward + Forward + Forward + Rightward,
        Clockwise180
    ),
    right=MoveThenTurn(
        Forward + Forward + Forward + Leftward,
        Clockwise180
    )
)


# Closed position, i.e. leader and follower facing each other with no space in between.
PosicionCerrada = Posicion(
    left=MoveThenTurn(
        Forward + Rightward,
        Clockwise180
    ),
    right=MoveThenTurn(
        Forward + Leftward,
        Clockwise180
    )
)


# The 90° position from which 'exhibe-la' and 'di-le que no' happen.
#
#          < FR
#     ^   ^< FL
#     LL  LR
#
# Leader facing forward, follower is on his front-right facing left.
PosicionCaida = Posicion(
    left=MoveThenTurn(
        Rightward + Rightward + Forward,
        CounterClockwise90
    ),
    right=MoveThenTurn(
        Rightward + Forward + Forward,
        CounterClockwise90
    )
)


# I don't actually know what this is called, but it is basically the following position:
#
#     ^   ^
#     LL  LR  ^   ^
#             FL  FR
#
# Follower is facing the same way as the leader and behind him.
PosicionAbajo = Posicion(
    left= Rightward2 + Backward,
    right=Rightward2 + Backward
)


# The position you find yourself in during a Cubanita:
#     ^   ^
#     FL  FR
#     ^   ^
#     LL  LR
PosicionCubanita = Posicion(
    left= Forward2,
    right=Forward2
)


# Same as Cubanita but with the roles reversed.
PosicionCubanito = Posicion(
    left= Backward2,
    right=Backward2
)


# Starting poses
FeetTogether = StartingPose(InPlace,InPlace)
LegsCrossedRightOverLeft = StartingPose(left=Backward + Rightward2, right=InPlace)
LegsCrossedLeftOverRight = StartingPose(left=InPlace, right=Backward + Leftward2)
FeetDiagonalLeftBackward = StartingPose(left=Backward, right=InPlace)
FeetDiagonalRightForward = StartingPose(left=InPlace, right=Forward)
FeetApartRight = StartingPose(InPlace,Rightward)
