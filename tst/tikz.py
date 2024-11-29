from pasosalsa.domain.instances.figuras import *
from pasosalsa.application.visualisers.tikz import TikzVisualiser


p = TikzVisualiser()
print(p.visualise(Guapea))
print()
print(p.visualise(Crusado))
print()
print(p.visualise(DiLeQueNo))
print()
print(p.visualise(Enchufla))
print()
print(p.visualise(EnchuflaDoble))
print()
print(p.visualise(ExhibelaSequence))