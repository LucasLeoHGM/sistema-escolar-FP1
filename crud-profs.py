import json

#def salvarDados
#def carregarDados

#def create

#def read

#def update

#def delete

while True:
    print('--MENU--')
    print('1) Cadastrar professor\n2) Listar professores\n 3) Atualizar professor\n' \
    '4) Deletar professor\n 5) Sair')
    opcao = int(input('Escolha uma opção do menu: '))
    if opcao == 1:
        id = int(input('Qual o ID do professor? '))
        email = str(input('Qual o e-amil do professor? '))
        nome = str(input('Qual o nome do professor? '))
        turma = str(input('Qual a turma do professor? '))
        materia = str(input('Qual a matéria do professor? '))
    elif opcao == 2:
        for i in professores:
            print(f'{i[nome] }')
