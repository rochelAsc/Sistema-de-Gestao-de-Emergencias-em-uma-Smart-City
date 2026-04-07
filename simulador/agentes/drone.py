from core.ambiente import Ambiente

class Drone:
    def __init__(self, id_drone, ambiente, bdi, quadrante=None):
        self.id = id_drone
        self.ambiente = ambiente
        self.bdi = bdi

        self.quadrante = quadrante

        self.rota = self._gerar_rota_patrol()
        self.idx_rota = 0

        # posiciona no primeiro ponto da rota
        self.x, self.y = self.rota[0]

        # Métrica simples
        self.passos = 0

    def _limites_quadrante(self):
        n = self.ambiente.tamanho
        meio = n // 2

        if self.quadrante == 1:
            return range(0, meio), range(0, meio)
        if self.quadrante == 2:
            return range(meio, n), range(0, meio)
        if self.quadrante == 3:
            return range(0, meio), range(meio, n)
        if self.quadrante == 4:
            return range(meio, n), range(meio, n)

        # fallback: toda a grade
        return range(0, n), range(0, n)

    def _gerar_rota_patrol(self):
        xs, ys = self._limites_quadrante()
        rota = []

        # varredura em serpentina para cobrir a área de forma determinística
        for i, x in enumerate(xs):
            linha = list(ys)
            if i % 2 == 1:
                linha.reverse()
            for y in linha:
                rota.append((x, y))

        # garante que haja pelo menos um ponto
        return rota if rota else [(0, 0)]

    def mover(self):
        self.idx_rota = (self.idx_rota + 1) % len(self.rota)
        self.x, self.y = self.rota[self.idx_rota]
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
