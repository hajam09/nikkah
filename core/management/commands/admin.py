from decouple import config
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError


class Command(BaseCommand):
    help = '🌟 Creates a default superuser \'admin\' with a Profile. Ignores if already exists.'

    def handle(self, *args, **kwargs):
        self.stdout.write('🔹 Starting creation of admin user and profile...')

        try:
            user = User(
                username='admin',
                email=config('ADMIN_EMAIL', cast=str),
                first_name=config('ADMIN_FIRST_NAME', cast=str),
                last_name=config('ADMIN_LAST_NAME', cast=str),
                is_staff=True,
                is_active=True,
                is_superuser=True,
            )
            user.set_password('admin')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Superuser {user.username} created successfully.'))

        except IntegrityError:
            self.stdout.write(self.style.WARNING('⚠️ Admin user already exists. Skipping creation.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Unexpected error: {e}'))

        self.stdout.write(self.style.SUCCESS('🎉 Admin user setup complete.'))
