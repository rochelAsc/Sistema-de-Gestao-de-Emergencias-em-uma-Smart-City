from core.ambiente import Ambiente

class Bombeiro:
    def __init__(self, id_bombeiro, ambiente, quadrante, pos_inicial=(0, 0)):
        self.id = id_bombeiro
        self.ambiente = ambiente
        self.quadrante = quadrante

        self.x, self.y = pos_inicial

        self.destino = None
        self.ocupado = False

        self.passos = 0

    def disponivel(self):
        return not self.ocupado

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
