## UAHub.space

Project for ukrainian citizens and refuges to find each other, find help in any country in the world.

See it in action https://uahub.space/

### Setup

Deploy to any Python supported hosting like:
- Heroku
- Digital Ocean
- Railway.app
- Fly.io
- etc.

By cloning a project from GitHub https://github.com/VetalM84/ua_hub.git

#### Environments

Setup .env file keys with essential data:
```
SECRET_KEY=
OPENBLAS_NUM_THREADS=4
CSRF_COOKIE_SECURE=
SESSION_COOKIE_SECURE=
SECURE_SSL_REDIRECT=
DJANGO_DEBUG=1

DATABASES=mysql
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306

RECAPTCHA_PUBLIC_KEY=
RECAPTCHA_PRIVATE_KEY=

RECIPIENT_LIST=
DEFAULT_FROM_EMAIL=
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=465
EMAIL_USE_SSL=1

YANDEX_TRANSLATE_KEY=

SOCIAL_AUTH_GITHUB_KEY=
SOCIAL_AUTH_GITHUB_SECRET=
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=
SOCIAL_AUTH_FACEBOOK_KEY=
SOCIAL_AUTH_FACEBOOK_SECRET=
```
Run commands from CLI:
```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```