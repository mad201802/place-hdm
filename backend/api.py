from map import PlaceMap, Colors
from exceptions import OutOfMapException
from fastapi import FastAPI
from fastapi.responses import Response

MAP_SIZE = 100
MAP_NAME = "map_v1"

app = FastAPI()
map = PlaceMap(f"{MAP_NAME}_{MAP_SIZE}", MAP_SIZE)

for i in range(MAP_SIZE):
    map.place_pixel(i, i, Colors.RED)

@app.get("/map")
def get_image():
    return Response(map.get_image_as_byte_array(), media_type="image/png")

@app.post("/place")
def place_pixel(x: int, y: int, color: str):
    if x < 0 or x >= MAP_SIZE or y < 0 or y >= MAP_SIZE:
        raise OutOfMapException(f"Position ({x+1},{y+1}) is outside the map")
    
    try:
        map.place_pixel(x, y, Colors[color])
    except:
        raise Exception()

    map.save_map()
    return Response(status_code=200)

@app.get("/colors")
def get_colors():
    return {i.name: i.value for i in Colors}