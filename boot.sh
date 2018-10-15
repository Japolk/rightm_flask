#!/bin/bash
flask init-db
flask take-limit $1
exec gunicorn -b :5000 --timeout 60 -w 4 api:app
