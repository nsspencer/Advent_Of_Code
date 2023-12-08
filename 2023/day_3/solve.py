#! /usr/bin/python

import os
import sys
from typing import List, Tuple
import re


INPUT_FILE = os.path.join(os.path.dirname(__file__), "input.txt")


class PartNumber:
    def __init__(self, number:int, line_index:int, start:int, stop:int) -> None:
        self.number = number
        self.line_index = line_index
        self.start = start
        self.stop = stop

    def contains_point(self, line_index:int, index:int) -> bool:
        if line_index != self.line_index:
            return False
        if index >= self.start and index < self.stop:
            return True
        return False
    
    def __repr__(self) -> str:
        return str(self.number)

    def __add__(self, other):
        if isinstance(other, PartNumber):
            return PartNumber(self.number + other.number, None, None, None)
        else:
            raise TypeError("Unsupported operand type for +")

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, PartNumber):
            return PartNumber(self.number * other.number, None, None, None)
        elif isinstance(other, int):
            return PartNumber(self.number * other, None, None, None)
        else:
            raise TypeError("Unsupported operand type for *")


def generate_bounding_indices(row:int, start:int, stop:int) -> list:
    """Create a list of indices that create a bounding box around a string of characters.
    Only non-negative indices will be created. You are responsible for bounds checking.

    Args:
        row (int): row index to start bounding box generation on
        start (int): start index of the string
        stop (int): end index of the strin

    Returns:
        list: possible indices that bound the string.
    """

    indices = []
    for i in range(start-1, stop+1):
        indices.append((row-1, i))
        indices.append((row+1, i))
    
    indices.append((row, start-1))
    indices.append((row, stop))

    final_indices = []
    for row, index in indices:
        if row >= 0 and index >= 0:
            final_indices.append((row, index))
    
    return final_indices


def check_character_adjacency(schematic:List[str], line_no:int, number_start_idx:int, number_end_index:int) -> bool:
    """Get the surrounding indices of the part.

    Args:
        schematic (List[str]): entire schematic file.
        line_no (int): line number that denotes where the part can be found
        number_start_idx (int): start index of the part string
        number_end_index (int): end index of the part string

    Returns:
        bool: True if the part passes the adjacency requirement, false otherwise.
    """
    bounding_indices = generate_bounding_indices(line_no, number_start_idx, number_end_index)
    
    for row, index in bounding_indices:
        try:
            char = schematic[row][index]
        except IndexError:
            continue

        if not char.isnumeric() and char != ".":
            return True
        
    return False


def parse_part_numbers(schematic:List[str]) -> list:
    """From a schematic file, parse all possible part numbers.

    Args:
        schematic (List[str]): List of strings representing a schematic file.

    Returns:
        list: All possible part numbers.
    """
    part_numbers = []

    for line_index, line in enumerate(schematic):
        # Regular expression pattern to find contiguous numeric characters
        pattern = r'\d+'

        # Find all matches of the pattern in the text along with their indices
        match_indices = [(match.start(), match.end()) for match in re.finditer(pattern, line)]

        # get all the part numbers that pass the adjacency check
        for start, stop in match_indices:
            if check_character_adjacency(schematic, line_index, start, stop) == True:
                part_numbers.append(PartNumber(int("".join(line[start:stop])), line_index, start, stop))

    return part_numbers


def calculate_gear_ratio(schematic:List[str], part_numbers:List[PartNumber]) -> int:
    """Calculate gear ratio for the schematic and all the valid part numners in it.

    Args:
        schematic (List[str]): list of strings represeting the schematic.
        part_numbers (List[PartNumber]): parsed and validated part numbers.

    Returns:
        int: value representing the gear ratio of the schematic.
    """
    gear_ratio = 0
    for line_index, line in enumerate(schematic):
        # find all the gears
        gears = [match.start() for match in re.finditer(r"\*", line)]
        if len(gears) == 0:
            continue
        
        # get only the parts that exist on lines that can apply to this gear
        possible_parts = [p for p in part_numbers if p.line_index in [line_index-1, line_index, line_index+1]]

        # check the valid part numbers touching the gears
        for gear_index in gears:
            touching_part_numbers = set()
            bounding_box = generate_bounding_indices(line_index, gear_index, gear_index+1)
            for _line_number, _index in bounding_box:
                for part in possible_parts:
                    if part.contains_point(_line_number, _index):
                        touching_part_numbers.add(part)
            
            if len(touching_part_numbers) == 2:
                p1 = touching_part_numbers.pop()
                p2 = touching_part_numbers.pop()
                gear_ratio += p1 * p2
    
    return gear_ratio.number



def main() -> int:
    # read the input and strip the newline characters
    with open(INPUT_FILE, "r") as infile:
        schematic = []
        for line in infile:
            line = line.replace("\n", "")
            schematic.append(line)        

    part_numbers = parse_part_numbers(schematic)
    gear_ratio = calculate_gear_ratio(schematic, part_numbers)

    print(f"Part Number Sum: {sum(part_numbers)}")
    print(f"Gear Ratio: {gear_ratio}")
    return 0


if __name__ == "__main__":
    sys.exit(main())