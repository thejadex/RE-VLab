#!/usr/bin/env python3
"""
Vercel Build Script for Django
This script is executed by Vercel to build the Django project
"""

import os
import sys
import subprocess

def main():
    """Main build function"""
    print("🔨 Building Django project for Vercel...")
    
    # Set environment variables
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'requirements_lab.settings')
    os.environ['VERCEL_URL'] = 'building.vercel.app'  # Temporary for build
    
    try:
        # Collect static files
        print("📁 Collecting static files...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput', '--clear'
        ], check=True, capture_output=True, text=True)
        
        print("✅ Static files collected successfully")
        print("🎉 Build completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
