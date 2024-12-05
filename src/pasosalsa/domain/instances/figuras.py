from ..abstracts.figuras import *
from ..abstracts.composition import *
from ..abstracts.patterns import *
from .movement import *
from .posiciones import *

# TODO: Activate this __all__ when you have finished all the TODOs below.
# __all__ = ["Guapea", "VueltaDerecha", "DiLeQueNo", "Cruzado", "CruzadoToEnchufla", "WideCruzado", "Enchufla", "HalfEnchufla",
#            "EnchuflaDoble", "Exhibela", "CubanBasicStep",
#            "EnchuflaSequence", "EnchuflaDobleSequence", "ExhibelaSequence"]


Guapea_Leader = BuildPattern(
    FeetTogether
).move(
    LeftFoot,
    Backward
).count().move(
    RightFoot,
    InPlace
).count().move(
    LeftFoot,
    Forward
).count().pause().move(
    RightFoot,
    Forward
).count().move(
    LeftFoot,
    InPlace
).count().move(
    RightFoot,
    Backward
).count().pause().finish()


Guapea = BuildFigura(
    "guapea"
).startsIn(
    PosicionAbierta
).withLeader(
    Guapea_Leader
).withFollower(
    Mirror(Guapea_Leader)
)



VueltaDerecha_Leader = BuildPattern(
    FeetTogether
).move(
    LeftFoot,
    Backward
).count().move(
    RightFoot,
    InPlace
).count().move(
    LeftFoot,
    Forward
).count().pause().move(
    RightFoot,
    InPlace
).count().move(
    LeftFoot,
    InPlace
).count().move(
    RightFoot,
    InPlace
).count().pause().finish()



VueltaDerecha_Follower = BuildPattern(
    FeetTogether
).move(
    RightFoot,
    Backward
).count().move(
    LeftFoot,
    InPlace
).count().move(
    RightFoot,
    Forward
).count().pause().move(
    LeftFoot,
    MoveThenTurn(
        Forward + Rightward,
        Clockwise45
    )
).count().move(
    RightFoot,
    Clockwise180
).count().move(
    RightFoot,
    Clockwise180
).move(
    LeftFoot,
    TurnThenMove(
        Clockwise(360 - 45),
        Leftward + Backward
    )
).count().pause().finish()



VueltaDerecha = BuildFigura(
    "vuelta derecha"
).startsIn(
    PosicionAbierta
).withLeader(
    VueltaDerecha_Leader
).withFollower(
    VueltaDerecha_Follower
)


# TODO: VD that goes into closed position for a CBS.
# VueltaDerechaCerranda =


# TODO: leader steps for vuelta doble
# VueltaDoble_Leader = BuildFigura(
#     "vuelta doble (L)",
#     FeetTogether
# ).move(
#     LeftFoot,
#     Backward
# ).count().move(
#     RightFoot,
#     InPlace
# ).count().move(
#     LeftFoot,
#     Forward
# ).count().pause().move(
#
# ).count().move(
#
# ).count().move(
#
# ).count().pause().finish()

# VueltaDoble = BuildFigura(
#     "vuelta doble"
# ).startsIn(
#     PosicionAbierta
# ).withLeader(
#     VueltaDoble_Leader
# ).withFollower(
#     VueltaDerecha_Follower
# )


DiLeQueNo_Leader = BuildPattern(
    FeetTogether
).move(
    LeftFoot,
    Forward
).count().move(
    RightFoot,
    Rightward
).count().move(
    LeftFoot,
    MoveThenTurn(
        Backward2 + Rightward2,
        CounterClockwise90
    )
).move(
    RightFoot,
    CounterClockwise90
).count().pause().move(
    RightFoot,
    Rightward
).count().move(
    LeftFoot,
    MoveThenTurn(
        Rightward2 + Forward,
        CounterClockwise90
    )
).count().move(
    RightFoot,
    MoveThenTurn(
        Forward2,
        CounterClockwise90
    )
).count().pause().finish()


# TODO: DQN follower
# DiLeQueNo_Follower = BuildPattern(
#     FeetTogether
# )
#
#
# DiLeQueNo = BuildFigura(
#     "di-le que no"
# ).startsIn(
#     PosicionCaida
# ).withLeader(
#     DiLeQueNo_Leader
# ).withFollower(
#     DiLeQueNo_Follower
# )


Cruzado_Left_Start = BuildPattern(
    FeetTogether
).move(
    LeftFoot,
    InPlace
).count().move(
    RightFoot,
    Backward
).count().move(
    LeftFoot,
    Rightward2
).count().pause().move(
    RightFoot,
    Forward + Rightward2
).count().move(
    LeftFoot,
    Backward
).count().move(
    RightFoot,
    Leftward + Leftward
).count().pause().finish()

Cruzado_Left_Start.setName("cruzado")


WideCruzado_Left_Start = BuildPattern(
    FeetTogether
).move(
    LeftFoot,
    Leftward
).count().move(
    RightFoot,
    Backward
).count().move(
    LeftFoot,
    Rightward + Rightward + Rightward
).count().pause().move(
    RightFoot,
    Forward + Rightward + Rightward + Rightward
).count().move(
    LeftFoot,
    Backward
).count().move(
    RightFoot,
    Leftward + Leftward + Leftward
).count().pause().finish()

WideCruzado_Left_Start.setName("wide cruzado")


# The "loopable" automatically finds the LeftFoot instructions below:
# Cruzado_Left_Continued = WithReplacedStep(
#     WithReplacedStartByEnd(Cruzado_Left_Start),
#     1,
#     LeftFoot,
#     Leftward2 + Forward
# )
Cruzado_Left_Loopable = Loopable(Cruzado_Left_Start)


Cruzado_Left_End = BuildPattern(
    LegsCrossedRightOverLeft
).move(
    LeftFoot,
    Leftward2 + Forward
).count().move(
    RightFoot,
    Backward
).count().move(
    LeftFoot,
    Rightward2
).count().pause().move(
    RightFoot,
    Clockwise90
).count().move(
    LeftFoot,
    Leftward2
).count().move(
    RightFoot,
    TurnThenMove(
        CounterClockwise90,
        Forward
    )
).count().pause().finish()

Cruzado_Left_End.setName("cruzado ending with feet together")


Enchufla_Leader = BuildPattern(
    FeetTogether
).move(
    LeftFoot,
    Backward
).count().move(
    RightFoot,
    Forward + Leftward + Leftward
).count().move(
    LeftFoot,
    MoveThenTurn(
        Forward + Forward,
        Clockwise180
    )
).move(
    RightFoot,
    Clockwise180
).count().pause().move(
    RightFoot,
    Backward
).count().move(
    LeftFoot,
    InPlace
).count().move(
    LeftFoot,
    CounterClockwise90
).move(
    RightFoot,
    MoveThenTurn(
        Forward + Forward + Leftward,
        CounterClockwise90
    )
).count().pause().finish()


# TODO: Enchufla follower
# Enchufla_Follower = BuildPattern(
#     FeetTogether
# )
#
#
#
# Enchufla = BuildFigura(
#     "enchufla"
# ).startsIn(
#     PosicionAbierta
# ).withLeader(
#     Enchufla_Leader
# ).withFollower(
#     Enchufla_Follower
# )





HalfEnchufla_Leader = BuildPattern(
    FeetTogether
).move(
    LeftFoot,
    Backward
).count().move(
    RightFoot,
    Forward + Leftward + Leftward
).count().move(
    LeftFoot,
    MoveThenTurn(
        Forward + Forward,
        Clockwise180
    )
).move(
    RightFoot,
    Clockwise180
).count().pause().move(
    RightFoot,
    Backward
).count().move(
    LeftFoot,
    Forward
).count().move(
    LeftFoot,
    CounterClockwise180
).move(
    RightFoot,
    MoveThenTurn(
        Forward2 + Leftward2,
        CounterClockwise180
    )
).count().pause().finish()


# TODO: HE follower
# HalfEnchufla_Follower = BuildPattern(
#     FeetTogether
# )
#
#
# HalfEnchufla = BuildFigura("half-enchufla")\
#     .startsIn(PosicionAbierta)\
#     .withLeader(HalfEnchufla_Leader)\
#     .withFollower(HalfEnchufla_Follower)


# EnchuflaDoble = FiguraSequence(
#     "enchufla doble",
#     HalfEnchufla, Enchufla
# )



LeaderCubanBasicStep = BuildPattern(
    FeetTogether
).move(
    RightFoot,
    CounterClockwise45
).move(
    LeftFoot,
    MoveThenTurn(
        Backward + Rightward,
        CounterClockwise90
    )
).count().move(
    RightFoot,
    InPlace
).count().move(
    RightFoot,
    Clockwise45
).move(
    LeftFoot,
    TurnThenMove(
        Clockwise90,
        Leftward + Forward
    )
).count().pause().move(
    LeftFoot,
    Clockwise45
).move(
    RightFoot,
    MoveThenTurn(
        Backward + Leftward,
        Clockwise90
    )
).count().move(
    LeftFoot,
    InPlace
).count().move(
    LeftFoot,
    CounterClockwise45
).move(
    RightFoot,
    TurnThenMove(
        CounterClockwise90,
        Rightward + Forward
    )
).count().pause().finish()



CubanBasicStep = BuildFigura("Cuban basic step")\
    .startsIn(PosicionCerrada)\
    .withLeader(LeaderCubanBasicStep)\
    .withFollower(Mirror(LeaderCubanBasicStep))

CumbiaBasic = CubanBasicStep  # "Cuban basic step" is used at our school, Cumbia basic is used e.g. here: https://salsayo.com/move/Back-Rocks and also https://thedancedojo.com/how-to-salsa-dance-for-beginners/back-and-cumbia-salsa-basic-steps


# Guapea, except
#   1. you "overstep" and your feet form a diagonal in resting position rather than being together, and
#   2. the men start forwards so that the distance between the partners is the same.
# Called "pa' ti, pa' mi" by Salsaficion (but that name is already used for a turn for woman, turn for man, turn for woman), "salsa" by our Cuban teacher and "basic step" by our Flemish teacher. Seems to be called Mambo elsewhere: https://salsayo.com/move/Basic-Steps and https://salsayo.com/move/Closed-Position-Basic-Steps
MamboBasicStep_Leader_Start = BuildPattern(
    FeetTogether
).move(
    LeftFoot,
    Forward
).count().move(
    RightFoot,
    InPlace
).count().move(
    LeftFoot,
    Backward2
).count().pause().move(
    RightFoot,
    Backward2
).count().move(
    LeftFoot,
    InPlace
).count().move(
    RightFoot,
    Forward2
).count().pause().finish()


WalkingVueltaDerecha_Follower_Start = BuildPattern(  # Is to vuelta derecha what Mambo is to Guapea.
    FeetTogether
).move(
    RightFoot,
    Backward
).count().move(
    LeftFoot,
    InPlace
).count().move(
    RightFoot,
    Forward2
).count().pause().move(
    LeftFoot,
    MoveThenTurn(
        Forward2 + Rightward,
        Clockwise45
    )
).count().move(
    RightFoot,
    Clockwise180
).count().move(
    RightFoot,
    Clockwise180
).move(
    LeftFoot,
    TurnThenMove(
        Clockwise(360 - 45),
        Leftward + Backward2
    )
).count().pause().finish()


WalkingVueltaDerecha_Follower_End = BuildPattern(  # Is to vuelta derecha what Mambo is to Guapea.
    FeetDiagonalRightForward
).move(
    RightFoot,
    Backward2
).count().move(
    LeftFoot,
    InPlace
).count().move(
    RightFoot,
    Forward2
).count().pause().move(
    LeftFoot,
    MoveThenTurn(
        Forward2 + Rightward,
        Clockwise45
    )
).count().move(
    RightFoot,
    TurnThenMove(
        Clockwise180,
        Forward
    )
).count().move(
    RightFoot,
    Clockwise180
).move(
    LeftFoot,
    TurnThenMove(
        Clockwise(360 - 45),
        Leftward + Backward2
    )
).count().pause().finish()


PasealaEnFrente = BuildFigura("pasea-la en frente")\
    .startsIn(PosicionCerrada)\
    .withLeader(Cruzado_Left_Start)\
    .withFollower(LikeFollowerIn(CubanBasicStep))


# TODO: Is this the same as Aguajea? I feel like aguajea has much more dramatic movements and is not a Cuban basic step but more like she's doing feet of half-enchufla. ("el aguaje" means "the tide" or "the wave", so "aguajea" is perhaps a neologism that means "to go back and forth like the waves of the sea")

Exhibela = BuildFigura("exhibela")\
    .startsIn(PosicionCaida)\
    .withLeader(PatternSequence(
        Cruzado_Left_Start,
        Cruzado_Left_End
    ))\
    .withFollower(PatternSequence(
        WalkingVueltaDerecha_Follower_Start,
        WalkingVueltaDerecha_Follower_End
    ))



Sacala_Leader = PatternSequence(
    TimeReversed(Mirror(LikeLeaderIn(Guapea))),
    BuildPattern(
        FeetTogether
    ).move(
        LeftFoot,
        Forward
    ).count().move(
        RightFoot,
        InPlace
    ).count().move(
        LeftFoot,
        Backward
    ).count().pause().move(
        RightFoot,
        Backward
    ).count().move(
        LeftFoot,
        MoveThenTurn(
            Forward + Rightward,
            Clockwise90
        )
    ).count().move(
        RightFoot,
        MoveThenTurn(
            Forward,
            Clockwise90
        )
    ).count().pause().finish()
)



Sacala = BuildFigura("sacala")\
    .startsIn(PosicionAbajo)\
    .withLeader(Sacala_Leader)\
    .withFollower(LikeFollowerIn(Exhibela))


# TODO: I have no idea how the leader nor the follower move in a sacala setup.
# Sacachufla_Leader = BuildPattern(
#     FeetTogether
# )

# EnchuflaSequence = FiguraSequence(
#     "enchufla sequence",
#     Enchufla, DiLeQueNo
# )
# EnchuflaDobleSequence = FiguraSequence(
#     "enchufla doble sequence",
#     EnchuflaDoble, DiLeQueNo
# )
# ExhibelaSequence = FiguraSequence(
#     "exhibela sequence",
#     Enchufla, Exhibela, DiLeQueNo
# )
# SacalaSequence = FiguraSequence(
#   "sacala sequence",
#   Sacachufla, Sacala, DiLeQueNo
# )
