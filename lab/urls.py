from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Scenarios (Student)
    path('scenarios/', views.scenario_list, name='scenario_list'),
    path('scenarios/<int:pk>/', views.scenario_detail, name='scenario_detail'),
    
    # Requirements
    path('submissions/<int:submission_id>/add-requirement/', views.add_requirement, name='add_requirement'),
    path('requirements/<int:pk>/edit/', views.edit_requirement, name='edit_requirement'),
    path('requirements/<int:pk>/delete/', views.delete_requirement, name='delete_requirement'),
    
    # Submissions
    path('submissions/<int:submission_id>/submit/', views.submit_scenario, name='submit_scenario'),
    path('submissions/<int:pk>/', views.submission_detail, name='submission_detail'),
    
    # SRS Documents
    # path('submissions/<int:submission_id>/srs/', views.srs_document, name='srs_document'),
    path('srs_document/', views.srs_document, name='srs_document'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    
    # Admin URLs (Fixed paths)
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/scenarios/', views.admin_scenarios, name='admin_scenarios'),
    path('admin-panel/scenarios/create/', views.create_scenario, name='create_scenario'),
    path('admin-panel/scenarios/<int:pk>/edit/', views.edit_scenario, name='edit_scenario'),
    path('admin-panel/scenarios/<int:pk>/delete/', views.delete_scenario, name='delete_scenario'),
    path('admin-panel/submissions/', views.admin_submissions, name='admin_submissions'),
    path('admin-panel/submissions/<int:submission_id>/feedback/', views.add_feedback, name='add_feedback'),
    
    # API endpoints for AJAX
    path('api/toggle-theme/', views.toggle_theme, name='toggle_theme'),

    path('student/dashboard/', views.student_dashboard, name='student_dashboard')
]
