"""
test_client.py
---------
Cliente de prueba para el servidor de simulación.
Conecta al servidor por websockets y recibe mensajes.
"""

import asyncio
import websockets
import json

async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        num_agents = input("How many agents do you want? (Default 1) ")
        width = input("How wide do you want the warehouse? (Default 30) ")
        length = input("How long do you want the warehouse? (Default 53) ")
        obstacles = []
        add_obstacles = input("Do you want to add obstacles? (y/n) (Default n) ")
        if add_obstacles.lower().strip() == "y":
            while True:
                x = input("Enter x coordinate of obstacle (empty to finish): ")
                if x.strip() == "": break
                y = input("Enter y coordinate of obstacle: ")
                obstacles.append((int(x), int(y)))
        data = {
            "num_agents": num_agents if num_agents.strip() != "" else 1,
            "width": width if width.strip() != "" else 30,
            "length": length if length.strip() != "" else 53,
            "obstacles": obstacles if obstacles else []
            }
        await websocket.send(json.dumps(data))
        response = await websocket.recv()
        print(response)

if __name__ == "__main__":
    asyncio.run(client())