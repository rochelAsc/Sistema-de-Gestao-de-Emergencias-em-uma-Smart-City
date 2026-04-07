from core.ambiente import Ambiente

class Bombeiro:
    def __init__(self, id_bombeiro, ambiente, quadrante):
        self.id = id_bombeiro
        self.ambiente = ambiente
        self.quadrante = quadrante

        self.x = 0
        self.y = 0

        self.destino = None
        self.ocupado = False

        self.passos = 0

    def receber_ordem(self, pos):
        self.destino = pos
        self.ocupado = True

    def mover_passo(self):
        if not self.destino:
            return
        
        dest_x, dest_y = self.destino

        if self.x < dest_x:
            self.x += 1
        elif self.x > dest_x:
            self.x -= 1
        elif self.y < dest_y:
            self.y += 1
        elif self.y > dest_y:
            self.y -= 1
        
        self.passos += 1

    def agir(self):
        if not self.destino:
            return

        # Se chegou no destino
        if (self.x, self.y) == self.destino:
            if self.ambiente.eh_fogo(self.x, self.y):
                self.ambiente.resolver_incidente(self.x, self.y)

            # libera o bombeiro
            self.destino = None
            self.ocupado = False

        else:
            self.mover_passo()