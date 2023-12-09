from dataclasses import dataclass
from typing import List
import re
from pathlib import Path
from copy import copy


@dataclass
class Card:
    id: int
    owned_numbers: List[int]
    winning_numbers: List[int]
    points: List[int]
    owned_winning_numbers: List[int]

    def __init__(self, line: str):
        pattern = r"^Card\s+(\d+):([\s*\d+\s*]+)\|([\s*\d+\s*]+)$"

        # Use re.match to search for the pattern in the line
        match = re.match(pattern, line)

        if match:
            self.id = int(match.group(1))
            self.owned_numbers = [int(n) for n in match.group(2).split()]
            self.winning_numbers = [int(n) for n in match.group(3).split()]
            self.points = self.__get_points()
            self.copies = []
            self.memory = []
        else:
            raise ValueError(
                "Line formatted in a wrong way. It should be like: 'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53'"
            )

    @property
    def owned_winning_numbers(self):
        return [n for n in self.owned_numbers if n in self.winning_numbers]

    def __get_points(self):
        if len(self.owned_winning_numbers) > 0:
            return 2 ** (len(self.owned_winning_numbers) - 1)
        else:
            return 0

    def set_copies(self, copies):
        self.copies = copies


def read_cards(input_path: str) -> List[Card]:
    cards = []
    with open(input_path) as file:
        for line in file:
            card = Card(line=line)
            cards.append(card)
    return cards


def not_efficient_process_copies(cards: List[Card]) -> List[Card]:
    """
    This method does the same of 'preprocess_copies' but it has an high computational complexity.
    With a long input, it is doesn't runs indefinetly
    """
    i = 0
    cards_dict = {card.id: card for card in cards}

    while i < len(cards):
        card = cards[i]
        print(f"Processing copies for card {card.id}...")
        for j in range(1, card.points + 1):
            # add subsequent copies
            copy_id = card.id + j
            if copy_id < len(cards_dict):
                cards.append(copy(cards_dict[copy_id]))
        i = i + 1
    return sorted([c.id for c in cards])


def process_copies(cards: List[Card]) -> List[int]:
    for i in range(len(cards)):
        # add subsequent copies
        cards[i].set_copies(
            [
                cards[i].id + j
                for j in range(1, len(cards[i].owned_winning_numbers) + 1)
                if i + j < len(cards)
            ]
        )

    # compute copied cards
    for i in range(len(cards) - 2, -1, -1):
        cards[i].memory = [
            c
            for card_copy in cards[i].copies
            for c in (card_copy, *cards[card_copy - 1].memory)
        ]

    # return original cards and copied
    return sorted(
        [c.id for c in cards] + [c for i in range(len(cards)) for c in cards[i].memory]
    )


if __name__ == "__main__":
    input_path = Path(__file__).parent.parent / "input.txt"
    cards = read_cards(input_path)
    print(f"Cards before copies: {[c.id for c in cards]}")
    copied_cards = process_copies(cards)
    total_cards = len(copied_cards)
    print(f"Cards with copies: {copied_cards}")
    print(f"Total cards: {total_cards}")
