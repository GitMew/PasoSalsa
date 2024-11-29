from ..abstracts.movement import *


InPlace   = Move(0,0)
Forward   = Move(+1,0)
Backward  = Move(-1,0)
Leftward  = Move(0,-1)
Rightward = Move(0,+1)

Forward2   = Forward   + Forward
Backward2  = Backward  + Backward
Leftward2  = Leftward  + Leftward
Rightward2 = Rightward + Rightward

CounterClockwise45  = Turn(45)
CounterClockwise90  = Turn(90)
CounterClockwise180 = Turn(180)
Clockwise45         = Turn(-45)
Clockwise90         = Turn(-90)
Clockwise180        = Turn(-180)

def Clockwise(degrees: int) -> Turn:
    return Turn(-degrees)

def CounterClockwise(degrees: int) -> Turn:
    return Turn(+degrees)


# TODO: All these starting positions are very inelegant to define.
#   - You don't want to copy "feet together" for both leader and follower.
#   - What if the follower starts turned 90°? Ideally you can define the follower's starting position on a coarse grid w.r.t. the leader.
#   - You can't really define the follower's absolute coordinates if you don't know where the leader will be.
#       - You really want something like "LeaderFeetTogether, FollowerInFront" but you can't define this in absolute terms obviously.

LeaderFeetTogether = {
    Foot.LeaderLeft:  FootPosition(x=0, y=0, rotation=90),
    Foot.LeaderRight: FootPosition(x=1, y=0, rotation=90)
}
LeaderLegsCrossedRightOverLeft = {
    Foot.LeaderLeft:  FootPosition(x=0,  y=0, rotation=90),
    Foot.LeaderRight: FootPosition(x=-1, y=1, rotation=90)
}
LeaderLegsCrossedLeftOverRight = {
    Foot.LeaderLeft:  FootPosition(x=0,  y=0,  rotation=90),
    Foot.LeaderRight: FootPosition(x=-1, y=-1, rotation=90)
}

FollowerFeetTogether = {
    Foot.FollowerLeft:  FootPosition(x=1, y=3, rotation=-90),
    Foot.FollowerRight: FootPosition(x=0, y=3, rotation=-90)
}
