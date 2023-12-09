from dataclasses import dataclass
from typing import List
import re
from pathlib import Path


@dataclass
class Card:
    id: int
    owned_numbers: List[int]
    winning_numbers: List[int]

    def __init__(self, line: str):
        pattern = r"^Card\s+(\d+):([\s*\d+\s*]+)\|([\s*\d+\s*]+)$"

        # Use re.match to search for the pattern in the line
        match = re.match(pattern, line)

        if match:
            self.card_id = int(match.group(1))
            self.owned_numbers = [int(n) for n in match.group(2).split()]
            self.winning_numbers = [int(n) for n in match.group(3).split()]
        else:
            raise ValueError(
                "Line formatted in a wrong way. It should be like: 'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53'"
            )

    @property
    def owned_winning_numbers(self):
        return [n for n in self.owned_numbers if n in self.winning_numbers]

    @property
    def points(self):
        if len(self.owned_winning_numbers) > 0:
            return 2 ** (len(self.owned_winning_numbers) - 1)
        else:
            return 0


def read_cards(input_path: str) -> List[Card]:
    cards = []
    with open(input_path) as file:
        for line in file:
            card = Card(line=line)
            cards.append(card)
    return cards


if __name__ == "__main__":
    input_path = Path(__file__).parent.parent / "input.txt"
    cards = read_cards(input_path)
    points = [c.points for c in cards]
    sum_points = sum(points)
    print(f"Card points: {points}")
    print(f"Sum: {sum_points}")
