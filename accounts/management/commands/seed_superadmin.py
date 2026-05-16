from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the Super Admin user"

    def handle(self, *args, **kwargs):
        email = "superadmin@youthkey.com"
        password = "YouthKey@2026"
        full_name = "Youth Key Super Admin"

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(
                f"Super Admin already exists: {email}"
            ))
            return

        user = User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            role="SUPER_ADMIN",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Super Admin created successfully!\n"
            f"📧 Email:    {email}\n"
            f"🔑 Password: {password}\n"
            f"👤 Name:     {full_name}\n"
            f"🛡️  Role:     SUPER_ADMIN\n"
        ))