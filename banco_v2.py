import textwrap

def main():
    menu = """\n
    ============MENU============
    [d] \tDepositar
    [s] \tSacar
    [e] \tExtrato
    [nu]\tNovo Usuário
    [nc]\tNova Conta
    [lc]\tListar Contas
    [q] \tSair
    => """

    saldo = 0 
    LIMITE = 500
    AGENCIA = "0001"
    extrato = ""
    numero_saques = 0 
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []

    while True:
        opcao = input(menu).upper()

        if opcao == 'D':
            valor_depositado, extrato = depositar(extrato)
            saldo += valor_depositado

        elif opcao == 'S':
            if saldo <= 0:
                print('Seu saldo está zerado! Não será possível sacar.')
            else:
                saldo, extrato, numero_saques = sacar(saldo, extrato, LIMITE, numero_saques, LIMITE_SAQUES)
        elif opcao == 'E':
            exibir_extrato(saldo, extrato)
        
        elif opcao == 'NU':
            criar_usuario(usuarios)

        elif opcao == 'NC':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == 'LC':
            listar_conta(contas)
            
        elif opcao == 'Q':
            print("--------SAÍDA--------")
            break

        else:
            print('Opção inválida! Tente novamente.')


def depositar(extrato):
    print("--------DEPOSITO--------")
    valor = float(input('Digite o valor do depósito: '))
    if valor <= 0:
        print('Não é possível depositar um valor maior que 0')
    else:
        print(f'Valor de R$ {valor:.2f} depositado com sucesso!')
        extrato += f"Depósito realizado de R$ {valor:.2f}\n"
        return valor, extrato 

def sacar(saldo, extrato, LIMITE, numero_saques, LIMITE_SAQUES):
    print("--------SAQUE--------")
    valor = float(input('Digite o valor de saque: '))
    if valor > saldo:
        print(f'Valor de saque é maior que seu saldo atual - R$ {saldo:.2f}')
    elif valor > LIMITE:
        print(f'Valor de saque maior que o limite de R$ {LIMITE:.2f}.')
    elif numero_saques >= LIMITE_SAQUES:
        print(f'Limite de saques diários já atingidos.')
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque no valor de: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\nSaque realizado com sucesso!")
    else:
        print('Operação falhou! Tente novamente.')

    return saldo, extrato, numero_saques
    
def exibir_extrato(saldo, extrato):
    print("--------EXTRATO--------")
    print(f'Seu saldo atual é de R$ {saldo:.2f}.')
    print(f'Extrato \n{extrato}')

def criar_usuario(usuarios):
    print("--------NOVO USUÁRIO--------")
    cpf = input("Digite o CPF (apenas número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Este CPF já existe na base de usuários.")
        return 
    nome = input("Digite o nome completo: ")
    data_nascimento = input("Digite a data de nascimento (DD-MM-AAAA): ")
    endereço = input("Digite o endereço: ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereço": endereço})
    print("Usuário cadastrado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = None
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            usuarios_filtrados = usuario
    if usuarios_filtrados:
        return usuarios_filtrados
    else:
        return None

def criar_conta(AGENCIA, numero_conta, usuarios):

    print("--------NOVA CONTA--------")
    cpf = input("Digite o CPF (apenas número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": AGENCIA, "numero_conta": numero_conta, "usuario": usuario}
    else:
        print("Usuário não encontrado! Favor cadastrar esse usuário na função 'Novo Usuário'.")

def listar_conta(contas):
    for conta in contas:
        saida = f"""\
            Agência:\t{conta['agencia']},
            C/C:\t\t{conta['numero_conta']},
            Titular:\t{conta['usuario']['nome']} 
            """
        print('=' * 30)
        print(textwrap.dedent(saida))

main()