from datetime import datetime
from Transacao import Transacao, Saque, Deposito

class Historico:
    def __init__(self):
        self_transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacao.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%y %H:%M:%s"),
            }
        )