#!/usr/bin/env python
"""
Complete reset and setup script for Requirements Engineering Lab
This will delete the database and start fresh
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def main():
    print("🚀 Resetting and setting up Requirements Engineering Lab...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Step 1: Remove old database and migrations
    print("🗑️  Cleaning up old files...")
    
    # Remove database
    db_file = Path('db.sqlite3')
    if db_file.exists():
        db_file.unlink()
        print("✅ Removed old database")
    
    # Remove migration files (keep __init__.py)
    migrations_dir = Path('lab/migrations')
    if migrations_dir.exists():
        for file in migrations_dir.glob('*.py'):
            if file.name != '__init__.py':
                file.unlink()
        print("✅ Removed old migration files")
    
    # Step 2: Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("⚠️  Warning: Some dependencies might not have installed correctly")
    
    # Step 3: Create migrations specifically for lab app
    if not run_command("python manage.py makemigrations lab", "Creating lab app migrations"):
        print("❌ Failed to create lab migrations")
        sys.exit(1)
    
    # Step 4: Apply all migrations
    if not run_command("python manage.py migrate", "Applying all migrations"):
        print("❌ Failed to apply migrations")
        sys.exit(1)
    
    # Step 5: Create sample data
    if not run_command("python manage.py setup_lab", "Creating sample data"):
        print("❌ Failed to create sample data")
        sys.exit(1)
    
    # Step 6: Create superuser (optional)
    print("🔧 Creating additional superuser (optional)...")
    print("You can skip this by pressing Ctrl+C")
    try:
        subprocess.run("python manage.py createsuperuser", shell=True, check=False)
    except KeyboardInterrupt:
        print("⏭️  Skipped superuser creation")
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Open: http://127.0.0.1:8000")
    print("3. Login with:")
    print("   👨‍💼 Admin: admin / admin123")
    print("   👨‍🎓 Student: student1 / student123")
    print("\n🔧 Features available:")
    print("- ✅ User registration (now working)")
    print("- ✅ Student dashboard with progress tracking")
    print("- ✅ Scenario-based requirements elicitation")
    print("- ✅ Admin panel for managing scenarios")
    print("- ✅ Feedback system")
    print("- ✅ Notifications")

if __name__ == "__main__":
    main()
