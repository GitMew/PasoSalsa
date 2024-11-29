from pasosalsa.domain.instances.figuras import *
from pasosalsa.application.visualisers.ascii import PositionOnlyAsciiVisualiser


p = PositionOnlyAsciiVisualiser()
print(p.visualise(Guapea))
print()
print(p.visualise(Crusado))
print()
print(p.visualise(DiLeQueNo))
