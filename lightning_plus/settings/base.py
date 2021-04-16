import os

from celery.schedules import crontab

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DEBUG = True

SECRET_KEY = "SECRET_KEY"

ALLOWED_HOSTS = ["*"]

DJANGO_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.sessions",
    "django.contrib.messages",
)
THIRD_PARTY_APPS = (
    "rest_framework",
    "mptt",
    "django_filters",
    "celery",
    "guardian",
    "django_extensions",
    "graphiql_debug_toolbar"
)

LOCAL_APPS = (
    "lightning_plus.api_basebone",
    "lightning_plus.bsm_config",
    "lightning_plus.lightning",
    "lightning_plus.shield",
    "lightning_plus.puzzle",
    "lightning_plus.graphql",
    "lightning_plus.scrm",
    "django.contrib.admin",
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "lightning_plus.contrib.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("Error", "twocucao@gmail.com")]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

APPEND_SLASH = False

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.

TIME_ZONE = "Asia/Shanghai"
CELERY_TIME_ZONE = "Asia/Shanghai"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "zh-hans"
# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
# Application definition
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [TEMPLATES_DIR],
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = "./static"
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MEDIA_ROOT = "./media"
MEDIA_URL = "/media/"

ROOT_URLCONF = "lightning_plus.urls"

WSGI_APPLICATION = "lightning_plus.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"

ADMIN_URL = r"^{}/".format(os.getenv("DJANGO_ADMIN_URL", "admin"))

INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

if not os.path.exists("/dev/log"):
    syslog_address = "/var/run/syslog"
    handlers = ["console"]
else:
    syslog_address = "/dev/log"
    handlers = ["syslog"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(process)d] %(name)s %(levelname)s: %(message)s"
        }
    },
    "handlers": {
        "stdout": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "stderr": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {"": {"handlers": ["stdout", "stderr"], "level": "DEBUG"}},
}

"""
Local settings
- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""

import os  # noqa

# MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa
INSTALLED_APPS += ("debug_toolbar",)  # noqa
MIDDLEWARE += ["lightning_plus.contrib.middleware.DebugToolbarMiddleware"]  # noqa
ENABLE_DEBUG_TOOLBAR = True

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
    "RESULTS_CACHE_SIZE": 100,
}
DEBUG_TOOLBAR_PANELS = [
    "ddt_request_history.panels.request_history.RequestHistoryPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG  # type:ignore

# CACHING
# ------------------------------------------------------------------------------
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# ========== CELERY START
CELERY_BROKER_URL = "amqp://lightning_plus:lightning_plus@localhost:5672/lightning_plus"

# CELERY_RESULT_BACKEND = "redis://{host}:{port}/1".format(
#     host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", "6379")
# )
CELERY_RESULT_BACKEND = None

CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_ALWAYS_EAGER = True
CELERYD_HIJACK_ROOT_LOGGER = False

# ========== CELERY END

# EMAIL CONFIGURATION
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "sender@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "app_specific_password")
EMAIL_PORT = 587

INTERNAL_IPS += ["*"]  # noqa

TEST_RUNNER = "django.test.runner.DiscoverRunner"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "lightning_plus",
        "USER": "lightning_plus",
        "PASSWORD": "lightning_plus",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "ATOMIC_REQUESTS": False,
        "CONN_MAX_AGE": 0,
        # 'OPTIONS': {
        #     'MAX_CONNS': 20,
        #     'REUSE_CONNS': 10
        # }
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/5",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

ENV = "LOCAL"

CELERY_BEAT_SCHEDULE = {
    "daily_midnight_settle": {
        "task": "daily_midnight_settle",
        "schedule": crontab(hour="0", minute="5"),
        "args": (),
    },
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "lightning_plus.api_basebone.drf.handler.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "lightning_plus.api_basebone.drf.authentication.CsrfExemptSessionAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

REAL_IP_ENVIRON = "X-Real-IP"

