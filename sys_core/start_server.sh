#!/bin/bash

# database migrations
python3 manage.py migrate

# Default admin user for DB (based on .env)
python3 manage.py create_app_admin 

# Start dev server
python3 manage.py runserver 0.0.0.0:8000