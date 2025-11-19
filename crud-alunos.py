import json

# Definir funções:
def cadastrar_aluno():
    email = str(input('Qual o email do aluno? '))
    nome = str(input('Qual o nome do aluno? '))
    turma = str(input('Qual a turma do aluno? '))
    with open("alunos.json", "r", encoding="utf-8") as arquivo:
        alunos = json.load(arquivo)
    novo = {"nome": nome, "email": email, "turma": turma}
    alunos.append (novo)
    with open("alunos.json", "w", encoding="utf-8") as arquivo:
        json.dump(alunos, arquivo, indent=4, ensure_ascii=False)
    print(f"Aluno {nome} cadastrado com sucesso.")

def listar_alunos():
    with open("alunos.json", "r", encoding="utf-8") as arquivo:
        alunos = json.load(arquivo)
    print("Lista de alunos:")
    for a in alunos:
        print(f"Nome: {a['nome']} - Turma: {a['turma']}")

def atualizar_aluno():
    with open("alunos.json", "r", encoding="utf-8") as arquivo:
        alunos = json.load(arquivo)
    # id = str(input('Qual o ID do aluno que deseja atualizar? '))
    # for a in alunos:
    #     if a["id"] == id:
    #         novo_nome = str(input('Qual o novo nome do aluno? '))
    #         novo_email = str(input('Qual o novo e-mail do aluno? '))
    #         nova_turma = str(input('Qual a nova turma do aluno? '))
    #         a['nome'] = novo_nome
    #         a['email'] = novo_email
    #         a['turma'] = nova_turma
    #         break
    with open("alunos.json", "w", encoding="utf-8") as arquivo:
        json.dump(alunos, arquivo, indent=4, ensure_ascii=False)
    print(f"Aluno atualizado com sucesso.")   

def deletar_aluno():
    with open("alunos.json", "r", encoding="utf-8") as arquivo:
        alunos = json.load(arquivo)
    id = str(input('Qual o ID do aluno que deseja deletar? '))
    for a in alunos:
        if a['id'] == id:
            alunos.remove(a)
            break
    with open("alunos.json", "w", encoding="utf-8") as arquivo:
        json.dump(alunos, arquivo, indent=4, ensure_ascii=False)
    print(f"Aluno deletado com sucesso.")
   

# Programa
while True:
    print('--MENU--')
    print('1) Cadastrar aluno\n2) Listar alunos\n3) Atualizar aluno\n'\
    '4) Deletar aluno\n5) Sair')
    opcao = int(input('Escolha uma opção do menu: '))
    while opcao != 1 and opcao != 2 and opcao != 3 and opcao !=4 and opcao != 5: #Pedir opções novamente caso necessário
        print("Opções inválidas. Por favor digite novamente")
        print('1) Cadastrar alunos\n2) Listar alunos\n 3) Atualizar aluno\n' \
        '4) Deletar aluno\n 5) Sair')
        opcao = int(input('Escolha uma opção do menu: '))
    #Opções:
    if opcao == 1:
        cadastrar_aluno()
    elif opcao == 2:
        listar_alunos()
    elif opcao == 3:
        atualizar_aluno()
    elif opcao == 4:
        deletar_aluno()
    else:
        print('Saindo do programa...')
        break


