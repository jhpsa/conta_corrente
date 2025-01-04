from tinydb import TinyDB, Query #banco de dados utilizado
from datetime import date, datetime #manipulação de datas/tempo
from math import floor #arredondar números para baixo
from getpass import getpass #esconder input

#reconhece o arquivo cadastros.json como uma tabela de usuários com as informações do número da conta, senha, saldo atual, se é VIP ou não
cadastros = TinyDB('cadastros.json') #e se for VIP, indicador de saldo negativo e tempo em segundos entre a última vez que juros foram cobrados e 14/7/2023 00:00:00
#usuário VIP => conta: 00000, senha: 0000
#usuário normal => conta: 00001, senha: 0001

#cria o arquivo movimentacoes.json com uma tabela das movimetações com as informações do número da conta do usuário relacionado à movimentação,
movimentacoes = TinyDB('movimentacoes.json') #data e hora de quando a movimentação foi realizada, valor movimentado e descrição do ocorrido

cc = '' #vai armazenar o número da conta corrente do usuário logado
senha = '' #vai armazenar a senha do usuário logado

#função para cadastrar novos usuários
def cadastrar():
    cc = input("Insira os 5 dígitos da sua conta corrente: ")
    print("")
    while len(cc) != 5 or not(cc.isnumeric()): #checa se a entrada para a conta corrente tem 5 caracteres numéricos, senão pede outra entrada
        cc = input("Entrada inválida. Insira os 5 dígitos da sua conta corrente: ")
        print("")
    if cadastros.get(Query().cc == cc): #se a conta já existir, pede a senha para logar
        print("Conta já existente.\n")
        senha = input("Insira os 4 dígitos da sua senha: ")
        print("")
        while not(cadastros.get(Query().cc==cc).get("senha") == senha): #pede a senha enquanto não for a correta
            senha = input("Senha errada. Insira novamente os 4 dígitos da sua senha: ")
            print("")
        print("Logado com sucesso!\n")
    else:
        senha = input("Insira os 4 dígitos da sua senha: ")
        print("")
        while len(senha) != 4 or not(senha.isnumeric()): #checa se a entrada para a senha tem 4 caracteres numéricos, se não pede outra entrada
            senha = input("Entrada inválida. Insira os 4 dígitos da sua senha: ")
            print("")
        cadastros.insert({'cc': cc, 'senha': senha, 'saldo': 0, 'VIP': False }) #cria um novo usuário com a conta corrente e a senha inseridas na tabela de usuários
        print("Conta cadastrada!\n")
    return cc, senha

#função para logar usuários já existentes
def logar():
    cc = input("Insira os 5 dígitos da sua conta corrente: ")
    print("")
    while not(cadastros.get(Query().cc == cc)): #checa se existe usuário com essa conta, senão deixa logar com outra conta ou cadastrar novo usuário
        res = input("Conta corrente inexistente. Deseja tentar logar novamente (1) ou criar uma nova conta (2)? ")
        print("")
        while res != '1' and res != '2':
            res = input("Resposta inválida. Deseja tentar logar novamente (1) ou criar uma nova conta (2)? ")
            print("")
        if res == '1':
            cc = input("Insira os 5 dígitos da sua conta corrente: ")
            print("")
        else:
            cc, senha = cadastrar()
            return cc, senha
    senha = input("Insira os 4 dígitos da sua senha: ")
    print("")
    while not(cadastros.get(Query().senha == senha)): #pede a senha enquanto não for a correta
        senha = input("Senha errada. Insira novamente os 4 dígitos da sua senha: ")
        print("")
    print("Logado com sucesso!\n")
    return cc, senha

print("-"*100+"\n")

#checa se vai logar usuário já existente ou criar um novo
res = input("Já tem cadastro? (S/N) ")
print("")

while res != "S" and res != "N":
    res = input("Resposta inválida. Já tem cadastro? (S/N) ")
    print("")

if res == "N":
    cc, senha = cadastrar()

else:
    cc, senha = logar()

#loop infinito para as ações do usuário logado/cadastrado
while True:
    print("-"*100+"\n")

    #mostra as possibilidades
    print("Ações:\n")

    #apenas para usuários VIP
    if cadastros.get(Query().cc==cc).get("VIP"):

        #se o usuário tem saldo negativo, checa se pelo menos 1 minuto se passou para reduzir o saldo
        if cadastros.get(Query().cc==cc).get("negativado"):
            d = datetime.now() - datetime(2023, 7, 14)
            minutes = floor((d.total_seconds() - cadastros.get(Query().cc==cc).get("time")) / 60.0 )
            if minutes >= 1:
                cadastros.update({'saldo': cadastros.get(Query().cc==cc).get("saldo") * 1.001 ** minutes}, Query().cc==cc)
                cadastros.update({'time': d.total_seconds()}, Query().cc==cc)
        
        #mostra opção da visita do gerente
        print("0 - Solicitar visita do gerente")
    
    print("1 - Ver Saldo")
    print("2 - Extrato")
    print("3 - Saque")
    print("4 - Depósito")
    print("5 - Transferência")
    print("6 - Trocar de usuário")
    print("7 - Sair\n")

    #checa qual ação deve ser executada, a menos que a entrada seja diferente de 1-7 (ou 0-7 para VIPs)
    op = input("Digite o número da ação desejada: ")
    print("")

    match op:
        
        #visita do gerente
        case "0":

            #checa se usuário é VIP, senão considera entrada inválida
            if cadastros.get(Query().cc==cc).get("VIP"):

                #confirma a ação antes de executar
                res = input("Deseja confirmar a visita do gerente? Serão debitados R$ 50.00 do seu saldo. (S/N) ")
                print("")
                while res != "S" and res != "N":
                        res = input("Entrada inválida. Deseja confirmar a visita do gerente? Serão debitados R$ 50.00 do seu saldo. (S/N) ")
                        print("")
                if res == "S":

                    #checa se a ação vai fazer o saldo ficar negativo
                    if cadastros.get(Query().cc==cc).get("saldo") >= 0 and cadastros.get(Query().cc==cc).get("saldo") - 50 < 0:
                        cadastros.update({'negativado': True}, Query().cc==cc)
                        d = datetime.now() - datetime(2023, 7, 14)
                        cadastros.update({'time': d.total_seconds()}, Query().cc==cc)
                    cadastros.update({'saldo': cadastros.get(Query().cc==cc).get("saldo") - 50}, Query().cc==cc)
                    movimentacoes.insert({'cc': cc, 'data':  date.today().strftime("%d/%m/%Y"), 'hora': datetime.now().strftime("%H:%M"), 'valor': -50, 'descricao': "Visita do gerente."})
                    print("Visita do gerente solicitada.\n")
                else:
                    print("Visita do gerente cancelada.\n")
            else:
                print("Opção inválida.\n")
            
            getpass("Pressione Enter para continuar... ")
            print("")

        #saldo
        case "1":

            #faz com que um valor entre -0.01 e 0.00 apareça como 0.00 em vez de -0.00
            if cadastros.get(Query().cc==cc).get("saldo") < 0 and cadastros.get(Query().cc==cc).get("saldo") > -0.01:
                print("Saldo: R$ 0.00")
            else:
                print("Saldo: R$", "{:.2f}".format(cadastros.get(Query().cc==cc).get("saldo"))+"\n")
            
            getpass("Pressione Enter para continuar... ")
            print("")
        
        #extrato
        case "2":
            print("Movimentações:\n")
            extrato = movimentacoes.search(Query().cc==cc) #procura todas as movimentações realizadas pelo usuário com a conta logada
            for mov in extrato:

                #se o valor da movimentação for negativo adiciona os parênteses
                if mov.get('valor') > -0.01:
                    print("Data:", mov.get('data'), "Hora:", mov.get('hora'), "Descrição:", mov.get('descricao'), "Valor: R$", "{:.2f}".format(mov.get('valor')))
                else:
                    print("Data:", mov.get('data'), "Hora:", mov.get('hora'), "Descrição:", mov.get('descricao'), "Valor: R$ (" + "{:.2f}".format(abs(mov.get('valor'))) + ")")
            print("")
            
            getpass("Pressione Enter para continuar... ")
            print("")

        #saque
        case "3":
            qtd = float(input("Digite o valor desejado para o saque: "))
            print("")

            while qtd <= 0:
                print("O valor precisa ser positivo.\n")
                res = input("Deseja sacar outra quantia? (S/N) ")
                print("")
                while res != "S" and res != "N":
                    res = input("Entrada inválida. Deseja sacar outra quantia? (S/N) ")
                    print("")
                if res == "S":
                    qtd = float(input("Digite o valor desejado para o saque: "))
                    print("")
                else:
                    break
            else:

                #se não for VIP não deixa sacar mais que o saldo atual e deixa inserir outro valor para a entrada
                if not(cadastros.get(Query().cc==cc).get("VIP")):
                    while cadastros.get(Query().cc==cc).get("saldo") < qtd:
                        print("Não é possível sacar um valor superior ao do saldo atual.\n")
                        res = input("Deseja sacar outra quantia? (S/N) ")
                        print("")
                        while res != "S" and res != "N":
                            res = input("Entrada inválida. Deseja sacar outra quantia? (S/N) ")
                            print("")
                        if res == "S":
                            qtd = float(input("Digite o valor desejado para o saque: "))
                            print("")
                        else:
                            break
                    else:
                        cadastros.update({'saldo': cadastros.get(Query().cc==cc).get("saldo") - qtd}, Query().cc==cc)
                        movimentacoes.insert({'cc': cc, 'data':  date.today().strftime("%d/%m/%Y"), 'hora': datetime.now().strftime("%H:%M:%S"), 'valor': -qtd, 'descricao': "Saque."})
                        print("Saque realizado com sucesso!\n")
                
                #se for VIP checa se o saque vai fazer o saldo ficar negativo
                else:
                    if cadastros.get(Query().cc==cc).get("saldo") >= 0 and cadastros.get(Query().cc==cc).get("saldo") - qtd < 0:
                        cadastros.update({'negativado': True}, Query().cc==cc)
                        d = datetime.now() - datetime(2023, 7, 14)
                        cadastros.update({'time': d.total_seconds()}, Query().cc==cc)
                    cadastros.update({'saldo': cadastros.get(Query().cc==cc).get("saldo") - qtd}, Query().cc==cc)
                    movimentacoes.insert({'cc': cc, 'data':  date.today().strftime("%d/%m/%Y"), 'hora': datetime.now().strftime("%H:%M:%S"), 'valor': -qtd, 'descricao': "Saque."})
                    print("Saque realizado com sucesso!\n")
                
                getpass("Pressione Enter para continuar... ")
                print("")

        #depósito
        case "4":
            qtd = float(input("Digite o valor desejado para o depósito: "))
            print("")

            while qtd <= 0:
                print("O valor precisa ser positivo.\n")
                res = input("Deseja depositar outra quantia? (S/N) ")
                print("")
                while res != "S" and res != "N":
                    res = input("Entrada inválida. Deseja depositar outra quantia? (S/N) ")
                    print("")
                if res == "S":
                    qtd = float(input("Digite o valor desejado para o depósito: "))
                    print("")
                else:
                    break
            else:

                #se for VIP checa se o depósito vai tirar o saldo do negativo
                if cadastros.get(Query().cc==cc).get("VIP") and cadastros.get(Query().cc==cc).get("saldo") < 0 and cadastros.get(Query().cc==cc).get("saldo") + qtd >= 0:
                        cadastros.update({'negativado': False}, Query().cc==cc)
                cadastros.update({'saldo': cadastros.get(Query().cc==cc).get("saldo") + qtd}, Query().cc==cc)
                movimentacoes.insert({'cc': cc, 'data':  date.today().strftime("%d/%m/%Y"), 'hora': datetime.now().strftime("%H:%M:%S"), 'valor': qtd, 'descricao': "Depósito."})
                print("Depósito realizado com sucesso!\n")
            
            getpass("Pressione Enter para continuar... ")
            print("")

        #transferênca
        case "5":
            conta = input("Insira os 5 dígitos da conta corrente para a qual deseja realizar a tranferência: ")
            print("")

            #checa se existe usuário com a conta a receber a transferência e se não é a mesma do usuário logado, se for deixa escolher outra conta
            while conta == cc or not(cadastros.get(Query().cc==conta)):
                if conta == cc:
                    print("Não é possível realizar uma transferência para sua própria conta.\n")
                elif not(cadastros.get(Query().cc==conta)):
                    print("Conta inexistente.\n")
                res = input("Deseja escolher outra conta? (S/N) ")
                print("")
                while res != "S" and res != "N":
                    res = input("Entrada inválida. Deseja escolher outra conta? (S/N) ")
                    print("")
                if res == "S":
                    conta = input("Insira os 5 dígitos da conta corrente para a qual deseja realizar a tranferência: ")
                    print("")
                else:
                    break
            else:

                #se não for VIP limita a transferência para o menor entre R$ 1000.00 e o saldo atual + 8, se exceder esse valor deixa inserir outra entrada para ele
                if not(cadastros.get(Query().cc==cc).get("VIP")):
                    qtd = float(input("Qual o valor desejado para a transferência? (Serão debitados R$ 8.00 adicionais) "))
                    print("")

                    while qtd <= 0:
                        print("O valor precisa ser positivo.\n")
                        res = input("Deseja transferir outra quantia? (S/N) ")
                        print("")
                        while res != "S" and res != "N":
                            res = input("Entrada inválida. Deseja transferir outra quantia? (S/N) ")
                            print("")
                        if res == "S":
                            qtd = float(input("Qual o valor desejado para a transferência? (Serão debitados R$ 8.00 adicionais) "))
                            print("")
                        else:
                            break
                    else:
                        while qtd + 8 > cadastros.get(Query().cc==cc).get("saldo"):
                            print("Não é possível transferir um valor superior ao do saldo atual.\n")
                            res = input("Deseja transferir outra quantia? (S/N) ")
                            print("")
                            while res != "S" and res != "N":
                                res = input("Entrada inválida. Deseja transferir outra quantia? (S/N) ")
                                print("")
                            if res == "S":
                                qtd = float(input("Qual o valor desejado para a transferência? (Serão debitados R$ 8.00 adicionais) "))
                                print("")
                            else:
                                break
                        else:
                            while qtd > 1000:
                                print("Não é permitido realizar uma transferência superior a R$ 1000.00.\n")
                                res = input("Deseja escolher outro valor para a transferência? (S/N) ")
                                print("")
                                while res != "S" and res != "N":
                                    res = input("Entrada inválida. Deseja escolher outro valor para a transferência? (S/N) ")
                                    print("")
                                if res == "S":
                                    qtd = float(input("Qual o valor desejado para a transferência? "))
                                    print("")
                                else:
                                    break
                            else:
                                cadastros.update({'saldo': cadastros.get(Query().cc==cc).get("saldo") - qtd - 8}, Query().cc==cc)

                                #inclui o débito de R$ 8.00 no extrato
                                movimentacoes.insert({'cc': cc, 'data':  date.today().strftime("%d/%m/%Y"), 'hora': datetime.now().strftime("%H:%M:%S"), 'valor': -qtd-8, 'descricao': "Transferência enviada para " + str(conta) + " (debitados R$ 8.00)."})
                                
                                #se o usuário que receberá a transferência for VIP, checa se a transferência vai fazer o saldo sair do negativo, se for o caso aplica os juros
                                if cadastros.get(Query().cc==conta).get("VIP") and cadastros.get(Query().cc==conta).get("saldo") < 0 and cadastros.get(Query().cc==conta).get("saldo") + qtd >= 0:
                                    cadastros.update({'negativado': False}, Query().cc==conta)
                                    d = datetime.now() - datetime(2023, 7, 14)
                                    minutes = floor((d.total_seconds() - cadastros.get(Query().cc==conta).get("time")) / 60.0 )
                                    if minutes >= 1:
                                        cadastros.update({'saldo': cadastros.get(Query().cc==conta).get("saldo") * 1.001 ** minutes}, Query().cc==conta)
                                        cadastros.update({'time': d.total_seconds()}, Query().cc==conta)
                                
                                cadastros.update({'saldo': cadastros.get(Query().cc==conta).get("saldo") + qtd}, Query().cc==conta)
                                movimentacoes.insert({'cc': conta, 'data':  date.today().strftime("%d/%m/%Y"), 'hora': datetime.now().strftime("%H:%M:%S"), 'valor': qtd, 'descricao': "Transferência recebida de " + str(cc) + "."})
                                print("Transferência de R$", "{:.2f}".format(qtd), "para a conta", conta, "realizada com sucesso.")
                else:
                    qtd = float(input("Qual o valor desejado para a transferência? (Adicionalmente será debitado 0.8% do valor) "))
                    print("")

                    while qtd <= 0:
                        print("O valor precisa ser positivo.\n")
                        res = input("Deseja transferir outra quantia? (S/N) ")
                        print("")
                        while res != "S" and res != "N":
                            res = input("Entrada inválida. Deseja transferir outra quantia? (S/N) ")
                            print("")
                        if res == "S":
                            qtd = float(input("Qual o valor desejado para a transferência? (Adicionalmente será debitado 0.8% do valor) "))
                            print("")
                        else:
                            break
                    else:
                        #checa se a transferência a ser realizada pelo usuário VIP, incluindo o débito de 0.8% do valor, vai fazer o saldo ficar negativo
                        if cadastros.get(Query().cc==cc).get("saldo") >= 0 and cadastros.get(Query().cc==cc).get("saldo") - 1.008 * qtd < 0:
                            cadastros.update({'negativado': True}, Query().cc==cc)
                            d = datetime.now() - datetime(2023, 7, 14)
                            cadastros.update({'time': d.total_seconds()}, Query().cc==cc)

                        cadastros.update({'saldo': cadastros.get(Query().cc==cc).get("saldo") - 1.008 * qtd}, Query().cc==cc)

                        #inclui a conta do 0.8% no extrato
                        movimentacoes.insert({'cc': cc, 'data':  date.today().strftime("%d/%m/%Y"), 'hora': datetime.now().strftime("%H:%M:%S"), 'valor': -qtd, 'descricao': "Transferência enviada para " + str(conta) + " (debitados 0.8" + "%" + "de " + str(qtd) + " = R$ " + "{:.2f}".format(0.008 * qtd) + ")."})
                        
                        #se o usuário que receberá a transferência for VIP, checa se a transferência vai fazer o saldo sair do negativo, se for o caso aplica os juros
                        if cadastros.get(Query().cc==conta).get("VIP") and cadastros.get(Query().cc==conta).get("saldo") < 0 and cadastros.get(Query().cc==conta).get("saldo") + qtd >= 0:
                            cadastros.update({'negativado': False}, Query().cc==conta)
                            d = datetime.now() - datetime(2023, 7, 14)
                            minutes = floor((d.total_seconds() - cadastros.get(Query().cc==conta).get("time")) / 60.0 )
                            if minutes >= 1:
                                cadastros.update({'saldo': cadastros.get(Query().cc==conta).get("saldo") * 1.001 ** minutes}, Query().cc==conta)
                                cadastros.update({'time': d.total_seconds()}, Query().cc==conta)
                        
                        cadastros.update({'saldo': cadastros.get(Query().cc==conta).get("saldo") + qtd}, Query().cc==conta)
                        movimentacoes.insert({'conta': cc, 'data':  date.today().strftime("%d/%m/%Y"), 'hora': datetime.now().strftime("%H:%M:%S"), 'valor': qtd, 'descricao': "Transferência recebida de " + str(cc) + "."})
                        print("Transferência de R$", "{:.2f}".format(qtd), "para a conta", conta, "realizada com sucesso.\n")
            
            getpass("Pressione Enter para continuar... ")
            print("")

        #troca de usuário
        case "6":
            cc, senha = logar() #loga (ou cadastra) o usuário
            print("Usuário trocado!\n")
            
            getpass("Pressione Enter para continuar... ")
            print("")

        #sair
        case "7":
            print("Até a próxima!\n")
            break #quebra o loop e encerra a execução do programa

        #entrada inválida    
        case _:
            print("Opção inválida.\n")
            
            getpass("Pressione Enter para continuar... ")
            print("")