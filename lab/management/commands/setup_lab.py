from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lab.models import UserProfile, Scenario, ScenarioSubmission, Requirement, Feedback

class Command(BaseCommand):
    help = 'Set up the Requirements Lab with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up Requirements Lab...')
        
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
            self.stdout.write(f'✓ Created admin user: admin/admin123')
        
        # Create sample student
        student_user, created = User.objects.get_or_create(
            username='student',
            defaults={
                'email': 'student@example.com',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        if created:
            student_user.set_password('student123')
            student_user.save()
            UserProfile.objects.create(user=student_user, role='student', student_id='STU001')
            self.stdout.write(f'✓ Created student user: student/student123')
        
        # Create sample scenario
        scenario, created = Scenario.objects.get_or_create(
            title='E-commerce Platform Development',
            defaults={
                'introduction': 'You are tasked with developing a comprehensive e-commerce platform for a growing retail business.',
                'aim': 'To create a user-friendly online shopping platform that supports product browsing, purchasing, and order management.',
                'objectives': 'Enable customer registration and authentication, implement product catalog with search functionality, develop shopping cart and checkout process, create order tracking system.',
                'description': '''The client is a mid-sized retail company that wants to expand their business online. They currently have a physical store but no online presence. The platform should support:

- Customer account management
- Product catalog with categories and search
- Shopping cart functionality
- Secure payment processing
- Order management and tracking
- Admin panel for inventory management
- Mobile-responsive design
- Integration with existing inventory system

The target audience includes tech-savvy millennials and Gen-X customers who prefer online shopping. The platform should be intuitive, fast, and secure.''',
                'created_by': admin_user
            }
        )
        if created:
            self.stdout.write(f'✓ Created scenario: {scenario.title}')
        
        self.stdout.write(self.style.SUCCESS('✓ Setup complete!'))
        self.stdout.write('You can now login with:')
        self.stdout.write('  Admin: admin/admin123')
        self.stdout.write('  Student: student/student123')
