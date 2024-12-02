from typing import List, TypeVar
import numpy.random as npr

from ...domain.abstracts.figuras import Figura
from ...domain.abstracts.composition import FiguraSequence
from ...domain.abstracts.simulation import areCompatibleFiguras

T = TypeVar("T")

class SequenceSampler:

    def __init__(self):
        self.rng = npr.default_rng(0)

    def _choose(self, options: List[T]) -> T:
        return self.rng.choice(options)

    def findContinuations(self, start: Figura, continuations: List[Figura]) -> List[Figura]:
        return [c for c in continuations if areCompatibleFiguras(start, c)]

    def create(self, minimal_counts: int, possible_figuras: List[Figura]) -> FiguraSequence:
        counts = 0
        figures = [self._choose(possible_figuras)]
        while counts < minimal_counts:
            figures.append(self._choose(self.findContinuations(figures[-1], possible_figuras)))
            counts += figures[-1].duration()
        return FiguraSequence(
            "generated sequence",
            *figures
        )
