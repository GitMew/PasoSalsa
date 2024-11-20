from pasosalsa.abstraction.figuras import *
from .movement import *


Guapea = BuildFigura("guapea",
    FeetTogether
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



DiLeQueNo = BuildFigura("di-le que no",
    FeetTogether
).move(
    Foot.LeaderLeft,
    Forward
).count().move(
    Foot.LeaderRight,
    Rightward
).count().move(
    Foot.LeaderLeft,
    MoveThenTurn(
        Move(-2,+2),
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
        Move(+1,+2),
        CounterClockwise90
    )
).count().move(
    Foot.LeaderRight,
    MoveThenTurn(
        Move(+2,0),
        CounterClockwise90
    )
).count().pause().finish()
