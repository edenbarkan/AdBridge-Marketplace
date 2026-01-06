# AdBridge Marketplace

A production-ready AdTech Marketplace MVP foundation built with Flask, PostgreSQL, and Docker.

## Features

- **User Authentication**: Register, login, and logout with session-based authentication
- **Role-Based Access Control**: Three roles (PUBLISHER, ADVERTISER, ADMIN)
- **Dashboards**: Separate dashboards for each user role
- **Database Migrations**: Flask-Migrate (Alembic) for database versioning
- **Docker Support**: Multi-container setup with PostgreSQL and Flask web server
- **Health Check**: `/healthz` endpoint for Kubernetes readiness checks
- **Error Handling**: Custom 403 and 404 error pages

## Tech Stack

- **Backend**: Python 3.11 + Flask
- **Database**: PostgreSQL 15
- **ORM**: Flask-SQLAlchemy
- **Migrations**: Flask-Migrate (Alembic)
- **Authentication**: Flask-Login (session-based)
- **Frontend**: Jinja2 templates + Bootstrap 5 (SSR)
- **Web Server**: Gunicorn
- **Containerization**: Docker Compose

## Project Structure

```
AdBridge-Marketplace/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration
│   ├── extensions.py         # Flask extensions
│   ├── models.py            # Database models
│   ├── auth/                # Authentication blueprint
│   ├── main/                # Main routes blueprint
│   ├── publisher/           # Publisher routes blueprint
│   ├── advertiser/          # Advertiser routes blueprint
│   ├── admin/               # Admin routes blueprint
│   ├── errors/              # Error handlers blueprint
│   └── templates/           # Jinja2 templates
├── wsgi.py                  # WSGI entry point
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── entrypoint.sh          # Container entrypoint script
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git (optional)

### Setup Steps

1. **Clone or download the project**

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your `SECRET_KEY` and other variables.

3. **Build and start containers**
   ```bash
   docker compose up -d --build
   ```

4. **Initialize database migrations** (first time only)
   ```bash
   docker compose exec web flask db init
   ```

5. **Create initial migration**
   ```bash
   docker compose exec web flask db migrate -m "Initial migration"
   ```

6. **Apply migrations**
   ```bash
   docker compose exec web flask db upgrade
   ```

   Note: The entrypoint script automatically runs `flask db upgrade` on container start, so migrations will be applied automatically. However, you still need to run `flask db init` and `flask db migrate` the first time.

7. **Access the application**
   - Web app: http://localhost:8000
   - Health check: http://localhost:8000/healthz

## Environment Variables

Required:
- `SECRET_KEY`: Flask secret key for session security
- `DATABASE_URL`: PostgreSQL connection string (auto-set in docker-compose.yml)

Optional:
- `FLASK_ENV`: Environment (development/production), default: production
- `PORT`: Server port, default: 8000
- `ADMIN_EMAIL`: Email for admin user bootstrap
- `ADMIN_PASSWORD`: Password for admin user bootstrap

Database variables (used by docker-compose.yml):
- `POSTGRES_DB`: Database name, default: adbridge
- `POSTGRES_USER`: Database user, default: adbridge
- `POSTGRES_PASSWORD`: Database password, default: adbridge123

## Usage

### Register a New User

1. Navigate to http://localhost:8000/auth/register
2. Fill in email, password, and select role (Publisher or Advertiser)
3. Complete additional fields based on selected role
4. Submit the form

### Login

1. Navigate to http://localhost:8000/auth/login
2. Enter your email and password
3. You'll be redirected to your role-specific dashboard

### Dashboards

- **Publisher Dashboard**: `/publisher/dashboard` - For users selling ad slots
- **Advertiser Dashboard**: `/advertiser/dashboard` - For users running campaigns
- **Admin Dashboard**: `/admin/dashboard` - For administrators

### Health Check

The `/healthz` endpoint returns `{"status": "ok"}` with HTTP 200, suitable for Kubernetes readiness probes.

## Database Migrations

### Create a new migration
```bash
docker compose exec web flask db migrate -m "Description of changes"
```

### Apply migrations
```bash
docker compose exec web flask db upgrade
```

### Rollback migration
```bash
docker compose exec web flask db downgrade
```

## Development

### Running Locally (without Docker)

1. Install Python 3.11+
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up PostgreSQL database and configure `DATABASE_URL` in `.env`
5. Run migrations:
   ```bash
   flask db upgrade
   ```
6. Run development server:
   ```bash
   python wsgi.py
   ```

### Code Structure

- **Application Factory**: `app/__init__.py` contains `create_app()` function
- **Blueprints**: Each feature area has its own blueprint module
- **Models**: SQLAlchemy models in `app/models.py`
- **Templates**: Jinja2 templates in `app/templates/`
- **Configuration**: Environment-based config in `app/config.py`

## API Endpoints

### Public Routes
- `GET /` - Landing page
- `GET /auth/login` - Login form
- `POST /auth/login` - Login submission
- `GET /auth/register` - Registration form
- `POST /auth/register` - Registration submission
- `GET /healthz` - Health check endpoint

### Protected Routes
- `GET /dashboard` - Role-based dashboard redirect
- `GET /publisher/dashboard` - Publisher dashboard (requires PUBLISHER or ADMIN)
- `GET /advertiser/dashboard` - Advertiser dashboard (requires ADVERTISER or ADMIN)
- `POST /auth/logout` - Logout (requires authentication)
- `GET /admin/dashboard` - Admin dashboard (requires ADMIN)

## Security Notes

- Passwords are hashed using Werkzeug's password hashing
- Session-based authentication via Flask-Login
- Role-based authorization decorators
- CSRF protection recommended for production (consider Flask-WTF)
- Never commit `.env` file to version control

## Troubleshooting

### Database connection errors
- Ensure PostgreSQL container is running: `docker compose ps`
- Check database credentials in `.env` match `docker-compose.yml`
- Verify database is healthy: `docker compose exec db pg_isready`

### Migration errors
- Ensure migrations directory exists: `docker compose exec web flask db init`
- Check database is accessible before running migrations
- Review migration files in `migrations/versions/`

### Port conflicts
- Change `PORT` in `.env` if 8000 is already in use
- Update port mapping in `docker-compose.yml` accordingly

## Production Deployment

Before deploying to production:

1. Set a strong `SECRET_KEY` in environment variables
2. Use a managed PostgreSQL database or secure database credentials
3. Configure proper CORS settings if needed
4. Set up SSL/TLS certificates
5. Configure proper logging and monitoring
6. Review and harden security settings
7. Set up database backups
8. Consider adding Flask-WTF for CSRF protection

## License

This is an MVP foundation. Customize as needed for your use case.

## Support

For issues or questions, please check the code comments and Flask documentation.

