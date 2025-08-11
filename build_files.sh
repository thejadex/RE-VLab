#!/bin/bash

# Vercel Build Script for Django
echo "Starting Django build process..."

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set Django settings
export DJANGO_SETTINGS_MODULE=requirements_lab.settings
export PYTHONPATH="/var/task"

# Create staticfiles directory
echo "Creating static files directory..."
mkdir -p staticfiles_build/static

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run migrations (optional - comment out if using external DB)
echo "Running database migrations..."
python manage.py migrate --noinput || echo "Migration failed - continuing..."

# Create superuser if needed (optional)
echo "Creating admin user..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell || echo "Superuser creation failed - continuing..."

echo "Build process completed!"
