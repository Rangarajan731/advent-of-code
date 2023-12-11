import os
import typing as t
from pathlib import Path

NUM_MAP = {
    "one": '1',
    "two": '2',
    "three": '3',
    "four": '4',
    "five": '5',
    "six": '6',
    "seven": '7',
    "eight": '8',
    "nine": '9'
}

class TextStack:
    def __init__(self):
        self.stack: t.List[str] = []
        self.max_length: int = 5
        self.check_length: int = 3
        self.length: int = 0

    def add(self, char: str) -> t.Union[int, None]:
        self.stack.append(char)
        self.length += 1 
        if self.length > self.max_length:
            _ = self.stack.pop(0)
        if self.length > 2:
            return self.check()
        return None

    def check(self) -> t.Union[int, None]: 
        num_str = "".join(self.stack)
        for i in range((self.length - self.check_length)+1): 
            if (val := NUM_MAP.get(num_str[i:])):
                #self.stack.clear()
                #self.length = 0
                return val
        else:
            return None 

    def clear(self):
        self.stack.clear()
        self.length = 0

def process_line(line: str):
    counter: int =  0
    first_digit = last_digit = ""
    stack = TextStack()
    char_digit: str = ""
    line = line.strip("\n")
    for char in line:
        if ord(char) >= 48 and ord(char) <=57:
            if counter == 0:
                first_digit = char
            last_digit = char
            stack.clear()
            counter += 1

        else:
            if (char := stack.add(char)):
                if counter == 0:
                    first_digit = char
                last_digit = char
                counter += 1
    if not (first_digit + last_digit):
        return 0
    return int(first_digit + last_digit)
if __name__ == "__main__":
    final_result: int = 0
    with Path(os.path.abspath(".")).parent.joinpath("input/day_1.txt").open() as f:
        for line in f:
            final_result += process_line(line=line)
        
    print(final_result)
