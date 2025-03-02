"""
server.py
---------
Script principal para ejecutar la simulación.
Simula el entorno y comunica con el cliente de unity por websockets.
"""
import asyncio
import time
from websockets.asyncio.server import serve
import json

from entorno import Entorno

async def handler(websocket):
    async for message in websocket:
        data = json.loads(message)
        # Default: 1 robot, 30x53 almacen 
        num_agents = int(data.get("num_agents", 1))
        width = int(data.get("width", 30))
        length = int(data.get("length", 53))
        obstaculos = data.get("obstacles", [])
        generar_txt = data.get("generate_txt", False)
        entorno = Entorno(num_agents, width, length, obstaculos=obstaculos)

        rutas = []
        for agent in entorno.agents:
            rutas.append(agent.ruta)
        response = {"rutas": rutas}

        await websocket.send(json.dumps(response))

        if generar_txt:
            # Crear un archivo de texto con las rutas
            # de la forma:
            # x1,x2,x3,x4
            # y1,y2,y3,y4
            for i, agent in enumerate(entorno.agents):
                with open(f"./rutas/rutas{i}.txt", "w") as f:
                    x = [x for x,y in agent.ruta]
                    y = [y for x,y in agent.ruta]
                    f.write(",".join(map(str, x)) + "\n")
                    f.write(",".join(map(str, y)) + "\n")

        for i in range(50):
            entorno.step()

async def main():
    # Esperar a que el cliente se conecte
    async with serve(handler, "localhost", 8765) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())