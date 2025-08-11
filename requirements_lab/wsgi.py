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

# Auto-setup on first request for Vercel
if os.environ.get('VERCEL_URL'):
    try:
        import django
        from django.conf import settings
        from django.core.management import execute_from_command_line
        
        # Ensure database tables exist
        try:
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if not tables:  # No tables exist, run migrations
                print("No tables found, running migrations...")
                execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
                
                # Create superuser
                from django.contrib.auth import get_user_model
                User = get_user_model()
                if not User.objects.filter(username='admin').exists():
                    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
                    print("Created admin user")
                    
        except Exception as db_error:
            print(f"Database setup error (continuing): {db_error}")
            
    except Exception as e:
        print(f"Setup error (continuing): {e}")

# Vercel handler
app = application
