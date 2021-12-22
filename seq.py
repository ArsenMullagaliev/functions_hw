from collections.abc import Sequence
from typing import TypeVar, Callable

T = TypeVar('T')


class Seq():

    def __init__(
            self,
            sequence: Sequence[T],
            funcs: list[(Callable, str)] = [(lambda x: x, 'map')]
    ):
        self._contents = sequence
        self._current_position = -1
        self._sequence_length = len(self._contents)
        self._functions = funcs

    def filter(self, func: Callable) -> 'Seq':
        extended_functions = self._functions + [(func, 'filter')]
        return Seq(sequence=self._contents, funcs=extended_functions)

    def map(self, func: Callable) -> 'Seq':
        extended_functions = self._functions + [(func, 'map')]
        return Seq(sequence=self._contents, funcs=extended_functions)

    def take(self, length: int) -> list:
        returned_seq = []
        for element in range(length):
            try:
                returned_seq.append(self.__next__())
            except StopIteration:
                continue
        return returned_seq

    def __iter__(self):
        return self

    def __next__(self):
        self._current_position += 1
        if self._current_position >= self._sequence_length:
            raise StopIteration
        else:
            current_element = self._contents[self._current_position]
            for func, type in self._functions:
                if type == 'map':
                    current_element = func(current_element)
                if type == 'filter' and func(current_element):
                    current_element = current_element
                if type == 'filter' and not func(current_element):
                    return self.__next__()
            return current_element


if __name__ == '__main__':
    numbers = [1, 2, 3, 4, 5]
    seq = Seq(numbers)
    res = seq.take(3)
    res = seq.filter(lambda n: n % 2 == 0).take(3)
    res = seq.map(lambda n: n + 10).take(3)
    res = seq.filter(lambda n: n % 2 == 0).map(lambda n: n + 10).take(3)
    assert res == [12, 14]
    print(res)
