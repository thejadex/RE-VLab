from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Scenario, ScenarioSubmission, Requirement, Feedback, SRSDocument, Notification

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ScenarioSubmission)
class ScenarioSubmissionAdmin(admin.ModelAdmin):
    list_display = ['scenario', 'student', 'status', 'submitted_at', 'created_at']
    list_filter = ['status', 'submitted_at', 'created_at']
    search_fields = ['scenario__title', 'student__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ['title', 'requirement_type', 'priority', 'submission', 'created_at']
    list_filter = ['requirement_type', 'priority', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['title', 'feedback_type', 'submission', 'admin', 'is_read', 'created_at']
    list_filter = ['feedback_type', 'is_read', 'created_at']
    search_fields = ['title', 'content']

@admin.register(SRSDocument)
class SRSDocumentAdmin(admin.ModelAdmin):
    list_display = ['submission', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['title', 'message']
