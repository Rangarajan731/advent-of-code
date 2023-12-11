import os
import typing as t
from pathlib import Path


class GearSystem:

    def __init__(self, length: int) -> None:
        self.length = length
        self.data_length = 3
        self.data: t.List[t.List[str]] = []
        self.parsed  = 0
        self.scanned = 0
        self.gears = set()
        self.gear_dict = {}

    def add_gear(self, gear: t.List, num: int):
        if self.gear_dict.get(gear):
            self.gear_dict[gear].append(num)
            return
        self.gear_dict[gear] = [num]
    
    def num_check_cond(self, x: int, y: int):
        return (ord(self.data[y][x]) > 47 and ord(self.data[y][x]) <58)

    
    def pos_check(self, x: int, y: int):
        return (x >= 0 and x < self.length) and (y >= 0 and y < self.data_length)  


    def scan_surrounding(self, x: int, y: int) -> bool:

        arr = [0, 1, -1]
        for i in arr:
            for j in arr:
                if self.pos_check(x=(x-i), y=(y-j)) and not (self.num_check_cond(x=(x-i), y=(y-j)) or self.data[y-j][x-i] == "."):
                    if self.data[y-j][x-i] == "*":
                        self.gears.add(((x-i), (self.scanned - j)))
                    return True 

        return False
       
   
    def scan(self):
        row_num = 1
        row: str = self.data[row_num]
        gear_sum: int = 0
        num: int = 0
        is_part = False

        for i in range(self.length):
            if self.num_check_cond(x=i, y=row_num):
                num = (num * 10) + int(self.data[row_num][i])
                if self.scan_surrounding(x=i, y=row_num):
                    is_part = True
            else:
                if is_part:
                    gear_sum += num
                    for gear in self.gears:
                        self.add_gear(gear, num)
                num = 0
                is_part = False
                self.gears = set()
        if is_part:
            gear_sum += num
            for gear in self.gears:
                self.add_gear(gear, num)
        return gear_sum


    def parse(self,f):
        gear_sum: int = 0
        self.data.append(['.' for _ in range(self.length)])
        for row in f:
            if self.parsed < (self.data_length - 1):  
                self.data.append(list(row.strip()))
                self.parsed += 1
                continue
            gear_sum += self.scan()
            self.scanned += 1
            self.data.pop(0)
            self.data.append(list(row.strip()))
            self.parsed += 1
        print(self.scanned)
        while (self.parsed != self.scanned):
            gear_sum += self.scan()
            self.scanned += 1
            self.data.pop(0)
            self.data.append(["."for _ in range(self.length)])
        print(self.scanned)
        print(self.parsed)
        return gear_sum

if __name__ == "__main__":
        g = GearSystem(length=140)
        p1 = g.parse(f)
        p2 = 0
        print(g.gear_dict)
        for k,v in g.gear_dict.items():
                if len(v) == 2:
                    p2 += (v[0] * v[1]) 
        print(f"part 1: {p1}")
        print(f"part 2: {p2}")