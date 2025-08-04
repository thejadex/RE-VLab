from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.contrib.auth.models import User
from lab.models import UserProfile, Scenario

class Command(BaseCommand):
    help = 'Check and fix database setup for Requirements Lab'

    def handle(self, *args, **options):
        self.stdout.write('Checking Requirements Lab setup...')
        
        # Check if tables exist
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = [
                'lab_userprofile',
                'lab_scenario', 
                'lab_scenariosubmission',
                'lab_requirement',
                'lab_feedback',
                'lab_srsdocument',
                'lab_notification'
            ]
            
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                self.stdout.write(self.style.WARNING(f'Missing tables: {missing_tables}'))
                self.stdout.write('Running migrations...')
                
                # Create and apply migrations
                call_command('makemigrations', 'lab')
                call_command('migrate')
                
                self.stdout.write(self.style.SUCCESS('✓ Migrations applied'))
            else:
                self.stdout.write(self.style.SUCCESS('✓ All tables exist'))
        
        # Check if sample data exists
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Creating sample data...')
            call_command('setup_lab')
        else:
            self.stdout.write(self.style.SUCCESS('✓ Sample data already exists'))
        
        self.stdout.write(self.style.SUCCESS('Setup check complete!'))
