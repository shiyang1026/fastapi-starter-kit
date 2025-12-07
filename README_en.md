[English](README_en.md) | [中文](README.md)

# FastAPI Starter Kit

This is a modern backend starter template based on FastAPI, designed to provide a high-performance, scalable, and developer-friendly infrastructure. It integrates mainstream Python async ecosystem tools to help developers build production-grade Web applications quickly.

## Features

This project features the following technology stack:

- **Web Framework**: FastAPI (High-performance async framework)
- **Database ORM**: SQLModel (Modern ORM combining SQLAlchemy and Pydantic)
- **Database Migration**: Alembic (Lightweight database version control)
- **Async Driver**: asyncpg (PostgreSQL)
- **Cache**: Redis (Async support)
- **Authentication & Security**:
  - PyJWT (JSON Web Token handling)
  - Pwdlib (Password hashing and verification using Argon2)
- **Dependency Management**: uv (Fast Python package and project manager)
- **Code Quality**: Ruff (Fast code analysis and formatter)

## Quick Start

Follow these steps to quickly set up your local development environment.

### Prerequisites

Ensure the following tools are installed locally:
- Python 3.12+
- Docker & Docker Compose
- uv (Recommended for dependency management)

### 1. Initialize Dependencies

Install the required Python dependencies:

```bash
uv sync
```

### 2. Start Infrastructure Services

Start PostgreSQL and Redis using Docker Compose:

```bash
make infra-up
```

### 3. Database Migration

Apply database migrations to create table structures:

```bash
make migrate
```

### 4. Start Development Server

### 5. Code Quality

This project uses Ruff for linting and formatting, which is the standard modern Python tool. Since it is included in the project's development dependencies, you don't need to install it manually. You can run it directly via `uv` or `make`.

Run linter:
```bash
make lint
```

Auto-format code:
```bash
make format
```

```bash
make dev
```

Once the server is running, you can access:
- API Docs (Swagger UI): http://127.0.0.1:8000/docs
- API Docs (ReDoc): http://127.0.0.1:8000/redoc

## Common Commands

This project provides a `Makefile` to simplify common operations:

- `make run`: Start production server (Uvicorn)
- `make dev`: Start development server
- `make infra-up`: Start infrastructure services (DB, Redis)
- `make infra-down`: Stop infrastructure services
- `make migration msg="description"`: Generate a new database migration script
- `make migrate`: Execute database migrations
- `make downgrade`: Rollback the last migration
- `make lint`: Run code linting (Ruff)
- `make format`: Auto-format code (Ruff)


## Database Development Workflow

The standard process when adding a new table:

1. **Define Model**: Create a new model file in `app/models/` (or add to an existing one).
2. **Register Model**: **Critical Step!** You must import the new model in `alembic/env.py`, otherwise Alembic cannot detect the changes.
   ```python
   # alembic/env.py
   from app.models.new_model import NewModel  # noqa
   ```
3. **Generate Migration**:
   ```bash
   make migration msg="add new model"
   ```
4. **Verify Script**: Check the generated Python script in `alembic/versions/`.
5. **Apply Migration**:
   ```bash
   make migrate
   ```

```bash
make dev
```

```
app/
├── api/          # API route definitions (Endpoints)
├── core/         # Core configuration (Config, Security, Events)
├── db/           # Database connection and Session management
├── models/       # SQLModel data model definitions
├── schemas/      # Pydantic data validation models (Request/Response)
├── services/     # Complex business logic layer
└── main.py       # Application entry point
```
