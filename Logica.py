import textwrap
from datetime import datetime

from Conta import Conta, ContaCorrente
from Historico import Historico
from Transacao import Saque, Deposito, Transacao
from Cliente import Cliente, PessoaFisica

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
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuário
        [q]\tSair
        => """
        return input(textwrap.dedent(menu))



    def filtrar_cliente(self, cpf):
        clientes_filtrados = [cliente for cliente in self.clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None

    def recuperar_conta_cliente(self, cliente):
        if not cliente.contas: print("\n @@@ Usuário não encontrado @@@") ; return
        return cliente.contas[0]

    def depositar(self):
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente: print("\n @@@ Cliente não encontrado @@@"); return
        
        valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)

        conta = self.recuperar_conta_cliente(cliente)
        if not conta: return
        
        cliente.realizar_transacao(conta, transacao)

    def sacar(self):
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente: print("\n @@@ Cliente não encontrado @@@"); return
        
        valor = float(input("Informe o valor do depósito: "))
        transacao = Saque(valor)

        conta = self.recuperar_conta_cliente(cliente)
        if not conta: return
        
        cliente.realizar_transacao(conta, transacao)

    def exibir_extrato(self):
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente: print("\n @@@ Cliente não encontrado @@@"); return
        
        conta = self.recuperar_conta_cliente(cliente)
        if not conta: return

        print("\n============================== EXTRATO ==============================")
        transacoes = conta.historico.transacoes
        extrato = ""

        if not transacoes:
            extrato = "Não foram realizadas movimentações."
        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

        print(extrato)
        print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
        print("=====================================================================")

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

        print("\n=== Cliente criado com sucesso! ===")


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


    def listar_contas(self):
        if not self.contas:
            print("\n @@@ Nenhuma conta Cadastrada! @@@")
            return 
        
        for conta in self.contas:
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