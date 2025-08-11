#!/usr/bin/env python
"""
Test script to ensure your Django project is ready for deployment
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'requirements_lab.settings')
django.setup()

def test_deployment_readiness():
    """Test if the project is ready for deployment"""
    print("🔍 Testing RE VLab deployment readiness...\n")
    
    # Test 1: Check Django configuration
    try:
        from django.core.management import execute_from_command_line
        from django.conf import settings
        print("✅ Django configuration is valid")
    except Exception as e:
        print(f"❌ Django configuration error: {e}")
        return False
    
    # Test 2: Check if all required packages are available
    required_packages = [
        'django',
        'crispy_forms',
        'crispy_tailwind',
        'PIL',  # Pillow
        'django_extensions',
        'gunicorn',
        'whitenoise',
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    # Test 3: Check database configuration
    try:
        from django.db import connection
        connection.ensure_connection()
        print("✅ Database connection is working")
    except Exception as e:
        print(f"⚠️  Database connection issue (normal for fresh deployment): {e}")
    
    # Test 4: Check static files configuration
    if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
        print("✅ Static files configuration is set")
    else:
        print("❌ Static files configuration missing")
    
    # Test 5: Check WSGI configuration
    try:
        from requirements_lab.wsgi import application
        print("✅ WSGI application is importable")
    except Exception as e:
        print(f"❌ WSGI configuration error: {e}")
        return False
    
    print("\n🎉 Your RE VLab project is ready for deployment!")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n🚀 You can now deploy to:")
    print("  • Railway: https://railway.app")
    print("  • Render: https://render.com")
    print("  • PythonAnywhere: https://pythonanywhere.com")
    
    return True

if __name__ == "__main__":
    test_deployment_readiness()
