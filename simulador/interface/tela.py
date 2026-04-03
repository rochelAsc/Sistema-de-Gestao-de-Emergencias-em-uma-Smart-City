import pygame

class TelaGrafica:
    def __init__(self, ambiente_logico) -> None:
        pygame.init()
        self.ambiente = ambiente_logico
        
        # variavel N aqui é o lado do quadrado NxN
        self.n = self.ambiente.tamanho_n 

        # tamanho fixo em pixels
        self.tamanho_tela = 800 
        
        # calculo de cada celula na grade é o tamanho da tela dividido pelo lado
        self.tamanho_celula = self.tamanho_tela // self.n 
        
        self.display = pygame.display.set_mode((self.tamanho_tela, self.tamanho_tela))
        pygame.display.set_caption("Smart City - Gestão de Emergências")

        self.cor_fundo = (240, 240, 240)      # Cinza bem claro
        self.cor_linha = (0, 0, 0)            # Preto absoluto
        self.cor_quadrante = (50, 50, 50)     # Cinza escuro pra dividir Q1, Q2, Q3, Q4
        
        # Cores temporarias para eventos
        self.cor_fogo = (255, 69, 0)          # Laranja
        self.cor_vitima = (0, 191, 255)       # Azul claro

    def desenhar_frame(self) -> None:
        self.display.fill(self.cor_fundo)
        
        for i in range(self.n + 1): 
            pos_pixel = i * self.tamanho_celula
            
            # Linha Vertical 
            pygame.draw.line(
                self.display, 
                self.cor_linha, 
                (pos_pixel, 0), 
                (pos_pixel, self.tamanho_tela), 
                1 
            )
            
            # Linha Horizontal 
            pygame.draw.line(
                self.display, 
                self.cor_linha, 
                (0, pos_pixel), 
                (self.tamanho_tela, pos_pixel), 
                1
            )

        # Desenha a linha divisória grossa dos Quadrantes por cima da grade
        meio_tela = self.tamanho_tela // 2
        
        # Linha vertical separando os quadrantes
        pygame.draw.line(
            self.display, 
            self.cor_quadrante, 
            (meio_tela, 0), 
            (meio_tela, self.tamanho_tela), 
            4
        )
        
        # Linha horizontal separando os quadrantes
        pygame.draw.line(
            self.display, 
            self.cor_quadrante, 
            (0, meio_tela), 
            (self.tamanho_tela, meio_tela), 
            4
        )

        pygame.display.flip()