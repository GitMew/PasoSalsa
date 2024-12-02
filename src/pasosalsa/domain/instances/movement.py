from ..abstracts.movement import *
from ..abstracts.patterns import StartingPose


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


FeetTogether = StartingPose(InPlace,InPlace)
LegsCrossedRightOverLeft = StartingPose(left=Backward + Rightward2, right=InPlace)
LegsCrossedLeftOverRight = StartingPose(left=InPlace, right=Backward + Leftward2)
