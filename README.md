# Authease Blog Demo

A full-featured Django blog application built to demonstrate and test [authease](https://pypi.org/project/authease/) — a ready-made authentication system for Django.

This project showcases every auth feature authease provides through both **Django templates** and **REST API endpoints**, so developers can see exactly how the package works in a real application.

## What This Demonstrates

### Authentication (powered by authease)
- **Registration** with Django's built-in password validation
- **OTP email verification** with resend cooldown timer
- **Login/Logout** with session management
- **Password reset** via email link
- **Change password** from settings page
- **Profile management** with custom fields (bio, profile picture, website, date of birth)
- **OAuth social login** — Sign in with **Google** or **GitHub**
- **Extensible User model** via `AbstractAutheaseUser`

### Blog Features
- Create, edit, and delete posts
- Like/unlike posts
- Comment system with author-only delete
- "My Posts" dashboard
- Reading time estimates
- **Dark mode** with theme toggle and persistence
- **Responsive design** with mobile offcanvas navigation

### API (DRF + Swagger)
- Full REST API for all blog operations
- JWT authentication via authease
- Interactive Swagger docs at `/swagger/`
- ReDoc at `/redoc/`

## Tech Stack

- **Django 6.0** — Web framework
- **authease 3.2.3** — Authentication system
- **Django REST Framework** — API layer
- **SimpleJWT** — JWT tokens
- **drf-yasg** — Swagger/OpenAPI docs
- **Bootstrap 5** — Frontend styling
- **SQLite** — Database (development)

## Quick Start

```bash
# Clone the repo
git clone https://github.com/Oluwatemmy/authease-blog-demo.git
cd authease-blog-demo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

Then visit `http://localhost:8000` to see the blog, or `http://localhost:8000/swagger/` for the API docs.

## Project Structure

```
authease-blog-demo/
├── blog_project/          # Django project settings & URLs
│   ├── settings.py
│   └── urls.py
├── blog/                  # Blog app
│   ├── models.py          # User (extends AbstractAutheaseUser), Post, Comment, Like
│   ├── views.py           # DRF API views
│   ├── serializers.py     # DRF serializers
│   ├── frontend_views.py  # Template-based views
│   ├── frontend_urls.py   # Frontend URL routes
│   └── templatetags/      # Custom template filters
├── templates/
│   ├── blog/              # Blog templates (base, home, post detail, etc.)
│   ├── authease/          # Auth templates (login, register, verify, settings, etc.)
│   └── email/             # Email templates (OTP verification, password reset)
└── requirements.txt
```

## Extending the User Model

This project demonstrates how to extend authease's user model with custom fields:

```python
from authease.auth_core.models import AbstractAutheaseUser

class User(AbstractAutheaseUser):
    bio = models.TextField(blank=True, default='')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, default='')
    date_of_birth = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True, default='')
```

Authease automatically detects these extra fields and includes them in the settings page.

## Configuration

Key settings in `settings.py`:

```python
AUTH_USER_MODEL = 'blog.User'           # Point to your custom user model
EMAIL_BACKEND = '...'                    # Configure your email backend
SITE_NAME = 'Blog App'                  # Used in emails
SITE_URL = 'http://localhost:8000'       # Used for password reset links
```

### OAuth Setup (Optional)

To enable social login, add your OAuth credentials to `settings.py`:

**GitHub:**
1. Create an OAuth App at [GitHub Developer Settings](https://github.com/settings/developers)
2. Set the callback URL to `http://localhost:8000/oauth/github/callback/`
3. Add to settings:
```python
GITHUB_CLIENT_ID = 'your-client-id'
GITHUB_CLIENT_SECRET = 'your-client-secret'
```

**Google:**
1. Create OAuth credentials in [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Set authorized redirect URI to `http://localhost:8000/oauth/google/callback/`
3. Add to settings:
```python
GOOGLE_CLIENT_ID = 'your-client-id'
```

## Screenshots

Visit the live demo or run locally to explore the UI.

## License

MIT

## Links

- [authease on PyPI](https://pypi.org/project/authease/)
- [Django Documentation](https://docs.djangoproject.com/)
