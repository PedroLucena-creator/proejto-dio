def main():
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

    saldo = 0 
    limite = 500
    extrato = ""
    numero_saques = 0 
    LIMITE_SAQUES = 3

    while True:
        opcao = input(menu).upper()

        if opcao == 'D':
            valor_depositado = deposito()
            saldo += valor_depositado

        elif opcao == 'S':
            print("--------SAQUE--------")
            if saldo <= 0:
                print('Seu saldo está zerado... Não será possível sacar.')
            else:
                saque = float(input('Digite quanto quer sacar: '))
                if saque > limite:
                    print(f'Valor de saque maior que o limite de {limite:.2f} reais.')
                else:
                    if saque > saldo:
                        print(f'Valor de saque é maior que seu saldo atual - {saldo:.2f}')
                    if numero_saques >= LIMITE_SAQUES:
                        print(f'Limite de saques diários já atingidos.')
                    else:
                        saldo -= saque
                        extrato += f"Saque: R$ {saque:.2f}"
                        numero_saques += 1
                    
        elif opcao == 'E':
            print("--------EXTRATO--------")
            print(f'Seu saldo atual é de R$ {saldo:.2f}.')
            print(f'Saques anteriores \n{extrato}')
        
        elif opcao == 'Q':
            print("--------SAÍDA--------")
            break

        else:
            print('Opção inválida! Tente novamente.')





def deposito():
    print("--------DEPOSITO--------")
    valor = float(input('Digite o valor do depósito: '))
    if valor <= 0:
        print('Não é possível depositar um valor maior que 0')
        return 0
    else:
        print(f'Valor de R$ {valor:.2f} depositado com sucesso!')
        return valor 

main()