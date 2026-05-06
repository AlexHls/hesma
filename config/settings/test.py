"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import env
from .base import hydro_fs, meta_fs, rt_fs, tracer_fs


def set_storage_location(storage, location):
    storage._location = str(location)
    storage.__dict__.pop("base_location", None)
    storage.__dict__.pop("location", None)

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="qUigIiktFdVettQJuL94SorB0QWGNrb9H8ibXmWuKkFdzlqJmvWXz5xP3uTO743e",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# DEBUGGING FOR TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore # noqa: F405

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "http://media.testserver"
MEDIA_ROOT = str(BASE_DIR / ".test-media")  # noqa: F405
set_storage_location(meta_fs, BASE_DIR / ".test-media" / "meta_data")  # noqa: F405
set_storage_location(hydro_fs, BASE_DIR / ".test-media" / "hydro_data")  # noqa: F405
set_storage_location(tracer_fs, BASE_DIR / ".test-media" / "tracer_data")  # noqa: F405
set_storage_location(rt_fs, BASE_DIR / ".test-media" / "rt_data")  # noqa: F405

# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(APPS_DIR / "static")  # noqa: F405
# Your stuff...
# ------------------------------------------------------------------------------
