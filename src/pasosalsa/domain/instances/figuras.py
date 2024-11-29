from ..abstracts.figuras import *
from ..abstracts.sequence import Sequence
from .movement import *


__all__ = ["Guapea", "VueltaDerecha", "DiLeQueNo", "Crusado", "CrusadoToEnchufla", "WideCrusado", "Enchufla", "HalfEnchufla",
           "EnchuflaDoble", "Exhibela", "CubanBasicStep",
           "EnchuflaSequence", "EnchuflaDobleSequence", "ExhibelaSequence"]


Guapea = BuildFigura(
    "guapea",
    LeaderFeetTogether
).move(
    Foot.LeaderLeft,
    Backward
).count().move(
    Foot.LeaderRight,
    InPlace
).count().move(
    Foot.LeaderLeft,
    Forward
).count().pause().move(
    Foot.LeaderRight,
    Forward
).count().move(
    Foot.LeaderLeft,
    InPlace
).count().move(
    Foot.LeaderRight,
    Backward
).count().pause().finish()



VueltaDerecha = BuildFigura(
    "vuelta derecha",
    FollowerFeetTogether
).move(
    Foot.FollowerRight,
    Backward
).count().move(
    Foot.FollowerLeft,
    InPlace
).count().move(
    Foot.FollowerRight,
    Forward
).count().pause().move(
    Foot.FollowerLeft,
    MoveThenTurn(
        Forward + Leftward,
        Clockwise45
    )
).count().move(
    Foot.FollowerRight,
    Clockwise180
).count().move(
    Foot.FollowerRight,
    Clockwise180
).move(
    Foot.FollowerLeft,
    TurnThenMove(
        Clockwise(360 - 45),
        Leftward + Backward
    )
).count().pause().finish()


# TODO: VD that goes into closed position for a CBS.
# VueltaDerechaCerranda =


# VueltaDoble = BuildFigura(
#     "vuelta doble",
#     LeaderFeetTogether
# ).move(
#     Foot.LeaderLeft,
#     Backward
# ).count().move(
#     Foot.LeaderRight,
#     InPlace
# ).count().move(
#     Foot.LeaderLeft,
#     Forward
# ).count().pause().move(
#
# ).count().move(
#
# ).count().move(
#
# ).count().pause().finish()



DiLeQueNo = BuildFigura(
    "di-le que no",
    LeaderFeetTogether
).move(
    Foot.LeaderLeft,
    Forward
).count().move(
    Foot.LeaderRight,
    Rightward
).count().move(
    Foot.LeaderLeft,
    MoveThenTurn(
        Backward2 + Rightward2,
        CounterClockwise90
    )
).move(
    Foot.LeaderRight,
    CounterClockwise90
).count().pause().move(
    Foot.LeaderRight,
    Rightward
).count().move(
    Foot.LeaderLeft,
    MoveThenTurn(
        Rightward2 + Forward,
        CounterClockwise90
    )
).count().move(
    Foot.LeaderRight,
    MoveThenTurn(
        Forward2,
        CounterClockwise90
    )
).count().pause().finish()



Crusado = BuildFigura(
    "crusado",
    LeaderFeetTogether
).move(
    Foot.LeaderLeft,
    InPlace
).count().move(
    Foot.LeaderRight,
    Backward
).count().move(
    Foot.LeaderLeft,
    Rightward2
).count().pause().move(
    Foot.LeaderRight,
    Forward + Rightward2
).count().move(
    Foot.LeaderLeft,
    Backward
).count().move(
    Foot.LeaderRight,
    Leftward + Leftward
).count().pause().finish()



WideCrusado = BuildFigura(
    "wide crusado",
    LeaderFeetTogether
).move(
    Foot.LeaderLeft,
    Leftward
).count().move(
    Foot.LeaderRight,
    Backward
).count().move(
    Foot.LeaderLeft,
    Rightward + Rightward + Rightward
).count().pause().move(
    Foot.LeaderRight,
    Forward + Rightward + Rightward + Rightward
).count().move(
    Foot.LeaderLeft,
    Backward
).count().move(
    Foot.LeaderRight,
    Leftward + Leftward + Leftward
).count().pause().finish()



CrusadoToEnchufla = BuildFigura(
    "crusado ending like enchufla",
    LeaderLegsCrossedRightOverLeft
).move(
    Foot.LeaderLeft,
    Leftward2 + Forward
).count().move(
    Foot.LeaderRight,
    Backward
).count().move(
    Foot.LeaderLeft,
    Rightward2
).count().pause().move(
    Foot.LeaderRight,
    TurnThenMove(
        Clockwise90,
        Backward
    )
).count().move(
    Foot.LeaderLeft,
    TurnThenMove(
        Clockwise90,
        InPlace
    )
).count().move(
    Foot.LeaderRight,
    MoveThenTurn(
        Forward + Forward + Forward + Leftward,
        CounterClockwise90
    )
).move(
    Foot.LeaderLeft,
    CounterClockwise90
).count().pause().finish()



Enchufla = BuildFigura(
    "enchufla",
    LeaderFeetTogether
).move(
    Foot.LeaderLeft,
    Backward
).count().move(
    Foot.LeaderRight,
    Forward + Leftward + Leftward
).count().move(
    Foot.LeaderLeft,
    MoveThenTurn(
        Forward + Forward,
        Clockwise180
    )
).move(
    Foot.LeaderRight,
    Clockwise180
).count().pause().move(
    Foot.LeaderRight,
    Backward
).count().move(
    Foot.LeaderLeft,
    InPlace
).count().move(
    Foot.LeaderLeft,
    CounterClockwise90
).move(
    Foot.LeaderRight,
    MoveThenTurn(
        Forward + Forward + Leftward,
        CounterClockwise90
    )
).count().pause().finish()



HalfEnchufla = BuildFigura(
    "half-enchufla",
    LeaderFeetTogether
).move(
    Foot.LeaderLeft,
    Backward
).count().move(
    Foot.LeaderRight,
    Forward + Leftward + Leftward
).count().move(
    Foot.LeaderLeft,
    MoveThenTurn(
        Forward + Forward,
        Clockwise180
    )
).move(
    Foot.LeaderRight,
    Clockwise180
).count().pause().move(
    Foot.LeaderRight,
    Backward
).count().move(
    Foot.LeaderLeft,
    Forward
).count().move(
    Foot.LeaderLeft,
    CounterClockwise180
).move(
    Foot.LeaderRight,
    MoveThenTurn(
        Forward2 + Leftward2,
        CounterClockwise180
    )
).count().pause().finish()



EnchuflaDoble = Sequence(
    "enchufla doble",
    HalfEnchufla, Enchufla
)



CubanBasicStep = BuildFigura(
    "cuban basic step",
    LeaderFeetTogether
).move(
    Foot.LeaderRight,
    CounterClockwise45
).move(
    Foot.LeaderLeft,
    MoveThenTurn(
        Backward + Rightward,
        CounterClockwise90
    )
).count().move(
    Foot.LeaderRight,
    InPlace
).count().move(
    Foot.LeaderRight,
    Clockwise45
).move(
    Foot.LeaderLeft,
    TurnThenMove(
        Clockwise90,
        Leftward + Forward
    )
).count().pause().move(
    Foot.LeaderLeft,
    Clockwise45
).move(
    Foot.LeaderRight,
    MoveThenTurn(
        Backward + Leftward,
        Clockwise90
    )
).count().move(
    Foot.LeaderLeft,
    InPlace
).count().move(
    Foot.LeaderLeft,
    CounterClockwise45
).move(
    Foot.LeaderRight,
    TurnThenMove(
        CounterClockwise90,
        Rightward + Forward
    )
).count().pause().finish()



Exhibela = Sequence(
    "exhibela",
    Crusado, CrusadoToEnchufla
)



EnchuflaSequence = Sequence(
    "enchufla sequence",
    Enchufla, DiLeQueNo
)
EnchuflaDobleSequence = Sequence(
    "enchufla doble sequence",
    EnchuflaDoble, DiLeQueNo
)
ExhibelaSequence = Sequence(
    "exhibela sequence",
    Enchufla, Exhibela, DiLeQueNo
)


# TODO: Sacala
# SacalaSequence = Sequence(
#   "sacala sequence",
#   Sacachufla, Sacala, DiLeQueNo
# )
