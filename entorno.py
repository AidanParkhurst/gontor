"""
entorno.py
---------
Simulación de una almácen con robots que recogen y entregan paquetes.
Aceptar un número de robots, ancho y alto del almacén, y opcionalmente
un punto de recogida y entrega.
"""

from mesa import Model
from mesa.space import SingleGrid

from robot import Robot

class Entorno(Model):
    punto_recogida = (0, 0)
    punto_entrega = (0, 0)
    
    def __init__(self, n, width, height, punto_recogida = (0,0), punto_entrega = None, seed = None):
        super().__init__(seed=seed)

        self.punto_recogida = punto_recogida
        self.punto_entrega = punto_entrega if punto_entrega else (width-1, height-1)

        self.num_agents = n
        self.grid = SingleGrid(width, height, torus=False)
        self.running = True

        for i in range(self.num_agents):
            a = Robot(self)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            while not self.grid.is_cell_empty((x, y)):
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height) 

            self.grid.place_agent(a, (x, y))

    def step(self):
        self.agents.shuffle_do("step")
        self.print_state()

    def print_state(self):
        print("Entorno:")
        for i in range(self.grid.width):
            for j in range(self.grid.height):
                if (i,j) == self.punto_recogida:
                    print("I", end="")
                elif (i,j) == self.punto_entrega:
                    print("M", end="")
                elif self.grid.is_cell_empty((i, j)):
                    print("-", end="")
                else:
                    if self.grid.get_cell_list_contents((i, j))[0].tiene_paquete:
                        print("P", end="")
                    else:
                        print("R", end="")
            print()