"""Check the original terminal application's behavior after translation."""

from contextlib import redirect_stdout
import io
import unittest
from unittest.mock import patch

import System


class TerminalTicketTest(unittest.TestCase):
    def setUp(self):
        System.tickets.clear()
        System.next_id = 1

    def test_crud_normalization_and_ids(self):
        ticket = System.create_ticket("  No internet  ", "  Network disconnected  ")
        self.assertEqual(ticket["title"], "No internet")
        self.assertEqual(ticket["description"], "Network disconnected")
        self.assertEqual(ticket["status"], "open")
        self.assertIs(System.get_ticket(1), ticket)
        self.assertIsNone(System.get_ticket(999))
        self.assertEqual(System.list_tickets(), [ticket])
        self.assertEqual(System.update_ticket(1, " CLOSED ")["status"], "closed")
        self.assertIs(System.delete_ticket(1), ticket)
        self.assertEqual(System.create_ticket("Another ticket", "Details")["id"], 2)

    def test_invalid_input_preserves_state(self):
        for title, description in [(" ", "Details"), ("Title", " ")]:
            with self.subTest(title=title, description=description):
                with self.assertRaises(ValueError):
                    System.create_ticket(title, description)
        self.assertEqual(System.tickets, [])
        self.assertEqual(System.next_id, 1)
        ticket = System.create_ticket("No internet", "Network disconnected")
        with self.assertRaises(ValueError):
            System.update_ticket(1, "cancelled")
        self.assertEqual(ticket["status"], "open")
        with self.assertRaisesRegex(ValueError, "Ticket not found"):
            System.delete_ticket(999)

    def test_menu_handles_invalid_input_and_completes_crud(self):
        answers = [
            "abc", "99", "2", "1", "Network", "Connection failed",
            "3", "abc", "1", "4", "1", " CLOSED ", "5", "1", "0",
        ]
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(output):
            System.main()
        for message in [
            "Invalid input", "Invalid option", "No tickets found",
            "created successfully", "Title: Network", "updated to closed",
            "deleted successfully", "System stopped",
        ]:
            self.assertIn(message, output.getvalue())
        self.assertEqual(System.tickets, [])


if __name__ == "__main__":
    unittest.main()
