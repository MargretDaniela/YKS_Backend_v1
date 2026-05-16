# test_email.py - Run with: python manage.py shell < test_email.py
from django.core.mail import send_mail
from django.conf import settings

print(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
print(f"📧 From: {settings.DEFAULT_FROM_EMAIL}")

try:
    send_mail(
        subject='🧪 TEST EMAIL - TheYKSApp',
        message='If you see this, Django email is working!\n\nBackend: ' + settings.EMAIL_BACKEND,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['danielamargret6@gmail.com'],
        fail_silently=False,
    )
    print("✅ send_mail() succeeded - check your terminal/console for output!")
except Exception as e:
    print(f"❌ send_mail() failed: {type(e).__name__}: {e}")