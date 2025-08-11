import os
import sys

# Test basic imports
print("Testing basic imports...")
try:
    import django
    print("✅ Django imported successfully")
except ImportError as e:
    print(f"❌ Django import failed: {e}")

# Set environment
os.environ['VERCEL_URL'] = 'test.vercel.app'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'requirements_lab.settings')

# Test Django setup
print("\nTesting Django setup...")
try:
    django.setup()
    print("✅ Django setup successful")
    
    from django.conf import settings
    print(f"✅ Settings loaded")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    import traceback
    traceback.print_exc()
