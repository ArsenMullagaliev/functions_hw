from collections.abc import Sequence
from typing import TypeVar, Callable

T = TypeVar('T')


class Seq():

    def __init__(self, sequence: Sequence[T]):
        self.contents = sequence

    def filter(self, func: Callable) -> 'Seq':
        filtered_seq = [x for x in self.contents if func(x)]
        return Seq(sequence=filtered_seq)

    def map(self, func: Callable) -> 'Seq':
        transformed_seq = [func(x) for x in self.contents]
        return Seq(sequence=transformed_seq)

    def take(self, length: int) -> list:
        slicer = slice(length)
        returned_seq = self.contents[slicer]
        return list(returned_seq)

    def __str__(self):
        return str(self.contents)


if __name__ == '__main__':
    numbers = [1, 2, 3, 4, 5]
    seq = Seq(numbers)
    res = seq.filter(lambda n: n % 2 == 0).map(lambda n: n + 10).take(3)
    assert res == [12, 14]
    print(res)
