from core.ambiente import Ambiente
from agente_base import AgenteBase
from typing import List, Tuple, Optional


class ReactAgent(AgenteBase):
    """
    Agente React — responsável por receber alertas e criar/coordenar dispatches.
    
    Funcionalidades:
    - Percebe incidentes no ambiente (fogo, vítimas, etc.)
    - Decide quais incidentes requerem ação imediata (baseado em prioridade/severidade)
    - Cria dispatches para unidades de resposta (bombeiros, ambulâncias, etc.)
    - Monitora o status dos dispatches e replica se necessário
    
    Atributos:
    - threshold_severidade: severidade mínima para gerar dispatch
    - dispatches_ativos: dict com dispatches em andamento
    - incidentes_percebidos: lista de incidentes detectados na última percepção
    """
    
    def __init__(
        self, 
        id_agente: str, 
        ambiente: Ambiente, 
        x_inicial: int, 
        y_inicial: int,
        threshold_severidade: int = 2
    ) -> None:
        super().__init__(id_agente, ambiente, x_inicial, y_inicial)
        self.threshold_severidade = threshold_severidade
        self.dispatches_ativos: dict = {}  # {dispatch_id: dispatch_info}
        self.incidentes_percebidos: List[dict] = []
        self.contador_dispatch = 0  # para gerar IDs únicos de dispatch
    
    def perceber_ambiente(self) -> List[dict]:
        """
        Percebe o ambiente e identifica incidentes (Fogo, Vítima).
        Retorna uma lista de incidentes com suas posições e tipos.
        
        Returns:
            list: [{'tipo': 'Fogo', 'x': 5, 'y': 10, 'severidade': 3}, ...]
        """
        self.incidentes_percebidos = []
        
        # Varre toda a grade procurando por incidentes
        for x in range(self.ambiente.tamanho_n):
            for y in range(self.ambiente.tamanho_n):
                celula = self.ambiente.grade[x][y]
                
                # Se encontrou incidente (não é 0 = vazio)
                if celula != 0:
                    # Determina tipo e severidade
                    if celula == "Fogo":
                        severidade = 3  # Fogo é alta prioridade
                        tipo = "Fogo"
                    elif celula == "Vítima":
                        severidade = 2  # Vítima é média-alta prioridade
                        tipo = "Vítima"
                    else:
                        # Tipo desconhecido, ignora
                        continue
                    
                    # Calcula distância manhattan do agente ao incidente
                    distancia = abs(self.x - x) + abs(self.y - y)
                    
                    incidente = {
                        'tipo': tipo,
                        'x': x,
                        'y': y,
                        'severidade': severidade,
                        'distancia': distancia,
                        'quadrante': self.ambiente.obter_quadrante(x, y)
                    }
                    self.incidentes_percebidos.append(incidente)
        
        return self.incidentes_percebidos
    
    def decidir_acao(self) -> Optional[Tuple]:
        """
        Decide qual ação tomar baseado nos incidentes percebidos.
        Prioriza incidentes por severidade e distância.
        
        Returns:
            tuple: ("criar_dispatch", incident_dict) ou None se não há ação
        """
        # Se não há incidentes percebidos, nada a fazer
        if not self.incidentes_percebidos:
            self.ocupado = False
            return None
        
        # Filtra incidentes acima do threshold de severidade
        incidentes_prioritarios = [
            inc for inc in self.incidentes_percebidos 
            if inc['severidade'] >= self.threshold_severidade
        ]
        
        if not incidentes_prioritarios:
            self.ocupado = False
            return None
        
        # Ordena por severidade (DESC) e depois por distância (ASC)
        # Maior severidade primeiro, depois o mais próximo
        incidente_alvo = sorted(
            incidentes_prioritarios,
            key=lambda x: (-x['severidade'], x['distancia'])
        )[0]
        
        # Marca agente como ocupado e retorna ação de criar dispatch
        self.ocupado = True
        return ("criar_dispatch", incidente_alvo)
    
    def acionar_atuadores(self, instrucao_acao: Tuple) -> bool:
        """
        Executa a instrução de ação (criar dispatch para unidades de resposta).
        
        Args:
            instrucao_acao: tuple ("criar_dispatch", incident_dict)
        
        Returns:
            bool: True se dispatch foi criado com sucesso, False caso contrário
        """
        if not instrucao_acao:
            return False
        
        acao, incidente_info = instrucao_acao
        
        if acao == "criar_dispatch":
            return self._criar_dispatch(incidente_info)
        
        return False
    
    def _criar_dispatch(self, incidente: dict) -> bool:
        """
        Cria um novo dispatch para unidades de resposta.
        
        Args:
            incidente: dict com informações do incidente
        
        Returns:
            bool: True se dispatch foi registrado com sucesso
        """
        self.contador_dispatch += 1
        dispatch_id = f"DISPATCH-{self.id}-{self.contador_dispatch}"
        
        # Determina tipo de unidade recomendada baseado no tipo de incidente
        if incidente['tipo'] == "Fogo":
            unidades_recomendadas = ["Bombeiros"]
        elif incidente['tipo'] == "Vítima":
            unidades_recomendadas = ["Ambulância", "Bombeiros"]
        else:
            unidades_recomendadas = ["Operador"]
        
        dispatch = {
            'id': dispatch_id,
            'origin_agent': self.id,
            'incident_type': incidente['tipo'],
            'incident_location': (incidente['x'], incidente['y']),
            'priority': self._calcular_prioridade(incidente['severidade']),
            'recommended_units': unidades_recomendadas,
            'timestamp': self.passos_dados,
            'quadrante': incidente['quadrante'],
            'status': 'ativo'
        }
        
        self.dispatches_ativos[dispatch_id] = dispatch
        print(f"[{self.id}] Dispatch criado: {dispatch_id} - "
              f"Incidente: {incidente['tipo']} em ({incidente['x']}, {incidente['y']}) - "
              f"Prioridade: {dispatch['priority']}")
        
        return True
    
    def _calcular_prioridade(self, severidade: int) -> str:
        """Converte severidade numérica em nível de prioridade textual."""
        if severidade >= 3:
            return "CRÍTICA"
        elif severidade == 2:
            return "ALTA"
        else:
            return "NORMAL"
    
    def mover_um_passo(self, dest_x: int, dest_y: int) -> bool:
        """
        ReactAgent não se move fisicamente no ambiente.
        Permanece em posição fixa (central) para coordenação.
        
        Returns:
            bool: False (não se move)
        """
        return False
    
    def obter_dispatches_ativos(self) -> dict:
        """Retorna dict de dispatches em andamento."""
        return self.dispatches_ativos
    
    def atualizar_dispatch_status(self, dispatch_id: str, novo_status: str) -> bool:
        """
        Atualiza o status de um dispatch (ex: "em_andamento", "concluído").
        
        Args:
            dispatch_id: ID do dispatch a atualizar
            novo_status: novo status
        
        Returns:
            bool: True se atualizado com sucesso
        """
        if dispatch_id in self.dispatches_ativos:
            self.dispatches_ativos[dispatch_id]['status'] = novo_status
            return True
        return False
