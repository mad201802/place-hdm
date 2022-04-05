from json import load
from PIL import Image
from enum import Enum
from exceptions import OutOfMapException
import io
import os

class Colors(Enum):
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"



class PlaceMap():
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.image = self.load_image()

    def load_image(self):
        if os.path.isfile(f"{self.name}.png"):
            return Image.open(f"{self.name}.png")
        return Image.new('RGB', (self.size, self.size), (255, 255, 255))

    def place_pixel(self, x: int, y: int, color: Colors):
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            raise OutOfMapException(f"Position ({x+1},{y+1}) is outside the map")
        self.image.putpixel((x, y),  self.__hex_to_rgb(color.value[0]) + (255,))

    def save_map(self):
        self.image.save(f"{self.name}.png")

    def get_image_as_byte_array(self):
        img_byte_arr = io.BytesIO()
        self.image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

    def __hex_to_rgb(self, hex: str) -> tuple:
        hex = hex.lstrip('#')
        if len(hex) < 6: hex += "0"*(6-len(hex))
        elif len(hex) > 6: hex = hex[0:6]
        rgb = tuple(int(hex[i:i+2], 16) for i in (0,2,4))
        return rgb