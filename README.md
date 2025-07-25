# PhoneBook FastAPI

A complete phonebook API built with FastAPI, PostgreSQL, and dual authentication (JWT + Google OAuth).

## 🚀 Quick Start (One-Click Setup)

**Requirements:** Docker and Docker Compose

```bash
# 1. Download or clone this repository
# 2. Run one command:
docker compose up --build

# That's it! 🎉
```

**The API will be available at:**
- 🌐 **API**: http://localhost:8000
- 📚 **Documentation**: http://localhost:8000/docs  
- 🗄️ **Database**: localhost:5432 (user: phonebook_user, password: phonebook_pass)

## ✨ Features

### Authentication
- **JWT Authentication**: Username/password with refresh tokens
- **Google OAuth**: Single sign-on with Google accounts
- **Secure cookies**: HTTP-only token storage

### API Endpoints
- `GET /` - API welcome message
- `POST /users/signup` - User registration
- `POST /users/token` - Login with credentials
- `GET /users/me` - Get current user profile
- `GET /google/login` - Google OAuth login
- `GET /contacts/` - List user's contacts
- `GET /contacts/{id}` - Get specific contact
- `POST /contacts/` - Create new contact
- `DELETE /contacts/{id}` - Delete contact

### Database
- **PostgreSQL** with automatic migrations
- **User-scoped data**: Users only see their own contacts
- **Persistent storage** with Docker volumes

## 🔧 Configuration (Optional)

To use Google OAuth, create a `.env` file:

```bash
# Copy template
cp .env.docker .env

# Edit with your credentials
SECRET_KEY=your-secure-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

Get Google OAuth credentials at: https://console.cloud.google.com/

## 🛠️ Development Commands

```bash
# Start services
docker compose up

# Start in background
docker compose up -d

# View logs
docker compose logs -f backend

# Stop services
docker compose down

# Reset everything (including database)
docker compose down -v
docker compose up --build

# Access database
docker compose exec postgres psql -U phonebook_user -d phonebook
```

## 📋 API Usage Examples

```bash
# Register a new user
curl -X POST "http://localhost:8000/users/signup" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"

# Login
curl -X POST "http://localhost:8000/users/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"

# Add a contact (after login)
curl -X POST "http://localhost:8000/contacts/" \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "name": "John Doe", "phone": "555-0123", "age": 30}' \
  --cookie-jar cookies.txt --cookie cookies.txt

# List contacts
curl "http://localhost:8000/contacts/" --cookie cookies.txt
```

## 🏗️ Architecture

- **main.py**: FastAPI app with middleware setup
- **models.py**: SQLAlchemy database models (User, Contact)
- **dependencies.py**: Database connection configuration
- **routers/**: API endpoints organized by feature
  - `users.py`: JWT authentication and user management
  - `google.py`: Google OAuth integration  
  - `contacts.py`: Contact CRUD operations
- **migrations/**: Alembic database migrations
- **start_app.py**: Startup script with database initialization

## 🐳 Docker Architecture

- **PostgreSQL container**: Database with health checks
- **FastAPI container**: Python app with automatic migrations
- **Persistent volumes**: Database data survives container restarts
- **Internal networking**: Secure container-to-container communication

## 🔒 Security Features

- Bcrypt password hashing
- JWT tokens with configurable expiration
- HTTP-only cookies prevent XSS attacks
- User-scoped data access
- Environment variable configuration
- Non-root container user

---

**Ready to use!** Just run `docker compose up --build` and start building your phonebook application. 📞