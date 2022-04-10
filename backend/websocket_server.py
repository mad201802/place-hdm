from map import PlaceBitMap
import websockets
import asyncio
import json

MAP_SIZE = 100
MAP_NAME = "map_v1"

connected = set()

map = PlaceBitMap(f"{MAP_NAME}_{MAP_SIZE}", MAP_SIZE)


async def broadcast(message):
    for ws in connected:
        if ws.open:
            await ws.send(message)
        else:
            connected.remove(ws)

async def on_message(message, ws):
    cmd = json.loads(message)
    if cmd["type"] == "set_pixel":
        await broadcast("pixel set")

async def handler(ws, path):

    # first connection (send map)
    connected.add(ws)
    await ws.send(map.get_map_bytes())

    async for message in ws:
        # message handler (json)
        print(message, path)
        await on_message(message, ws)

    connected.remove(ws)
    # client disconnected
    

async def start_server():
    async with websockets.serve(handler, 'localhost', 8765):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(start_server())
