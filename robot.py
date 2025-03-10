"""
robot.py
---------
Representa un robot en el almacén.
"""

from mesa import Agent
from pathfinding import aestrella
import random

class Robot(Agent):
    def __init__(self, model, id):
        super().__init__(model)

        self.id = id
        self.ruta = []
        self.tiene_paquete = False
        self.entregas = 0
        self.historia = []
        self.destinos = []

        # Si el robot empieza en el punto de recogida, recoge un paquete
        if self.pos == self.model.punto_recogida: self.actuar()

        self.elige_destino()


    def update_ruta(self):
        # Si no hay ruta, generar una nueva
        if not self.ruta:
            destino = self.destinos[-1]
            self.ruta = aestrella(self.model, self.pos, destino)
        else:   
            # Si hay ruta, y va a chocar con otro robot, espera o cambia de ruta
            if self.va_a_chocar(self.ruta[0]): self.ruta.insert(0, self.pos)
    
    def force_update_ruta(self,agentes_para_evitar):
        destino = self.destinos[-1]
        self.ruta = aestrella(self.model, self.pos, destino,agentes_para_evitar)

    def va_a_chocar(self, destino):
        agentes_para_evitar = []
        for agent in self.model.agents:
            if agent != self and (agent.pos == destino or (agent.ruta and agent.ruta[0] == destino)):
                agentes_para_evitar.append(agent)
        
        if agentes_para_evitar:
            agentes_no_atrapados = [agent for agent in agentes_para_evitar if not agent.atrapado]
            if not self.atrapado: agentes_no_atrapados.append(self)
            agente_ids = [agent.id for agent in agentes_no_atrapados]

            # Si este id es el menor y no está atrapado, va primero
            if self.id == min(agente_ids):
                self.force_update_ruta(agentes_para_evitar)
                return False

            # Por los demas, esperar
            return True

        # No va a chocar
        return False


    def step(self):
        self.historia.append(self.pos)
        # print("Ruta:", self.ruta)
        # print("Meta", self.destinos[-1])
        # Si la celda actual es la celda destino, deja o recoge un paquete
        if self.pos == self.destinos[-1]: self.actuar()

        # Si no hay ruta, generar una nueva
        self.update_ruta()

        # Si no hay ruta, el robot está atrapado
        if not self.ruta:
            print("Robot", self.id, "atrapado")
            self.atrapado = True
            return
 
        self.atrapado = False
        self.model.grid.move_agent(self, self.ruta.pop(0))

    
    def actuar(self):
        if self.tiene_paquete:
            self.tiene_paquete = False
            self.entregas += 1
        else:
            self.tiene_paquete = True

        self.elige_destino()
    
    def elige_destino(self):
        if self.tiene_paquete:
            self.destinos.append(random.choice(self.model.puntos_entregas))
        else:
            self.destinos.append(self.model.punto_recogida)