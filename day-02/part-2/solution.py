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
        self.power: int = None
        
    def add_set_game(self, set_game: Set):
        self.sets.append(set_game)
    
    def is_possible(self, bag: Bag) -> bool:
        return all([game_set.is_possible(bag) for game_set in self.sets])
    
    def minimum_bag(self) -> Bag:
        red = max([set_game.red for set_game in self.sets])
        blue = max([set_game.blue for set_game in self.sets])
        green = max([set_game.green for set_game in self.sets])
        return Bag(red=red, blue=blue, green=green)
    
    def compute_power(self) -> int:
        bag = self.minimum_bag()
        self.power = bag.red * bag.blue * bag.green
    
    def __str__(self) -> str:
        sets_str = "; ".join(f"{s.red} red, {s.blue} blue, {s.green} green" for s in self.sets)
        return f"Game {self.id}: {sets_str}" + f" [Power: {self.power}]" if self.power else ""
    
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

def get_games(file_path: str) -> List[Game]:
    games = []
    with open(file_path, 'r') as file:
        for line in file:
            game = read_game(line.strip())
            game.compute_power()
            games.append(game)
    return games

def compute_power_power_games(games: List[Game]) -> None:
    [game.compute_power() for game in games]
        

if __name__ == "__main__":
    input_path = "../input.txt"
    games = get_games(input_path)
    sum_power = sum([game.power for game in games])
    print(f"Power games:\n{"\n".join([str(game) for game in games])}")
    print(f"\nSum powers: {sum_power}")
