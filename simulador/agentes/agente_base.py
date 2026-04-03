from core.ambiente import Ambiente

class AgenteBase:
    def __init__(self, id_agente: str, ambiente: Ambiente, x_inicial: int, y_inicial: int) -> None:
        self.id = id_agente
        self.ambiente = ambiente
        self.x = x_inicial
        self.y = y_inicial
        
        # Medida de Desempenho
        self.passos_dados = 0
        self.ocupado = False

    def perceber_ambiente(self) -> list:
        """
        coleta os dados do ambiente
        espera-se o retorno de uma list porque:
        drone vai retornar uma lista de incidentes percebidos
        bombeiros/socorristas podem retornar uma lista com a rota atual
        """
        pass

    def decidir_acao(self) -> tuple | None:
        """
        "pennsa" no que fazer com base nas percepções
        espera-se um conjunto com a instrução 
        ("mover", 5, 10) ou ("resgatar", 2, 2).
        retornar None se o agente estiver desocupado
        """
        pass

    def acionar_atuadores(self, instrucao_acao: tuple) -> bool:
        """
        recebe a decisão e executa no ambiente
        retorna booleano pra indicar se deu certo ou nao
        """
        pass

    def mover_um_passo(self, dest_x: int, dest_y: int) -> bool:
        """
        como todos andam na grade da mesma forma, a logica de andar fica nessa superclasse
        retorna True se chegou ao destino final, False se ainda caminhando
        """
        pass