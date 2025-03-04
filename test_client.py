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

        initial_positions = []
        for i in range(int(num_agents)):
            print(f"Agent {i+1}")
            x = input("Enter x coordinate of initial position (Empty for random): ")
            y = input("Enter y coordinate of initial position: ")
            if x.strip() == "": break
            initial_positions.append((int(x), int(y)))

        width = input("How wide do you want the warehouse? (Default 30) ")
        length = input("How long do you want the warehouse? (Default 53) ")

        obstacles = []
        add_obstacles = input("Do you want to add obstacles? (y/n) (Default n) ")
        if add_obstacles.lower().strip() == "y":
            by_corners = input("Do you want to add obstacles by corners? (y/n) (Default n) ")
            if by_corners.lower().strip() == "y":
                while True:
                    xs = []
                    ys = []
                    for i in range(4):
                        x = input(f"Enter x coordinate of corner {i}: ")
                        xs.append(int(x))
                        y = input(f"Enter y coordinate of corner {i}: ")
                        ys.append(int(y))
                    xs.sort()
                    ys.sort() 
                    for x in range(xs[0], xs[-1]+1):
                        for y in range(ys[0], ys[-1]+1):
                            obstacles.append((x, y))
                    add_more = input("Do you want to add more obstacles? (y/n) (Default n) ")
                    if add_more.lower().strip() != "y": break
            else:
                while True:
                    x = input("Enter x coordinate of obstacle (empty to finish): ")
                    if x.strip() == "": break
                    y = input("Enter y coordinate of obstacle: ")
                    obstacles.append((int(x), int(y)))

        generate_txt = input("Do you want to generate a txt file with the routes? (y/n) (Default n) ")

        data = {
            "num_agents": num_agents if num_agents.strip() != "" else 1,
            "initial_positions": initial_positions,
            "width": width if width.strip() != "" else 30,
            "length": length if length.strip() != "" else 53,
            "obstacles": obstacles if obstacles else [],
            "generate_txt": generate_txt.lower().strip() == "y"
            }
        await websocket.send(json.dumps(data))
        response = await websocket.recv()
        print(response)

async def robotario_client():
    # Los valores de los archivos son metros, pero hacemos el grid en centímetros 
    robotario_scale = 100
    robotario_width = 8 * robotario_scale
    robotario_length = 12 * robotario_scale
    # Los valores de los archivos usan el centro del robotario como origen, pero el grid usa la esquina inferior izquierda
    off_x = robotario_width // 2
    off_y = robotario_length // 2

    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # Initial Robot positions from file InitialPositions.txt
        initial_positions = []
        with open("./robotario/InitialPositions.txt", "r") as f:
            xs = f.readline().strip().split(",")
            ys = f.readline().strip().split(",")
            for x, y in zip(xs, ys):
                init_x = float(x) * robotario_scale + off_x
                init_y = float(y) * robotario_scale + off_y
                initial_positions.append((int(init_x), int(init_y)))
        
        num_obstacles = input("How many obstacles do you have? (Default 0) ")
        obstacles = []
        for i in range(int(num_obstacles)):
            corners = []
            # Obstacle positions from file Obstacle_(i+1).txt
            with open(f"./robotario/Obstacle_{i+1}.txt", "r") as f:
                xs = f.readline().strip().split(",")
                ys = f.readline().strip().split(",")
                for x, y in zip(xs, ys):
                    corners.append((float(x), float(y)))
            # TODO: Hay mejores formas de hacer esto (conectando las aristas externas?)
            xs = [x for x, y in corners]
            ys = [y for x, y in corners]
            xs.sort()
            ys.sort()
            for x in range(int(xs[0]*robotario_scale), int(xs[-1]*robotario_scale)+1):
                for y in range(int(ys[0]*robotario_scale), int(ys[-1]*robotario_scale)+1):
                    obstacles.append((x + off_x, y + off_y))

        # Target positions from file TargetPositions.txt
        target_positions = []
        with open("./robotario/TargetPositions.txt", "r") as f:
            xs = f.readline().strip().split(",")
            ys = f.readline().strip().split(",")
            for x, y in zip(xs, ys):
                target_x = float(x)*robotario_scale + off_x
                target_y = float(y)*robotario_scale + off_y
                target_positions.append((int(target_x), int(target_y)))

        data = {
            "width": robotario_width,
            "length": robotario_length,
            "num_agents": 2,
            "initial_positions": initial_positions,
            "target_positions": target_positions,
            "obstacles": obstacles,
            "generate_txt": True 
            }
        print(data)

        # TODO: Salida que acepta target_positions y initial_positions
        # await websocket.send(json.dumps(data))
        # response = await websocket.recv()
        # print(response)

if __name__ == "__main__":
    if input("Modo robotario? (y/n) (Default n) ").lower().strip() == "y":
        asyncio.run(robotario_client())
    else:
        asyncio.run(client())