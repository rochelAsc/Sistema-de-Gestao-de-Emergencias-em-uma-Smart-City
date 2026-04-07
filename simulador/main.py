from interface.pygame_view import PygameView
from core.ambiente import Ambiente, FOGO, VITIMA
from agentes.drone import Drone
from agentes.bombeiro import Bombeiro
from agentes.socorrista_fifo import SocorristaFIFO
from agentes.socorrista_utilidade import SocorristaUtilidade
from agentes.bdi import BDI

import random
import time

CONFIG = {
    "FPS": 5,
    "PROB_EVENTO": 0.3,
    "DRONE_STEPS": 1
}

def gerar_posicao_balanceada(tamanho):
    metade = tamanho // 2

    q = random.choice([1, 2, 3, 4])

    if q == 1:
        return random.randint(0, metade - 1), random.randint(0, metade - 1)
    elif q == 2:
        return random.randint(metade, tamanho - 1), random.randint(0, metade - 1)
    elif q == 3:
        return random.randint(0, metade - 1), random.randint(metade, tamanho - 1)
    else:
        return random.randint(metade, tamanho - 1), random.randint(metade, tamanho - 1)

def main():
    ambiente = Ambiente(tamanho=15)
    bdi = BDI()

    t = ambiente.tamanho - 1
    centro = (ambiente.meio, ambiente.meio)

    drones = [
        Drone("D1", ambiente, bdi, 0, 0),
        Drone("D2", ambiente, bdi, 0, ambiente.tamanho // 2)
    ]

    bombeiros = [
        Bombeiro("B1", ambiente, quadrante=1),
        Bombeiro("B2", ambiente, quadrante=2),
        Bombeiro("B3", ambiente, quadrante=3),
        Bombeiro("B4", ambiente, quadrante=4),
    ]

    for b in bombeiros:
        bdi.registrar_bombeiro(b)

    soc_fifo = SocorristaFIFO("S1", ambiente, hospital_pos=centro)
    soc_util = SocorristaUtilidade("S2", ambiente, hospital_pos=centro)

    bdi.registrar_socorristas(soc_fifo, soc_util)

    view = PygameView(ambiente)

    # LOOP
    for passo in range(500):

        print(f"\n===== PASSO {passo} =====")

        # Gerar eventos aleatórios
        if random.random() < CONFIG["PROB_EVENTO"]:
            x, y = gerar_posicao_balanceada(ambiente.tamanho)
            
            if (x, y) not in ambiente.incidentes:
                tipo = random.choice([FOGO, VITIMA])
                ambiente.adicionar_incidente(x, y, tipo)

        # Drones percebem
        for drone in drones:
            for _ in range(CONFIG["DRONE_STEPS"]):
                drone.atualizar()

        # BDI decide
        bdi.atualizar(ambiente)

        # Bombeiros agem
        for b in bombeiros:
            b.agir()

        # Socorristas agem
        soc_fifo.agir()
        soc_util.agir()

        print("\n===== RESULTADOS FINAIS =====")

        print("\nSOCORRISTA FIFO:")
        print("Resgates:", soc_fifo.resgates)
        print("Passos:", soc_fifo.passos)

        print("\nSOCORRISTA UTIL:")
        print("Resgates:", soc_util.resgates)
        print("Passos:", soc_util.passos)

        # eficiência simples
        ef_fifo = soc_fifo.resgates / (soc_fifo.passos + 1)
        ef_util = soc_util.resgates / (soc_util.passos + 1)

        print("\nEFICIÊNCIA:")
        print("FIFO:", ef_fifo)
        print("UTIL:", ef_util)

        view.desenhar(drones, bombeiros, [soc_fifo, soc_util])
        view.tick(CONFIG["FPS"])


if __name__ == "__main__":
    main()
