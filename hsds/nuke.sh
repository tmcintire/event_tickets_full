#!/usr/bin/env bash

rm db/db.sqlite3
rm -rf /equipment/migrations/
touch equipment/migrations/__init__.py
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver