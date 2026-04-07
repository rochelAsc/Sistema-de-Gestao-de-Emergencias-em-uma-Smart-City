from core.ambiente import FOGO, VITIMA
import random

class Drone:
    def __init__(self, id_drone, ambiente, bdi, x_inicial=0, y_inicial=0):
        self.id = id_drone
        self.ambiente = ambiente
        self.bdi = bdi

        self.x = x_inicial
        self.y = y_inicial

        self.sentido = 1
        self.direcao = "direita"
        self.passos = 0

    def perceber(self):
        pos = (self.x, self.y)

        if self.ambiente.eh_fogo(self.x, self.y):
            print(f"[DRONE {self.id}] detectou FOGO em {pos}")
            self.bdi.receber_mensagem(FOGO, pos)

        elif self.ambiente.eh_vitima(self.x, self.y):
            print(f"[DRONE {self.id}] detectou VÍTIMA em {pos}")
            self.bdi.receber_mensagem(VITIMA, pos)

    def mover(self):
        t = self.ambiente.tamanho

        if self.direcao == "direita":
            if self.x < t - 1:
                self.x += 1
            else:
                self.y = (self.y + 1) % t
                self.direcao = "esquerda"

        elif self.direcao == "esquerda":
            if self.x > 0:
                self.x -= 1
            else:
                self.y = (self.y + 1) % t
                self.direcao = "direita"
        
        self.passos += 1

    def atualizar(self):
        self.perceber()
        self.mover()