from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# =====================
# USER MANAGER
# =====================
class UserManager(BaseUserManager):
    def _assign_permissions(self):
    # Guard: only run for User model, not related models
      if not hasattr(self, 'role'):
        return
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff",     True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role",         "SUPER_ADMIN")
        return self.create_user(email, password, **extra_fields)


# =====================
# USER MODEL
# =====================
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("SUPER_ADMIN", "Super Admin"),
        ("ADMIN",       "Admin"),
        ("MENTOR",      "Mentor"),
        ("STUDENT",     "Student"),
    ]

    email       = models.EmailField(unique=True)
    full_name   = models.CharField(max_length=150)
    role        = models.CharField(max_length=20, choices=ROLE_CHOICES, default="STUDENT")
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["full_name"]
    objects = UserManager()

    def __str__(self):
        return f"{self.full_name} ({self.role})"

    def save(self, *args, **kwargs):
        if self.role == "SUPER_ADMIN":
            self.is_staff     = True
            self.is_superuser = True
        elif self.role in ["ADMIN", "MENTOR"]:
            self.is_staff     = True
            self.is_superuser = False
        else:
            self.is_staff     = False
            self.is_superuser = False
        super().save(*args, **kwargs)
        self._assign_permissions()

    def _assign_permissions(self):
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        self.user_permissions.clear()

        if self.role == "SUPER_ADMIN":
            return

        if self.role == "ADMIN":
            allowed = [
                ("accounts",      "user",              ["view", "add", "change", "delete"]),
                ("courses",       "course",            ["view", "add", "change", "delete"]),
                ("courses",       "enrollment",        ["view", "add", "change"]),
                ("mentorship",    "mentorshipsession", ["view", "add", "change", "delete"]),
                ("mentorship",    "booking",           ["view", "change"]),
                ("payments",      "payment",           ["view", "change"]),
                ("attendance",    "attendance",        ["view"]),
                ("notifications", "notification",      ["view", "add", "change"]),
            ]
            self._set_permissions(allowed)

        elif self.role == "MENTOR":
            allowed = [
                ("courses",    "course",            ["view", "add", "change"]),
                ("mentorship", "mentorshipsession", ["view", "add", "change"]),
                ("mentorship", "booking",           ["view", "change"]),
                ("attendance", "attendance",        ["view", "add", "change"]),
                ("accounts",   "user",              ["view", "change"]),
            ]
            self._set_permissions(allowed)

    def _set_permissions(self, allowed):
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        for app_label, model_name, actions in allowed:
            try:
                ct = ContentType.objects.get(app_label=app_label, model=model_name)
                for action in actions:
                    try:
                        perm = Permission.objects.get(
                            content_type=ct,
                            codename=f"{action}_{model_name}"
                        )
                        self.user_permissions.add(perm)
                    except Permission.DoesNotExist:
                        pass
            except ContentType.DoesNotExist:
                pass


# =====================
# OTP CODE MODEL
# =====================
class OTPCode(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_codes')
    code       = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used    = models.BooleanField(default=False)

    def is_valid(self):
        from django.utils import timezone
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.user.email} — {self.code}"