# Django Boilerplate Project

A complete Django project boilerplate following best practices and design patterns.

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory:

```env
ENVIRONMENT=development
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

## Project Structure

- `project_name/`: Main project directory with settings
- `apps/`: All Django applications
- `apps/core/`: Core/shared functionality
- `templates/`: Global templates
- `static/`: Static files
- `media/`: User-uploaded files

## Adding New Apps

1. Create app in `apps/` directory:
```bash
python manage.py startapp myapp apps/myapp
```

2. Add app to `INSTALLED_APPS` in `settings/base.py`

3. Create URLs in `apps/myapp/urls.py` and include in main `urls.py`

## Development

- Use `requirements-dev.txt` for development dependencies
- Run tests: `python manage.py test`
- Format code: `black .`
- Lint code: `flake8`

## Production Deployment

1. Set `ENVIRONMENT=production` in `.env`
2. Configure production database (PostgreSQL)
3. Set up static file serving (WhiteNoise or CDN)
4. Configure allowed hosts
5. Set up SSL/HTTPS

