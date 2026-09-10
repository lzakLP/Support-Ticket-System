tickets = []
proximo_id = 1


def criar_ticket(title, description):
    global proximo_id

    ticket = {
        "id": proximo_id,
        "title": title,
        "description": description,
        "status": "open",
    }

    tickets.append(ticket)

    proximo_id += 1


def listar_ticket():
    for ticket in tickets:
        print(f'ID: {ticket["id"]}')
        print(f'Title: {ticket["title"]}')
        print(f'Description: {ticket["description"]}')
        print(f'Status: {ticket["status"]}')
        print("----------------------------")


def buscar_ticket(id_ticket):
    for ticket in tickets:
        if ticket["id"] == id_ticket:
            return ticket

    return None


def atualizar_ticket(id_ticket, novo_status):
    status_validos = ["open", "in_progress", "closed"]

    if novo_status in status_validos:
        ticket = buscar_ticket(id_ticket)

        if ticket is not None:
            ticket["status"] = novo_status

        else:
            print("---------------------")
            print("Ticket não encontrado")
            print("---------------------")

    else:
        print("------------------")
        print(" Status Inválido")
        print("------------------")


def excluir_ticket(id_ticket):
    ticket = buscar_ticket(id_ticket)

    if ticket is not None:
        tickets.remove(ticket)
        print("---------------")
        print("Ticket Excluído")
        print("---------------")

    else:
        print("---------------------")
        print("Ticket não encontrado")
        print("---------------------")
        

def return_to_menu():
    while True:

        option = int(input("Enter 0 to return to the menu: "))

        if option == 0:
            break


executando = True

while executando:
    print("============================")
    print("   Support Ticket System")
    print("============================")
    print("1 - Criar ticket")
    print("2 - Listar tickets")
    print("3 - Buscar ticket")
    print("4 - Atualizar ticket")
    print("5 - Excluir ticket")
    print("0 - Sair")
    print("============================")
    
    
    try:
         opcao = int(input("Escolha uma opção: "))
     
    
    except ValueError:
         print("Opção Inválida")
    


    if opcao == 1:
        print("==========================")
        title = input("Digite o título do ticket: ")
        description = input("Digite a descrição do ticket: ")

        criar_ticket(title, description)
        
        return_to_menu()

    elif opcao == 2:
        listar_ticket()
        
        return_to_menu()
    

    elif opcao == 3:
        id_ticket = int(input("Digite o ID do ticket: "))

        ticket = buscar_ticket(id_ticket)

        if ticket is not None:
            print(f'ID: {ticket["id"]}')
            print(f'Title: {ticket["title"]}')
            print(f'Description: {ticket["description"]}')
            print(f'Status: {ticket["status"]}')
            print("----------------------------")
        else:
            print("Ticket não encontrado")
        
        return_to_menu()
        
        
    elif opcao == 4:
        id_ticket = int(input("Digite o ID do Ticket: "))
        novo_status = int(input("Digite o novo Status: "))
        
        atualizar_ticket(id_ticket, novo_status)
        
    elif opcao == 5:
        id_ticket = int(input("Digite o ID do Ticket: "))
        
        excluir_ticket(id_ticket)

    elif opcao == 0:
        executando = False
