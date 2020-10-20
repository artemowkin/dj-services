from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'v@ai^w!acn9t2i&3d!_3@_6=$bwa!no&#%x*$^9+43ev+f5h_+'

DEBUG = True

ALLOWED_HOSTS = []


ROOT_URLCONF = 'testproj.urls'

WSGI_APPLICATION = 'testproj.wsgi.application'


INSTALLED_APPS = [
    'testapp'
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
