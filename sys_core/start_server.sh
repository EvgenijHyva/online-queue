#!/bin/bash

# database makemigrations
python3 manage.py makemigrations

# database migrations
python3 manage.py migrate

# Default admin user for DB (based on .env)
python3 manage.py create_app_admin 

# Compile messages
python3 manage.py compilemessages

# Start dev server
python3 manage.py runserver 0.0.0.0:8000