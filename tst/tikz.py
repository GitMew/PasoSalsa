from pasosalsa.domain.instances.figuras import *
from pasosalsa.application.visualisers.general import WhichPerson
from pasosalsa.application.visualisers.tikz import TikzVisualiser


viz = TikzVisualiser(which=WhichPerson.LEADER)
print(viz.visualise(Guapea))
print()
print(viz.visualise(Crusado_Left))
print()
print(viz.visualise(DiLeQueNo_Leader))
print()
print(viz.visualise(Enchufla_Leader))
print()
print(viz.visualise(Exhibela))
print()
print(viz.visualise(Sacala))
print()
