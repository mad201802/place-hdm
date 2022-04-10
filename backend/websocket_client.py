import websockets
import asyncio
import json

connection = None

async def start_client():
    print("Starting websocket client")
    async with websockets.connect('ws://localhost:8765/tet') as websocket:
        map = await websocket.recv()
        print("Received map", map)

        while True:
            pixel_update = await websocket.recv()
            print(f"Received update: {pixel_update}")

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(start_client())
    pixels = input("Pixel pos:")
    connection.send()