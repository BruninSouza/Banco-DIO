import textwrap
from datetime import datetime

def menu():
    menu = """
========== Menu ==========
[e]\textrato
[d]\tdeposito
[s]\tsacar
[cn]\tcriar Cliente
[cc]\tCriar Conta
[ls]\tListas Contas
[q]\tsair
=> """
    return input(textwrap.dedent(menu))

def visualizar_extrato(saldo, /, *, extrato):
    if extrato != "":
        extrato = f"""
Saldo atual: {saldo}

========== EXTRATO ==========

{extrato}
"""
    else:
        extrato = f"""
Saldo atual: {saldo}
                  
Não foram realizadas movimentações
"""
    return extrato

def sacar(*,saldo, valor, extrato, limite, numero_saques, limites_saque):
    excedeu_saques = numero_saques > limites_saque
    excedeu_limite = valor > limite
    excedeu_saldo = valor > saldo
    saque_negativo = valor < 0

    if excedeu_saques: print("\n@@@ Limite máximo de 3 saques diários atingido @@@")
    elif saque_negativo: print ("\n@@@ Não pode-se sacar valor negativo! Tente novamente @@@")
    elif excedeu_saldo: print("\n@@@ Não se pode sacar um valor superior ao que está na conta! @@@")
    elif excedeu_limite: print("\n@@@ Não se pode sacar mais do que 500 reais! @@@")
    elif not saque_negativo:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"                 
        numero_saques += 1
        print("=== Saque realizado com Sucesso!! ===")

    return saldo, extrato

def depositar(saldo, valor, extrato):
    if valor >= 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print("=== Depósito realizado com Sucesso!! ===")
    else: print ("\n@@@ Não pode-se depositar valor negativo! Tente novamente @@@")

    return saldo, extrato

def filtrar_usuario(usuarios, cpf):
    for _ in usuarios:
            if _["cpf"] == cpf: return _
            else: return False

def criar_usuario(usuarios):
    cpf = input("Digite seu CPF (EX: xxx.xxx.xxx-xx): ")
    usuario = filtrar_usuario(usuarios, cpf)
    if usuario: print("\n Já existe usuário com esse CPF"); return

    nome = input("Digite seu nome: ")
    data_nascimento = datetime.strptime(input("Digite sua data de nascimento (ex: dd-mm-yyyy): "), "%d-%m-%Y")
    data = data_nascimento.strftime("%d-%m-%Y")
    endereco = input("Digite seu endereço (logradouro, nro - bairro - cidade/UF)")

    usuarios.append({"cpf": cpf, "nome":nome, "data_nascimento": data, "endereco": endereco})
    print ("\n === Usuário cadastrado com sucesso!! ===")
    return usuario

def criar_conta(agencia, num_conta, usuarios):
    if usuarios == []: return "\n @@@ Não há usuários cadastrados no sistema @@@"
    cpf_usuario = input("Digite o CPF que será associado à conta (xxx.xxx.xxx-xx): ")
    usuario = filtrar_usuario(usuarios, cpf_usuario)
    if usuario: 
        print("\n === Conta criada com sucesso!! ===")
        return {"agencia": agencia, "numero_conta": num_conta, "usuario":usuario}

    return "\n@@@ Usuário não encontrado @@@"

def listar_contas(contas):
    for conta in contas:
        linha = f"""
            agência:\t{conta["agencia"]}
            C/C:\t{conta["numero_conta"]}
            titular:\t{conta["usuario"]["nome"]}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE = 500
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    numero_saques = 0
    extrato = " "
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "e":
            print(visualizar_extrato(saldo, extrato = extrato))   
            
        elif opcao == "d":
            try:
                valor_deposito = float(input("Digite quanto será depositado: "))
                    
                saldo, extrato = depositar(saldo, valor_deposito, extrato)
            except ValueError: print("\n@@@ Por favor, Digite um valor válido!! @@@")
            

        elif opcao == "s":
            saldo_zerado = saldo <= 0
            if saldo_zerado: print("\n@@@ Sua conta está sem saldo para ser sacado! @@@"); continue

            try:
                valor_saque = float(input("Digite quanto será sacado: "))
                saldo, extrato = sacar(saldo = saldo, 
                                        valor = valor_saque, 
                                        extrato = extrato, 
                                        limite = LIMITE, 
                                        numero_saques = numero_saques, 
                                        limites_saque=LIMITE_SAQUES)
            except ValueError: print("\n@@@ Por favor, Digite um valor válido!! @@@")
        
        elif opcao == "cn":
            try: 
                criar_usuario(usuarios)
            except ValueError: print("\n@@@ Por favor, Digite um valor válido!! @@@")

        elif opcao == "cc":
            num_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, 
                            num_conta, 
                            usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "ls":
            listar_contas(contas)

        elif opcao == "q":
            break

        else: print("Opção inválida, por favor selecione novamente uma operação válida")

main()