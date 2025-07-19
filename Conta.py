from Historico import Historico
from Transacao import Transacao, Saque, Deposito
class Conta:

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo 

        if excedeu_saldo: print("\n@@@ Não se pode sacar um valor superior ao que está na conta! @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n*** Saque realizado com sucesso!! ***")
            return True
        else: print("\n@@@ Operação falhou! o valor informado é inválido. @@@")

        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n*** Deposito realizado com sucesso!! ***")
        else: 
            print("\n@@@ Operação falhou! o valor informado é inválido. @@@")
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len({transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__})
        excedeu_saques = numero_saques > self.limite_saques
        excedeu_limite = valor > self.limite
        
        if excedeu_saques: print("\n@@@ Operação falhou! Você excedeu o limite diário de saques. @@@")
        elif excedeu_limite: print("\n @@@ Operação falhou! Você ultrapassou o valor máximo permitido num saque. @@@")
        else: return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""\
            Agencia:\t{self.agencia}
            C/C:\t\t{self.numero}
            titular:\t{self.cliente}
        """
