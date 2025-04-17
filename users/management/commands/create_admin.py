from django.core.management.base import BaseCommand
from users.models import User
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates an admin user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin@admin.com').exists():
            User.objects.create_superuser(
                username='admin@admin.com',
                email='admin@admin.com',
                password='admin123',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))