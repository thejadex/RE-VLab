#!/usr/bin/env python3
"""
Quick Compatibility Check - Simple version of the compatibility test
"""

import os
import json
from pathlib import Path

def check_render_setup():
    """Quick check for Render configuration"""
    print("🔍 Checking Render Configuration...")
    
    files_to_check = ["render.yaml", "Procfile", "requirements.txt"]
    missing_files = []
    
    for file in files_to_check:
        if os.path.exists(file):
            print(f"  ✅ {file} - Found")
        else:
            print(f"  ❌ {file} - Missing")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_vercel_setup():
    """Quick check for Vercel configuration"""
    print("\n🔍 Checking Vercel Configuration...")
    
    files_to_check = ["vercel.json", "build_files.sh", "requirements.txt"]
    missing_files = []
    
    for file in files_to_check:
        if os.path.exists(file):
            print(f"  ✅ {file} - Found")
        else:
            print(f"  ❌ {file} - Missing")
            missing_files.append(file)
    
    # Check vercel.json structure
    if os.path.exists("vercel.json"):
        try:
            with open("vercel.json", 'r') as f:
                config = json.load(f)
                if "builds" in config and "routes" in config:
                    print(f"  ✅ vercel.json - Valid structure")
                else:
                    print(f"  ⚠️  vercel.json - Missing required sections")
        except:
            print(f"  ❌ vercel.json - Invalid JSON")
    
    return len(missing_files) == 0

def check_django_files():
    """Check Django project files"""
    print("\n🔍 Checking Django Project Files...")
    
    files_to_check = [
        "manage.py",
        "requirements_lab/settings.py", 
        "requirements_lab/wsgi.py",
        "lab/models.py"
    ]
    
    missing_files = []
    
    for file in files_to_check:
        if os.path.exists(file):
            print(f"  ✅ {file} - Found")
        else:
            print(f"  ❌ {file} - Missing")
            missing_files.append(file)
    
    return len(missing_files) == 0

def main():
    """Main compatibility check"""
    print("🚀 RE-VLab Quick Compatibility Check")
    print("=" * 50)
    
    render_ok = check_render_setup()
    vercel_ok = check_vercel_setup()
    django_ok = check_django_files()
    
    print("\n📊 Summary:")
    print(f"  Render Setup: {'✅ Ready' if render_ok else '❌ Issues found'}")
    print(f"  Vercel Setup: {'✅ Ready' if vercel_ok else '❌ Issues found'}")
    print(f"  Django Files: {'✅ Ready' if django_ok else '❌ Issues found'}")
    
    if render_ok and vercel_ok and django_ok:
        print("\n🎉 All configurations look good!")
        print("💡 Both Render and Vercel deployments should work")
        print("🔧 Remember to set environment variables on your deployment platform")
    else:
        print("\n⚠️  Some issues found - check the details above")
    
    return render_ok and vercel_ok and django_ok

if __name__ == "__main__":
    main()
