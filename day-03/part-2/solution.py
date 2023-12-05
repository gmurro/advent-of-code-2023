from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
import re
from typing import List, Tuple
from functools import reduce


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

    def is_neighbor(self, other: Number) -> bool:
        """
        Checks if the given number is a neighbor of the current symbol based on x and y coordinates.
        """
        return (
            min(abs(self.x - other.x[0]), abs(self.x - other.x[1])) <= 1 and
            abs(self.y - other.y) <= 1 
        )


    def check_gear(self,  numbers: List[Number]) -> bool:
        """
        Checks if there are two neighboring elements in the matrix that are are part numbers.
        """
        neighbours = []
        for number in numbers:
            if self.is_neighbor(number):
                neighbours.append(number)
        if len(neighbours) == 2:
            self.gear_ratio = reduce(lambda x, y: x.value * y.value, neighbours)
            return True
        else:
            return False


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
    
    def set_part_number(self, matrix: List[List[Element]]) -> None:
        self.part_number = self.is_part_number(matrix=matrix)
    


class Engine:
    def __init__(self, schema: str):
        self.schema = schema
        self.matrix = self.__get_symbol_matrix()

    def __get_symbol_matrix(self) -> List[List[Element]]:
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
    
    def get_gears(self) -> List[Symbol]:
        part_numbers = self.get_part_numbers()
        gears = [
            symbol
            for line in self.matrix
            for symbol in line
            if symbol.value == "*" and symbol.check_gear(part_numbers)
        ]
        return gears


if __name__ == "__main__":
    file_path = "../input.txt"
    with open(file_path) as file:
        engine_schema = file.read()

    engine = Engine(engine_schema)
    gears = engine.get_gears()
    
    gears_ratio = [g.gear_ratio for g in gears]
    sum_gears_ration = sum(gears_ratio)
    
    
    print(f"Gears: {gears}")
    print(f"Sum: {sum_gears_ration}")
