from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column, HTML
import random
import string
from .models import UserProfile, Scenario, Requirement, Feedback, SRSDocument

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    # student_id = forms.CharField(max_length=20, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'username',
            'email',
            'password1',
            'password2',
            Submit('submit', 'Create Account', css_class='coursera-btn-primary w-full mt-4')
        )
        
        # Add Coursera-style classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'coursera-input'
            
        # Add placeholders
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Create a password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'
    
    def generate_student_id(self):
        """Generate a unique student ID starting with STU"""
        while True:
            # Generate random 6-digit number
            random_number = ''.join(random.choices(string.digits, k=6))
            student_id = f"STU{random_number}"
            
            # Check if this ID already exists
            if not UserProfile.objects.filter(student_id=student_id).exists():
                return student_id
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role='student',
                student_id=self.generate_student_id()
            )
        return user

class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = ['title', 'difficulty', 'introduction', 'aim', 'objectives', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'coursera-input'}),
            'difficulty': forms.Select(attrs={'class': 'coursera-input'}),
            'introduction': forms.Textarea(attrs={'rows': 4, 'class': 'coursera-input'}),
            'aim': forms.Textarea(attrs={'rows': 3, 'class': 'coursera-input'}),
            'objectives': forms.Textarea(attrs={'rows': 4, 'class': 'coursera-input'}),
            'description': forms.Textarea(attrs={'rows': 6, 'class': 'coursera-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-coursera-blue focus:ring-coursera-blue'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'introduction',
            'aim',
            'objectives',
            'description',
            'is_active',
            Submit('submit', 'Save Scenario', css_class='coursera-btn-primary')
        )
        
        # Add placeholders
        self.fields['title'].widget.attrs['placeholder'] = 'Enter scenario title'
        self.fields['introduction'].widget.attrs['placeholder'] = 'Provide an introduction to the scenario'
        self.fields['aim'].widget.attrs['placeholder'] = 'What is the main aim of this scenario?'
        self.fields['objectives'].widget.attrs['placeholder'] = 'List the learning objectives'
        self.fields['description'].widget.attrs['placeholder'] = 'Detailed description of the scenario'

class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ['requirement_type', 'title', 'description', 'priority']
        widgets = {
            'requirement_type': forms.Select(attrs={'class': 'coursera-input'}),
            'title': forms.TextInput(attrs={'class': 'coursera-input'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'coursera-input'}),
            'priority': forms.Select(attrs={'class': 'coursera-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'requirement_type',
            'title',
            'description',
            'priority',
            Submit('submit', 'Add Requirement', css_class='coursera-btn-primary')
        )
        
        # Add placeholders
        self.fields['title'].widget.attrs['placeholder'] = 'Enter requirement title'
        self.fields['description'].widget.attrs['placeholder'] = 'Describe the requirement in detail'

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_type', 'title', 'content']
        widgets = {
            'feedback_type': forms.Select(attrs={'class': 'coursera-input'}),
            'title': forms.TextInput(attrs={'class': 'coursera-input'}),
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'coursera-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'feedback_type',
            'title',
            'content',
            Submit('submit', 'Submit Feedback', css_class='coursera-btn-primary')
        )
        
        # Add placeholders
        self.fields['title'].widget.attrs['placeholder'] = 'Enter feedback title'
        self.fields['content'].widget.attrs['placeholder'] = 'Provide detailed feedback'

class SRSDocumentForm(forms.ModelForm):
    class Meta:
        model = SRSDocument
        fields = [
            'introduction', 'overall_description', 'system_features',
            'external_interface_requirements', 'non_functional_requirements',
            'other_requirements'
        ]
        widgets = {
            'introduction': forms.Textarea(attrs={'rows': 4, 'class': 'coursera-input'}),
            'overall_description': forms.Textarea(attrs={'rows': 4, 'class': 'coursera-input'}),
            'system_features': forms.Textarea(attrs={'rows': 4, 'class': 'coursera-input'}),
            'external_interface_requirements': forms.Textarea(attrs={'rows': 4, 'class': 'coursera-input'}),
            'non_functional_requirements': forms.Textarea(attrs={'rows': 4, 'class': 'coursera-input'}),
            'other_requirements': forms.Textarea(attrs={'rows': 4, 'class': 'coursera-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Software Requirements Specification</h3>'),
            'introduction',
            'overall_description',
            'system_features',
            'external_interface_requirements',
            'non_functional_requirements',
            'other_requirements',
            Submit('submit', 'Save SRS Document', css_class='coursera-btn-primary')
        )
