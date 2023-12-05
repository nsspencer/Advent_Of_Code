#! /usr/bin/python

import sys
import os
from typing import List, Dict


INPUT_FILE = os.path.join(os.path.dirname(__file__), "input.txt")


class Game:
    def __init__(self, id:int, cubes_pairs:List[Dict]) -> None:
        self.id = id
        self.cubes_pairs = cubes_pairs
        
    def check_possibility(self, possbilities_map:dict) -> bool:
        """Determines if the game would be playable with the provided possible number of cubes and their
        respective counts.

        Args:
            possbilities_map (dict): dictionary of cube colors and counts.

        Returns:
            bool: True if the game was possible, false otherwise.
        """
        for key in possbilities_map:
            possible_cubes = possbilities_map[key]
            
            for pair in self.cubes_pairs:
                picked_cubes = pair.get(key, None)
                if picked_cubes == None:
                    continue
                
                if possible_cubes < picked_cubes:
                    return False
                
        return True
    
    def get_power(self) -> int:
        """Calculate the power (sum of maximum cube value of each color).

        Returns:
            int: Power of this game.
        """
        # get all the counts of the different colored cubes across the pairs
        cube_values = {} # list of dicts
        for pair in self.cubes_pairs:
            for key in pair:
                if cube_values.get(key, None) == None:
                    cube_values[key] = [pair[key]]
                else:
                    cube_values[key].append(pair[key])
        
        # get minimum required cubes for the game
        minimum_required_cubes = {}
        for key in cube_values:
            minimum_required_cubes[key] = max(cube_values[key])
        
        # compute power
        power = 1
        for key in minimum_required_cubes:
            power *= minimum_required_cubes[key]
            
        return power
            
def create_game(text:str) -> Game:
    """Given a line of text, create a Game object and return it.

    Args:
        text (str): Line of input text representing a Game.

    Returns:
        Game: Game object with an ID and the pairs of cubes selected.
    """
    splits = text.split(":")
    game_id = int(splits[0].split(" ")[1])
    raw_pairs = splits[1]
    raw_pairs = raw_pairs.lstrip(" ").replace("\n"," ")
    
    cube_pairs = []
    for pair in raw_pairs.split(";"):
        pair = pair.lstrip(" ").rstrip(" ")
        pair_split = pair.split(", ")
        cube_pairing = {}
        for count_color in pair_split:
            count, color = count_color.split(" ")
            cube_pairing[color] = int(count)
        cube_pairs.append(cube_pairing)

    return Game(game_id, cube_pairs)
    

def main() -> int:
    with open(INPUT_FILE, "r") as infile:
        game_lines = infile.readlines()
        
    games = []
    for line in game_lines:
        games.append(create_game(line))
    
    # 12 red cubes, 13 green cubes, and 14 blue cubes
    required_cubes = {"red" : 12, "green" : 13, "blue" : 14}
    
    total_power = 0
    possible_games = []
    for game in games:
        total_power += game.get_power()
        if game.check_possibility(required_cubes) == True:
            possible_games.append(game.id)
    
    print(f"Possible Games: {sum(possible_games)}")
    print(f"Total Power: {total_power}")
    return 0


if __name__ == "__main__":
    sys.exit(main())