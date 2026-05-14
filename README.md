### 1. Setup & Installation

Clone the repository, navigate to the root directory, and install the project along with its CLI binaries in editable mode:

```bash
# Install dependencies and local CLI entry points
uv sync
uv pip install -e .

```

---

## 🛠️ Custom CLI Tool (`nexus`)

The project includes a custom command-line interface named `nexus` (configured via `pyproject.toml`). You can execute it from anywhere within the project tree using `uv run`.

### Database Migrations

| Command | Description |
| --- | --- |
| `uv run nexus db:upgrade` | Upgrade the database schema to the latest Alembic revision. |
| `uv run nexus db:downgrade 1` | Rollback the last applied database migration. |

### Application Controls

| Command | Description |
| --- | --- |
| `uv run nexus dev` | Start the FastAPI backend server in development mode with auto-reload. |
| `uv run nexus prod` | Spin up the production server using Uvicorn/Gunicorn. |
| `uv run nexus shell` | Open an interactive IPython/Python environment with pre-imported models and database sessions. |

### Localization & Utilities

| Command | Description |
| --- | --- |
| `uv run nexus seed` | Populate the database tables with initial development mock data. |

---

## 💻 Manual Developer Commands

If you ever need to bypass the `nexus` wrapper application and talk directly to individual tool chains, use these native fallback commands:

### Running Python Modules Locally

If you want to run the CLI directly through the python interpreter without installing it:

```bash
uv run python -m cli db:upgrade

```

### Direct Database Manipulations (Alembic)

```bash
# Run migrations using raw Alembic configuration
uv run alembic upgrade head

# Generate a raw migration file
uv run alembic revision --autogenerate -m "description"

```

### Running the Backend Engine

```bash
# Boot the FastAPI instance manually
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```

---

## 📂 Project Anatomy

```text
fastapi-template/
├── alembic/          # Database structural version histories
├── app/              # Core application logic (API router, models, schemas, services)
├── cli/              # Command line system workspace
│   ├── __main__.py   # Main engine runner hook (`main()`)
│   ├── commands.py   # Shell registry matching commands to code routines
│   └── database.py   # Database upgrade/downgrade routine implementations
├── lang/             # Translation sheets and multi-lingual processing blocks
├── pyproject.toml    # Application configurations, dependencies, and CLI bindings
└── README.md         # Documentation index

```

---

## ⚙️ Environment Configuration

Copy the sample environment file to configure your local database credentials, secrets, and language properties before launching your engines:

```bash
cp .env.example .env

```

"""