from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.role})"
    

@receiver(post_save, sender=User)
def create_user_profile_signal(sender, instance, created, **kwargs):
    if created:
        # Create profile for new users
        role = 'admin' if instance.is_superuser else 'student'
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={'role': role}
        )


class Scenario(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    introduction = models.TextField()
    aim = models.TextField()
    objectives = models.TextField()
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.created_by.username}"
    
    def get_absolute_url(self):
        return reverse('scenario_detail', kwargs={'pk': self.pk})

class ScenarioSubmission(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('feedback_received', 'Feedback Received'),
    ]
    
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['scenario', 'student']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.scenario.title}"
    
    def submit(self):
        self.status = 'submitted'
        self.submitted_at = timezone.now()
        self.save()
    
    def get_absolute_url(self):
        return reverse('submission_detail', kwargs={'pk': self.pk})

class Requirement(models.Model):
    REQUIREMENT_TYPES = [
        ('functional', 'Functional Requirement'),
        ('non_functional', 'Non-Functional Requirement'),
        ('business', 'Business Requirement'),
    ]
    
    submission = models.ForeignKey(ScenarioSubmission, on_delete=models.CASCADE, related_name='requirements')
    requirement_type = models.CharField(max_length=20, choices=REQUIREMENT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=[
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['requirement_type', '-created_at']
    
    def __str__(self):
        return f"{self.get_requirement_type_display()}: {self.title}"

class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('general', 'General Comments'),
        ('clarification', 'Request for Clarification'),
        ('improvement', 'Suggestion for Improvement'),
    ]
    
    submission = models.ForeignKey(ScenarioSubmission, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback for {self.submission.student.username} - {self.title}"

class SRSDocument(models.Model):
    submission = models.OneToOneField(ScenarioSubmission, on_delete=models.CASCADE, related_name='srs_document')
    introduction = models.TextField(blank=True)
    overall_description = models.TextField(blank=True)
    system_features = models.TextField(blank=True)
    external_interface_requirements = models.TextField(blank=True)
    non_functional_requirements = models.TextField(blank=True)
    other_requirements = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"SRS - {self.submission.scenario.title}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"

# Signal to create notifications for new scenarios
@receiver(post_save, sender=Scenario)
def create_scenario_notification(sender, instance, created, **kwargs):
    if created and instance.is_active:
        # Get all students
        student_profiles = UserProfile.objects.filter(role='student')
        for profile in student_profiles:
            Notification.objects.create(
                user=profile.user,
                title='New Scenario Available',
                message=f'A new scenario "{instance.title}" has been added and is ready for you to work on.',
                link=f'/scenarios/{instance.pk}/'
            )
