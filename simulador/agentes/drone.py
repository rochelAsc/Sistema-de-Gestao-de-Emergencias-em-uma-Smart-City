from core.ambiente import Ambiente
import random

class Drone:
    def __init__(self, id_drone, ambiente, bdi, x_inicial=0, y_inicial=0):
        self.id = id_drone
        self.ambiente = ambiente
        self.bdi = bdi

        self.x = x_inicial
        self.y = y_inicial

        # Métrica simples
        self.passos = 0

    def mover(self):
        direcoes = [
            (0, 1),     # baixo
            (0, -1),    # cima
            (1, 0),     # direita
            (-1, 0)     # esqueda
        ]

        dx, dy = random.choice(direcoes)

        novo_x = self.x + dx
        novo_y = self.y + dy

        if self.ambiente.dentro_limite(novo_x, novo_y):
            self.x = novo_x
            self.y = novo_y
            self.passos += 1

    def perceber(self):
        pos = (self.x, self.y)

        if self.ambiente.eh_fogo(self.x, self.y):
            self.bdi.receber_mensagem("fogo", pos)

        elif self.ambiente.eh_vitima(self.x, self.y):
            self.bdi.receber_mensagem("vitima", pos)

    def atualizar(self):
        self.mover()
        self.perceber()