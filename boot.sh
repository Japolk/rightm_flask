#!/bin/bash
flask init-db
exec gunicorn -b :5000 --timeout 60 -w 4 api:app
