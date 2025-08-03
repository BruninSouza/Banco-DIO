import textwrap
from datetime import datetime

from Conta import ContaCorrente
from Transacao import Saque, Deposito
from Cliente import PessoaFisica
from Utils import Decorador, Iterador

class Logica:

    def __init__(self):
        self._clientes = []
        self._contas = []

    @property
    def clientes(self):
        return self._clientes    

    @property
    def contas(self):
        return self._contas 
        
    def menu(self):
        menu = """\n
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nu]\tNovo usuário
        [nc]\tNova conta
        [lc]\tListar contas
        [q]\tSair
        => """
        return input(textwrap.dedent(menu))

    def filtrar_cliente(self, cpf):
        clientes_filtrados = [cliente for cliente in self.clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None

    def recuperar_conta_cliente(self, cliente):
        if not cliente.contas: print("\n @@@ Usuário não encontrado @@@") ; return
        return cliente.contas[0]

    @Decorador.log_transacao
    def depositar(self):
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente: print("\n @@@ Cliente não encontrado @@@"); return
        
        valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)

        conta = self.recuperar_conta_cliente(cliente)
        if not conta: return
        
        cliente.realizar_transacao(conta, transacao)

    @Decorador.log_transacao
    def sacar(self):
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente: print("\n @@@ Cliente não encontrado @@@"); return
        
        valor = float(input("Informe o valor do depósito: "))
        transacao = Saque(valor)

        conta = self.recuperar_conta_cliente(cliente)
        if not conta: return
        
        cliente.realizar_transacao(conta, transacao)

    @Decorador.log_transacao
    def exibir_extrato(self):
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente: print("\n @@@ Cliente não encontrado @@@"); return
        
        conta = self.recuperar_conta_cliente(cliente)
        if not conta: return

        print("\n============================== EXTRATO ==============================")
        extrato = ""
        tem_transacao = False 
        transacoes = conta.historico.transacoes

        for transacao in conta.historico.gerar_relatorio():
            tem_transacao = True
            extrato += f"\n{transacao['tipo']:<8}\tR$ {transacao['valor']:.2f}\t{transacao['data']}"

        if not tem_transacao:
            extrato = "Não foram realizadas movimentações."

        print(extrato)
        print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
        print("=====================================================================")
    
    @Decorador.log_transacao
    def criar_cliente(self):
        cpf = input("Informe o CPF (somente número): ")
        cliente = self.filtrar_cliente(cpf)

        if cliente:
            print("\n@@@ Já existe cliente com esse CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

        self.clientes.append(cliente)

        print("\n=== Cliente cadastra com sucesso! ===")


    @Decorador.log_transacao
    def criar_conta(self):
        numero_conta = len(self.contas) + 1
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
            return

        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        self.contas.append(conta)
        cliente.contas.append(conta)

        print("\n=== Conta criada com sucesso! ===")

    @Decorador.log_transacao
    def listar_contas(self):
        for conta in Iterador(self.contas):
            print("=" * 100)
            print(textwrap.dedent(str(conta)))

def main():
    banco = Logica()

    while True:
        opcao = banco.menu()
        
        if opcao == "d":
           banco.depositar()

        elif opcao == "s":
            banco.sacar()

        elif opcao == "e":
            banco.exibir_extrato()

        elif opcao == "nu":
            banco.criar_cliente()

        elif opcao == "nc":
            banco.criar_conta()

        elif opcao == "lc":
            banco.listar_contas()

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()