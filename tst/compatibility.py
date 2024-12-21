from pasosalsa.domain.instances.salsa.figuras import *
from pasosalsa.domain.abstracts.sequence import areCompatible

print(areCompatible(Guapea, Enchufla))
print(areCompatible(Enchufla, Guapea))  # <-- Should be False if you take follower into account, else it's True.
print(areCompatible(Enchufla, DiLeQueNo))
print(areCompatible(Crusado, Guapea))
print(areCompatible(Guapea, Crusado))
print(areCompatible(Guapea, CrusadoToEnchufla))
print(areCompatible(Crusado, CrusadoToEnchufla))