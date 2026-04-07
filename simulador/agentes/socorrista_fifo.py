class SocorristaFIFO:
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

    # def receber_lista(self, lista):
    #     if not self.lista_resgates:
    #         self.lista_resgates = lista.copy()

    def receber_vitima(self, vitima):
        self.lista_resgates.append(vitima)

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
        # Se não tem tarefas
        if not self.lista_resgates and self.estado == "livre":
            return

        # Se está livre, pega próxima vítima da fila
        if self.estado == "livre":
            self.alvo_atual = self.lista_resgates.pop(0)
            self.estado = "indo_vitima"

        # Indo até a vítima
        if self.estado == "indo_vitima":
            chegou = self.mover_passo(*self.alvo_atual)

            if chegou:
                # remove vítima do ambiente
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