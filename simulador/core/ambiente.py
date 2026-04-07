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