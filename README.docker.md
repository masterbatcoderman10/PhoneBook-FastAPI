# Docker Setup for PhoneBook API

## Quick Start

1. **Copy the environment file:**
   ```bash
   cp .env.docker .env
   ```

2. **Edit the `.env` file with your values:**
   - Generate a secure `SECRET_KEY` (32+ character random string)
   - Add your Google OAuth credentials (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`)

3. **Start the application:**
   ```bash
   docker-compose up --build
   ```

4. **Access the API:**
   - API: http://localhost:8000
   - Database: localhost:5432 (username: phonebook_user, password: phonebook_pass)

## Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f postgres

# Stop services
docker-compose down

# Reset database (removes all data)
docker-compose down -v
docker-compose up --build

# Run database migrations manually
docker-compose exec backend alembic upgrade head

# Access database shell
docker-compose exec postgres psql -U phonebook_user -d phonebook
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing key | `your-32-char-secret-key-here` |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | From Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret | From Google Cloud Console |

## Database

- **Host:** postgres (internal), localhost:5432 (external)
- **Database:** phonebook
- **User:** phonebook_user
- **Password:** phonebook_pass

## Troubleshooting

- **Port conflicts:** Change `8000:8000` to `8001:8000` in docker-compose.yml
- **Database issues:** Run `docker-compose down -v` to reset volumes
- **Import errors:** Ensure all files use absolute imports (not relative imports)