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
             print("Ticket não encontrado")
             print("---------------------")
         
   
    else:
     print("Status Inválido")
     print("---------------")
     
     
def excluir_ticket(id_ticket):
    ticket = buscar_ticket(id_ticket)
    
    if ticket is not None:
         tickets.remove(ticket)
         print("Ticket Excluído")
         print("---------------")

    else:
         print("Ticket não encontrado")
         print("---------------------")


criar_ticket("PC não liga", "Sem sinal de energia")
criar_ticket("Impressora não funciona", "Papel preso no equipamento")

atualizar_ticket(89, "closed")
excluir_ticket(1)

listar_ticket()
