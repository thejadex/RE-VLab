from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import date
# from django.views.decorators.cache import cache_page

import json
from .models import (
    UserProfile, Scenario, ScenarioSubmission, Requirement, 
    Feedback, SRSDocument, Notification
)
from .forms import (
    StudentRegistrationForm, ScenarioForm, RequirementForm, 
    FeedbackForm, SRSDocumentForm
)


def check_admin_permission(request):
    """
    Helper function to check if user has admin permissions.
    Returns (is_admin, user_profile) tuple.
    Handles superusers properly by creating/updating their profiles.
    """
    if request.user.is_superuser:
        # Ensure superuser has admin profile
        user_profile, created = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={'role': 'admin'}
        )
        if user_profile.role != 'admin':
            user_profile.role = 'admin'
            user_profile.save()
        return True, user_profile
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        return user_profile.role == 'admin', user_profile
    except UserProfile.DoesNotExist:
        # Create student profile for non-superusers
        user_profile = UserProfile.objects.create(user=request.user, role='student')
        return False, user_profile

def home(request):
    # Redirect authenticated users to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'lab/home.html')


def register(request):
    # Redirect authenticated users to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful! Welcome to the Requirements Lab.')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def custom_login(request):
    # Redirect authenticated users to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')

def custom_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard(request):
    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'admin' if request.user.is_superuser else 'student'}
    )
    
    # If this is a superuser but profile says student, update to admin
    if request.user.is_superuser and user_profile.role != 'admin':
        user_profile.role = 'admin'
        user_profile.save()
    
    if user_profile.role == 'admin' or request.user.is_superuser:
        return admin_dashboard(request)
    else:
        return student_dashboard(request)

# @cache_page(60 * 20)
def student_dashboard(request):
    # Get active scenarios (scenarios the student has started but not completed)
    active_submissions = ScenarioSubmission.objects.filter(
        student=request.user,
        status='draft'
    ).select_related('scenario')[:5]
    
    # Get user's submissions for progress tracking
    submissions = ScenarioSubmission.objects.filter(student=request.user)
    
    # Calculate progress including partial progress for active submissions
    total_scenarios = Scenario.objects.filter(is_active=True).count()
    completed_scenarios = submissions.filter(status__in=['submitted', 'feedback_received']).values_list('scenario_id', flat=True).distinct()
    completed_count = len(completed_scenarios)
    
    # Calculate partial progress for active (draft) submissions
    active_submissions_data = submissions.filter(status='draft').select_related('scenario')
    active_progress = 0
    
    for active_sub in active_submissions_data:
        # Count total requirements for the scenario and user's progress
        total_reqs = Requirement.objects.filter(submission=active_sub).count()
        if total_reqs > 0:
            # Add partial progress (0.5 for scenarios with active work)
            active_progress += 0.5
    
    # Calculate total progress: completed scenarios + partial progress from active work
    total_progress = completed_count + active_progress
    progress_percentage = round((total_progress / total_scenarios * 100)) if total_scenarios > 0 else 0
    
    # Get recent activities (completed submissions)
    recent_activities = submissions.filter(status='submitted').order_by('-submitted_at')[:5]
    
    # Get feedback count
    feedback_count = submissions.filter(status='feedback_received').count()
    
    # Get draft submissions count for sidebar
    draft_submissions = submissions.filter(status='draft').count()
    completed_submissions = submissions.filter(status__in=['submitted', 'feedback_received']).count()
    
    context = {
        'active_submissions': active_submissions,
        'completed_scenarios': completed_scenarios,
        'progress_percentage': progress_percentage,
        'recent_activities': recent_activities,
        'feedback_count': feedback_count,
        'total_scenarios': total_scenarios,
        'completed_count': completed_count,
        'draft_submissions': draft_submissions,
        'completed_submissions': completed_submissions,
    }
    
    return render(request, 'lab/student_dashboard.html', context)

# @cache_page(60 * 20)
@login_required
def admin_dashboard(request):
    # Check admin permissions using helper function
    is_admin, user_profile = check_admin_permission(request)
    if not is_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Get admin statistics
    total_scenarios = Scenario.objects.count()
    total_students = UserProfile.objects.filter(role='student').count()
    total_submissions = ScenarioSubmission.objects.count()
    pending_reviews = ScenarioSubmission.objects.filter(status='submitted').count()
    
    # Get recent submissions for review
    recent_submissions = ScenarioSubmission.objects.filter(
        status='submitted'
    ).order_by('-submitted_at')[:5]
    
    # Get recent activity (scenarios created, submissions reviewed, new students)
    recent_activities = []
    
    # Recent scenarios created
    recent_scenarios = Scenario.objects.filter(created_by=request.user).order_by('-created_at')[:3]
    for scenario in recent_scenarios:
        recent_activities.append({
            'type': 'scenario_created',
            'title': 'New scenario created',
            'description': scenario.title,
            'time': scenario.created_at,
            'icon': 'fas fa-plus',
            'color': 'from-blue-500 to-blue-600'
        })
    
    # Recent feedback given
    recent_feedback = Feedback.objects.filter(admin=request.user).order_by('-created_at')[:3]
    for feedback in recent_feedback:
        recent_activities.append({
            'type': 'feedback_given',
            'title': 'Submission reviewed',
            'description': f"Feedback for {feedback.submission.scenario.title}",
            'time': feedback.created_at,
            'icon': 'fas fa-check',
            'color': 'from-green-500 to-green-600'
        })
    
    # Recent student registrations
    recent_students = UserProfile.objects.filter(role='student').order_by('-created_at')[:3]
    for student_profile in recent_students:
        recent_activities.append({
            'type': 'student_registered',
            'title': 'New student registered',
            'description': student_profile.user.get_full_name() or student_profile.user.username,
            'time': student_profile.created_at,
            'icon': 'fas fa-user',
            'color': 'from-purple-500 to-purple-600'
        })
    
    # Sort all activities by time and take the most recent 5
    recent_activities.sort(key=lambda x: x['time'], reverse=True)
    recent_activities = recent_activities[:5]
    
    context = {
        'total_scenarios': total_scenarios,
        'total_students': total_students,
        'total_submissions': total_submissions,
        'pending_reviews': pending_reviews,
        'recent_submissions': recent_submissions,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'lab/admin_dashboard.html', context)

# @login_required
# def scenario_list(request):
#     # Only students should access this
#     user_profile = get_object_or_404(UserProfile, user=request.user)
#     if user_profile.role != 'student':
#         return redirect('admin_scenarios')
    
#     scenarios = Scenario.objects.filter(is_active=True)
#     user_submissions = {}
    
#     submissions = ScenarioSubmission.objects.filter(student=request.user)
#     user_submissions = {sub.scenario_id: sub for sub in submissions}
    
#     context = {
#         'scenarios': scenarios,
#         'user_submissions': user_submissions,
#     }
    
#     return render(request, 'lab/scenario_list.html', context)

@login_required
def scenario_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.role != 'student':
        return redirect('admin_scenarios')

    scenarios = Scenario.objects.filter(is_active=True)
    submissions = ScenarioSubmission.objects.filter(student=request.user)
    submissions_by_scenario = {sub.scenario_id: sub for sub in submissions}

    # Attach submission to each scenario (or None)
    for scenario in scenarios:
        scenario.user_submission = submissions_by_scenario.get(scenario.id)
        # Add status for template logic
        if scenario.user_submission:
            scenario.submission_status = scenario.user_submission.status
        else:
            scenario.submission_status = 'not_started'

    context = {
        'scenarios': scenarios,
    }
    return render(request, 'lab/scenario_list.html', context)

@login_required
def scenario_detail(request, pk):
    scenario = get_object_or_404(Scenario, pk=pk, is_active=True)
    
    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'student'}
    )
    
    # Check if user is admin
    if user_profile.role == 'admin':
        # Admin can view scenario details but not work on them
        context = {
            'scenario': scenario,
            'is_admin_view': True,
            'submission': None,
            'user_submission': None,
            'functional_reqs': [],
            'non_functional_reqs': [],
            'business_reqs': [],
            'requirement_form': None,
        }
        return render(request, 'lab/scenario_detail.html', context)
    
    # Only students can work on scenarios
    if user_profile.role != 'student':
        messages.error(request, 'Access denied. Only students can work on scenarios.')
        return redirect('admin_scenarios')
    
    # Get or create submission for student
    submission, created = ScenarioSubmission.objects.get_or_create(
        scenario=scenario,
        student=request.user,
        defaults={'status': 'draft'}
    )
    
    # Get requirements grouped by type
    functional_reqs = submission.requirements.filter(requirement_type='functional')
    non_functional_reqs = submission.requirements.filter(requirement_type='non_functional')
    business_reqs = submission.requirements.filter(requirement_type='business')
    
    context = {
        'scenario': scenario,
        'submission': submission,
        'user_submission': submission,  # Add this for template compatibility
        'functional_reqs': functional_reqs,
        'non_functional_reqs': non_functional_reqs,
        'business_reqs': business_reqs,
        'requirement_form': RequirementForm(),
        'is_admin_view': False,
    }
    
    return render(request, 'lab/scenario_detail.html', context)

@login_required
def add_requirement(request, submission_id):
    submission = get_object_or_404(ScenarioSubmission, pk=submission_id, student=request.user)
    
    if submission.status != 'draft':
        messages.error(request, 'Cannot modify submitted requirements.')
        return redirect('scenario_detail', pk=submission.scenario.pk)
    
    # if submission.status not in ['draft', 'feedback_received']:
    #     messages.error(request, 'Cannot modify submitted requirements.')
    #     return redirect('scenario_detail', pk=submission.scenario.pk)
    
    if request.method == 'POST':
        form = RequirementForm(request.POST)
        if form.is_valid():
            requirement = form.save(commit=False)
            requirement.submission = submission
            requirement.save()
            messages.success(request, f'Requirement "{requirement.title}" added successfully!')
            return redirect('scenario_detail', pk=submission.scenario.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    
    return redirect('scenario_detail', pk=submission.scenario.pk)

@login_required
def edit_requirement(request, pk):
    requirement = get_object_or_404(Requirement, pk=pk, submission__student=request.user)
    
    if requirement.submission.status != 'draft':
        messages.error(request, 'Cannot modify submitted requirements.')
        return redirect('scenario_detail', pk=requirement.submission.scenario.pk)
    
    if request.method == 'POST':
        form = RequirementForm(request.POST, instance=requirement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Requirement updated successfully!')
            return redirect('scenario_detail', pk=requirement.submission.scenario.pk)
    else:
        form = RequirementForm(instance=requirement)
    
    context = {
        'form': form,
        'requirement': requirement,
    }
    
    return render(request, 'lab/edit_requirement.html', context)

@login_required
def delete_requirement(request, pk):
    requirement = get_object_or_404(Requirement, pk=pk, submission__student=request.user)
    
    if requirement.submission.status != 'draft':
        messages.error(request, 'Cannot modify submitted requirements.')
        return redirect('scenario_detail', pk=requirement.submission.scenario.pk)
    
    if request.method == 'POST':
        scenario_pk = requirement.submission.scenario.pk
        requirement.delete()
        messages.success(request, 'Requirement deleted successfully!')
        return redirect('scenario_detail', pk=scenario_pk)
    
    return render(request, 'lab/delete_requirement.html', {'requirement': requirement})

@login_required
def submit_scenario(request, submission_id):
    submission = get_object_or_404(ScenarioSubmission, pk=submission_id, student=request.user)
    
    if submission.status != 'draft':
        messages.error(request, 'This submission has already been submitted.')
        return redirect('scenario_detail', pk=submission.scenario.pk)
    
    if request.method == 'POST':
        # Check if submission has requirements
        if not submission.requirements.exists():
            messages.error(request, 'Please add at least one requirement before submitting.')
            return redirect('scenario_detail', pk=submission.scenario.pk)
        
        submission.submit()
        messages.success(request, 'Scenario submitted successfully! You will receive feedback soon.')
        
        # Create notification for admins
        admin_users = UserProfile.objects.filter(role='admin').values_list('user', flat=True)
        for admin_user_id in admin_users:
            Notification.objects.create(
                user_id=admin_user_id,
                title='New Submission for Review',
                message=f'{request.user.get_full_name() or request.user.username} submitted requirements for {submission.scenario.title}',
                link=f'/submissions/{submission.pk}/'
            )
        
        return redirect('dashboard')
    
    return render(request, 'lab/submit_scenario.html', {'submission': submission})

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark notifications as read when viewed
    notifications.filter(is_read=False).update(is_read=True)
    
    paginator = Paginator(notifications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'lab/notifications.html', {'page_obj': page_obj})

# Admin Views
@login_required
def admin_scenarios(request):
    is_admin, user_profile = check_admin_permission(request)
    if not is_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    scenarios = Scenario.objects.all().order_by('-created_at')
    return render(request, 'lab/admin_scenarios.html', {'scenarios': scenarios})

@login_required
def create_scenario(request):
    is_admin, user_profile = check_admin_permission(request)
    if not is_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ScenarioForm(request.POST)
        if form.is_valid():
            scenario = form.save(commit=False)
            scenario.created_by = request.user
            scenario.save()
            messages.success(request, 'Scenario created successfully!')
            return redirect('admin_scenarios')
    else:
        form = ScenarioForm()
    
    return render(request, 'lab/create_scenario.html', {'form': form})

@login_required
def edit_scenario(request, pk):
    is_admin, user_profile = check_admin_permission(request)
    if not is_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    scenario = get_object_or_404(Scenario, pk=pk)
    
    if request.method == 'POST':
        form = ScenarioForm(request.POST, instance=scenario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Scenario updated successfully!')
            return redirect('admin_scenarios')
    else:
        form = ScenarioForm(instance=scenario)
    
    return render(request, 'lab/edit_scenario.html', {'form': form, 'scenario': scenario})

@login_required
def delete_scenario(request, pk):
    is_admin, user_profile = check_admin_permission(request)
    if not is_admin:
        messages.error(request, 'Access denied.')
        return redirect('admin_dashboard')
    
    scenario = get_object_or_404(Scenario, pk=pk)
    
    if request.method == 'POST':
        scenario_title = scenario.title
        scenario.delete()
        messages.success(request, f'Scenario "{scenario_title}" has been deleted successfully.')
        return redirect('admin_scenarios')
    
    return redirect('admin_scenarios')

@login_required
def admin_submissions(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.role != 'admin' and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Get all submissions
    submissions = ScenarioSubmission.objects.select_related('scenario', 'student', 'student__userprofile').prefetch_related('requirements').all().order_by('-updated_at')
    
    # Calculate statistics
    total_submissions = submissions.count()
    pending_reviews = submissions.filter(status='submitted').count()
    completed_reviews = submissions.filter(status='feedback_received').count()
    draft_submissions = submissions.filter(status='draft').count()
    
    # Get scenario statistics
    scenario_stats = {}
    scenarios = Scenario.objects.filter(is_active=True).annotate(
        submission_count=Count('scenariosubmission'),
        submitted_count=Count('scenariosubmission', filter=Q(scenariosubmission__status='submitted')),
        draft_count=Count('scenariosubmission', filter=Q(scenariosubmission__status='draft'))
    ).order_by('title')
    
    for scenario in scenarios:
        scenario_stats[scenario.id] = {
            'title': scenario.title,
            'total': scenario.submission_count,
            'submitted': scenario.submitted_count,
            'draft': scenario.draft_count,
        }
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        submissions = submissions.filter(status=status_filter)
    
    # Filter by scenario if provided
    scenario_filter = request.GET.get('scenario')
    if scenario_filter:
        submissions = submissions.filter(scenario_id=scenario_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        submissions = submissions.filter(
            Q(student__username__icontains=search_query) |
            Q(student__first_name__icontains=search_query) |
            Q(student__last_name__icontains=search_query) |
            Q(scenario__title__icontains=search_query)
        )
    
    # Get recent activity for submissions
    recent_submissions = submissions.filter(status='submitted').order_by('-submitted_at')[:5]
    
    # Pagination
    paginator = Paginator(submissions, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'scenarios': scenarios,
        'scenario_stats': scenario_stats,
        'total_submissions': total_submissions,
        'pending_reviews': pending_reviews,
        'completed_reviews': completed_reviews,
        'draft_submissions': draft_submissions,
        'recent_submissions': recent_submissions,
        'status_filter': status_filter,
        'scenario_filter': scenario_filter,
        'search_query': search_query,
    }
    
    return render(request, 'lab/admin_submissions.html', context)

@login_required
def submission_detail(request, pk):
    submission = get_object_or_404(ScenarioSubmission, pk=pk)
    
    # Check permissions
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.role == 'admin':
        # Admin can view any submission
        pass
    elif submission.student == request.user:
        # Student can view their own submission
        pass
    else:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Get requirements grouped by type
    functional_reqs = submission.requirements.filter(requirement_type='functional')
    non_functional_reqs = submission.requirements.filter(requirement_type='non_functional')
    business_reqs = submission.requirements.filter(requirement_type='business')
    
    # Get feedback
    feedbacks = submission.feedbacks.all().order_by('-created_at')
    
    context = {
        'submission': submission,
        'functional_reqs': functional_reqs,
        'non_functional_reqs': non_functional_reqs,
        'business_reqs': business_reqs,
        'feedbacks': feedbacks,
        'feedback_form': FeedbackForm() if user_profile.role == 'admin' else None,
    }
    
    return render(request, 'lab/submission_detail.html', context)

@login_required
def add_feedback(request, submission_id):
    is_admin, user_profile = check_admin_permission(request)
    if not is_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    submission = get_object_or_404(ScenarioSubmission, pk=submission_id)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.submission = submission
            feedback.admin = request.user
            feedback.save()
            
            # Update submission status
            submission.status = 'feedback_received'
            submission.save()
            
            # Create notification for student
            Notification.objects.create(
                user=submission.student,
                title='New Feedback Received',
                message=f'You have received feedback for {submission.scenario.title}',
                link=f'/submissions/{submission.pk}/'
            )
            
            messages.success(request, 'Feedback added successfully!')
            return redirect('submission_detail', pk=submission.pk)
    
    return redirect('submission_detail', pk=submission.pk)

@login_required
# def srs_document(request, submission_id):
#     submission = get_object_or_404(ScenarioSubmission, pk=submission_id, student=request.user)
    
#     srs_doc, created = SRSDocument.objects.get_or_create(submission=submission)
    
#     if request.method == 'POST':
#         form = SRSDocumentForm(request.POST, instance=srs_doc)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'SRS Document saved successfully!')
#             return redirect('srs_document', submission_id=submission.pk)
#     else:
#         form = SRSDocumentForm(instance=srs_doc)
    
#     context = {
#         'form': form,
#         'submission': submission,
#         'srs_doc': srs_doc,
#     }
    
#     return render(request, 'lab/srs_document.html', context)

def srs_document(request):
    return render(request, 'lab/srs_document.html', {
        'today': date.today().strftime('%Y-%m-%d')
    })


# API Views
@login_required
@require_POST
def toggle_theme(request):
    """Toggle between light and dark theme"""
    try:
        data = json.loads(request.body)
        theme = data.get('theme', 'light')
        
        # Store theme preference in session
        request.session['theme'] = theme
        
        return JsonResponse({'success': True, 'theme': theme})
    except:
        return JsonResponse({'success': False})
