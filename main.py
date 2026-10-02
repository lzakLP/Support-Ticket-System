"""
Receive HTTP requests, validate ticket data, and persist it with SQLite.
Explore and test the available operations at /docs.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Path, Response

import database
from schemas import TicketCreate, TicketRead, TicketUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run once at startup without deleting an existing table.
    database.create_tables()
    yield


app = FastAPI(
    title="Support Ticket System",
    description="A learning project for Python, SQL, and databases with FastAPI and SQLite.",
    version="0.2.0",
    lifespan=lifespan,
)


@app.post("/tickets", response_model=TicketRead, status_code=201)
def create_ticket(data: TicketCreate):
    return database.create_ticket(data.title, data.description)


@app.get("/tickets", response_model=list[TicketRead])
def list_tickets():
    return database.list_tickets()


@app.get("/tickets/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: int = Path(gt=0)):
    ticket = database.get_ticket(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return ticket


@app.patch("/tickets/{ticket_id}", response_model=TicketRead)
def update_ticket(data: TicketUpdate, ticket_id: int = Path(gt=0)):
    ticket = database.update_ticket(ticket_id, data.status)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return ticket


@app.delete("/tickets/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int = Path(gt=0)):
    deleted = database.delete_ticket(ticket_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return Response(status_code=204)
