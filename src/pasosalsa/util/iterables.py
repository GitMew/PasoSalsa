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


def drop(n: int, i: Iterable[T]) -> Iterable[T]:
    for thing in i:
        n -= 1
        if n >= 0:
            continue
        yield thing


def at(index: int, i: Iterable[T]) -> Optional[T]:
    assert index >= 0
    return first(drop(index, i))  # E.g.: if you want index 1, you drop 1 and take the first after that.
