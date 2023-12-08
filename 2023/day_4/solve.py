#! /usr/bin/python

import os
import sys
from typing import List, Tuple


INPUT_FILE = os.path.join(os.path.dirname(__file__), "input.txt")


class Card:
    def __init__(self, number:int, winning_numbers:list, player_numbers:list) -> None:
        self.number = number
        self.winning_numbers = winning_numbers
        self.player_numbers = player_numbers

    def get_value(self) -> int:
        matches = 0
        for number in self.player_numbers:
            if number in self.winning_numbers:
                matches += 1
                
        if matches == 0:
            return 0

        return 2**(matches-1)

    @staticmethod
    def from_line(raw_line:str):
        left_right_split = raw_line.split("|")
        left_split = left_right_split[0].split(": ")
        card_number = int(left_split[0].split(" ")[-1])
        winning_numbers = [int(i) for i in left_split[1].split(" ") if i != '']
        player_numbers = [int(i) for i in left_right_split[1].split(" ") if i != '']

        return Card(card_number, winning_numbers, player_numbers)


def main() -> int:
    # read the input and strip the newline characters
    with open(INPUT_FILE, "r") as infile:
        cards = []
        for line in infile:
            line = line.replace("\n", "")
            cards.append(Card.from_line(line))
    
    total_value = 0
    for card in cards:
        total_value += card.get_value()
    
    print(f"Total Value: {total_value}")


    return 0


if __name__ == "__main__":
    sys.exit(main())