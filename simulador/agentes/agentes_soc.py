from core.ambiente import Ambiente
from agente_base import AgenteBase
from typing import List, Tuple, Optional, Dict
from collections import defaultdict
import time


class SOCAgent(AgenteBase):
    """
    Agente SOC (Security Operations Center) — agregador e correlador de eventos de segurança.
    
    Funcionalidades:
    - Recebe eventos de segurança de múltiplas fontes (sensores, câmeras, etc.)
    - Agrega e correlaciona eventos por localização/alvo
    - Detecta padrões de ataque ou anomalias
    - Emite alertas correlacionados de severidade aumentada
    - Monitora status geral de segurança por quadrante
    
    Atributos:
    - eventos_recentes: dict para rastrear eventos por localização dentro de janela de tempo
    - correlation_window: janela de tempo (passos) para correlação de eventos
    - correlation_threshold: número de eventos para gerar alerta correlacionado
    - alertas_emitidos: histórico de alertas emitidos
    """
    
    def __init__(
        self, 
        id_agente: str, 
        ambiente: Ambiente, 
        x_inicial: int, 
        y_inicial: int,
        correlation_window: int = 5,
        correlation_threshold: int = 3
    ) -> None:
        super().__init__(id_agente, ambiente, x_inicial, y_inicial)
        self.correlation_window = correlation_window
        self.correlation_threshold = correlation_threshold
        
        # Rastreia eventos recentes: {(x, y): [(timestamp, tipo, severidade), ...]}
        self.eventos_recentes: Dict[Tuple[int, int], List[Tuple]] = defaultdict(list)
        
        # Histórico de alertas emitidos
        self.alertas_emitidos: List[dict] = []
        
        # Contadores para IDs únicos
        self.contador_alerta = 0
        
        # Status de segurança por quadrante
        self.status_quadrantes = {
            "Q1": {"eventos": 0, "nivel_alerta": "NORMAL"},
            "Q2": {"eventos": 0, "nivel_alerta": "NORMAL"},
            "Q3": {"eventos": 0, "nivel_alerta": "NORMAL"},
            "Q4": {"eventos": 0, "nivel_alerta": "NORMAL"},
        }
    
    def perceber_ambiente(self) -> List[dict]:
        """
        Percebe eventos de segurança no ambiente.
        Identifica qualquer mudança (novos incidentes) como potencial evento de segurança.
        
        Returns:
            list: [{'tipo': 'Fogo', 'x': 5, 'y': 10, 'severidade': 3, 'timestamp': 10}, ...]
        """
        eventos_detectados = []
        
        # Varre a grade procurando por eventos de segurança
        for x in range(self.ambiente.tamanho_n):
            for y in range(self.ambiente.tamanho_n):
                celula = self.ambiente.grade[x][y]
                
                if celula != 0:
                    # Classifica evento e determina severidade
                    if celula == "Fogo":
                        tipo_evento = "Incêndio"
                        severidade = 3
                    elif celula == "Vítima":
                        tipo_evento = "Vítima"
                        severidade = 2
                    else:
                        continue
                    
                    evento = {
                        'tipo': tipo_evento,
                        'x': x,
                        'y': y,
                        'severidade': severidade,
                        'timestamp': self.passos_dados,
                        'quadrante': self.ambiente.obter_quadrante(x, y)
                    }
                    eventos_detectados.append(evento)
                    
                    # Registra evento para correlação
                    self.eventos_recentes[(x, y)].append(
                        (self.passos_dados, tipo_evento, severidade)
                    )
        
        return eventos_detectados
    
    def decidir_acao(self) -> Optional[Tuple]:
        """
        Decide qual ação tomar baseado em correlação de eventos.
        Verifica se há eventos correlacionados que requerem alerta elevado.
        
        Returns:
            tuple: ("emitir_alerta_correlacionado", alerta_dict) ou None
        """
        # Limpa eventos expirados (fora da janela de correlação)
        self._limpar_eventos_expirados()
        
        # Procura por localizações com múltiplos eventos
        for (x, y), eventos in list(self.eventos_recentes.items()):
            if len(eventos) >= self.correlation_threshold:
                # Encontrou correlação
                alerta_dict = {
                    'localizacao': (x, y),
                    'quadrante': self.ambiente.obter_quadrante(x, y),
                    'count_eventos': len(eventos),
                    'eventos_detalhes': eventos
                }
                self.ocupado = True
                return ("emitir_alerta_correlacionado", alerta_dict)
        
        self.ocupado = False
        return None
    
    def acionar_atuadores(self, instrucao_acao: Tuple) -> bool:
        """
        Executa a ação de emitir alerta correlacionado.
        
        Args:
            instrucao_acao: tuple ("emitir_alerta_correlacionado", alerta_dict)
        
        Returns:
            bool: True se alerta foi emitido com sucesso
        """
        if not instrucao_acao:
            return False
        
        acao, alerta_info = instrucao_acao
        
        if acao == "emitir_alerta_correlacionado":
            return self._emitir_alerta_correlacionado(alerta_info)
        
        return False
    
    def _emitir_alerta_correlacionado(self, alerta_info: dict) -> bool:
        """
        Emite um alerta de severidade aumentada baseado em correlação de eventos.
        
        Args:
            alerta_info: dict com informações de eventos correlacionados
        
        Returns:
            bool: True se alerta foi registrado com sucesso
        """
        self.contador_alerta += 1
        alerta_id = f"ALERTA-{self.id}-{self.contador_alerta}"
        
        x, y = alerta_info['localizacao']
        count = alerta_info['count_eventos']
        quadrante = alerta_info['quadrante']
        
        # Calcula severidade aumentada baseada no número de eventos
        severidade_base = max(e[2] for e in alerta_info['eventos_detalhes'])
        severidade_correlacionada = min(5, severidade_base + 1)  # Aumenta severidade
        
        alerta = {
            'id': alerta_id,
            'origin_agent': self.id,
            'tipo': 'ALERTA_CORRELACIONADO',
            'localizacao': (x, y),
            'quadrante': quadrante,
            'count_eventos': count,
            'severidade_original': severidade_base,
            'severidade_correlacionada': severidade_correlacionada,
            'nivel_alerta': self._determinar_nivel_alerta(severidade_correlacionada),
            'timestamp': self.passos_dados,
            'status': 'ativo'
        }
        
        self.alertas_emitidos.append(alerta)
        
        # Atualiza status de segurança do quadrante
        self.status_quadrantes[quadrante]['eventos'] += count
        self.status_quadrantes[quadrante]['nivel_alerta'] = alerta['nivel_alerta']
        
        print(f"[{self.id}] Alerta correlacionado emitido: {alerta_id} - "
              f"Localização: {(x, y)} ({quadrante}) - "
              f"Eventos correlacionados: {count} - "
              f"Severidade: {severidade_correlacionada} ({alerta['nivel_alerta']})")
        
        # Reseta eventos para essa localização após emitir alerta (evita spam)
        self.eventos_recentes[(x, y)] = []
        
        return True
    
    def _limpar_eventos_expirados(self) -> None:
        """Remove eventos que saíram da janela de correlação."""
        tempo_limite = self.passos_dados - self.correlation_window
        
        for localizacao in list(self.eventos_recentes.keys()):
            eventos = self.eventos_recentes[localizacao]
            # Mantém apenas eventos dentro da janela
            eventos_validos = [e for e in eventos if e[0] > tempo_limite]
            self.eventos_recentes[localizacao] = eventos_validos
    
    def _determinar_nivel_alerta(self, severidade: int) -> str:
        """Converte severidade em nível de alerta."""
        if severidade >= 4:
            return "CRÍTICO"
        elif severidade == 3:
            return "ALTO"
        elif severidade == 2:
            return "MÉDIO"
        else:
            return "BAIXO"
    
    def mover_um_passo(self, dest_x: int, dest_y: int) -> bool:
        """
        SOCAgent não se move fisicamente no ambiente.
        Permanece centralizado para monitoramento global.
        
        Returns:
            bool: False (não se move)
        """
        return False
    
    def obter_alertas_ativos(self) -> List[dict]:
        """Retorna lista de alertas emitidos."""
        return self.alertas_emitidos
    
    def obter_status_quadrantes(self) -> dict:
        """Retorna status de segurança de todos os quadrantes."""
        return self.status_quadrantes
    
    def obter_status_geral(self) -> str:
        """
        Retorna status geral de segurança baseado em todos os quadrantes.
        
        Returns:
            str: 'CRÍTICO', 'ALTO', 'MÉDIO' ou 'NORMAL'
        """
        niveis = [self.status_quadrantes[q]['nivel_alerta'] for q in self.status_quadrantes]
        
        if 'CRÍTICO' in niveis:
            return 'CRÍTICO'
        elif 'ALTO' in niveis:
            return 'ALTO'
        elif 'MÉDIO' in niveis:
            return 'MÉDIO'
        else:
            return 'NORMAL'
    
    def atualizar_status_alerta(self, alerta_id: str, novo_status: str) -> bool:
        """
        Atualiza o status de um alerta (ex: "ativo", "respondido", "resolvido").
        
        Args:
            alerta_id: ID do alerta a atualizar
            novo_status: novo status
        
        Returns:
            bool: True se atualizado com sucesso
        """
        for alerta in self.alertas_emitidos:
            if alerta['id'] == alerta_id:
                alerta['status'] = novo_status
                return True
        return False
