import time
from core.ambiente import FOGO, VITIMA

class BDI:
    def __init__(self):
        self.fogos = set()
        self.vitimas = set()

        # fila de vítimas ainda não despachadas
        self.vitimas_pendentes = []

        self.bombeiros = []
        self.socorrista_fifo = None
        self.socorrista_util = None

        # controle de alternância
        self.turno = 0  # 0 -> FIFO, 1 -> UTIL

        self.tempo_inicio = time.time()

    def registrar_bombeiro(self, bombeiro):
        self.bombeiros.append(bombeiro)

    def registrar_socorristas(self, fifo, util):
        self.socorrista_fifo = fifo
        self.socorrista_util = util

    def receber_mensagem(self, tipo, pos):
        nome = "FOGO" if tipo == FOGO else "VITIMA"
        print(f"[BDI] recebeu {nome} em {pos}")

        if tipo == FOGO:
            if pos not in self.fogos:
                self.fogos.add(pos)

        elif tipo == VITIMA:
            if pos not in self.vitimas:
                self.vitimas.add(pos)

                if pos not in self.vitimas_pendentes:
                    self.vitimas_pendentes.append(pos)

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
                print(f"[BDI] enviando vítima {vitima} para SOCORRISTA FIFO")
                self.socorrista_fifo.receber_vitima(vitima) 
                self.turno = 1

            elif self.turno == 1 and util_livre:
                print(f"[BDI] enviando vítima {vitima} para SOCORRISTA UTIL")
                self.socorrista_util.receber_vitima(vitima)
                self.turno = 0

            else:
                # fallback: manda pra quem estiver livre
                if fifo_livre:
                    print(f"[BDI] enviando vítima {vitima} para SOCORRISTA FIFO")
                    self.socorrista_fifo.receber_vitima(vitima)
                elif util_livre:
                    print(f"[BDI] enviando vítima {vitima} para SOCORRISTA UTIL")
                    self.socorrista_util.receber_vitima(vitima)
                else:
                    nova_fila.append(vitima)

        self.vitimas_pendentes = nova_fila

    # def despachar_bombeiros(self, ambiente):
    #     fogos_por_quadrante = {1: [], 2: [], 3: [], 4: []}

    #     for fogo in self.fogos:
    #         q = ambiente.obter_quadrante(*fogo)
    #         fogos_por_quadrante[q].append(fogo)

    #     fogos_atribuidos = set()

    #     fogos_em_atendimento = {
    #         b.destino for b in self.bombeiros if b.destino is not None
    #     }

    #     # cada bombeiro cuida do seu quadrante
    #     for b in self.bombeiros:
    #         if b.ocupado:
    #             continue

    #         fogos_q = fogos_por_quadrante[b.quadrante]

    #         disponiveis = [f for f in fogos_q if f not in fogos_atribuidos and f not in fogos_em_atendimento]
    #         if disponiveis:
    #             alvo = min(
    #                 disponiveis,
    #                 key=lambda f: abs(f[0] - b.x) + abs(f[1] - b.y)
    #             )

    #             fogos_atribuidos.add(alvo)

    #             print(f"[BDI] enviando Bombeiro {b.id} para {alvo}")
    #             b.receber_ordem(alvo)

    #     # cooperação entre quadrantes
    #     fogos_restantes = [
    #         f for lista in fogos_por_quadrante.values()
    #         for f in lista
    #         if f not in fogos_atribuidos and f not in fogos_em_atendimento
    #     ]

    #     bombeiros_livres = [b for b in self.bombeiros if not b.ocupado]

    #     for b, fogo in zip(bombeiros_livres, fogos_restantes):
    #         print(f"[BDI] REDIRECIONANDO Bombeiro {b.id} para {fogo}")
    #         b.receber_ordem(fogo)
    #         fogos_atribuidos.add(fogo)

    def despachar_bombeiros(self, ambiente):
        fogos_por_quadrante = {1: [], 2: [], 3: [], 4: []}

        for fogo in self.fogos:
            q = ambiente.obter_quadrante(*fogo)
            fogos_por_quadrante[q].append(fogo)

        alvos_ocupados = set()  # evita duplicação

        # Cada bombeiro cuida do seu quadrante
        for b in self.bombeiros:
            if b.ocupado:
                alvos_ocupados.add(b.destino)
                continue

            fogos_q = fogos_por_quadrante[b.quadrante]

            # remove fogos já atribuídos
            fogos_q = [f for f in fogos_q if f not in alvos_ocupados]

            if fogos_q:
                alvo = min(
                    fogos_q,
                    key=lambda f: abs(f[0] - b.x) + abs(f[1] - b.y)
                )

                print(f"[BDI] enviando Bombeiro {b.id} (Q{b.quadrante}) para {alvo}")
                b.receber_ordem(alvo)
                alvos_ocupados.add(alvo)

        # Só chama ajuda se houver MAIS DE UM fogo no quadrante
        for q, fogos in fogos_por_quadrante.items():

            if len(fogos) <= 1:
                continue  # NÃO chama ajuda

            fogos_disponiveis = [f for f in fogos if f not in alvos_ocupados]

            if not fogos_disponiveis:
                continue

            bombeiros_livres = [
                b for b in self.bombeiros
                if not b.ocupado and b.quadrante != q
            ]

            for fogo in fogos_disponiveis:
                if not bombeiros_livres:
                    break

                b = bombeiros_livres.pop(0)

                print(f"[BDI] SOLICITANDO APOIO: Bombeiro {b.id} -> {fogo} (Q{q})")
                b.receber_ordem(fogo)
                alvos_ocupados.add(fogo)

    def limpar_conhecimento(self, ambiente):
        # Remove vítimas que não existem mais
        self.vitimas = {v for v in self.vitimas if ambiente.eh_vitima(*v)}

        # Também limpa pendentes
        self.vitimas_pendentes = [
            v for v in self.vitimas_pendentes if ambiente.eh_vitima(*v)
        ]

        self.fogos = {f for f in self.fogos if ambiente.eh_fogo(*f)}

    def atualizar(self, ambiente):
        print("\n[BDI] ===== NOVO CICLO =====")
        print("[BDI] Desejo: eliminar incêndios e salvar vítimas")
        print("[BDI] Intenção: despachar agentes disponíveis")
        
        self.limpar_conhecimento(ambiente)

        self.despachar_bombeiros(ambiente)
        self.despachar_socorristas()

    def tempo_total(self):
        return time.time() - self.tempo_inicio