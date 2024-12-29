from ..abstracts.movement import *


InPlace   = Move(0,0)  # Not the same as a None move! Stepping in-place is still stepping!
Forward   = Move(+1,0)
Backward  = Move(-1,0)
Leftward  = Move(0,-1)
Rightward = Move(0,+1)

Forward2   = Forward   + Forward
Backward2  = Backward  + Backward
Leftward2  = Leftward  + Leftward
Rightward2 = Rightward + Rightward

Forward3   = Forward2   + Forward
Backward3  = Backward2  + Backward
Leftward3  = Leftward2  + Leftward
Rightward3 = Rightward2 + Rightward

# 4 units is the most you can step. You start legs spread and you end legs spread.
Forward4   = Forward3   + Forward
Backward4  = Backward3  + Backward
Leftward4  = Leftward3  + Leftward
Rightward4 = Rightward3 + Rightward


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
