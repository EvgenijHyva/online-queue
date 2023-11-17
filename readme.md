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
```
