import os
import pickle
from enum import Enum
from bitstring import BitArray
from PIL import Image
import numpy as np
import random
import timeit

FILE_ENDING = ".map"

class Colors(Enum):
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW = (255,255,0)
    MAGENTA = (255,0,255)
    CYAN = (0,255,255)
    ORANGE = (255,128,0)
    PURPLE = (128,0,255)
    BROWN = (128,64,0)
    LIGHT_GRAY = (192,192,192)
    DARK_GRAY = (128,128,128)
    LIGHT_RED = (255,128,128)
    LIGHT_GREEN = (128,255,128)
    LIGHT_BLUE = (128,128,255)

COLOR_MAP = {
    "0000": Colors.WHITE,
    "1111": Colors.BLACK,
    "0001": Colors.RED,
    "0010": Colors.GREEN,
    "0011": Colors.BLUE,
    "0100": Colors.YELLOW,
    "0101": Colors.MAGENTA,
    "0110": Colors.CYAN,
    "0111": Colors.ORANGE,
    "1000": Colors.PURPLE,
    "1001": Colors.BROWN,
    "1010": Colors.LIGHT_GRAY,
    "1011": Colors.DARK_GRAY,
    "1100": Colors.LIGHT_RED,
    "1101": Colors.LIGHT_GREEN,
    "1110": Colors.LIGHT_BLUE
}

# MAP BYTE: 11 Bit Map Size, 4 Bit for color, x and y is equal to the offset in relation to mapsize
class PlaceBitMap():
    def __init__(self, name: str, p_map_size: int=1000, n_map_bits: int = 11, n_color_bits: int=4):
        if p_map_size > 2**n_map_bits:
            raise ValueError("Map size is too big")
        self.name = name
        self.p_map_size = p_map_size
        self.n_map_bits = n_map_bits
        self.n_color_bits = n_color_bits
        self.map_bits = self.create_or_load_map()
    
    def create_or_load_map(self):
        if os.path.isfile(self.name + FILE_ENDING):
            return self.load_map()
        return self.create_map()

    def load_map(self):
        return pickle.load(open(self.name + FILE_ENDING, "rb"))

    def create_map(self):
        map_bit_part = BitArray(uint=self.p_map_size, length=self.n_map_bits)
        pixel_bit_part = BitArray(uint=0, length=self.p_map_size ** 2 * self.n_color_bits)
        full_map = map_bit_part + pixel_bit_part

        self.save_map(full_map)
        return full_map

    def get_map_size(self):
        return f"{len(self.map_bits) / 8e+6} MByte"

    def render(self):
        image = np.zeros(shape=(self.p_map_size,self.p_map_size, 3), dtype=np.uint8)
        pixel_map = self.map_bits[self.n_map_bits:].bin
        for row in range(0, self.p_map_size):
            row_offset = row * self.p_map_size * self.n_color_bits
            for col in range(0, self.p_map_size):
                offset = row_offset + col * self.n_color_bits
                color = np.array(COLOR_MAP[pixel_map[offset: offset + self.n_color_bits]].value)
                image[row][col] = color
        return np.array(image)

    def set_pixel(self, x: int, y: int, color: Colors):
        offset = self.n_map_bits + (y * self.p_map_size * self.n_color_bits) + (x * self.n_color_bits)
        self.map_bits.overwrite(f'0b{list(COLOR_MAP.keys())[list(COLOR_MAP.values()).index(color)]}', offset)

    def save_map_as_image(self):
        image = self.render()
        image = Image.fromarray(image, 'RGB')
        image.save(self.name + "_img.png")

    def save_map(self, object=None):
        if object:
            pickle.dump(object, open(self.name + FILE_ENDING, "wb"))
        else:
            pickle.dump(self.map_bits, open(self.name + FILE_ENDING, "wb"))

map = PlaceBitMap(name="test", p_map_size=2**12-1, n_map_bits=12, n_color_bits=4)
start_time = timeit.default_timer()
for i in range(0, map.p_map_size):
    for j in range(0, map.p_map_size):
        map.set_pixel(i, j, Colors.RED)
print(timeit.default_timer() - start_time)
map.save_map()
map.save_map_as_image()
print(map.get_map_size())