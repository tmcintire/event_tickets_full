#!/usr/bin/env bash

python manage.py dumpdata -e contenttypes -e auth -e sessions --indent 2 >> data.json