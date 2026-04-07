import math

class SocorristaUtilidade:
    def __init__(self, id_agente, ambiente, hospital_pos):
        self.id = id_agente
        self.ambiente = ambiente

        self.x, self.y = hospital_pos  # começa no hospital
        self.hospital = hospital_pos

        self.lista_resgates = []
        self.estado = "livre"  # "indo_vitima", "levando_hospital"
        self.alvo_atual = None

        # Métricas
        self.passos = 0
        self.resgates = 0

    def disponivel(self):
        return self.estado == "livre"

    def receber_vitima(self, vitima):
        self.lista_resgates.append(vitima)

    # def receber_lista(self, lista):
    #     if not self.lista_resgates:
    #         self.lista_resgates = lista.copy()

    def distancia(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def escolher_proxima_vitima(self):
        return min(
            self.lista_resgates,
            key=lambda v: self.distancia((self.x, self.y), v)
        )

    def mover_passo(self, dest_x, dest_y):
        if self.x < dest_x:
            self.x += 1
        elif self.x > dest_x:
            self.x -= 1
        elif self.y < dest_y:
            self.y += 1
        elif self.y > dest_y:
            self.y -= 1

        self.passos += 1
        return (self.x, self.y) == (dest_x, dest_y)

    def agir(self):
        # Sem tarefas
        if not self.lista_resgates and self.estado == "livre":
            return

        # Escolhe melhor vítima dinamicamente
        if self.estado == "livre":
            self.alvo_atual = self.escolher_proxima_vitima()
            self.lista_resgates.remove(self.alvo_atual)
            self.estado = "indo_vitima"

        # Indo até a vítima
        if self.estado == "indo_vitima":
            chegou = self.mover_passo(*self.alvo_atual)

            if chegou:
                if self.ambiente.eh_vitima(*self.alvo_atual):
                    self.ambiente.resolver_incidente(*self.alvo_atual)

                self.estado = "levando_hospital"

        # Levando para o hospital
        elif self.estado == "levando_hospital":
            chegou = self.mover_passo(*self.hospital)

            if chegou:
                self.resgates += 1
                self.estado = "livre"
                self.alvo_atual = None