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

application = get_wsgi_application()

# Vercel handler
app = application
