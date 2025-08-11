"""
WSGI config for requirements_lab project.
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'requirements_lab.settings')

# Initialize Django
application = get_wsgi_application()

# Auto-migrate on Vercel startup
if os.environ.get('VERCEL_URL'):
    try:
        from django.core.management import execute_from_command_line
        print("Running migrations on Vercel startup...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        # Create superuser if it doesn't exist
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("Created admin user: admin/admin123")
    except Exception as e:
        print(f"Migration/setup error (continuing anyway): {e}")

# Vercel handler
app = application
