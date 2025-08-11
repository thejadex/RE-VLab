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
        from django.contrib.auth.models import User
        import django
        django.setup()
        
        # Check if database is initialized
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
            if not cursor.fetchone():
                # Run migrations
                execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
                
        # Create test users directly
        try:
            # Create admin user
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@example.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            admin_user.set_password('admin123')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            
            # Create admin profile
            from lab.models import UserProfile
            UserProfile.objects.get_or_create(
                user=admin_user,
                defaults={'role': 'admin'}
            )
            
            # Create student user
            student_user, created = User.objects.get_or_create(
                username='student',
                defaults={
                    'email': 'student@example.com',
                    'first_name': 'Test',
                    'last_name': 'Student'
                }
            )
            student_user.set_password('student123')
            student_user.save()
            
            # Create student profile
            UserProfile.objects.get_or_create(
                user=student_user,
                defaults={'role': 'student', 'student_id': 'STU001'}
            )
            
            print("✓ Test users created: admin/admin123, student/student123")
            
        except Exception as e:
            print(f"User creation error: {e}")
            
    except Exception as e:
        print(f"Database initialization error: {e}")

# Vercel handler
app = application
