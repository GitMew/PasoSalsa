from pasosalsa.domain.instances.salsa.figuras import *
from pasosalsa.application.visualisers.general import WhichPerson
from pasosalsa.application.visualisers.tikz import TikzVisualiser


viz = TikzVisualiser(which=WhichPerson.BOTH_FROM_LEADER, rotate_everything_by=0,
                     loop_count_after=8, do_colour=True)
# print(viz.visualise(Guapea))
# print(viz.visualise(VueltaDerecha))
# print(viz.visualise(VueltaDoble))
print(viz.visualise(VueltaDerechaCerranda))
# print(viz.visualise(DiLeQueNo))
# print(viz.visualise(Enchufla))
# print(viz.visualise(HalfEnchufla))
# print(viz.visualise(Exhibela))
# print(viz.visualise(Sacala))
# print(viz.visualise(Sacachufla))
# print(viz.visualise(Aguajea))
# print(viz.visualise(PalMedio))
# print(viz.visualise(SacalaSequence))
# print(viz.visualise(Cruzado_Left_Start))
# print(viz.visualise(Loopable(Cruzado_Left_Start)))
# print(viz.visualise(PasealaEnFrente))
# print(viz.visualise(CubanBasicStep))