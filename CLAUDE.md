# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a FastAPI-based phonebook application with PostgreSQL database and OAuth authentication. The project structure follows a modular router-based architecture:

- **main.py**: FastAPI application entry point with middleware and router registration
- **routers/**: Contains API endpoints organized by feature:
  - `contacts.py`: CRUD operations for contacts with JWT authentication
  - `users.py`: User authentication, signup, and JWT token management
  - `google.py`: Google OAuth authentication flow
- **migrations.py**: SQLAlchemy models for User and Contact entities
- **dependencies.py**: Database connection and engine configuration
- **migrations/**: Alembic database migration files

## Key Components

### Authentication System
The app supports dual authentication:
1. **JWT-based**: Username/password with access and refresh tokens stored in HTTP-only cookies
2. **Google OAuth**: OAuth2 flow using Authlib integration

### Database Models
- **User**: id, username, password (hashed), verified, disabled
- **Contact**: id, user_id (FK), name, phone, age

### Security Features
- JWT tokens with configurable expiration (30min access, 12hr refresh)
- Bcrypt password hashing
- HTTP-only cookies for token storage
- User-scoped contact access (users only see their own contacts)

## Development Commands

### Running the Application
```bash
uvicorn main:app --reload
```

### Database Operations
```bash
# Generate new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Downgrade one revision
alembic downgrade -1
```

### Environment Setup
- Requires `.env` file with: `SECRET_KEY`, `PSQL_URL`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
- PostgreSQL database configured in alembic.ini (port 2345, database: phonebook)

## Important Notes

- **Hard-coded secrets**: Google client credentials are exposed in contacts.py:26-27 and should be moved to environment variables
- **Database**: Uses PostgreSQL with connection pooling (pool_size=3, max_overflow=0)
- **Session middleware**: Required for Google OAuth state management
- **Import structure**: Uses relative imports within package structure