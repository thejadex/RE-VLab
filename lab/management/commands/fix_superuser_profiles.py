from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lab.models import UserProfile


class Command(BaseCommand):
    help = 'Fix superuser profiles to ensure they have admin role'

    def handle(self, *args, **options):
        # Get all superusers
        superusers = User.objects.filter(is_superuser=True)
        
        if not superusers.exists():
            self.stdout.write(
                self.style.WARNING('No superusers found in the system.')
            )
            return
        
        fixed_count = 0
        created_count = 0
        
        for superuser in superusers:
            profile, created = UserProfile.objects.get_or_create(
                user=superuser,
                defaults={'role': 'admin'}
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created admin profile for superuser: {superuser.username}'
                    )
                )
            elif profile.role != 'admin':
                profile.role = 'admin'
                profile.save()
                fixed_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated profile for superuser: {superuser.username} to admin role'
                    )
                )
            else:
                self.stdout.write(
                    f'Superuser {superuser.username} already has admin profile'
                )
        
        if fixed_count > 0 or created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Summary: Created {created_count} profiles, Fixed {fixed_count} profiles'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('All superuser profiles are correctly configured!')
            )