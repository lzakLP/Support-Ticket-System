"""Behavior tests use temporary databases and never modify the user database."""

import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

import database
from main import app


class TicketAPITest(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.db_path = Path(self.directory.name) / "test.db"
        self.patch_db = patch.object(database, "DB_PATH", self.db_path)
        self.patch_db.start()
        self.addCleanup(self.patch_db.stop)
        self.client = self.enterContext(TestClient(app))

    def create(self):
        return self.client.post(
            "/tickets", json={"title": "  No internet  ", "description": "  Network disconnected  "}
        )

    def test_crud_cycle_and_id_after_deletion(self):
        self.assertEqual(self.client.get("/tickets").json(), [])
        response = self.create()
        self.assertEqual(response.status_code, 201)
        ticket = response.json()
        self.assertEqual(ticket, {
            "id": 1, "title": "No internet", "description": "Network disconnected", "status": "open"
        })
        self.assertEqual(self.client.get("/tickets/1").json(), ticket)
        self.assertEqual(len(self.client.get("/tickets").json()), 1)
        response = self.client.patch("/tickets/1", json={"status": " IN_PROGRESS "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "in_progress")
        response = self.client.delete("/tickets/1")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertEqual(self.client.get("/tickets").json(), [])
        self.assertEqual(self.create().json()["id"], 2)

    def test_invalid_fields_do_not_create_tickets(self):
        for body in [
            {"title": "   ", "description": "x"},
            {"title": "x", "description": "\t\n"},
            {"title": "x"},
            {"title": 123, "description": "x"},
            {"title": "x", "description": "x", "id": 99},
        ]:
            with self.subTest(body=body):
                self.assertEqual(self.client.post("/tickets", json=body).status_code, 422)
        self.assertEqual(self.client.get("/tickets").json(), [])
        self.assertEqual(self.create().json()["id"], 1)

    def test_invalid_status_preserves_data(self):
        self.create()
        for value in ["cancelled", "", 1, None]:
            with self.subTest(value=value):
                response = self.client.patch("/tickets/1", json={"status": value})
                self.assertEqual(response.status_code, 422)
        self.assertEqual(self.client.get("/tickets/1").json()["status"], "open")

    def test_missing_ticket_id(self):
        self.assertEqual(self.client.get("/tickets/999").status_code, 404)
        self.assertEqual(self.client.patch("/tickets/999", json={"status": "closed"}).status_code, 404)
        self.assertEqual(self.client.delete("/tickets/999").status_code, 404)

    def test_invalid_ticket_id(self):
        for value in ["abc", "0", "-1", "1.5"]:
            with self.subTest(value=value):
                self.assertEqual(self.client.get(f"/tickets/{value}").status_code, 422)

    def test_persistence_in_another_process(self):
        self.create()
        code = """
import os
from pathlib import Path
from fastapi.testclient import TestClient
import database
from main import app
database.DB_PATH = Path(os.environ['TICKET_TEST_DB'])
with TestClient(app) as client:
    response = client.get('/tickets/1')
    assert response.status_code == 200
    assert response.json()['title'] == 'No internet'
    response = client.post('/tickets', json={'title': 'Another ticket', 'description': 'Test'})
    assert response.json()['id'] == 2
"""
        env = {**os.environ, "TICKET_TEST_DB": str(self.db_path)}
        subprocess.run(
            [sys.executable, "-B", "-c", code],
            cwd=Path(__file__).resolve().parent,
            env=env, check=True, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(len(self.client.get("/tickets").json()), 2)

    def test_quotes_and_sql_are_treated_as_data(self):
        title = "Printer's tray'); DROP TABLE tickets; --"
        response = self.client.post("/tickets", json={"title": title, "description": "Test"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.get("/tickets/1").json()["title"], title)
        self.assertEqual(len(self.client.get("/tickets").json()), 1)

    def test_api_documentation_and_routes(self):
        self.assertEqual(self.client.get("/docs").status_code, 200)
        schema = self.client.get("/openapi.json").json()
        self.assertIn("post", schema["paths"]["/tickets"])
        self.assertIn("patch", schema["paths"]["/tickets/{ticket_id}"])


if __name__ == "__main__":
    unittest.main()
