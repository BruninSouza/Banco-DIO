menu = """
[e] extrato
[d] deposito
[s] sacar
[q] sair

=> """

saldo = 0
numero_saques = 0
LIMITE = 500
LIMITE_SAQUE = 3

saques = []
depositos = []

while True:
    opcao = input(menu).strip()

    if opcao == "e":
        print(f"""
Saldo atual: {saldo}
Depositos realizados: {depositos}
Saques realizados: {saques}
""")
        
    elif opcao == "d":
        try:
            valor_deposito = float(input("Digite quanto será depositado: "))
            if valor_deposito < 0: print ("Não pode-se depositar valor negativo! Tente novamente"); continue
            saldo += valor_deposito
            depositos.append(valor_deposito)
        except ValueError: print("Por favor Digite um valor válido!")

    elif opcao == "s":
        try: 
            if numero_saques < 3:
                if saldo > 0:
                    valor_saque = float(input("Digite quanto será sacado: "))
                    if valor_saque < 0: print ("Não pode-se sacar valor negativo! Tente novamente"); continue
                    elif valor_saque > saldo: print("Não se pode sacar um valor superior ao que está na conta!"); continue
                    elif valor_saque > 500: print("Não se pode sacar mais do que 500 reais!"); continue
                    saldo -= valor_saque
                    saques.append(valor_saque)
                else: print("Sua conta está sem saldo para ser sacado!") 
            else: print("Limite máximo de 3 saques diários atingido")
            numero_saques += 1
        except ValueError: print("Por favor Digite um valor válido!")

        
    
    elif opcao == "q":
        break

    else: print("Opção inválida, por favor selecione novamente uma operação válida")