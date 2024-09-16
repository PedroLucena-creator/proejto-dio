from abc import ABC, abstractmethod
import datetime

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

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
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
        print("--------SAQUE--------")
        saldo = self._saldo
        if valor > saldo:
            print(f'Valor de saque é maior que seu saldo atual - R$ {saldo:.2f}')

        elif valor > 0:
            self._saldo -= valor
            print('Saque realizado com sucesso!')
            return True
        
        else:
            print('Operação falhou! Tente novamente.')

        return False
    
    def depositar(self, valor):
        print("--------DEPOSITO--------")
        if valor <= 0:
            print('Não é possível depositar um valor maior que 0')
            return False
        
        else:
            self._saldo += valor
            print(f'Valor de R$ {valor:.2f} depositado com sucesso!')
            return True 
        
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])
        
        if valor > self.limite:
            print(f'Valor de saque maior que o limite de R$ {self.limite:.2f}.')

        elif numero_saques >= self.limite_saques:
            print(f'Limite de saques diários já atingidos.')

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia},
            C/C:\t{self.numero},
            Titular:\t{self.cliente.nome} 
            """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

def depositar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        conta = filtrar_conta(cliente)
        if conta:
            valor = float(input('Digite o valor do depósito: '))
            transacao = Deposito(valor)
            cliente.realizar_transacao(conta, transacao)
        else:
            print('Conta não encontrada.')
    else:
        print('Cliente não encontrado.')

def sacar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        conta = filtrar_conta(cliente)
        if conta:
            valor = float(input('Digite o valor de saque: '))
            transacao = Saque(valor)
            cliente.realizar_transacao(conta, transacao)
        else:
            print('Conta não encontrada.')
    else:
        print('Cliente não encontrado.')

def exibir_extrato(clientes):
    print("--------EXTRATO--------")
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        conta = filtrar_conta(cliente)
        if conta:
            transacoes = conta.historico.transacoes
            if transacoes:
                extrato = ""
                for transacao in transacoes:
                    extrato += f"{transacao['tipo']}: R$ {transacao['valor']:.2f} - Data: {transacao['data']}\n"
                print(f'Saldo atual: R$ {conta.saldo:.2f}')
                print(extrato)
            else:
                print("Conta não possui movimentações.")
    else:
        print("Cliente não encontrado.")


            
def main():
    clientes = []
    contas = []

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

    while True:
        opcao = input(menu).upper()

        if opcao == 'D':
            depositar(clientes)

        elif opcao == 'S':
            sacar(clientes)

        elif opcao == 'E':
            exibir_extrato(clientes)
        
        elif opcao == 'NU':
            criar_usuario(clientes)

        elif opcao == 'NC':
            numero_conta = len(contas) + 1
            conta = criar_conta(numero_conta, clientes, contas)

            if conta:
                contas.append(conta)

        elif opcao == 'LC':
            listar_conta(contas)
            
        elif opcao == 'Q':
            print("--------SAÍDA--------")
            break

        else:
            print('Opção inválida! Tente novamente.')

def criar_usuario(clientes):
    print("--------NOVO USUÁRIO--------")
    cpf = input("Digite o CPF (apenas número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Este CPF já existe na base de usuários.")
        return 
    nome = input("Digite o nome completo: ")
    data_nascimento = input("Digite a data de nascimento (DD-MM-AAAA): ")
    endereço = input("Digite o endereço: ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereço)
    clientes.append(cliente)
    print("Usuário cadastrado com sucesso!")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = None
    for cliente in clientes:
        if cliente.cpf == cpf:
            clientes_filtrados = cliente
    if clientes_filtrados:
        return clientes_filtrados
    else:
        return None

def filtrar_conta(cliente):
    if not cliente.contas:
        print("Cliente não possui contas!")
        return 
    return cliente.contas[0]

def criar_conta(numero_conta, clientes, contas):

    print("--------NOVA CONTA--------")
    cpf = input("Digite o CPF (apenas número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Usuário não encontrado! Favor cadastrar esse usuário na função 'Novo Usuário'.")
        return 
    conta = ContaCorrente.nova_conta(cliente=cliente, numero= numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print('Conta criada com sucesso!')

def listar_conta(contas):
    print("--------LISTAR CONTAS--------")
    if contas == []:
        print('Não existem contas no momento.')
        return
    for conta in contas:
        print(conta)

main()

