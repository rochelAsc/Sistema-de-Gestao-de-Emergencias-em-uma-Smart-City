# import random

# VAZIO = 0
# FOGO = 1
# VITIMA = 2

# class Ambiente:
#     def __init__(self, tamanho=20):
#         self.tamanho = tamanho
        
#         # Cria a matriz n x n preenchida com zeros (0 = célula vazia)
#         # Exemplo: se n=20, cria 20 listas, cada uma com 20 zeros.
#         self.grade = [[VAZIO for _ in range(tamanho)] for _ in range(tamanho)]
        
#         # Calcula onde fica a linha divisória (o meio da tela)
#         self.meio = tamanho // 2

#     def dentro_limite(self, x, y):
#         return 0 <= x < self.tamanho and 0 <= y < self.tamanho
    
#     def obter_celula(self, x, y):
#         if self.dentro_limite(x, y):
#             return self.grade[x][y]
#         return None
    
#     def eh_fogo(self, x, y):
#         return self.obter_celula(x, y) == FOGO

#     def eh_vitima(self, x, y):
#         return self.obter_celula(x, y) == VITIMA

#     def obter_quadrante(self, x, y):
#         if not self.dentro_limite(x, y):
#             return None

#         if x < self.meio and y < self.meio:
#             return 1  # Canto Superior Esquerdo
#         elif x >= self.meio and y < self.meio:
#             return 2  # Canto Superior Direito
#         elif x < self.meio and y >= self.meio:
#             return 3  # Canto Inferior Esquerdo
#         else:
#             return 4  # Canto Inferior Direito

#         # if x < self.meio and y < self.meio:
#         #     return "Q1"  # Canto Superior Esquerdo
#         # elif x >= self.meio and y < self.meio:
#         #     return "Q2"  # Canto Superior Direito
#         # elif x < self.meio and y >= self.meio:
#         #     return "Q3"  # Canto Inferior Esquerdo
#         # else:
#         #     return "Q4"  # Canto Inferior Direito

#     def adicionar_incidente(self, x, y, tipo):
#         """
#         Adiciona um incidente na grade ('Fogo' ou 'Vítima') se a célula estiver vazia.
#         """
#         if not self.dentro_limite(x, y):
#             return False
        
#         if self.grade[x][y] != VAZIO:
#             return False
        
#         self.grade[x][y] = tipo
#         return True

#         # if self.grade[x][y] == 0:
#         #     self.grade[x][y] = tipo
#         #     return True
#         # return False

#     def resolver_incidente(self, x, y):
#         """
#         Limpa a célula (usado quando o bombeiro apaga o fogo ou socorrista salva vítima).
#         """
#         if self.dentro_limite(x, y):
#             self.grade[x][y] = VAZIO

#     def listar_incidentes(self):
#         fogos = []
#         vitimas = []

#         for x in range(self.tamanho):
#             for y in range(self.tamanho):
#                 if self.grade[x][y] == FOGO:
#                     fogos.append((x, y))
#                 elif self.grade[x][y] == VITIMA:
#                     vitimas.append((x, y))

#         return fogos, vitimas
    
#     def gerar_incidentes(self, prob=0.05):
#         for x in range(self.tamanho):
#             for y in range(self.tamanho):
#                 if self.grade[x][y] == VAZIO:
#                     if random.random() < prob:
#                         tipo = random.choice([FOGO, VITIMA])
#                         self.grade[x][y] = tipo

import random

VAZIO = 0
FOGO = 1
VITIMA = 2

class Ambiente:
    def __init__(self, tamanho=20):
        self.tamanho = tamanho
        
        self.grade = [[VAZIO for _ in range(tamanho)] for _ in range(tamanho)]
        
        self.meio = tamanho // 2

        self.incidentes = {}

    def dentro_limite(self, x, y):
        return 0 <= x < self.tamanho and 0 <= y < self.tamanho
    
    def obter_celula(self, x, y):
        if self.dentro_limite(x, y):
            return self.grade[x][y]
        return None
    
    def eh_fogo(self, x, y):
        return self.incidentes.get((x, y)) == FOGO

    def eh_vitima(self, x, y):
        return self.incidentes.get((x, y)) == VITIMA

    def obter_quadrante(self, x, y):
        if not self.dentro_limite(x, y):
            return None

        if x < self.meio and y < self.meio:
            return 1                            # Canto Superior Esquerdo
        elif x >= self.meio and y < self.meio:
            return 2                            # Canto Superior Direito
        elif x < self.meio and y >= self.meio:
            return 3                            # Canto Inferior Esquerdo
        else:
            return 4                            # Canto Inferior Direito

    # Sincroniza o dicionário com a grade
    def atualizar_incidentes(self):
        self.incidentes.clear()

        for x in range(self.tamanho):
            for y in range(self.tamanho):
                if self.grade[x][y] != VAZIO:
                    self.incidentes[(x, y)] = self.grade[x][y]

    # Adiciona um incidente na grade ('Fogo' ou 'Vítima') se a célula estiver vazia.
    def adicionar_incidente(self, x, y, tipo):
        if not self.dentro_limite(x, y):
            return False
        
        if self.grade[x][y] != VAZIO:
            return False
        
        # adiciona incidente e atualiza dicionário
        self.grade[x][y] = tipo
        self.incidentes[(x, y)] = tipo
        return True

    # Limpa a célula (usado quando o bombeiro apaga o fogo ou socorrista salva vítima).
    def resolver_incidente(self, x, y):
        if self.dentro_limite(x, y):
            self.grade[x][y] = VAZIO

            # remove do dicionário
            if (x, y) in self.incidentes:
                del self.incidentes[(x, y)]

    # def listar_incidentes(self):
    #     fogos = []
    #     vitimas = []

    #     for x in range(self.tamanho):
    #         for y in range(self.tamanho):
    #             if self.grade[x][y] == FOGO:
    #                 fogos.append((x, y))
    #             elif self.grade[x][y] == VITIMA:
    #                 vitimas.append((x, y))

    #     return fogos, vitimas
    
    def listar_incidentes(self):
        fogos = []
        vitimas = []

        for (x, y), tipo in self.incidentes.items():
            if tipo == FOGO:
                fogos.append((x, y))
            elif tipo == VITIMA:
                vitimas.append((x, y))

        return fogos, vitimas
    
    def gerar_incidentes(self, prob=0.05):
        for x in range(self.tamanho):
            for y in range(self.tamanho):
                if self.grade[x][y] == VAZIO:
                    if random.random() < prob:
                        tipo = random.choice([FOGO, VITIMA])
                        self.grade[x][y] = tipo
                        self.incidentes[(x, y)] = tipo