from ...abstracts.figuras import *
from ...abstracts.composition import *
from .posiciones import *

__all__ = ["Guapea", "VueltaDerecha", "VueltaDerechaCerranda", "VueltaDoble",
           "DiLeQueNo", "Enchufla", "HalfEnchufla", "EnchuflaDoble", "Exhibela", "Sacala",
           "PalMedio", "CubanBasicStep", "PasealaEnFrente", "Aguajea",
           "Setenta", "EnchuflaSequence", "EnchuflaDobleSequence", "ExhibelaSequence", "SacalaSequence"]


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



Guapea = BuildFigura("guapea")\
    .startsIn(PosicionAbierta)\
    .withLeader(Guapea_Leader)\
    .withFollower(Mirror(Guapea_Leader))



VueltaDerecha = BuildFigura("vuelta derecha")\
    .startsIn(PosicionAbierta)\
    .withLeader(
        BuildPattern(
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
    )\
    .withFollower(
        BuildPattern(
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
    )



# Version of a vuelta derecha where the leader moves in closer at the end.
VueltaDerechaCerranda_Leader = UntilCount(4, LikeLeaderIn(VueltaDerecha)).move(
    RightFoot,
    Forward
).count().move(
    LeftFoot,
    Forward
).count().move(
    RightFoot,
    InPlace  # FIXME: Hmmm I don't think this is right, but I need to check what I do myself.
).count().pause().finish()



VueltaDerechaCerranda = BuildFigura("vuelta derecha cerranda")\
    .startsIn(PosicionAbierta)\
    .withLeader(VueltaDerechaCerranda_Leader)\
    .withFollower(LikeFollowerIn(VueltaDerecha))



VueltaDoble = BuildFigura("vuelta doble")\
    .startsIn(PosicionAbierta)\
    .withLeader(Mirror(LikeFollowerIn(VueltaDerecha)))\
    .withFollower(LikeFollowerIn(VueltaDerecha))



# My di-le que no (DQN), and in fact the entire PasoSalsa package's rectangular grid interpretation of salsa, were
# inspired by the following 33-second video: https://www.youtube.com/watch?v=h8Xj1Kin9Qs
DiLeQueNo = BuildFigura("di-le que no")\
    .startsIn(PosicionCaida)\
    .withLeader(
        BuildPattern(
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
    )\
    .withFollower(
        BuildPattern(
            FeetTogether
        ).move(
            RightFoot,
            Backward
        ).count().move(
            LeftFoot,
            Forward
        ).count().move(
            LeftFoot,
            CounterClockwise90
        ).move(
            RightFoot,
            MoveThenTurn(
                Forward2 + Forward + Leftward,
                CounterClockwise90
            )
        ).count().pause().move(  # After this, the follower has to move forward 3 units and rotate 180°.
            LeftFoot,
            MoveThenTurn(
                Forward,  # It's more like 1.5 units.
                CounterClockwise90
            )
        ).count().move(
            RightFoot,
            MoveThenTurn(
                Forward2 + Forward + Leftward,  # In practice, followers only move Forward2 since they don't mind ending in FeetDiagonalRightForward (it has the same freedoms as FeetTogether when ending on a left foot movement).
                CounterClockwise180
            )
        ).count().move(
            LeftFoot,
            TurnThenMove(
                CounterClockwise90,
                Backward2 + Leftward  # It's again more like 1.5 units, so that the movement of the left foot, which always goes to baseline, is 1.5 + 1.5 instead of 2 + 1.
            )
        ).count().pause().finish()
    )



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
    Leftward2 + Forward
).count().move(
    LeftFoot,
    MoveThenTurn(
        Leftward + Forward2 + Forward2,  # 4 units is the most you can step. You start legs spread and you end legs spread.
        Clockwise180
    )
).move(
    RightFoot,
    Clockwise180
).count().pause().move(
    RightFoot,
    Rightward + Backward2 + Backward
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



Enchufla_Follower = BuildPattern(
    FeetTogether
).move(
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
        Leftward2 + Forward2 + Forward,
        CounterClockwise180
    )
).count().pause().move(
    LeftFoot,
    Backward2
).count().move(
    RightFoot,
    Leftward
).count().move(
    LeftFoot,
    Leftward + Forward
).count().pause().finish()



# My enchufla / enchufa-la / enchufa is mainly based on experience. I don't think I've actually seen it online the way
# I do it, but followers seem to like it. The gist is that the leader and follower both turn 180°, followed by
# the leader turning back 90° to create the posicion caida.
# I've been told that this is wrong because the leader should end at 180° and the follower at 90°. My version of the leader
# is taken from Salsificion's enchufla (https://www.youtube.com/watch?v=_XZRaU3_pD8), although there, the follower turns
# an extra 90° to end up next to the leader, and in the DQN that follows, the leader only turns 90°. One of my teachers
# told me that those two features are probably symptoms of casino.
# So, my enchufla and DQN stop and start in caida, and the leader turns 180° in my DQN.
Enchufla = BuildFigura("enchufla")\
    .startsIn(PosicionAbierta)\
    .withLeader(Enchufla_Leader)\
    .withFollower(Enchufla_Follower)



HalfEnchufla_Leader = BuildPattern(
    FeetTogether
).move(
    LeftFoot,
    Backward
).count().move(
    RightFoot,
    Forward + Leftward2
).count().move(
    LeftFoot,
    MoveThenTurn(
        Forward2,
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


HalfEnchufla_Follower = BuildPattern(
    FeetTogether
).move(
    RightFoot,
    Backward
).count().move(
    LeftFoot,
    Forward  # Could be in place, but I don't think that's right.
).count().move(
    RightFoot,
    MoveThenTurn(
        Forward2 + Leftward2,  # The leader also does this, so she can as well.
        CounterClockwise180
    )
).move(
    LeftFoot,
    CounterClockwise180
).count().pause().move(
    LeftFoot,
    Backward
).count().move(
    RightFoot,
    Leftward2 + Forward  # I actually have no idea if this is right, but if the leader can do it, the follower can too, no?
).count().move(
    RightFoot,
    Clockwise180
).move(
    LeftFoot,
    MoveThenTurn(
        Forward2,
        Clockwise180
    )
).count().pause().finish()


# This is my own formalisation on the half-enchufla. It may be wrong (especially with the large steps being taken), but
# the way it ended up is quite neat since the leader's 1-2-3 is the follower's 5-6-7 and vice versa.
HalfEnchufla = BuildFigura("half-enchufla")\
    .startsIn(PosicionAbierta)\
    .withLeader(HalfEnchufla_Leader)\
    .withFollower(HalfEnchufla_Follower)



EnchuflaDoble = FiguraSequence(
    "enchufla doble",
    HalfEnchufla, Enchufla
)



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


# In casino, "balancing step" is called "para el medio". https://salsaselfie.com/2020/12/28/cuban-salsa-para-el-medio
# The correct way to do it is apparently for 7 to end with feet APART, not feet together, which is counter-intuitive but makes sense from a weight shifting perspective.
#  - On the 7 of the previous bar, open right.
#  - On 1, let left join right.
#  - On 3, move left back.
#  - On 5, let right join left.
#  - On 7, move right back.
PalMedio_Leader = BuildPattern(FeetApartRight).move(
    LeftFoot,
    Rightward
).count().pause().move(
    LeftFoot,
    Leftward
).count().pause().move(
    RightFoot,
    Leftward
).count().pause().move(
    RightFoot,
    Rightward
).count().pause().finish()


PalMedio = BuildFigura("Pal medio")\
    .startsIn(PosicionCerrada)\
    .withLeader(PalMedio_Leader)\
    .withFollower(Mirror(PalMedio_Leader))

BalancingStep = PalMedio


CubanBasicStep = BuildFigura("Cuban basic step")\
    .startsIn(PosicionCerrada)\
    .withLeader(LeaderCubanBasicStep)\
    .withFollower(Mirror(LeaderCubanBasicStep))

CumbiaBasic = CubanBasicStep  # "Cuban basic step" is used at our school, Cumbia basic is used e.g. here: https://salsayo.com/move/Back-Rocks and also https://thedancedojo.com/how-to-salsa-dance-for-beginners/back-and-cumbia-salsa-basic-steps


# The following step is like Guapea, except
#   1. you "overstep" and your feet form a diagonal in resting position rather than being together, and
#   2. the men start forwards so that the distance between the partners is the same.
# This move has various names:
#   - Salsaficion calls it "pa' ti, pa' mi", but that name is already used for a turn for woman, turn for man, turn for woman.
#   - Our Cuban teacher calls it "salsa".
#   - Our Flemish teacher calls it "basic step".
#   - Salsayo calls it "mambo": https://salsayo.com/move/Basic-Steps and https://salsayo.com/move/Closed-Position-Basic-Steps
#   - Dance Papi calls it "son montuno": https://www.youtube.com/watch?v=Qv5BKoV72nA
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

SonMontuno_Leader_Start = MamboBasicStep_Leader_Start


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


# Also called "para abajo / pa'bajo" and also "adentro y afuera".
#   - The example video at https://salsayo.com/move/Para-Abajo shows the leader doing a lateral step (which also has
#     a hundred different names, e.g. "timba" according to my Cuban teacher) rather than a cruzado.
#   - Dance Papi uses "lleva-la pa'bajo", but note that their version looks more like aguajea below; in particular, the
#     follower is turning 180° every bar, and the leader is not doing a cruzado but instead steps forward twice,
#     which is confusing to followers since they will think it's a di-le que no.  https://www.youtube.com/watch?v=Qv5BKoV72nA
PasealaEnFrente = BuildFigura("pasea-la en frente")\
    .startsIn(PosicionCerrada)\
    .withLeader(Cruzado_Left_Start)\
    .withFollower(LikeFollowerIn(CubanBasicStep))


# Aguaje is a more dramatic version of paseala en frente where the follower does more than a Cuban basic step;
# she's really turning 180° every bar, moving from left-caida on 3 to right-caida on 7, which allows it to be chained with exhibela and dqn.
# Etymology: "el aguaje" means "the tide" or "the wave", so "aguajea" is perhaps a neologism that means "to go back and forth like the waves of the sea".
Aguajea_Follower = BuildPattern(FeetTogether).move(
    RightFoot,
    Backward
).count().move(
    LeftFoot,
    Rightward + Forward
).count().move(
    RightFoot,
    MoveThenTurn(
        Forward2 + Leftward,
        CounterClockwise180
    )
).move(
    LeftFoot,
    CounterClockwise180
).count().pause().move(
    LeftFoot,
    Backward
).count().move(
    RightFoot,
    Leftward + Forward
).count().move(
    LeftFoot,
    MoveThenTurn(
        Forward2 + Rightward,
        Clockwise180
    )
).move(
    RightFoot,
    Clockwise180
).count().pause().finish()



Aguajea = BuildFigura("aguajea")\
    .startsIn(PosicionCaida)\
    .withLeader(Cruzado_Left_Start)\
    .withFollower(Aguajea_Follower)


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


Sacachufla_Leader = UntilCount(
    5, LikeLeaderIn(Enchufla)
).move(
    LeftFoot,
    Rightward + Forward
).count().move(
    LeftFoot,
    CounterClockwise180
).move(
    RightFoot,
    MoveThenTurn(
        Forward2 + Leftward,
        CounterClockwise180
    )
).count().pause().finish()



Sacachufla = BuildFigura("enchufla for sacala")\
    .startsIn(PosicionAbierta)\
    .withLeader(Sacachufla_Leader)\
    .withFollower(LikeFollowerIn(Enchufla))


# Some popular figure sequences

EnchuflaSequence = FiguraSequence(
    "enchufla sequence",
    Enchufla, DiLeQueNo
)
EnchuflaDobleSequence = FiguraSequence(
    "enchufla doble sequence",
    EnchuflaDoble, DiLeQueNo
)
ExhibelaSequence = FiguraSequence(
    "exhibela sequence",
    Enchufla, Exhibela, DiLeQueNo
)
SacalaSequence = FiguraSequence(
  "sacala sequence",
  Sacachufla, Sacala, DiLeQueNo
)
Setenta = FiguraSequence(
    "setenta",
    VueltaDerecha, Enchufla, DiLeQueNo
)
