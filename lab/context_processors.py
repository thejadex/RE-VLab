from .models import ScenarioSubmission

def sidebar_progress(request):
    if not request.user.is_authenticated:
        return {}
    draft_submissions = ScenarioSubmission.objects.filter(student=request.user, status='draft').count()
    completed_submissions = ScenarioSubmission.objects.filter(student=request.user, status='submitted').count()
    feedback_received = ScenarioSubmission.objects.filter(student=request.user, status='feedback_received').count()
    return {
        'draft_submissions': draft_submissions,
        'completed_submissions': completed_submissions,
        'feedback_received': feedback_received,
    }

def notifications_processor(request):
    """Context processor to add unread notifications count to all templates"""
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
    else:
        unread_count = 0
    
    return {
        'unread_notifications_count': unread_count,
        'has_unread_notifications': unread_count > 0
    }