#! /usr/bin/python

import sys
import os
import re
from typing import List

INPUT_FILE = os.path.join(os.path.dirname(__file__), "input_1.txt")

# define the valid regex patterns to search for, and assign a numeric value to the pattern
patterns = {
    "0" : 0,
    "1" : 1,
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "zero" : 0,
    "one" : 1,
    "two" : 2,
    "three" : 3,
    "four" : 4,
    "five" : 5,
    "six" : 6,
    "seven" : 7,
    "eight" : 8,
    "nine" : 9
}


class PatternResult:
    """Represents a patternt that was found in a substring, the index it was found at, 
    and the numerical representation of that pattern.
    """
    def __init__(self, pattern_text:str, index:int, value:int) -> None:
        self.pattern_text = pattern_text
        self.index = index
        self.value = value
    

def pattern_matcher(patterns:dict, text:str) -> List[PatternResult]:
    """Creates a list of PatternResult objects that represent the patterns that were
    present in the text and the indices they were found at.

    Args:
        patterns (dict) : dictionary mapping of patterns to numerical representation to check for
        text (str): string to check for patterns

    Returns:
        tuple: List of PatternResult objects representing the found patterns in the text.
    """
    pattern_results = []
    
    for pattern in patterns:
        # check every pattern for all occurences in the text
        results = [m.start() for m in re.finditer(pattern, text)]
        
        # only take the first and last occurance index
        if len(results) > 1:
            pattern_results.append(PatternResult(pattern, results[0], patterns[pattern]))
            pattern_results.append(PatternResult(pattern, results[-1], patterns[pattern]))
        elif len(results) > 0:
            pattern_results.append(PatternResult(pattern, results[0], patterns[pattern]))        
    
    # return the sorted list of patterns and the incices they were found at
    return sorted(pattern_results, key = lambda x : x.index, reverse=False)
    

def main() -> int:
    with open(INPUT_FILE, "r") as infile:
        data_lines = infile.readlines()
    
    sum_total = 0
    
    # iterate through every line of text
    for line in data_lines:
        # find all patterns in the text
        found_patterns = pattern_matcher(patterns, line)
        
        # get the first and last pattern found in the text
        first_pattern, last_pattern = found_patterns[0], found_patterns[-1]
        
        # combine the two numerics into one two digit number
        value = first_pattern.value*10 + last_pattern.value
        
        # increment the total with this value
        sum_total += value
    
    print(f"Result: {sum_total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())