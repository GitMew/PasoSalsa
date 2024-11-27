from pasosalsa.abstraction.movement import *


InPlace   = Move(0,0)
Forward   = Move(+1,0)
Backward  = Move(-1,0)
Leftward  = Move(0,-1)
Rightward = Move(0,+1)

Forward2   = Forward   + Forward
Backward2  = Backward  + Backward
Leftward2  = Leftward  + Leftward
Rightward2 = Rightward + Rightward

CounterClockwise90 = Turn(90)
CounterClockwise45 = Turn(45)
Clockwise90        = Turn(-90)
Clockwise45        = Turn(-45)
HalfTurn           = Turn(180)

LeaderFeetTogether = {
    Foot.LeaderLeft: FootPosition(0, 0, 90),
    Foot.LeaderRight: FootPosition(1, 0, 90)
}
