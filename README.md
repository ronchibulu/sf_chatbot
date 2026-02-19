# SleekFlow Chatbot - TODO List Application

A modern TODO list application with real-time collaboration, built with Next.js, FastAPI, and PostgreSQL.

## Tech Stack

### Frontend
- **Next.js 16** (App Router, TypeScript, Turbopack)
- **BetterAuth** for authentication (session management)
- **Tailwind CSS v4** for styling
- **shadcn/ui** for UI components
- **Package Manager**: `bun` (NOT npm/yarn)

### Backend
- **FastAPI** (Python 3.10+, async)
- **SQLModel 0.0.31** for ORM
- **Alembic** for database migrations
- **PostgreSQL** (shared with BetterAuth)
- **Package Manager**: `uv` (NOT pip/poetry)

### Database
- **PostgreSQL 16** running in Docker

---

## Prerequisites

- **Node.js** 20.9+ for frontend
- **Python** 3.10+ for backend
- **Bun** package manager: `npm install -g bun`
- **uv** package manager: `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Docker** and **Docker Compose** for PostgreSQL

---

## Project Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd sleekflow_chatbot
```

### 2. Start PostgreSQL Database
```bash
docker-compose up -d
```

Verify PostgreSQL is running:
```bash
docker-compose ps
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
bun install

# Create environment file (copy and edit)
cp .env.example .env.local
```

**Edit `frontend/.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=postgresql://user:password@localhost:5432/sleekflow_db
BETTER_AUTH_SECRET=your-secret-key-at-least-32-chars-long
BETTER_AUTH_URL=http://localhost:3000
```

**Run BetterAuth migration to create auth tables:**
```bash
bun run better-auth migrate
```

### 4. Backend Setup

```bash
cd backend

# Install dependencies
uv sync

# Create environment file (copy and edit)
cp .env.example .env
```

**Edit `backend/.env`:**
```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/sleekflow_db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

**Run database migrations:**
```bash
uv run alembic upgrade head
```

---

## Running the Application

### Start All Services

**Terminal 1: PostgreSQL (if not running)**
```bash
docker-compose up -d
```

**Terminal 2: Frontend**
```bash
cd frontend
bun run dev
```
Frontend will be available at: http://localhost:3000

**Terminal 3: Backend**
```bash
cd backend
uv run python -m app.main
# OR using uvicorn directly:
uv run uvicorn app.main:app --reload
```
Backend API will be available at: http://localhost:8000

---

## Authentication Flow

### Session Management (BetterAuth - Frontend Only)

1. User registers/logs in via BetterAuth (Next.js `/api/auth/login`)
2. BetterAuth creates session in PostgreSQL and sets httpOnly cookie: `better-auth.session_token`
3. All authentication and session management is handled by the frontend
4. Backend does not interact with Better Auth tables (user, session, account, verification)

### Password Security

- **Hashing**: BetterAuth uses **bcrypt** by default for password hashing
- **Sessions**: Stored in PostgreSQL with httpOnly cookies (secure, no localStorage)
- **Session Expiry**: 7 days (configurable in BetterAuth config)

---

## Database Schema

### BetterAuth Tables (created by BetterAuth migration)

- **user**: User accounts (id, email, name, emailVerified, createdAt, updatedAt)
- **session**: Active sessions (id, sessionToken, userId, expiresAt)
- **account**: OAuth accounts (if using social login)
- **verification**: Email verification tokens

### Application Tables (created by Alembic migrations)

- **TodoList**: TODO lists (will be added in Epic 2)
- **TodoItem**: TODO items (will be added in Epic 3)
- **ListMember**: Shared list permissions (will be added in Epic 4)
- **Activity**: Activity feed (will be added in Epic 6)

---

## Testing

### Backend Tests
```bash
cd backend

# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_auth.py -v

# Run with coverage
uv run pytest --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd frontend

# Run tests
bun test

# Run tests in watch mode
bun test --watch
```

---

## Project Structure

### Frontend (Feature-Based)
```
frontend/
├── src/
│   ├── app/                     # Next.js App Router
│   │   ├── api/auth/[...all]/   # BetterAuth handler
│   │   ├── page.tsx             # Home page
│   │   └── layout.tsx           # Root layout
│   ├── features/                # Feature modules
│   │   ├── auth/                # Authentication
│   │   ├── lists/               # TODO lists
│   │   └── items/               # TODO items
│   └── shared/                  # Shared code
│       ├── components/ui/       # shadcn/ui components
│       ├── lib/                 # Utilities
│       ├── hooks/               # React hooks
│       └── stores/              # Zustand stores
├── .env.local                   # Environment variables
└── package.json
```

### Backend (Layered)
```
backend/
├── app/
│   ├── main.py                  # FastAPI application
│   ├── api/
│   │   ├── deps.py              # Dependencies (auth, db)
│   │   └── v1/endpoints/        # API routes
│   ├── models/                  # SQLModel database models
│   │   ├── user.py              # User model
│   │   └── session.py           # Session model
│   ├── schemas/                 # Pydantic request/response schemas
│   ├── services/                # Business logic layer
│   └── db/
│       ├── session.py           # DB session (old, deprecated)
│       └── database.py          # DB connection
├── alembic/                     # Database migrations
├── tests/                       # Test suite
├── .env                         # Environment variables
└── pyproject.toml               # Dependencies (managed by uv)
```

---

## Development Workflow

### Package Managers (CRITICAL)

**Frontend: MUST use `bun`**
```bash
bun install              # Install dependencies
bun add <package>        # Add package
bun remove <package>     # Remove package
bun run dev              # Start dev server
```

**Backend: MUST use `uv`**
```bash
uv sync                  # Install dependencies
uv add <package>         # Add package
uv remove <package>      # Remove package
uv run python script.py  # Run Python script
uv run pytest            # Run tests
```

### Creating Database Migrations

```bash
cd backend

# Auto-generate migration from model changes
uv run alembic revision --autogenerate -m "add todo_items table"

# Review generated migration in alembic/versions/

# Apply migration
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

### Git Workflow

**Branch naming:**
- Feature: `feature/feature-name`
- Bug fix: `bugfix/bug-description`
- Hotfix: `hotfix/critical-issue`

**Commit format:**
```
<type>: <short description>

<optional detailed description>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

---

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Troubleshooting

### PostgreSQL Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps

# View PostgreSQL logs
docker-compose logs -f postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Frontend Issues
```bash
# Clear Next.js cache
cd frontend
rm -rf .next

# Reinstall dependencies
rm -rf node_modules bun.lockb
bun install
```

### Backend Issues
```bash
# Clear Python cache
cd backend
find . -type d -name "__pycache__" -exec rm -rf {} +

# Recreate virtual environment
rm -rf .venv
uv sync
```

### Database Reset
```bash
# WARNING: This deletes all data
docker-compose down -v
docker-compose up -d

# Re-run migrations
cd frontend && bun run better-auth migrate
cd backend && uv run alembic upgrade head
```

---

## Environment Variables Reference

### Frontend (`.env.local`)
| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost:5432/sleekflow_db` |
| `BETTER_AUTH_SECRET` | BetterAuth secret key (32+ chars) | `your-secret-key-at-least-32-chars-long` |
| `BETTER_AUTH_URL` | Frontend base URL | `http://localhost:3000` |

### Backend (`.env`)
| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection (async driver) | `postgresql+psycopg://user:password@localhost:5432/sleekflow_db` |
| `SECRET_KEY` | FastAPI secret key | `your-secret-key-here` |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `http://localhost:3000` |

---

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [BetterAuth Documentation](https://better-auth.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com)
- [Project Architecture](_bmad-output/planning-artifacts/architecture.md)
- [Project Context](_bmad-output/project-context.md)

---

## License

[Your License Here]

## Contributors

[Your Team/Contributors Here]
