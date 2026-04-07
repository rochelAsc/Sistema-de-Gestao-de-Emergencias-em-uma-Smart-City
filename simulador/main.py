# from core.ambiente import Ambiente, FOGO, VITIMA
# from agentes.drone import Drone
# from agentes.bombeiro import Bombeiro
# from agentes.socorrista_fifo import SocorristaFIFO
# from agentes.socorrista_utilidade import SocorristaUtilidade
# from agentes.bdi import BDI

# import random
# import time

# def main():
#     # ==========================
#     # AMBIENTE
#     # ==========================
#     ambiente = Ambiente(tamanho=10)

#     # ==========================
#     # BDI
#     # ==========================
#     bdi = BDI()

#     # ==========================
#     # AGENTES
#     # ==========================
#     drones = [
#         Drone("D1", ambiente, bdi, 0, 0),
#         Drone("D2", ambiente, bdi, 9, 9)
#     ]

#     bombeiros = [
#         Bombeiro("B1", ambiente, quadrante=1),
#         Bombeiro("B2", ambiente, quadrante=2),
#         Bombeiro("B3", ambiente, quadrante=3),
#         Bombeiro("B4", ambiente, quadrante=4),
#     ]

#     for b in bombeiros:
#         bdi.registrar_bombeiro(b)

#     soc_fifo = SocorristaFIFO("S1", ambiente, hospital_pos=(0, 0))
#     soc_util = SocorristaUtilidade("S2", ambiente, hospital_pos=(0, 0))

#     bdi.registrar_socorristas(soc_fifo, soc_util)

#     # ==========================
#     # LOOP
#     # ==========================
#     for passo in range(100):

#         print(f"\n===== PASSO {passo} =====")

#         # 1. Gerar eventos aleatórios
#         if random.random() < 0.3:
#             x = random.randint(0, 9)
#             y = random.randint(0, 9)
#             tipo = random.choice([FOGO, VITIMA])
#             ambiente.adicionar_incidente(x, y, tipo)

#         # 2. Drones percebem
#         for drone in drones:
#             drone.atualizar()

#         # 3. BDI decide
#         bdi.atualizar(ambiente)

#         # 4. Bombeiros agem
#         for b in bombeiros:
#             b.agir()

#         # 5. Socorristas agem
#         soc_fifo.agir()
#         soc_util.agir()

#         # ==========================
#         # LOGS
#         # ==========================
#         print("Fogos (BDI):", list(bdi.fogos))
#         print("Vítimas (BDI):", list(bdi.vitimas))

#         print("FIFO → passos:", soc_fifo.passos, "| resgates:", soc_fifo.resgates)
#         print("UTIL → passos:", soc_util.passos, "| resgates:", soc_util.resgates)

#         time.sleep(0.2)


# if __name__ == "__main__":
#     main()

from interface.pygame_view import PygameView
from core.ambiente import Ambiente, FOGO, VITIMA
from agentes.drone import Drone
from agentes.bombeiro import Bombeiro
from agentes.socorrista_fifo import SocorristaFIFO
from agentes.socorrista_utilidade import SocorristaUtilidade
from agentes.bdi import BDI

import random
import time

def main():
    # ==========================
    # AMBIENTE
    # ==========================
    ambiente = Ambiente(tamanho=10)

    # ==========================
    # BDI
    # ==========================
    bdi = BDI()

    # ==========================
    # AGENTES
    # ==========================
    drones = [
        Drone("D1", ambiente, bdi, 0, 0),
        Drone("D2", ambiente, bdi, 9, 9)
    ]

    bombeiros = [
        Bombeiro("B1", ambiente, quadrante=1),
        Bombeiro("B2", ambiente, quadrante=2),
        Bombeiro("B3", ambiente, quadrante=3),
        Bombeiro("B4", ambiente, quadrante=4),
    ]

    for b in bombeiros:
        bdi.registrar_bombeiro(b)

    soc_fifo = SocorristaFIFO("S1", ambiente, hospital_pos=(0, 0))
    soc_util = SocorristaUtilidade("S2", ambiente, hospital_pos=(0, 0))

    bdi.registrar_socorristas(soc_fifo, soc_util)


    view = PygameView(ambiente)
    # ==========================
    # LOOP
    # ==========================
    for passo in range(100):

        print(f"\n===== PASSO {passo} =====")

        # 1. Gerar eventos aleatórios
        if random.random() < 0.3:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            tipo = random.choice([FOGO, VITIMA])
            ambiente.adicionar_incidente(x, y, tipo)

        # 2. Drones percebem
        for drone in drones:
            drone.atualizar()

        # 3. BDI decide
        bdi.atualizar(ambiente)

        # 4. Bombeiros agem
        for b in bombeiros:
            b.agir()

        # 5. Socorristas agem
        soc_fifo.agir()
        soc_util.agir()

        # ==========================
        # LOGS
        # ==========================
        print("Fogos (BDI):", list(bdi.fogos))
        print("Vítimas (BDI):", list(bdi.vitimas))

        print("FIFO → passos:", soc_fifo.passos, "| resgates:", soc_fifo.resgates)
        print("UTIL → passos:", soc_util.passos, "| resgates:", soc_util.resgates)

        view.desenhar(drones, bombeiros, [soc_fifo, soc_util])
        view.tick(5)


if __name__ == "__main__":
    main()
