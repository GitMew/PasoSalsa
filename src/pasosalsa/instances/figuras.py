from pasosalsa.abstraction.figuras import *
from .movement import *


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
    Rightward + Rightward
).count().pause().move(
    Foot.LeaderRight,
    Forward + Rightward + Rightward
).count().move(
    Foot.LeaderLeft,
    Backward
).count().move(
    Foot.LeaderRight,
    Leftward + Leftward
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
        HalfTurn
    )
).move(
    Foot.LeaderRight,
    HalfTurn
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
