# import time

# class BDI:
#     def __init__(self):
#         self.fogos = []  
#         self.vitimas = []  

#         self.bombeiros = []         # lista de bombeiros
#         self.socorrista_fifo = None
#         self.socorrista_util = None

#         self.tempo_inicio = time.time()

#     # registro
#     def registrar_bombeiro(self, bombeiro):
#         self.bombeiros.append(bombeiro)

#     def registrar_socorristas(self, fifo, util):
#         self.socorrista_fifo = fifo
#         self.socorrista_util = util

#     # drone
#     def receber_mensagem(self, tipo, pos):
#         # if tipo == "fogo":
#         #     if pos not in self.fogos:
#         #         self.fogos.append(pos)

#         # elif tipo == "vitima":
#         #     if pos not in self.vitimas:
#         #         self.vitimas.append(pos)
#         if tipo == "fogo":
#             self.fogos.add(pos)

#         elif tipo == "vitima":
#             self.vitimas.add(pos)

#     def atualizar_crencas(self, ambiente):
#         self.fogos = {
#             pos for pos in self.fogos
#             if ambiente.eh_fogo(*pos)
#         }

#         self.vitimas = {
#             pos for pos in self.vitimas
#             if ambiente.eh_vitima(*pos)
#         }

#     def despachar_bombeiros(self, ambiente):
#         # organiza fogos por quadrante
#         fogos_por_quadrante = {1: [], 2: [], 3: [], 4: []}

#         for fogo in self.fogos:
#             q = ambiente.obter_quadrante(*fogo)
#             fogos_por_quadrante[q].append(fogo)

#         # para cada quadrante
#         for q, fogos in fogos_por_quadrante.items():
#             if not fogos:
#                 continue

#             # pega bombeiro do quadrante
#             bombeiros_q = [b for b in self.bombeiros if b.quadrante == q]

#             # 1 bombeiro padrão
#             if fogos and bombeiros_q:
#                 b = bombeiros_q[0]
#                 if not b.ocupado:
#                     b.receber_ordem(fogos[0])

#             # REGRA DE EXCEÇÃO:
#             # mais de um fogo → pedir ajuda
#             if len(fogos) > 1:
#                 bombeiros_livres = [b for b in self.bombeiros if not b.ocupado]

#                 for i in range(1, len(fogos)):
#                     if i < len(bombeiros_livres):
#                         bombeiros_livres[i].receber_ordem(fogos[i])

#     def despachar_socorristas(self):
#         if not self.vitimas:
#             return

#         lista_vitimas = list(self.vitimas)
#         #metade = len(lista_vitimas) // 2

#         lista_fifo = lista_vitimas
#         lista_util = lista_vitimas

#         if self.socorrista_fifo:
#             self.socorrista_fifo.receber_lista(lista_fifo)

#         if self.socorrista_util:
#             self.socorrista_util.receber_lista(lista_util)

#     def atualizar(self, ambiente):
#         self.atualizar_crencas(ambiente)

#         # INTENTIONS
#         self.despachar_bombeiros(ambiente)
#         self.despachar_socorristas()

import time

class BDI:
    def __init__(self):
        # ==========================
        # BELIEFS
        # ==========================
        self.fogos = set()
        self.vitimas = set()

        # fila de vítimas ainda não despachadas
        self.vitimas_pendentes = []

        # ==========================
        # AGENTES
        # ==========================
        self.bombeiros = []
        self.socorrista_fifo = None
        self.socorrista_util = None

        # controle de alternância
        self.turno = 0  # 0 -> FIFO, 1 -> UTIL

        # ==========================
        # MÉTRICAS
        # ==========================
        self.tempo_inicio = time.time()

    # ==========================
    # REGISTROS
    # ==========================
    def registrar_bombeiro(self, bombeiro):
        self.bombeiros.append(bombeiro)

    def registrar_socorristas(self, fifo, util):
        self.socorrista_fifo = fifo
        self.socorrista_util = util

    def receber_mensagem(self, tipo, pos):
        if tipo == "fogo":
            if pos not in self.fogos:
                self.fogos.add(pos)

        elif tipo == "vitima":
            if pos not in self.vitimas:
                self.vitimas.add(pos)
                self.vitimas_pendentes.append(pos)

    # ==========================
    # CRENÇAS
    # ==========================
    # def atualizar_crencas(self, ambiente):
    #     for (x, y), tipo in ambiente.incidentes.items():
    #         if tipo == "FOGO":
    #             self.fogos.add((x, y))

    #         elif tipo == "VITIMA":
    #             if (x, y) not in self.vitimas:
    #                 self.vitimas.add((x, y))
    #                 self.vitimas_pendentes.append((x, y))

    # ==========================
    # DESPACHO INTELIGENTE
    # ==========================
    def despachar_socorristas(self):
        if not self.vitimas_pendentes:
            return

        nova_fila = []

        for vitima in self.vitimas_pendentes:

            fifo_livre = self.socorrista_fifo.disponivel()
            util_livre = self.socorrista_util.disponivel()

            # nenhum disponível → mantém na fila
            if not fifo_livre and not util_livre:
                nova_fila.append(vitima)
                continue

            # alternância inteligente
            if self.turno == 0 and fifo_livre:
                self.socorrista_fifo.receber_vitima(vitima)
                self.turno = 1

            elif self.turno == 1 and util_livre:
                self.socorrista_util.receber_vitima(vitima)
                self.turno = 0

            else:
                # fallback: manda pra quem estiver livre
                if fifo_livre:
                    self.socorrista_fifo.receber_vitima(vitima)
                elif util_livre:
                    self.socorrista_util.receber_vitima(vitima)
                else:
                    nova_fila.append(vitima)

        self.vitimas_pendentes = nova_fila

    def limpar_conhecimento(self, ambiente):
        # Remove vítimas que não existem mais
        self.vitimas = {v for v in self.vitimas if ambiente.eh_vitima(*v)}

        # Também limpa pendentes
        self.vitimas_pendentes = [
            v for v in self.vitimas_pendentes if ambiente.eh_vitima(*v)
        ]

    # ==========================
    # LOOP
    # ==========================
    def atualizar(self, ambiente):
        self.limpar_conhecimento(ambiente)
        self.despachar_socorristas()

    # ==========================
    # MÉTRICAS
    # ==========================
    def tempo_total(self):
        return time.time() - self.tempo_inicio