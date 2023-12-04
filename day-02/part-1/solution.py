from dataclasses import dataclass
from typing import List
import re

@dataclass
class Bag:
    red: int
    blue: int
    green: int

@dataclass
class Set:
    red: int = 0
    blue: int = 0
    green: int = 0
    
    def is_possible(self, bag: Bag) -> bool:
        if self.red > bag.red or self.blue > bag.blue or self.green > bag.green: 
            return False
        else:
            return True

class Game:
    def __init__(self, id: int) -> None:
        self.id = id
        self.sets: List[Set] = []
        
    def add_set_game(self, set_game: Set):
        self.sets.append(set_game)
    
    def is_possible(self, bag: Bag) -> bool:
        return all([game_set.is_possible(bag) for game_set in self.sets])
    
    def __str__(self) -> str:
        sets_str = "; ".join(f"{s.red} red, {s.blue} blue, {s.green} green" for s in self.sets)
        return f"Game {self.id}: {sets_str}"
    
    def __repr__(self) -> str:
        return self.__str__()
    

def read_game(line: str) -> Game:
    try:
        id, game_str = re.findall(r'Game\s(\d+):\s(.*)', line)[0]
        game = Game(int(id))
        sets_game_str = game_str.split("; ")
        for set_game_str in sets_game_str:
            set_game = Set()
            cubes = re.findall(r'(\d+)\s(blue|red|green)',set_game_str)
            for quantity, color in cubes:
                setattr(set_game, color, int(quantity))
            game.add_set_game(set_game)
        return game
        
    except Exception as e:
        raise ValueError("Incorrect format of the game line") from e

def get_valid_games(file_path: str, bag: Bag) -> List[Game]:
    valid_games = []
    with open(file_path, 'r') as file:
        for line in file:
            game = read_game(line.strip())
            if game.is_possible(bag=bag):
                valid_games.append(game)
    return valid_games

if __name__ == "__main__":
    input_path = "../input.txt"
    bag = Bag(red=12, green=13, blue=14)
    valid_games = get_valid_games(input_path, bag)
    sum_ids = sum([game.id for game in valid_games])
    print(f"Valid games:\n{"\n".join([str(game) for game in valid_games])}")
    print(f"\nSum ids: {sum_ids}")
