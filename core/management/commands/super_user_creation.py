from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        CustomUser = get_user_model()
        
        if not CustomUser.objects.filter(username=os.environ['DJANGO_SUPERUSER_USERNAME']).exists():
            CustomUser.objects.create_superuser(
                username=os.environ['DJANGO_SUPERUSER_USERNAME'],
                email=os.environ['DJANGO_SUPERUSER_EMAIL'],
                password=os.environ['DJANGO_SUPERUSER_PASSWORD']
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
