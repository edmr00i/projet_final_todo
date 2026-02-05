"""
Configuration Django pour le projet de gestion de tâches.

Ce fichier contient toutes les configurations nécessaires au fonctionnement
de l'application Django, incluant:
    - Configuration de la base de données (SQLite3)
    - Applications installées (Django, DRF, CORS, taches)
    - Middleware (sécurité, sessions, CORS, authentification)
    - Configuration Django REST Framework (authentification par token)
    - Configuration CORS pour autoriser les requêtes depuis le frontend React
    - Paramètres de sécurité, internationalisation, fichiers statiques

IMPORTANT: Ce fichier contient des paramètres de développement.
Pour la production, il faut:
    - Changer SECRET_KEY et le garder secret
    - Mettre DEBUG = False
    - Configurer ALLOWED_HOSTS
    - Utiliser une base de données de production (PostgreSQL, MySQL, etc.)
    - Configurer les fichiers statiques avec un serveur web (Nginx, Apache)

Pour plus d'informations:
    https://docs.djangoproject.com/en/6.0/topics/settings/
    https://docs.djangoproject.com/en/6.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ibl60*dggsl22g2^+!ub)3@g_x(+djk=)k$ju^2%@+mkuab+1g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'taches',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Dossier du build React (frontend/dist) pour collectstatic et service du SPA
STATICFILES_DIRS = [
    BASE_DIR / 'frontend' / 'dist',
]

# Django REST Framework Configuration
# https://www.django-rest-framework.org/api-guide/authentication/
# Configuration de l'authentification et des permissions pour l'API REST.
# Toutes les vues de l'API nécessitent une authentification par token.
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ],
# }

# CORS Configuration
# Configuration pour autoriser les requêtes cross-origin depuis le frontend React.
# En production, remplacer par les domaines réels de votre application.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server par défaut
    "http://127.0.0.1:5173",  # Alternative localhost
]

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

