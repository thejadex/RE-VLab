#!/usr/bin/env python3
"""
Vercel Deployment Checker for RE VLab
Run this script to check if your project is ready for Vercel deployment.
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print status."""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (MISSING)")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists and print status."""
    if Path(dir_path).is_dir():
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} (MISSING)")
        return False

def check_requirements():
    """Check if required packages are in requirements.txt."""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    content = requirements_file.read_text()
    required_packages = ["Django", "gunicorn", "whitenoise"]
    missing_packages = []
    
    for package in required_packages:
        if package.lower() not in content.lower():
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages in requirements.txt: {', '.join(missing_packages)}")
        return False
    else:
        print("✅ All required packages found in requirements.txt")
        return True

def main():
    """Main deployment check function."""
    print("🚀 RE VLab Vercel Deployment Checker")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Check required files
    files_to_check = [
        ("vercel.json", "Vercel configuration"),
        ("build_files.sh", "Build script"),
        ("requirements.txt", "Python dependencies"),
        ("manage.py", "Django management script"),
        ("requirements_lab/wsgi.py", "WSGI application"),
        ("requirements_lab/settings.py", "Django settings"),
    ]
    
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # Check directories
    dirs_to_check = [
        ("templates", "Templates directory"),
        ("lab", "Lab app directory"),
        ("requirements_lab", "Project directory"),
    ]
    
    for dir_path, description in dirs_to_check:
        if not check_directory_exists(dir_path, description):
            all_checks_passed = False
    
    # Check requirements
    if not check_requirements():
        all_checks_passed = False
    
    # Check build script permissions (Unix-like systems)
    build_script = Path("build_files.sh")
    if build_script.exists() and hasattr(os, 'access'):
        if os.access(build_script, os.X_OK):
            print("✅ Build script has execute permissions")
        else:
            print("⚠️  Build script may need execute permissions (chmod +x build_files.sh)")
    
    print("\n" + "=" * 50)
    
    if all_checks_passed:
        print("🎉 All checks passed! Your project is ready for Vercel deployment.")
        print("\nNext steps:")
        print("1. Push your code to a Git repository")
        print("2. Connect the repository to Vercel")
        print("3. Configure environment variables")
        print("4. Deploy!")
        print("\nSee VERCEL_DEPLOYMENT.md for detailed instructions.")
    else:
        print("❌ Some checks failed. Please fix the issues above before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main()
