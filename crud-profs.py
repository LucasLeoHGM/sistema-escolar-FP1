import json
professores = []

def salvar_dados():
    with open("professores.json", "w", encoding = "utf-8") as arquivo:
        json.dump(professores, arquivo, indent=4, ensure_ascii=False)

def carregar_dados():
    try:
        with open("professores.joson", "r", encoding= "utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:   
        return []
    
professores = carregar_dados()
#def salvarDados
#def carregarDados

#def create

#def read

#def update

#def delete

while True:
    print('--MENU--')
    print('1) Cadastrar professor\n2) Listar professores\n3) Atualizar professor\n' \
    '4) Deletar professor\n5) Sair')
    opcao = int(input('Escolha uma opção do menu: '))
    if opcao == 1:
        id = int(input('Qual o ID do professor? '))
        email = str(input('Qual o e-amil do professor? '))
        nome = str(input('Qual o nome do professor? '))
        turma = str(input('Qual a turma do professor? '))
        materia = str(input('Qual a matéria do professor? '))
        professor = {
            "id": id,
            "nome": nome,
            "email": email,
            "turma": turma,
            "materia": materia,

        }

        professores.append(professor)
        print("Professor cadastrado com sucesso")
    elif opcao == 2:
        for i in professores:
            print({i["nome"] })

    elif opcao == 3:
        id_buscar = int(input("Informe o ID do professor que deseja atualizar: "))
        for p in professores:
            if p["id"] ==  id_buscar:
                print(f"Professor(a) selecionado: {p['nome']}")
                nova_turma = input("Informe a nova turma do professor: ")
                nova_materia = input("Informe a nova matéria do professor: ")

                if nova_turma:
                    p["turma"] =  nova_turma
                if nova_materia:
                    p["materia"] = nova_materia
                
                salvar_dados()

                print("Dados atualizados!")
                break

    elif opcao == 4:
        id_delete = int(input("Informe o Id do professor(a) que deseja deletar: "))

        for p in professores:
            if p["id"] == id_delete:
                confirmar = input(f"Tem certeza que deseja deletar {p['nome']} ?\n(s/n)").lower()
                if confirmar == "s":
                    professores.remove(p)
                    salvar_dados()
                    print("Professor(a) removido com sucesso")
                else:
                    print("Operação cancelada")
                    break
            else:
                print("Professor(a) não encontrado!")
            
    elif opcao == 5:
        print("Saindo...")
        break

    else:
        print("Opção inválida, tente novamente")


