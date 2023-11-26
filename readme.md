# Online queue project

```bash
# python3 is required for this project
pip install virtualenv
virtualenv venv
# using venv and installation
source venv/bin/activate
pip install -r requrements.txt

# for creting default admin (custom command)
python3 manage.py create_app_admin
```

Updatet dependencies should be also recorded <i>requirements.txt</i>

```bash
pip freeze > requirements.txt
```

Migrations

```bash
# for creating new changes in apps need also verify migrations for DB
python3 manage.py makemigrations
# apply mirations
python3 manage.py migrate
```

### Make sure this contain actual environment variables

You basically can copy-paste them from my template file env_template.txt

```
# This is basic section for every django project
SECRET_KEY=<YOUR VALUE> # Secret key for Django
DEBUG=False # default True for dev

# AppSettings example
DJANGO_ADMIN_USERNAME=user
DJANGO_ADMIN_PASSWORD=password
DJANGO_ADMIN_EMAIL=admin@some.mail

# Postgres DB settings example
DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=admin
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Redis
REDIS_PASSWORD=mysecret
```

### Locales <i>Ru</i>, <i>Fi</i>, <i>En</i>.

```bash
# creating locales
python manage.py makemessages -l en
python manage.py makemessages -l ru
python manage.py makemessages -l fi
# compile languages
python manage.py compilemessages
```

# Development

Docker containers
[docker redis](https://hub.docker.com/_/redis)

```bash
# Redis
docker run -d -p 6379:6379 --name my-redis redis
```

[docker postgres](https://hub.docker.com/_/postgres)

```bash
# Postgres
docker run --name postgres -e POSTGRES_PASSWORD=admin -p 5432:5432 -d postgis/postgis
```
