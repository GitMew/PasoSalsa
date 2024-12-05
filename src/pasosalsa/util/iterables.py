from typing import TypeVar, Iterable, Optional


T = TypeVar("T")

def peek(s: Iterable[T]) -> T:
    for thing in s:
        return thing


def first(i: Iterable[T]) -> Optional[T]:
    result = None
    for thing in i:
        result = thing
        break
    return result


def last(i: Iterable[T]) -> Optional[T]:
    result = None
    for thing in i:
        result = thing
    return result
