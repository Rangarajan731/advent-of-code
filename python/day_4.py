import os
import re
from pathlib import Path


input_dict = {}
input_length: int = 0 

def create_input_dict(f):
    card_num = 1
    for line in f:
        nums =  line.strip().split(":")[-1]
        input_dict[card_num] = [set(re.split(pattern="\s+", string=i.strip())) for i in re.split(pattern="\s+\|\s+", string=nums)]
        card_num += 1
    return card_num - 1

def part2(start: int, end: int, memo):
    global input_dict, input_length
    
    #end of list
    if start > end:
        return 0
    # for dummy iteration when there is no new card generated
    if end == -1:
        return 0
    if memo.get((start, end)):
        return memo[(start, end)]
    winning_set, actual_set = input_dict[start]
    card_length = len(actual_set.intersection(winning_set))
    if card_length == 0:
        new_end = -1
    elif (start + card_length) > input_length:
        new_end = input_length
    else:
        new_end = start + card_length
    memo[(start, end)] = 1 + part2(start=start+1, end=new_end,memo=memo) + part2(start=start+1, end=end, memo=memo)  
    return memo[(start, end)]

def part1():
    p0 = 0
    for winning_set, actual_set in input_dict.values():
        length = len(actual_set.intersection(winning_set))
        p0 += 2**(length - 1) if (length > 0) else 0
    return  p0       
    
if __name__ == "__main__":
    with Path(os.path.abspath(".")).parent.joinpath("input/day_4.txt").open() as f:
        input_length = create_input_dict(f)
        print(f"Part 1: {part1()}")
        # memoization
        memo = {}
        print(f"Part 2: {part2(start=1, end=input_length, memo=memo)}")


        


