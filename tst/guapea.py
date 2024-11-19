from pasosalsa.figures import *


Guapea = Figura(name="guapea", base={
    Foot.LeaderLeft: StartingPosition(0, 0, 0),
    Foot.LeaderRight: StartingPosition(1, 0, 0)
}).move(
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
).count().pause()
