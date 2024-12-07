from pasosalsa.domain.instances.figuras import *
from pasosalsa.application.visualisers.general import WhichPerson
from pasosalsa.application.visualisers.tikz import TikzVisualiser


viz = TikzVisualiser(which=WhichPerson.BOTH)
# print(viz.visualise(Guapea))
# print()
# print(viz.visualise(VueltaDerecha))
# print()
# print(viz.visualise(Cruzado_Left_Start))
# print()
# print(viz.visualise(DiLeQueNo))
# print()
# print(viz.visualise(Enchufla_Leader))
# print()
# print(viz.visualise(Loopable(Cruzado_Left_Start)))
# print(viz.visualise(Exhibela))
# print()
# print(viz.visualise(Sacala))
# print()
# print(viz.visualise(Aguajea))
print(viz.visualise(HalfEnchufla))