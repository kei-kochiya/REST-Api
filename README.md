# Proseka API

A high-performance, asynchronous REST API built with FastAPI. This project demonstrates a production-ready backend architecture including modular routing, dependency injection, and asynchronous database operations.

## Features
- **FastAPI**: High performance web framework.
- **Asynchronous Execution**: Utilizes `aiosqlite` and FastAPI's async endpoints for non-blocking operations.
- **SQLAlchemy ORM**: Object-relational mapping for database interactions.
- **Alembic Migrations**: Robust database schema version control.
- **Pydantic Validation**: Strict data validation and serialization.
- **Testing**: Comprehensive test suite using Pytest.

## Project Structure
- `routers/`: Contains API endpoints separated by feature.
- `schemas/`: Pydantic models for request and response validation.
- `database/`: SQLAlchemy models and asynchronous database connection setup.
- `alembic/`: Database migration scripts.
- `test_main.py`: Automated test suite.

## Requirements
- Python 3.10+
- `uv` package manager

## Installation
1. Clone the repository.
2. Install dependencies using uv:
   ```bash
   uv sync
   ```
3. Run database migrations to set up the SQLite database:
   ```bash
   uv run alembic upgrade head
   ```

## Running the Application
Start the uvicorn server with hot-reload enabled:
```bash
uv run uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`. You can view the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Testing
Run the test suite using pytest:
```bash
uv run pytest
```
