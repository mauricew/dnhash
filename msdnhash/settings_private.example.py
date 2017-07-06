import os.path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

debug = True
allowed_hosts = []
secret = 'myverysecretkey'
database = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
}