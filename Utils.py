from datetime import datetime
import functools 

class Decorador():
    def log_transacao(funcao):
        
        @functools.wraps(funcao)
        def decorador(*args, **kwargs):
            log_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            nome_funcao = funcao.__name__.upper()
            print (f"\n{nome_funcao} {log_hora}\n")
            return funcao(*args, **kwargs)
        
        return decorador
    
class Iterador():
    def __init__(self, contas):
        self.contas = contas
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:  
            conta = self.contas[self._index]
            return f"""
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally: self._index += 1