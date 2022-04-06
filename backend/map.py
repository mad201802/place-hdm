import os
import pickle
from enum import Enum
from bitstring import BitArray
from PIL import Image
import numpy as np

FILE_ENDING = ".map"

class ColorMap(Enum):
    WHITE = '0000'
    BLACK = '1111'

# MAP BYTE: 11 Bit Map Size, 4 Bit for color, x and y is equal to the offset in relation to mapsize
class PlaceBitMap():
    def __init__(self, name: str, p_map_size: int=100, n_map_bits: int = 11, n_color_bits: int=4):
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

        # self.save_map(full_map)
        return full_map

    def get_map_size(self):
        return f"{len(self.map_bits) / 8e+6} MByte"

    def render(self):
        image = []
        pixel_map = self.map_bits[self.n_map_bits:].bin
        for row in range(0, self.p_map_size):
            row_offset = row * self.p_map_size * self.n_color_bits
            current_line = []
            for col in range(0, self.p_map_size):
                column_offset = col * self.n_color_bits
                offset = row_offset + column_offset
                color = ColorMap(pixel_map[offset: offset + self.n_color_bits])
                if color is ColorMap.WHITE:
                    current_line.append(0)
                else:
                    current_line.append(255)
            image.append(current_line)
        return np.array(image)

    def set_pixel(self, x: int, y: int, color: ColorMap):
        offset = self.n_map_bits + (y * (self.p_map_size - self.n_color_bits)) + (x * self.n_color_bits)
        print(offset)
        self.map_bits.overwrite(f'0b{color.value}', offset)

    def save_map(self, object=None):
        if object:
            pickle.dump(object, open(self.name + FILE_ENDING, "wb"))
        else:
            pickle.dump(self.map_bits, open(self.name + FILE_ENDING, "wb"))

map = PlaceBitMap(name="test")
map.set_pixel(0, 0, ColorMap.BLACK)
map.set_pixel(1, 1, ColorMap.BLACK)
map.set_pixel(2, 2, ColorMap.BLACK)

img_array = map.render()
print(img_array.shape)
img = Image.fromarray(img_array, 'L')
img.save("img.png")