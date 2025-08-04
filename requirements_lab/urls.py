"""
URL configuration for requirements_lab project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lab.urls')),
    path('lab/', RedirectView.as_view(url='/', permanent=True)),  # Redirect lab/ to home
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
