class Bombeiro:
    def __init__(self, id_bombeiro, ambiente, quadrante):
        self.id = id_bombeiro
        self.ambiente = ambiente
        self.quadrante = quadrante

        self.base = self.definir_base()

        self.x, self.y = self.base

        self.destino = None
        self.ocupado = False

        self.passos = 0

    def definir_base(self):
        t = self.ambiente.tamanho
        m = t // 2

        if self.quadrante == 1:
            return (m//2, m//2)
        elif self.quadrante == 2:
            return (m + m//2, m//2)
        elif self.quadrante == 3:
            return (m//2, m + m//2)
        else:
            return (m + m//2, m + m//2)

    def receber_ordem(self, pos):
        if self.destino != pos:
            print(f"[BOMBEIRO {self.id}] recebeu ordem para {pos}")
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
        # se não tem destino, espera ordem
        if not self.destino:
            return

        self.mover_passo()

        # Se chegou no destino
        if (self.x, self.y) == self.destino:
            if self.ambiente.eh_fogo(self.x, self.y):
                print(f"[BOMBEIRO {self.id}] apagou fogo em {(self.x, self.y)}")
                self.ambiente.resolver_incidente(self.x, self.y)
            # libera para nova ordem    
            self.destino = None
            self.ocupado = False