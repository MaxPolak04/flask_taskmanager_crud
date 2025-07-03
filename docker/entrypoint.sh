#!/bin/bash

echo "📦 Pliki w katalogu /app:"
ls -l /app

echo "Pliki w /:"
ls -l /

exec gunicorn -w 4 -b 0.0.0.0:8000 run:app
