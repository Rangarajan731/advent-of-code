import os
import typing as t
from pathlib import Path


class GameParser:

    def __init__(self, red: int, green: int, blue: int):
        self.actual_red = red
        self.actual_green = green
        self.actual_blue = blue
        self._max_blue = self._max_green = self._max_red = 0
        self.boolean = True

    def _upd_max_red(self, count: int) -> int:
        if self._max_red < count:
            self._max_red = count
        return count
        
    def _upd_max_green(self, count: int) -> int:
        if self._max_green < count:
            self._max_green = count
        return count

    def _upd_max_blue(self, count: int) -> int:
        if self._max_blue < count:
            self._max_blue = count
        return count

    def get_game_id(self):
        #moving pointer to game ID
        start: int = 5
        self.pointer = start
        while True:
            if self.text[self.pointer] == ":":
                game_id = int(self.text[start: self.pointer])
                break
            self.pointer += 1
        self.pointer += 2 
        return game_id

    def get_set_detail(self):
        temp: int = self.pointer
        for char in self.text[self.pointer:]:
            if char == ";":
                self.get_cube_detail(start=self.pointer, end=temp)
                    #return False
                self.pointer = temp + 2 #adapting for empty spaces
            temp += 1
        self.get_cube_detail(start=self.pointer, end=self.length)
            #return False
        return True

    def get_color_and_count(self, start: int, end: str) -> t.Tuple[int, str]:
        temp: int = start
        count: int = 0
        color: str = ""
        while (temp < end):
            if self.text[temp] == " ":
                count = int(self.text[start: temp])
                color = self.text[(temp + 1): end]
                break
            temp += 1  
        return count, color

    def _cube_cond_check(self, start: int, end: int):
        count, color = self.get_color_and_count(start=start, end=end)
        red_cond = (color == "red") and (self._upd_max_red(count) > self.actual_red)
        blue_cond = (color == "blue") and (self._upd_max_blue(count) > self.actual_blue)
        green_cond = (color == "green") and (self._upd_max_green(count) > self.actual_green)
        if red_cond or green_cond or blue_cond:
            return False
        return True   
    
    def get_cube_detail(self, start: int, end: int) -> bool:
        i: int = start
        while (i<end):
            if self.text[i] == ",":
                if self._cube_cond_check(start=start, end=i) :
                    self.boolean = False 
                    #return False
                start = i+2
                i = start
                continue
            i += 1
        if self._cube_cond_check(start=start, end=end):
            self.boolean = False

    def get_pow_of_cube(self) -> int:
        resp = self._max_red * self._max_green * self._max_blue
        self._max_red =  self._max_green = self._max_blue = 0
        return resp

        
    def parse(self, text) -> int:
        self.text = text
        self.pointer = 0
        self.length = len(self.text)
        game_id = self.get_game_id()
        self.get_set_detail()
        if not self.boolean:
            return 0,self.get_pow_of_cube()
        return game_id, self.get_pow_of_cube()


if __name__ == "__main__":

    with Path(os.path.abspath(".")).parent.joinpath("input/day_2.txt").open() as f:
        final_result: int = 0
        final_pov_of_set: int = 0 
        parser = GameParser(red=12, green=13, blue=14)
        for line in f:
            line = line.strip("\n")
            i, j = parser.parse(text=line)
            final_result += i
            final_pov_of_set += j
        print(final_result)
        print(final_pov_of_set)
            
