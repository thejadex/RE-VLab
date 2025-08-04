from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile, Scenario, ScenarioSubmission, Requirement

class RequirementsLabTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test users
        self.student_user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='testadmin',
            email='admin@test.com',
            password='testpass123'
        )
        
        # Create user profiles
        UserProfile.objects.create(
            user=self.student_user,
            role='student',
            student_id='TEST001'
        )
        UserProfile.objects.create(
            user=self.admin_user,
            role='admin'
        )
        
        # Create test scenario
        self.scenario = Scenario.objects.create(
            title='Test E-commerce Platform',
            introduction='Test introduction',
            aim='Test aim',
            objectives='Test objectives',
            description='Test description',
            created_by=self.admin_user
        )
    
    def test_home_page_loads(self):
        """Test that the home page loads correctly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Requirements Engineering Virtual Laboratory')
    
    def test_student_registration(self):
        """Test student registration process"""
        response = self.client.post(reverse('register'), {
            'username': 'newstudent',
            'first_name': 'New',
            'last_name': 'Student',
            'email': 'newstudent@test.com',
            'student_id': 'NEW001',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newstudent').exists())
    
    def test_student_dashboard_access(self):
        """Test student can access dashboard"""
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back')
    
    def test_admin_dashboard_access(self):
        """Test admin can access admin dashboard"""
        self.client.login(username='testadmin', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Dashboard')
    
    def test_scenario_list_access(self):
        """Test scenario list is accessible"""
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.get(reverse('scenario_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.scenario.title)
    
    def test_scenario_submission_creation(self):
        """Test that accessing a scenario creates a submission"""
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.get(reverse('scenario_detail', kwargs={'pk': self.scenario.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Check if submission was created
        submission = ScenarioSubmission.objects.get(
            scenario=self.scenario,
            student=self.student_user
        )
        self.assertEqual(submission.status, 'draft')
    
    def test_requirement_creation(self):
        """Test adding a requirement to a submission"""
        submission = ScenarioSubmission.objects.create(
            scenario=self.scenario,
            student=self.student_user
        )
        
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.post(reverse('add_requirement', kwargs={'submission_id': submission.pk}), {
            'requirement_type': 'functional',
            'title': 'User Login',
            'description': 'Users should be able to log in to the system',
            'priority': 'high'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Requirement.objects.filter(
            submission=submission,
            title='User Login'
        ).exists())
    
    def test_admin_can_create_scenario(self):
        """Test admin can create new scenarios"""
        self.client.login(username='testadmin', password='testpass123')
        response = self.client.post(reverse('create_scenario'), {
            'title': 'New Test Scenario',
            'introduction': 'New introduction',
            'aim': 'New aim',
            'objectives': 'New objectives',
            'description': 'New description',
            'is_active': True
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Scenario.objects.filter(title='New Test Scenario').exists())

    def test_unauthorized_access_denied(self):
        """Test that students cannot access admin functions"""
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.get(reverse('admin_scenarios'))
        self.assertEqual(response.status_code, 302)  # Redirect due to access denied
