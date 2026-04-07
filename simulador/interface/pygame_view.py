import pygame
from core.ambiente import FOGO, VITIMA

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 200, 0)
LARANJA = (255, 140, 0)
ROXO = (160, 32, 240)

class PygameView:
    def __init__(self, ambiente, largura=600, altura=600):
        pygame.init()

        self.ambiente = ambiente
        self.largura = largura
        self.altura = altura

        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Simulação Smart City 🚑🔥")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 18)

        self.tamanho_grid = ambiente.tamanho
        self.cell_size = largura // self.tamanho_grid

    # ==========================
    # DESENHO
    # ==========================
    def desenhar_grid(self):
        for x in range(self.tamanho_grid):
            for y in range(self.tamanho_grid):
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.tela, PRETO, rect, 1)

    def desenhar_divisa_quadrantes(self):
        meio_px = self.cell_size * (self.tamanho_grid // 2)
        pygame.draw.line(self.tela, (80, 80, 80), (meio_px, 0), (meio_px, self.altura), 2)
        pygame.draw.line(self.tela, (80, 80, 80), (0, meio_px), (self.largura, meio_px), 2)

    def desenhar_incidentes(self):
        for (x, y), tipo in self.ambiente.incidentes.items():
            cx = x * self.cell_size
            cy = y * self.cell_size

            if tipo == FOGO:
                pygame.draw.rect(self.tela, LARANJA, (cx, cy, self.cell_size, self.cell_size))
            elif tipo == VITIMA:
                pygame.draw.rect(self.tela, VERMELHO, (cx, cy, self.cell_size, self.cell_size))

    def desenhar_agente(self, x, y, cor):
        cx = x * self.cell_size + self.cell_size // 2
        cy = y * self.cell_size + self.cell_size // 2

        pygame.draw.circle(self.tela, cor, (cx, cy), self.cell_size // 3)

    def desenhar(self, drones, bombeiros, socorristas):
        self.tela.fill(BRANCO)

        self.desenhar_grid()
        self.desenhar_divisa_quadrantes()
        self.desenhar_incidentes()

        # drones (azul)
        for d in drones:
            self.desenhar_agente(d.x, d.y, AZUL)

        # bombeiros (verde)
        for b in bombeiros:
            self.desenhar_agente(b.x, b.y, VERDE)

        # socorristas
        self.desenhar_agente(socorristas[0].x, socorristas[0].y, ROXO)   # FIFO
        self.desenhar_agente(socorristas[1].x, socorristas[1].y, PRETO)  # UTIL

        self.desenhar_legenda()

        pygame.display.flip()

    def desenhar_legenda(self):
        itens = [
            ("Drone (patrulha)", AZUL),
            ("Bombeiro", VERDE),
            ("Socorrista FIFO", ROXO),
            ("Socorrista Utilidade", PRETO),
            ("Fogo", LARANJA),
            ("Vítima", VERMELHO),
        ]

        x = 10
        y = 10
        for label, cor in itens:
            pygame.draw.rect(self.tela, cor, (x, y, 14, 14))
            texto = self.font.render(label, True, PRETO)
            self.tela.blit(texto, (x + 20, y - 2))
            y += 20

    # ==========================
    # LOOP CONTROL
    # ==========================
    def tick(self, fps=5):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.clock.tick(fps)
