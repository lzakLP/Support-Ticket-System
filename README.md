# Support Ticket System

A learning project built to deepen my understanding of **Python, SQL, and relational databases** through a practical support-ticket application.

The project started as a terminal program with an in-memory list. It now includes a **FastAPI REST API backed by SQLite**, while retaining the terminal version as an earlier learning stage. The goal is to understand how Python functions, validation, HTTP requests, SQL statements, and persistent storage work together.

## Current version: 0.2.0

### What changed

- Added a FastAPI API for creating, listing, retrieving, updating, and deleting tickets.
- Replaced in-memory storage in the API with a persistent SQLite database.
- Added Pydantic models for request validation and response formats.
- Added input normalization, positive ticket-ID validation, and clear HTTP errors.
- Added database constraints and parameterized SQL queries.
- Added automated tests, including persistence checks in a separate process.
- Translated identifiers, comments, messages, examples, and tests into English.
- Preserved and translated `System.py`, the introductory terminal application.
- Updated the setup instructions and documented the learning goals and current scope.

## Learning goals

This project is intended to help me build practical knowledge of:

- **Python:** functions, conditionals, loops, collections, exceptions, modules, type annotations, classes, and context managers.
- **SQL:** `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `WHERE`, and `ORDER BY`.
- **Databases:** tables, rows, columns, primary keys, constraints, connections, transactions, and persistence.
- **APIs:** HTTP methods, endpoints, JSON request bodies, response models, and status codes.
- **Software development:** separation of responsibilities, automated testing, Git, and documentation.

The database used here is **SQLite**. SQL is the language used to query it; Microsoft SQL Server and SQL Server Management Studio are separate technologies and are not used in this version.

## Features

- Create tickets with a required title and description.
- List tickets or retrieve one by ID.
- Update a ticket's status to `open`, `in_progress`, or `closed`.
- Delete tickets.
- Reject empty fields, unsupported statuses, unexpected request fields, and invalid IDs.
- Normalize surrounding whitespace and status capitalization.
- Keep API data after stopping and restarting the server.
- Explore and try requests through interactive documentation at `/docs`.

New tickets receive an automatically generated ID and the default status `open`.
Updating currently changes only the status; title and description editing is not implemented.

## Technology stack

| Technology | Purpose |
|---|---|
| Python | Application logic and the built-in `sqlite3` database interface |
| FastAPI | API routing, request handling, and interactive documentation |
| Pydantic | Data validation and response schemas |
| Uvicorn | Local HTTP server for the API |
| SQLite | Persistent relational storage in a local file |
| unittest and HTTPX | Automated application tests |
| Git and GitHub | Version history and project documentation |

The application executes SQL directly to make database operations visible during learning. No ORM or separate database server is required.

## Project structure

```text
Support-Ticket-System/
|-- main.py                 # API routes and application startup
|-- schemas.py              # Request validation and response models
|-- database.py             # SQLite connection and SQL operations
|-- System.py               # Earlier terminal version, using in-memory data
|-- test_api.py             # API and database behavior tests
|-- test_system.py          # Terminal version behavior tests
|-- requirements.txt        # Application dependencies
|-- requirements-dev.txt    # Additional testing dependencies
|-- .gitignore
|-- LICENSE
`-- README.md
```

The API creates `tickets.db` beside `database.py` on startup. The database, virtual environment, and generated cache files are excluded from version control.

## How the API works

```text
HTTP request
    -> FastAPI route in main.py
    -> input validation using schemas.py
    -> SQL operation in database.py
    -> SQLite file: tickets.db
    -> response data returned to the client as JSON
```

FastAPI validates the declared request model before executing the route function. `database.py` receives the validated values and handles storage without depending on HTTP.

Each database operation opens and closes its own connection. Write operations use a transaction that commits on success or rolls back on an exception. SQL values are passed separately through placeholders rather than inserted into query strings.

## Requirements

- Python **3.12 or newer**; this version was tested with Python 3.12.
- Git, if cloning the repository.
- Internet access for the initial dependency installation.

SQLite support is included with Python; you do not need to install a separate SQLite server.

## Installation and execution

First, clone the repository and enter its directory:

```bash
git clone https://github.com/lzakLP/Support-Ticket-System.git
cd Support-Ticket-System
```

### Windows / PowerShell

Run each command separately from the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

If `py` is unavailable, use `python -m venv .venv` for the first command. These commands call the virtual environment's Python directly, so environment activation is optional.

### macOS / Linux

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m uvicorn main:app --reload
```

With the server running, open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

- `main:app` refers to the `app` object in `main.py`.
- `--reload` restarts the development server when source files change.
- Keep the terminal open while using the API.
- Press **Ctrl+C** to stop the server.
- If port 8000 is occupied, add `--port 8001` and open `/docs` on that port.

## Try the API

In `/docs`, expand an operation, click **Try it out**, supply the requested data, and click **Execute**.

### 1. Create a ticket

Send `POST /tickets` with:

```json
{
  "title": "No internet",
  "description": "I cannot connect to the office network."
}
```

Expected status: **201 Created**. Example response on a fresh database:

```json
{
  "id": 1,
  "title": "No internet",
  "description": "I cannot connect to the office network.",
  "status": "open"
}
```

Use the actual ID returned by your request in the following steps.

### 2. List and retrieve tickets

- `GET /tickets` returns all tickets ordered by ID.
- `GET /tickets/1` returns the ticket with ID 1, if it exists.
- An empty collection returns **200 OK** with `[]`.

### 3. Update the status

Send `PATCH /tickets/1` with:

```json
{
  "status": "in_progress"
}
```

The response contains the updated ticket. `" CLOSED "` is normalized to `"closed"`. A value such as `"cancelled"` is rejected without changing the ticket.

### 4. Verify persistence

Stop the server with Ctrl+C, run the same startup command again, and retrieve the ticket. It remains available because the data was committed to the same database file.

### 5. Delete a ticket

Send `DELETE /tickets/1`. A successful deletion returns **204 No Content** with an empty response body. Retrieving the deleted ID returns **404 Not Found**.

## Endpoint reference

| Method | Path | Request body | Success response |
|---|---|---|---|
| POST | `/tickets` | `title`, `description` | 201, created ticket |
| GET | `/tickets` | None | 200, ticket list |
| GET | `/tickets/{ticket_id}` | None | 200, one ticket |
| PATCH | `/tickets/{ticket_id}` | `status` | 200, updated ticket |
| DELETE | `/tickets/{ticket_id}` | None | 204, empty body |

Errors:

- **404:** the requested ticket does not exist.
- **422:** request validation failed, such as an empty title, missing description, unsupported status, or invalid ID.

HTTP response codes and the ticket's `status` field have different meanings: `200` describes a successful request, while `closed` describes the ticket's workflow state.

## Run the terminal learning version

`System.py` retains the earlier menu-based implementation:

```powershell
py System.py
```

On macOS/Linux, use `python3 System.py`.

This version uses only the Python standard library. Its tickets are stored in memory, are lost when it exits, and are independent from the API's SQLite database.

## Run the tests

On Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -v
```

On macOS/Linux:

```bash
./.venv/bin/python -m pip install -r requirements-dev.txt
./.venv/bin/python -m unittest discover -v
```

The tests cover CRUD behavior, input normalization, invalid requests, missing tickets, IDs after deletion, persistence in another process, parameterized queries, API documentation, and terminal interactions.

API tests use temporary database files and do not modify your `tickets.db`. CLI tests reset their in-memory state between cases.

## Current scope and future learning

This is a local educational application. Current limitations and possible next learning steps include:

- Users, authentication, priorities, categories, and ticket history.
- Pagination and filtering for ticket listings.
- Rules controlling allowed status transitions.
- Database relationships, joins, and additional SQL queries.
- Schema migrations when the database structure changes.
- Deployment and operational practices.

`CREATE TABLE IF NOT EXISTS` initializes a missing table; it does not migrate an existing table to a different structure. The database file needs to be preserved to keep its data.

## License

This project is distributed under the [MIT License](LICENSE).
