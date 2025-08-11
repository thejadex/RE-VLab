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

# Initialize database for Vercel deployment
if os.environ.get('VERCEL_URL') or os.environ.get('VERCEL'):
    try:
        from django.core.management import execute_from_command_line
        from django.db import connection
        import django
        django.setup()
        
        # Check if database is initialized
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
            if not cursor.fetchone():
                # Run migrations
                execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
                
        # Run setup_lab command to create initial data
        try:
            execute_from_command_line(['manage.py', 'setup_lab'])
        except Exception as e:
            print(f"Setup lab command error: {e}")
            
    except Exception as e:
        print(f"Database initialization error: {e}")

# Vercel handler
app = application
