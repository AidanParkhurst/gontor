"""
robot.py
---------
Representa un robot en el almacén.
"""

from mesa import Agent
from pathfinding import aestrella

class Robot(Agent):
    ruta = []
    tiene_paquete = False
    paquetes = 0

    def __init__(self, model):
        super().__init__(model)

    def step(self):
        # Si no hay ruta, generar una nueva
        if not self.ruta:
            destino = self.model.punto_entrega if self.tiene_paquete else self.model.punto_recogida
            self.ruta = aestrella(self.model, self.pos, destino)

        # Si la celda actual es la siguiente celda de la ruta, quitarla de la ruta 
        if self.pos == self.ruta[0]: self.ruta.pop(0)

        # Si hay robot en la celda destino, esperar según las reglas:
        if not self.model.grid.is_cell_empty(self.ruta[0]):
            pass # TODO: Implementar reglas de espera

        # Si no hay robot en la celda destino, moverse a la siguiente celda
        self.model.grid.move_agent(self, self.ruta.pop(0))

        # Si la celda actual es la celda destino, deja o recoge un paquete
        if self.pos == self.model.punto_recogida:
            self.tiene_paquete = True
            print("Recogiendo paquete")
        elif self.pos == self.model.punto_entrega:
            self.tiene_paquete = False
            self.paquetes += 1
            print("Dejando paquete:", self.paquetes)