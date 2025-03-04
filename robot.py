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
    wait_counter = 0

    def __init__(self, model):
        super().__init__(model)

    def update_ruta(self):
        if not self.ruta:
            if self.pos == self.model.punto_recogida:
                self.tiene_paquete = True 
            elif self.pos == self.model.punto_entrega:
                self.tiene_paquete = False

            destino = self.model.punto_entrega if self.tiene_paquete else self.model.punto_recogida
            self.ruta = aestrella(self.model, self.pos, destino)
    
    def force_update_ruta(self,agente_para_evitar):
        destino = self.model.punto_entrega if self.tiene_paquete else self.model.punto_recogida
        self.ruta = aestrella(self.model, self.pos, destino,agente_para_evitar)

    def va_a_chocar(self, destino):
        for agent in self.model.agents:
            if agent != self and agent.ruta and (agent.ruta[0] == destino or agent.pos == destino):
                paquete_diff = (self.tiene_paquete != agent.tiene_paquete) and self.tiene_paquete
                x_diff = (self.pos[0] != agent.pos[0]) and self.pos[0] < agent.pos[0]

                if (paquete_diff or (not paquete_diff and x_diff) \
                    or (not paquete_diff and not x_diff and self.pos[1] < agent.pos[1])):
                    self.force_update_ruta(agent)
                    return False

                return True

        return False

    def step(self):
        # Si no hay ruta, generar una nueva
        self.update_ruta()

        # Si la celda actual es la siguiente celda de la ruta, quitarla de la ruta 
        if self.pos == self.ruta[0]: self.ruta.pop(0)

        # Si hara robot en la celda destino, esperar según las reglas:
        if self.va_a_chocar(self.ruta[0]):
            self.ruta.insert(0, self.pos)
            self.wait_counter += 1


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