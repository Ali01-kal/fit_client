from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


def env(name, default=None, cast=str):
    value = os.getenv(name, default)
    if value is None:
        return None
    if cast is bool:
        return str(value).lower() in {"1", "true", "yes", "on"}
    if cast is list:
        return [item.strip() for item in str(value).split(",") if item.strip()]
    return cast(value)


SECRET_KEY = env("SECRET_KEY", "unsafe-dev-key")
DEBUG = env("DEBUG", True, bool)
ALLOWED_HOSTS = env("ALLOWED_HOSTS", "127.0.0.1,localhost", list)
CSRF_TRUSTED_ORIGINS = env(
    "CSRF_TRUSTED_ORIGINS", "http://127.0.0.1:8000,http://localhost:8000", list
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core.apps.CoreConfig",
    "accounts.apps.AccountsConfig",
    "clients.apps.ClientsConfig",
    "trainers.apps.TrainersConfig",
    "programs.apps.ProgramsConfig",
    "memberships.apps.MembershipsConfig",
    "attendance.apps.AttendanceConfig",
    "payments.apps.PaymentsConfig",
    "appointments.apps.AppointmentsConfig",
    "nutrition.apps.NutritionConfig",
    "reviews.apps.ReviewsConfig",
    "reports.apps.ReportsConfig",
    "api.apps.ApiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "fit_client.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.global_stats",
            ],
        },
    }
]

WSGI_APPLICATION = "fit_client.wsgi.application"
ASGI_APPLICATION = "fit_client.asgi.application"

db_url = env("DATABASE_URL", "sqlite:///db.sqlite3")
if db_url.startswith("sqlite:///"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / db_url.replace("sqlite:///", ""),
        }
    }
else:
    # Simple parser for postgres URLs: postgresql://user:pass@host:port/dbname
    from urllib.parse import urlparse

    parsed = urlparse(db_url)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed.path.lstrip("/"),
            "USER": parsed.username,
            "PASSWORD": parsed.password,
            "HOST": parsed.hostname,
            "PORT": parsed.port or 5432,
            "CONN_MAX_AGE": env("DB_CONN_MAX_AGE", 60, int),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = env("TIME_ZONE", "Asia/Almaty")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_REDIRECT_URL = "core:dashboard"
LOGOUT_REDIRECT_URL = "core:home"
LOGIN_URL = "login"

EMAIL_BACKEND = env(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "noreply@fitclient.local")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = env("SECURE_REFERRER_POLICY", "same-origin")
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = env("SECURE_HSTS_SECONDS", 0 if DEBUG else 3600, int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env("SECURE_HSTS_INCLUDE_SUBDOMAINS", not DEBUG, bool)
SECURE_HSTS_PRELOAD = env("SECURE_HSTS_PRELOAD", False, bool)

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[{levelname}] {name}: {message}", "style": "{"}
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"}
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}
