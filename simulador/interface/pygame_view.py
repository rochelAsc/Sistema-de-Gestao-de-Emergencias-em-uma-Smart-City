import pygame
from core.ambiente import FOGO, VITIMA

LARGURA = 700
ALTURA = 700

FUNDO = (245, 245, 245)
GRID = (210, 210, 210)

FOGO_COR = (255, 170, 90)
VITIMA_COR = (240, 100, 100)

DRONE_COR = (0, 0, 0)
BOMBEIRO_COR = (70, 130, 255)

SOC_FIFO_COR = (180, 80, 255)
SOC_UTIL_COR = (0, 170, 120)

class PygameView:
    def __init__(self, ambiente):
        pygame.init()

        self.ambiente = ambiente

        self.cols = ambiente.tamanho
        self.rows = ambiente.tamanho

        self.largura = LARGURA
        self.altura = ALTURA

        self.tile_size = self.largura // self.cols

        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Smart City Simulation")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16)

    def desenhar_grid(self):
        for x in range(self.cols):
            for y in range(self.rows):
                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                pygame.draw.rect(self.tela, GRID, rect, 1)

    def desenhar_divisao_quadrantes(self):
        meio_x = self.largura // 2
        meio_y = self.altura // 2

        pygame.draw.line(self.tela, (80, 80, 80), (meio_x, 0), (meio_x, self.altura), 3)
        pygame.draw.line(self.tela, (80, 80, 80), (0, meio_y), (self.largura, meio_y), 3)

    def desenhar_incidentes(self):
        for (x, y), tipo in self.ambiente.incidentes.items():
            rect = pygame.Rect(
                x * self.tile_size,
                y * self.tile_size,
                self.tile_size,
                self.tile_size
            )

            if tipo == FOGO:
                pygame.draw.rect(self.tela, FOGO_COR, rect)
            elif tipo == VITIMA:
                pygame.draw.rect(self.tela, VITIMA_COR, rect)

    def desenhar_drone(self, x, y):
        cx = x * self.tile_size + self.tile_size // 2
        cy = y * self.tile_size + self.tile_size // 2

        size = self.tile_size // 2

        pygame.draw.polygon(self.tela, DRONE_COR, [
            (cx, cy - size),
            (cx - size//1.5, cy + size//1.5),
            (cx + size//1.5, cy + size//1.5)
        ])

    def desenhar_bombeiro(self, x, y):
        cx = x * self.tile_size + self.tile_size // 2
        cy = y * self.tile_size + self.tile_size // 2

        pygame.draw.circle(self.tela, BOMBEIRO_COR, (cx, cy), self.tile_size // 3)

    def desenhar_socorrista(self, x, y, cor):
        cx = x * self.tile_size + self.tile_size // 2
        cy = y * self.tile_size + self.tile_size // 2

        size = self.tile_size // 2

        pygame.draw.rect(
            self.tela,
            cor,
            (cx - size//2, cy - size//2, size, size)
        )

    def desenhar_agentes(self, drones, bombeiros, socorristas):
        for d in drones:
            self.desenhar_drone(d.x, d.y)

        for b in bombeiros:
            self.desenhar_bombeiro(b.x, b.y)

        # socorristas
        self.desenhar_socorrista(socorristas[0].x, socorristas[0].y, SOC_FIFO_COR)
        self.desenhar_socorrista(socorristas[1].x, socorristas[1].y, SOC_UTIL_COR)

    def desenhar_hud(self, soc_fifo, soc_util):
        texto1 = self.font.render(
            f"FIFO → passos: {soc_fifo.passos} | resgates: {soc_fifo.resgates}",
            True, (0, 0, 0)
        )

        texto2 = self.font.render(
            f"UTIL → passos: {soc_util.passos} | resgates: {soc_util.resgates}",
            True, (0, 0, 0)
        )

        self.tela.blit(texto1, (10, 10))
        self.tela.blit(texto2, (10, 30))

    def desenhar(self, drones, bombeiros, socorristas):
        self.tela.fill(FUNDO)

        self.desenhar_incidentes()
        self.desenhar_grid()
        self.desenhar_divisao_quadrantes() 
        self.desenhar_agentes(drones, bombeiros, socorristas)
        self.desenhar_hud(socorristas[0], socorristas[1])

        pygame.display.flip()

    def tick(self, fps=10):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.clock.tick(fps)