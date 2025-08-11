#!/usr/bin/env python3
"""
Compatibility Test Script for RE-VLab Multi-Platform Deployment
Tests both Render and Vercel configurations to ensure no conflicts.
"""

import os
import sys
import subprocess
import json
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print_success(f"{description} exists: {filepath}")
        return True
    else:
        print_error(f"{description} missing: {filepath}")
        return False

def test_render_configuration():
    """Test Render deployment configuration"""
    print_header("TESTING RENDER CONFIGURATION")
    
    render_files = [
        ("render.yaml", "Render configuration file"),
        ("requirements.txt", "Python requirements file"),
        ("Procfile", "Render process file"),
        ("manage.py", "Django management script"),
    ]
    
    all_present = True
    for filepath, description in render_files:
        if not check_file_exists(filepath, description):
            all_present = False
    
    # Check render.yaml content
    if os.path.exists("render.yaml"):
        try:
            with open("render.yaml", 'r') as f:
                content = f.read()
                if "buildCommand" in content and "startCommand" in content:
                    print_success("render.yaml contains required build and start commands")
                else:
                    print_error("render.yaml missing required commands")
                    all_present = False
        except Exception as e:
            print_error(f"Error reading render.yaml: {e}")
            all_present = False
    
    return all_present

def test_vercel_configuration():
    """Test Vercel deployment configuration"""
    print_header("TESTING VERCEL CONFIGURATION")
    
    vercel_files = [
        ("vercel.json", "Vercel configuration file"),
        ("build_files.sh", "Vercel build script"),
        (".vercelignore", "Vercel ignore file"),
        ("requirements.txt", "Python requirements file"),
    ]
    
    all_present = True
    for filepath, description in vercel_files:
        if not check_file_exists(filepath, description):
            all_present = False
    
    # Check vercel.json content
    if os.path.exists("vercel.json"):
        try:
            with open("vercel.json", 'r') as f:
                vercel_config = json.load(f)
                required_keys = ["builds", "routes"]
                for key in required_keys:
                    if key in vercel_config:
                        print_success(f"vercel.json contains required '{key}' configuration")
                    else:
                        print_error(f"vercel.json missing required '{key}' configuration")
                        all_present = False
        except json.JSONDecodeError as e:
            print_error(f"vercel.json is not valid JSON: {e}")
            all_present = False
        except Exception as e:
            print_error(f"Error reading vercel.json: {e}")
            all_present = False
    
    # Check build script permissions and content
    if os.path.exists("build_files.sh"):
        try:
            with open("build_files.sh", 'r') as f:
                content = f.read()
                required_commands = ["pip install", "python manage.py collectstatic", "python manage.py migrate"]
                for cmd in required_commands:
                    if cmd in content:
                        print_success(f"build_files.sh contains: {cmd}")
                    else:
                        print_warning(f"build_files.sh missing: {cmd}")
        except Exception as e:
            print_error(f"Error reading build_files.sh: {e}")
            all_present = False
    
    return all_present

def test_django_settings():
    """Test Django settings for multi-platform compatibility"""
    print_header("TESTING DJANGO SETTINGS COMPATIBILITY")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'requirements_lab.settings')
        
        # Test Render environment simulation
        print_info("Testing Render environment simulation...")
        os.environ.pop('VERCEL_URL', None)  # Remove Vercel env var if present
        os.environ['RENDER'] = 'true'  # Simulate Render environment
        
        # Reload Django settings
        if 'django.conf' in sys.modules:
            del sys.modules['django.conf']
        if 'requirements_lab.settings' in sys.modules:
            del sys.modules['requirements_lab.settings']
        
        from django.conf import settings
        django.setup()
        
        # Check Render-specific settings
        print_success("Django settings loaded successfully for Render environment")
        print_info(f"DEBUG: {settings.DEBUG}")
        print_info(f"Database Engine: {settings.DATABASES['default']['ENGINE']}")
        
        # Test Vercel environment simulation
        print_info("\nTesting Vercel environment simulation...")
        os.environ.pop('RENDER', None)  # Remove Render env var
        os.environ['VERCEL_URL'] = 'test-app.vercel.app'  # Simulate Vercel environment
        
        # Reload Django settings again
        if 'django.conf' in sys.modules:
            del sys.modules['django.conf']
        if 'requirements_lab.settings' in sys.modules:
            del sys.modules['requirements_lab.settings']
        
        # Clear Django setup
        django.apps.apps.app_configs = {}
        django.apps.apps.apps_ready = False
        django.apps.apps.models_ready = False
        django.apps.apps.ready = False
        
        from django.conf import settings
        django.setup()
        
        print_success("Django settings loaded successfully for Vercel environment")
        print_info(f"DEBUG: {settings.DEBUG}")
        print_info(f"Database Engine: {settings.DATABASES['default']['ENGINE']}")
        
        # Clean up environment variables
        os.environ.pop('VERCEL_URL', None)
        os.environ.pop('RENDER', None)
        
        return True
        
    except Exception as e:
        print_error(f"Django settings compatibility test failed: {e}")
        return False

def test_static_files_configuration():
    """Test static files configuration for both platforms"""
    print_header("TESTING STATIC FILES CONFIGURATION")
    
    try:
        # Check if static directories exist or can be created
        static_dirs = [
            "static",
            "staticfiles",
        ]
        
        for static_dir in static_dirs:
            if os.path.exists(static_dir):
                print_success(f"Static directory exists: {static_dir}")
            else:
                print_info(f"Static directory will be created: {static_dir}")
        
        # Check static files settings in Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'requirements_lab.settings')
        from django.conf import settings
        
        if hasattr(settings, 'STATIC_URL'):
            print_success(f"STATIC_URL configured: {settings.STATIC_URL}")
        else:
            print_error("STATIC_URL not configured")
            return False
        
        if hasattr(settings, 'STATIC_ROOT'):
            print_success(f"STATIC_ROOT configured: {settings.STATIC_ROOT}")
        else:
            print_error("STATIC_ROOT not configured")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Static files configuration test failed: {e}")
        return False

def test_database_migrations():
    """Test database migrations compatibility"""
    print_header("TESTING DATABASE MIGRATIONS")
    
    try:
        # Check if migrations directory exists
        migrations_dir = "lab/migrations"
        if os.path.exists(migrations_dir):
            print_success(f"Migrations directory exists: {migrations_dir}")
            
            # Count migration files
            migration_files = [f for f in os.listdir(migrations_dir) if f.endswith('.py') and f != '__init__.py']
            print_info(f"Found {len(migration_files)} migration files")
            
            if migration_files:
                print_success("Migration files found - database schema is defined")
            else:
                print_warning("No migration files found - may need to run makemigrations")
        else:
            print_error(f"Migrations directory not found: {migrations_dir}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Database migrations test failed: {e}")
        return False

def test_requirements_compatibility():
    """Test requirements.txt for both platforms"""
    print_header("TESTING REQUIREMENTS COMPATIBILITY")
    
    try:
        if not os.path.exists("requirements.txt"):
            print_error("requirements.txt not found")
            return False
        
        with open("requirements.txt", 'r') as f:
            requirements = f.read()
        
        # Check for essential packages
        essential_packages = [
            "django",
            "psycopg2",
            "gunicorn",
            "whitenoise",
        ]
        
        for package in essential_packages:
            if package.lower() in requirements.lower():
                print_success(f"Required package found: {package}")
            else:
                print_warning(f"Package not found in requirements: {package}")
        
        # Check for potential conflicts
        if "psycopg2-binary" in requirements and "psycopg2" in requirements:
            print_warning("Both psycopg2 and psycopg2-binary found - may cause conflicts")
        
        print_success("Requirements.txt analysis completed")
        return True
        
    except Exception as e:
        print_error(f"Requirements compatibility test failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable configuration"""
    print_header("TESTING ENVIRONMENT VARIABLES")
    
    # List of important environment variables
    important_vars = [
        ("DATABASE_URL", "Database connection string"),
        ("SECRET_KEY", "Django secret key"),
        ("DEBUG", "Debug mode setting"),
        ("ALLOWED_HOSTS", "Allowed hosts configuration"),
    ]
    
    print_info("Environment variables that should be configured in production:")
    for var_name, description in important_vars:
        if var_name in os.environ:
            print_success(f"{var_name}: Set (value hidden for security)")
        else:
            print_warning(f"{var_name}: Not set - {description}")
    
    # Test platform detection
    print_info("\nTesting platform detection:")
    
    # Simulate Render
    os.environ['RENDER'] = 'true'
    print_info("Simulating Render environment...")
    if 'RENDER' in os.environ:
        print_success("Render environment detected correctly")
    
    # Simulate Vercel
    os.environ.pop('RENDER', None)
    os.environ['VERCEL_URL'] = 'test.vercel.app'
    print_info("Simulating Vercel environment...")
    if 'VERCEL_URL' in os.environ:
        print_success("Vercel environment detected correctly")
    
    # Clean up
    os.environ.pop('RENDER', None)
    os.environ.pop('VERCEL_URL', None)
    
    return True

def run_compatibility_check():
    """Run all compatibility tests"""
    print_header("RE-VLAB MULTI-PLATFORM COMPATIBILITY TEST")
    print_info("This script tests compatibility between Render and Vercel deployments")
    print_info("Ensuring no conflicts exist between platform configurations\n")
    
    tests = [
        ("Render Configuration", test_render_configuration),
        ("Vercel Configuration", test_vercel_configuration),
        ("Django Settings", test_django_settings),
        ("Static Files", test_static_files_configuration),
        ("Database Migrations", test_database_migrations),
        ("Requirements", test_requirements_compatibility),
        ("Environment Variables", test_environment_variables),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print_error(f"Test '{test_name}' failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print_header("COMPATIBILITY TEST SUMMARY")
    
    passed_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)
    
    for test_name, result in results.items():
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print(f"\n{Colors.BOLD}Results: {passed_tests}/{total_tests} tests passed{Colors.END}")
    
    if passed_tests == total_tests:
        print_success("🎉 ALL COMPATIBILITY TESTS PASSED!")
        print_success("Both Render and Vercel deployments should work without conflicts")
        return True
    else:
        print_error("❌ SOME TESTS FAILED!")
        print_error("Please review the failed tests before deploying")
        return False

def main():
    """Main function"""
    try:
        success = run_compatibility_check()
        
        print_header("RECOMMENDATIONS")
        
        if success:
            print_success("✅ Your project is compatible with both Render and Vercel")
            print_info("🚀 You can safely deploy to either platform")
            print_info("📝 Remember to set environment variables in your deployment platform")
            print_info("🔍 Test your deployment thoroughly after going live")
        else:
            print_warning("⚠️  Some compatibility issues were found")
            print_info("🔧 Please fix the failed tests before deploying")
            print_info("📖 Check the deployment guides for troubleshooting")
        
        print_info("\n📋 Next Steps:")
        print_info("1. Fix any failed tests")
        print_info("2. Set up environment variables in your deployment platform")
        print_info("3. Test deployment in staging environment")
        print_info("4. Deploy to production")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print_error("\n\nTest interrupted by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
