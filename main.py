def fucntio_extrato(saldo, /, *, extrato):
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

def saque(*,saldo, valor, extrato, limite, numero_saques, limites_saque):
    saldo -= valor
    extrato += f"Saque: R$ {valor_saque:.2f}\n"                 
    numero_saques += 1
    return saldo, extrato

def deposito(saldo, valor, extrato):
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    return saldo, extrato

menu = """
[e] extrato
[d] deposito
[s] sacar
[q] sair
[p] print saldo
=> """

saldo = 0
numero_saques = 0
LIMITE = 500
LIMITE_SAQUE = 2
extrato = ""

while True:
    opcao = input(menu).strip().lower()

    if opcao == "e":
        print(fucntio_extrato(saldo, extrato = extrato))   
        
    elif opcao == "d":
        try:
            valor_deposito = float(input("Digite quanto será depositado: "))
            if valor_deposito >= 0:
                saldo = deposito(saldo, valor_deposito, extrato)[0]
                extrato = deposito(saldo, valor_deposito, extrato)[1]
            else: print ("Não pode-se depositar valor negativo! Tente novamente")
        except ValueError: print("Por favor Digite um valor válido!")

    elif opcao == "s":

        saque(saldo = saldo, valor = valor_saque, extrato = extrato, 
              limite = LIMITE, numero_saques = numero_saques, limites_saque=LIMITE_SAQUE)

        saldo_zerado = saldo <= 0
        excedeu_saques = numero_saques > LIMITE_SAQUE

        try: 
            if saldo_zerado: print("Sua conta está sem saldo para ser sacado!"); continue
            elif excedeu_saques: print("Limite máximo de 3 saques diários atingido"); continue

            valor_saque = float(input("Digite quanto será sacado: "))
            excedeu_limite = valor_saque > LIMITE
            excedeu_saldo = valor_saque > saldo
            saque_negativo = valor_saque < 0
            
            if saque_negativo: print ("Não pode-se sacar valor negativo! Tente novamente")
            elif excedeu_saldo: print("Não se pode sacar um valor superior ao que está na conta!")
            elif excedeu_limite: print("Não se pode sacar mais do que 500 reais!")
            elif not saque_negativo:
                saldo = saque(saldo = saldo, valor = valor_saque, extrato = extrato, 
                    limite = LIMITE, numero_saques = numero_saques, limites_saque=LIMITE_SAQUE)[0]
                saldo = saque(saldo = saldo, valor = valor_saque, extrato = extrato, 
                    limite = LIMITE, numero_saques = numero_saques, limites_saque=LIMITE_SAQUE)[1]
        except ValueError: print("Por favor Digite um valor válido!")
    
    elif opcao == "q":
        break

    else: print("Opção inválida, por favor selecione novamente uma operação válida")