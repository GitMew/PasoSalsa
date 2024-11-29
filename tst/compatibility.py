from pasosalsa.instances.figuras import *
from pasosalsa.abstraction.sequence import areCompatible

print(areCompatible(Guapea, Enchufla))
print(areCompatible(Enchufla, Guapea))  # <-- Should be False if you take follower into account, else it's True.
print(areCompatible(Enchufla, DiLeQueNo))
print(areCompatible(Crusado, Guapea))
print(areCompatible(Guapea, Crusado))
print(areCompatible(Guapea, CrusadoToEnchufla))
print(areCompatible(Crusado, CrusadoToEnchufla))