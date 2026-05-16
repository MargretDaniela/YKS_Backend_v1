# import random
# from django.core.mail import send_mail
# from django.utils import timezone
# from datetime import timedelta
# from .models import OTPCode


# def generate_otp():
#     return str(random.randint(100000, 999999))


# def send_otp_email(user):
#     from .models import OTPCode
#     # Delete any existing OTP for this user
#     OTPCode.objects.filter(user=user).delete()

#     code = generate_otp()
#     expires_at = timezone.now() + timedelta(minutes=10)

#     # Use bulk_create to avoid triggering User.save()
#     OTPCode.objects.create(user=user, code=code, expires_at=expires_at)

#     send_mail(
#         subject='Your Youth K.E.Y Series Verification Code',
#         message=f'''Hello {user.full_name},

# Your verification code is:

# {code}

# This code expires in 10 minutes.

# If you did not create an account, please ignore this email.

# — Youth K.E.Y Series Team''',
#         from_email='Youth KEY Series <danielamargret6@gmail.com>',        recipient_list=[user.email],
#         fail_silently=False,
#     )
#     return code

import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import OTPCode


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(user):
    from .models import OTPCode
    OTPCode.objects.filter(user=user).delete()

    code       = generate_otp()
    expires_at = timezone.now() + timedelta(minutes=10)
    OTPCode.objects.create(user=user, code=code, expires_at=expires_at)

    send_mail(
        subject='Your Youth K.E.Y Series Verification Code',
        message=f'''Hello {user.full_name},

Your verification code is:

{code}

This code expires in 10 minutes.

If you did not create an account, please ignore this email.

— Youth K.E.Y Series Team''',
        from_email='Youth KEY Series <danielamargret6@gmail.com>',
        recipient_list=[user.email],
        fail_silently=False,
    )
    return code


def send_password_reset_email(user, code):
    send_mail(
        subject='Reset Your Youth K.E.Y Series Password',
        message=f'''Hello {user.full_name},

You requested to reset your password. Use the code below:

{code}

This code expires in 10 minutes.

If you did not request a password reset, please ignore this email.

— Youth K.E.Y Series Team''',
        from_email='Youth KEY Series <danielamargret6@gmail.com>',
        recipient_list=[user.email],
        fail_silently=False,
    )