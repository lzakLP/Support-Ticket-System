"""
Sistema de chamados pelo terminal, permite: 
------------------------------------------------

 -Criar chamados;
 -Consultar chamados;
 -Atualizar chamados;
 -Excluir chamados.
 
------------------------------------------------
As funções validam e manipulam os dados; 
O menu recebe as entradas e exibe os resultados.

__________________________________________________
"""
tickets = []
proximo_id = 1
STATUS_VALIDOS = ["open", "in_progress", "closed"]


def criar_ticket(title, description):
    global proximo_id

    title = title.strip()
    description = description.strip()

    if not title:
        raise ValueError("O título é obrigatório.")
    if not description:
        raise ValueError("A descrição é obrigatória.")

    ticket = {
        "id": proximo_id,
        "title": title,
        "description": description,
        "status": "open",
    }

    tickets.append(ticket)
    proximo_id += 1
    return ticket


def listar_tickets():
    return tickets.copy()


def buscar_ticket(id_ticket):
    for ticket in tickets:
        if ticket["id"] == id_ticket:
            return ticket

    return None


def atualizar_ticket(id_ticket, novo_status):
    novo_status = novo_status.strip().lower()

    if novo_status not in STATUS_VALIDOS:
        raise ValueError("Status inválido. Use open, in_progress ou closed.")

    ticket = buscar_ticket(id_ticket)

    if ticket is None:
        raise ValueError("Chamado não encontrado.")

    ticket["status"] = novo_status
    return ticket


def excluir_ticket(id_ticket):
    ticket = buscar_ticket(id_ticket)

    if ticket is None:
        raise ValueError("Chamado não encontrado.")

    tickets.remove(ticket)
    return ticket


# A partir daqui ficam as funções de interação com o terminal.
def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def exibir_ticket(ticket):
    print(f'ID: {ticket["id"]}')
    print(f'Título: {ticket["title"]}')
    print(f'Descrição: {ticket["description"]}')
    print(f'Status: {ticket["status"]}')
    print("-" * 42)


def main():
    while True:
        print("\n" + "=" * 42)
        print("           SISTEMA DE CHAMADOS")
        print("=" * 42)
        print("1 - Criar chamado")
        print("2 - Listar chamados")
        print("3 - Buscar chamado por ID")
        print("4 - Atualizar status")
        print("5 - Excluir chamado")
        print("0 - Sair")

        opcao = ler_inteiro("Escolha uma opção: ")

        if opcao == 0:
            print("Sistema encerrado.")
            break

        try:
            if opcao == 1:
                title = input("Título: ")
                description = input("Descrição: ")

                ticket = criar_ticket(title, description)

                print(f'Chamado {ticket["id"]} criado com sucesso.')

            elif opcao == 2:
                chamados = listar_tickets()

                if not chamados:
                    print("Nenhum chamado cadastrado.")
                else:
                    for ticket in chamados:
                        exibir_ticket(ticket)

            elif opcao == 3:
                id_ticket = ler_inteiro("ID do chamado: ")
                ticket = buscar_ticket(id_ticket)

                if ticket is None:
                    print("Chamado não encontrado.")
                else:
                    exibir_ticket(ticket)

            elif opcao == 4:
                id_ticket = ler_inteiro("ID do chamado: ")
                novo_status = input(
                    "Novo status (open, in_progress, closed): "
                )

                ticket = atualizar_ticket(id_ticket, novo_status)

                print(
                    f'Chamado {ticket["id"]} '
                    f'atualizado para {ticket["status"]}.'
                )

            elif opcao == 5:
                id_ticket = ler_inteiro("ID do chamado: ")
                ticket = excluir_ticket(id_ticket)

                print(f'Chamado {ticket["id"]} excluído com sucesso.')

            else:
                print("Opção inválida. Escolha um número de 0 a 5.")

        except ValueError as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
