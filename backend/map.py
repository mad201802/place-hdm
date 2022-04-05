from PIL import Image
from enum import Enum
from matplotlib import pyplot as plt

class Colors(Enum):
    RED = "#FF4500",


class PlaceMap():
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.image = Image.new('RGB', (size, size), (255, 255, 255))

    def save_map(self):
        self.image.save(f"{self.name}.png")