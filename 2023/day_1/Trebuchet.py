#! /usr/bin/python

import sys
import os


INPUT_FILE = os.path.join(os.path.dirname(__file__), "input.txt")


def main() -> int:
    with open(INPUT_FILE, "r") as infile:
        data_lines = infile.readlines()
    
    sum_total = 0
    
    # iterate through every line of text
    for line in data_lines:
        first_numeric = None
        last_numeric = None
        
        # find the first numeric
        for char in line:
            if char.isnumeric():
                first_numeric = char
                break
        
        # find the last numeric
        for char in line[::-1]:
            if char.isnumeric():
                last_numeric = char
                break
        
        # combine the two numerics into one two digit number
        value = int(first_numeric)*10 + int(last_numeric)
        
        # increment the total with this value
        sum_total += value
    
    # final result
    print(sum_total)
    return 0


if __name__ == "__main__":
    sys.exit(main())