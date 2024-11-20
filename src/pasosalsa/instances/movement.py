from pasosalsa.abstraction.movement import *


InPlace   = Move(0,0)
Forward   = Move(+1,0)
Backward  = Move(-1,0)
Leftward  = Move(0,-1)
Rightward = Move(0,+1)

CounterClockwise90 = Turn(90)
Clockwise90        = Turn(-90)
HalfTurn           = Turn(180)

FeetTogether = {
    Foot.LeaderLeft: FootPosition(0, 0, 90),
    Foot.LeaderRight: FootPosition(1, 0, 90)
}
