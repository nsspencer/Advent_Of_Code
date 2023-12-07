#! /usr/bin/python

import os
import sys
from typing import List, Tuple
import re


INPUT_FILE = os.path.join(os.path.dirname(__file__), "input.txt")


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


def check_adjacency(schematic:List[str], line_no:int, number_start_idx:int, number_end_index:int) -> bool:
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
            if check_adjacency(schematic, line_index, start, stop) == True:
                part_numbers.append(int("".join(line[start:stop])))

    return part_numbers


def main() -> int:
    # read the input and strip the newline characters
    with open(INPUT_FILE, "r") as infile:
        schematic = []
        for line in infile:
            line = line.replace("\n", "")
            schematic.append(line)        

    part_numbers = parse_part_numbers(schematic)

    print(f"Part Number Sum: {sum(part_numbers)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())