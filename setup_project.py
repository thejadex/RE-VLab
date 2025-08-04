#!/usr/bin/env python
"""
Complete setup script for Requirements Engineering Lab
Run this script to set up the entire project from scratch
"""

import os
import sys
import subprocess
import django
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Requirements Engineering Lab...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Step 1: Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("⚠️  Warning: Some dependencies might not have installed correctly")
    
    # Step 2: Create migrations
    if not run_command("python manage.py makemigrations", "Creating database migrations"):
        print("❌ Failed to create migrations")
        sys.exit(1)
    
    # Step 3: Apply migrations
    if not run_command("python manage.py migrate", "Applying database migrations"):
        print("❌ Failed to apply migrations")
        sys.exit(1)
    
    # Step 4: Create sample data
    if not run_command("python manage.py setup_lab", "Creating sample data"):
        print("❌ Failed to create sample data")
        sys.exit(1)
    
    # Step 5: Run tests
    print("🧪 Running tests...")
    if run_command("python manage.py test", "Running test suite"):
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed, but the system should still work")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Open: http://127.0.0.1:8000")
    print("3. Login with:")
    print("   👨‍💼 Admin: admin / admin123")
    print("   👨‍🎓 Student: student1 / student123")
    print("\n🔧 Troubleshooting:")
    print("- If you see errors, try: python manage.py check_setup")
    print("- For help, check the README.md file")

if __name__ == "__main__":
    main()
