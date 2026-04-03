class Ambiente:
    def __init__(self, tamanho_n=20):
        self.tamanho_n = tamanho_n
        
        # Cria a matriz n x n preenchida com zeros (0 = célula vazia)
        # Exemplo: se n=20, cria 20 listas, cada uma com 20 zeros.
        self.grade = [[0 for _ in range(tamanho_n)] for _ in range(tamanho_n)]
        
        # Calcula onde fica a linha divisória (o meio da tela)
        self.meio = tamanho_n // 2

    def obter_quadrante(self, x, y):
        """
        Recebe uma coordenada (x, y) e retorna a qual quadrante ela pertence.
        A origem (0,0) no Python fica no canto superior esquerdo.
        """
        if x < self.meio and y < self.meio:
            return "Q1"  # Canto Superior Esquerdo
        elif x >= self.meio and y < self.meio:
            return "Q2"  # Canto Superior Direito
        elif x < self.meio and y >= self.meio:
            return "Q3"  # Canto Inferior Esquerdo
        else:
            return "Q4"  # Canto Inferior Direito

    def adicionar_incidente(self, x, y, tipo):
        """
        Adiciona um incidente na grade ('Fogo' ou 'Vítima') se a célula estiver vazia.
        """
        if self.grade[x][y] == 0:
            self.grade[x][y] = tipo
            return True
        return False

    def resolver_incidente(self, x, y):
        """
        Limpa a célula (usado quando o bombeiro apaga o fogo ou socorrista salva vítima).
        """
        self.grade[x][y] = 0

# ==========================================
# ÁREA DE TESTE ISOLADO LÓGICO
# ==========================================
if __name__ == "__main__":
    print("Iniciando teste lógico do Ambiente...\n")
    
    # Cria uma cidade pequena de 10x10 para testar
    cidade = Ambiente(tamanho_n=10)
    
    print(f"O meio da cidade é na linha/coluna: {cidade.meio}")
    
    # Testando os quadrantes (Exemplos)
    # Se o meio é 5, a coordenada (2,2) deve ser Q1
    coord1 = (2, 2)
    print(f"A coordenada {coord1} está no: {cidade.obter_quadrante(coord1[0], coord1[1])}")
    
    # A coordenada (8,2) passou do meio no X, então deve ser Q2
    coord2 = (8, 2)
    print(f"A coordenada {coord2} está no: {cidade.obter_quadrante(coord2[0], coord2[1])}")
    
    # A coordenada (8,8) passou do meio nos dois, deve ser Q4
    coord3 = (8, 8)
    print(f"A coordenada {coord3} está no: {cidade.obter_quadrante(coord3[0], coord3[1])}")
    
    print("\nAdicionando um fogo em (2,2)...")
    sucesso = cidade.adicionar_incidente(2, 2, "Fogo")
    print(f"Deu certo? {sucesso}. O que tem em (2,2) agora? {cidade.grade[2][2]}")