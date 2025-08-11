"""
Django settings for requirements_lab project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Robust host parsing
_raw_hosts = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(',') if h.strip()]

# Auto-include Render provided hostname if available
_render_url = os.environ.get('RENDER_EXTERNAL_URL')  # e.g. https://re-vlab.onrender.com
if _render_url:
    _render_host = _render_url.replace('https://', '').replace('http://', '').strip('/')
    if _render_host and _render_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_render_host)

# Auto-include Vercel provided hostname if available
_vercel_url = os.environ.get('VERCEL_URL')  # e.g. re-vlab-abc123.vercel.app
if _vercel_url:
    if _vercel_url not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_vercel_url)

# Add Vercel domains
VERCEL_DOMAINS = [
    '.vercel.app',
    '.vercel.com'
]
for domain in VERCEL_DOMAINS:
    if domain not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(domain)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_tailwind',
    'lab',  # Make sure this is here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'requirements_lab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'lab.context_processors.sidebar_progress',
                'lab.context_processors.notifications_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'requirements_lab.wsgi.application'

# Database
# Check for Vercel Postgres first, then other production database URLs
POSTGRES_URL = os.environ.get('POSTGRES_URL')
DATABASE_URL = os.environ.get('DATABASE_URL')

if POSTGRES_URL:
    # Vercel Postgres
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(POSTGRES_URL, conn_max_age=600, ssl_require=True)
        }
    except ImportError:
        # Fallback to SQLite if dj_database_url is not available
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
elif DATABASE_URL:
    # Other production database URLs (Railway, Heroku, etc.)
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL)
        }
    except ImportError:
        # Fallback to SQLite if dj_database_url is not available
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # Default SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# CSRF trusted origins (for Render / Vercel frontends) - supply comma-separated list in env
_raw_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if _raw_csrf:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _raw_csrf.split(',') if o.strip()]
else:
    CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if h not in ('localhost', '127.0.0.1')]


# Security headers & HTTPS settings only when not in DEBUG
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Vercel-specific static files configuration
if os.environ.get('VERCEL'):
    STATIC_ROOT = BASE_DIR / 'staticfiles_build' / 'static'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
elif os.environ.get('RENDER'):
    # Explicit Render configuration (maintains existing behavior)
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    # Default configuration (works for Render and local development)
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Login URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
