from typing import TypeVar, Iterable, Optional


T = TypeVar("T")

def peek(s: Iterable[T]) -> T:
    for thing in s:
        return thing


def last(i: Iterable[T]) -> Optional[T]:
    result = None
    for thing in i:
        result = thing
    return result
