#!/bin/bash
# Render.com deployment script for RE VLab Django app

echo "🚀 Starting RE VLab deployment on Render..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run Django setup
echo "🔧 Running Django migrations..."
python manage.py migrate

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🌟 Starting Gunicorn server..."
gunicorn requirements_lab.wsgi:application --bind 0.0.0.0:$PORT

echo "✅ RE VLab is now running!"
