from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lab.models import UserProfile, Scenario, ScenarioSubmission, Requirement, Feedback

class Command(BaseCommand):
    help = 'Create sample data for the Requirements Lab'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@requirementslab.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            UserProfile.objects.create(user=admin_user, role='admin')
            self.stdout.write(f'Created admin user: admin/admin123')
        
        # Create sample student
        student_user, created = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student1@example.com',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        if created:
            student_user.set_password('student123')
            student_user.save()
            UserProfile.objects.create(user=student_user, role='student', student_id='STU001')
            self.stdout.write(f'Created student user: student1/student123')
        
        # Create sample scenarios
        scenarios_data = [
            {
                'title': 'E-commerce Platform Development',
                'introduction': 'You are tasked with developing a comprehensive e-commerce platform for a growing retail business.',
                'aim': 'To create a user-friendly online shopping platform that supports product browsing, purchasing, and order management.',
                'objectives': 'Enable customer registration and authentication, implement product catalog with search functionality, develop shopping cart and checkout process, create order tracking system.',
                'description': '''
The client is a mid-sized retail company that wants to expand their business online. They currently have a physical store but no online presence. The platform should support:

- Customer account management
- Product catalog with categories and search
- Shopping cart functionality
- Secure payment processing
- Order management and tracking
- Admin panel for inventory management
- Mobile-responsive design
- Integration with existing inventory system

The target audience includes tech-savvy millennials and Gen-X customers who prefer online shopping. The platform should be intuitive, fast, and secure.
                '''
            },
            {
                'title': 'University Course Management System',
                'introduction': 'Design a comprehensive course management system for a university to handle student enrollment, course scheduling, and academic records.',
                'aim': 'To streamline university operations by providing an integrated system for course management, student enrollment, and academic tracking.',
                'objectives': 'Implement student and faculty registration, create course scheduling system, develop grade management functionality, enable transcript generation.',
                'description': '''
The university currently uses multiple disconnected systems for different academic functions. They need a unified platform that can:

- Manage student and faculty profiles
- Handle course creation and scheduling
- Process student enrollment and waitlists
- Track attendance and grades
- Generate transcripts and reports
- Manage academic calendar and events
- Support different user roles (students, faculty, admin)
- Integrate with existing student information systems

The system should be scalable to handle 10,000+ students and support both on-campus and online courses.
                '''
            },
            {
                'title': 'Healthcare Appointment Booking System',
                'introduction': 'Develop a digital appointment booking system for a multi-specialty healthcare clinic.',
                'aim': 'To improve patient experience and clinic efficiency through automated appointment scheduling and management.',
                'objectives': 'Create patient registration system, implement doctor availability management, develop appointment booking interface, enable automated reminders.',
                'description': '''
A healthcare clinic with multiple specialties wants to modernize their appointment booking process. Currently, all appointments are scheduled via phone calls, leading to inefficiencies and patient dissatisfaction.

The system requirements include:

- Patient registration and profile management
- Doctor and staff scheduling
- Appointment booking with specialty selection
- Automated email/SMS reminders
- Appointment rescheduling and cancellation
- Waitlist management
- Integration with electronic health records
- HIPAA compliance and data security
- Mobile app for patients
- Reporting and analytics for clinic management

The clinic serves 500+ patients daily across 15 different specialties.
                '''
            }
        ]
        
        for scenario_data in scenarios_data:
            scenario, created = Scenario.objects.get_or_create(
                title=scenario_data['title'],
                defaults={
                    'introduction': scenario_data['introduction'],
                    'aim': scenario_data['aim'],
                    'objectives': scenario_data['objectives'],
                    'description': scenario_data['description'],
                    'created_by': admin_user
                }
            )
            if created:
                self.stdout.write(f'Created scenario: {scenario.title}')
        
        # Create sample submission with requirements
        if Scenario.objects.exists():
            scenario = Scenario.objects.first()
            submission, created = ScenarioSubmission.objects.get_or_create(
                scenario=scenario,
                student=student_user
            )
            
            if created:
                # Add sample requirements
                sample_requirements = [
                    {
                        'requirement_type': 'functional',
                        'title': 'User Registration',
                        'description': 'The system shall allow new users to create accounts with email verification.',
                        'priority': 'high'
                    },
                    {
                        'requirement_type': 'functional',
                        'title': 'Product Search',
                        'description': 'Users shall be able to search for products using keywords, categories, and filters.',
                        'priority': 'high'
                    },
                    {
                        'requirement_type': 'non_functional',
                        'title': 'Response Time',
                        'description': 'The system shall respond to user requests within 2 seconds under normal load.',
                        'priority': 'medium'
                    },
                    {
                        'requirement_type': 'business',
                        'title': 'Payment Processing',
                        'description': 'The system shall support multiple payment methods including credit cards and PayPal.',
                        'priority': 'high'
                    }
                ]
                
                for req_data in sample_requirements:
                    Requirement.objects.create(
                        submission=submission,
                        **req_data
                    )
                
                self.stdout.write(f'Created sample submission with requirements')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('You can now login with:')
        self.stdout.write('Admin: admin/admin123')
        self.stdout.write('Student: student1/student123')
