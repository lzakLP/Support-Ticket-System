"""
Terminal-based ticket management: create, read, update, and delete tickets.
Functions manage in-memory data; the menu handles input and output.
This introductory version loses its tickets when the process exits.
"""
tickets = []
next_id = 1
VALID_STATUSES = ["open", "in_progress", "closed"]


def create_ticket(title, description):
    global next_id

    title = title.strip()
    description = description.strip()

    if not title:
        raise ValueError("A title is required.")
    if not description:
        raise ValueError("A description is required.")

    ticket = {
        "id": next_id,
        "title": title,
        "description": description,
        "status": "open",
    }

    tickets.append(ticket)
    next_id += 1
    return ticket


def list_tickets():
    return tickets.copy()


def get_ticket(ticket_id):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    return None


def update_ticket(ticket_id, new_status):
    new_status = new_status.strip().lower()

    if new_status not in VALID_STATUSES:
        raise ValueError("Invalid status. Use open, in_progress, or closed.")

    ticket = get_ticket(ticket_id)

    if ticket is None:
        raise ValueError("Ticket not found.")

    ticket["status"] = new_status
    return ticket


def delete_ticket(ticket_id):
    ticket = get_ticket(ticket_id)

    if ticket is None:
        raise ValueError("Ticket not found.")

    tickets.remove(ticket)
    return ticket


# The following functions handle terminal interaction.
def read_integer(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Invalid input. Enter an integer.")


def display_ticket(ticket):
    print(f'ID: {ticket["id"]}')
    print(f'Title: {ticket["title"]}')
    print(f'Description: {ticket["description"]}')
    print(f'Status: {ticket["status"]}')
    print("-" * 42)


def main():
    while True:
        print("\n" + "=" * 42)
        print("           SUPPORT TICKET SYSTEM")
        print("=" * 42)
        print("1 - Create ticket")
        print("2 - List tickets")
        print("3 - Find ticket by ID")
        print("4 - Update status")
        print("5 - Delete ticket")
        print("0 - Exit")

        option = read_integer("Choose an option: ")

        if option == 0:
            print("System stopped.")
            break

        try:
            if option == 1:
                title = input("Title: ")
                description = input("Description: ")

                ticket = create_ticket(title, description)

                print(f'Ticket {ticket["id"]} created successfully.')

            elif option == 2:
                stored_tickets = list_tickets()

                if not stored_tickets:
                    print("No tickets found.")
                else:
                    for ticket in stored_tickets:
                        display_ticket(ticket)

            elif option == 3:
                ticket_id = read_integer("Ticket ID: ")
                ticket = get_ticket(ticket_id)

                if ticket is None:
                    print("Ticket not found.")
                else:
                    display_ticket(ticket)

            elif option == 4:
                ticket_id = read_integer("Ticket ID: ")
                new_status = input(
                    "New status (open, in_progress, closed): "
                )

                ticket = update_ticket(ticket_id, new_status)

                print(
                    f'Ticket {ticket["id"]} '
                    f'updated to {ticket["status"]}.'
                )

            elif option == 5:
                ticket_id = read_integer("Ticket ID: ")
                ticket = delete_ticket(ticket_id)

                print(f'Ticket {ticket["id"]} deleted successfully.')

            else:
                print("Invalid option. Choose a number from 0 to 5.")

        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
