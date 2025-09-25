from app.settings import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "thss",
        "USER": "root",
        "PASSWORD": "thss",
        "HOST": "db",
        "PORT": "3306",
    }
}
