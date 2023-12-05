from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
import re
from typing import List, Tuple


@dataclass
class Element(ABC):
    """
    Represents an abstract element with a value and coordinates (x, y).

    Attributes:
        value (str): The value of the element.
        x (int): The x-coordinate of the element.
        y (int): The y-coordinate of the element.
    """

    value: str
    x: int
    y: int


class Symbol(Element):
    """
    Represents a symbol with a value and coordinates (x, y).
    """

    pass


class Period(Element):
    """
    Represents a period with a value and coordinates (x, y).
    """

    value: str = "."

    def __init__(self, x: int, y: int) -> None:
        super().__init__(self.value, x, y)


class Number(Element):
    """
    Represents a number with a value, x-axis coordinates, and y-coordinate.

    Attributes:
        value (int): The value of the number.
        x (Tuple[int, int]): The start and end coordinates of the x-axis.
        y (int): The y-coordinate of the number.
    """

    def __init__(self, value: int, x: Tuple[int, int], y: int) -> None:
        self.value = value
        self.x = x
        self.y = y

    def is_part_number(self, matrix: List[List[Element]]) -> bool:
        """
        Checks if the neighboring elements in the matrix are symbols.
        """
        rows, cols = len(matrix), len(matrix[0])

        for i in range(max(0, self.y - 1), min(rows, self.y + 2)):
            for j in range(max(0, self.x[0] - 1), min(cols, self.x[1] + 2)):
                if (self.x[0] <= j <= self.x[1]) and (self.y == i):
                    continue  # Skip the cells that are part of the number itself

                # Check if the neighboring element is a symbol
                if isinstance(matrix[i][j], Symbol):
                    return True
        return False


class Engine:
    def __init__(self, schema: str):
        self.schema = schema
        self.matrix = self.__get_symbol_matrix()

    def __get_symbol_matrix(self) -> List[Symbol]:
        matrix = [
            [
                Symbol(char, x, y) if re.match(r"[^\w\d\n.]", char) else Period(x, y)
                for x, char in enumerate(line)
            ]
            for y, line in enumerate(self.schema.splitlines())
        ]
        return matrix

    def get_part_numbers(self) -> List[Number]:
        numbers = [
            Number(int(match.group(0)), (match.start(0), match.end(0)-1), y)
            for y, line in enumerate(self.schema.splitlines())
            for match in re.finditer(r"(\d+)", line)
        ]
        return list(filter(lambda x: x.is_part_number(self.matrix), numbers))


if __name__ == "__main__":
    file_path = "../input.txt"
    with open(file_path) as file:
        engine_schema = file.read()

    engine = Engine(engine_schema)
    part_numbers = engine.get_part_numbers()
    
    part_numbers = [n.value for n in part_numbers]
    sum_part_numbers = sum(part_numbers)
    
    print(f"Part numbers: {part_numbers}")
    print(f"Sum part numbers: {sum_part_numbers}")
