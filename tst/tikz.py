from pasosalsa.domain.instances.figuras import *
from pasosalsa.domain.instances.figuras import Cruzado_Left_Start, Loopable, Sacachufla
from pasosalsa.application.visualisers.general import WhichPerson
from pasosalsa.application.visualisers.tikz import TikzVisualiser


viz = TikzVisualiser(which=WhichPerson.BOTH)
print(viz.visualise(Guapea))
print()
print(viz.visualise(VueltaDerecha))
print()
print(viz.visualise(DiLeQueNo))
print()
print(viz.visualise(Enchufla))
print()
print(viz.visualise(Exhibela))
print()
print(viz.visualise(Sacachufla))
print()
print(viz.visualise(Aguajea))
print()
print(viz.visualise(HalfEnchufla))
print()
print(viz.visualise(Aguajea))
print()
print(viz.visualise(PalMedio))
print()
# print(viz.visualise(Cruzado_Left_Start))
# print()
# print(viz.visualise(Loopable(Cruzado_Left_Start)))
# print()
