# # Create your models here.
# from django.db import models
# from django.conf import settings


# class MentorshipSession(models.Model):
#     class SessionType(models.TextChoices):
#         ONE_ON_ONE = "ONE_ON_ONE", "One-on-one"
#         GROUP = "GROUP", "Group"

#     class Status(models.TextChoices):
#         PENDING = "PENDING", "Pending"
#         APPROVED = "APPROVED", "Approved"
#         COMPLETED = "COMPLETED", "Completed"
#         CANCELLED = "CANCELLED", "Cancelled"

#     mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentor_sessions')
#     student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_sessions')
#     session_type = models.CharField(max_length=20, choices=SessionType.choices)
#     date = models.DateField()
#     time = models.TimeField()
#     status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
#     meeting_link = models.URLField(blank=True)
#     notes = models.TextField(blank=True)

#     def __str__(self):
#         return f"{self.mentor} with {self.student}"


# class Booking(models.Model):
#     session = models.ForeignKey(MentorshipSession, on_delete=models.CASCADE)
#     payment_status = models.CharField(max_length=50)
#     access_code = models.CharField(max_length=50)

#     def __str__(self):
#         return f"Booking for {self.session}"

# C:\Users\Admin\Desktop\TheYKSApp\mentorship\models.py
from django.db import models
from django.conf import settings

class MentorshipSession(models.Model):
    class SessionType(models.TextChoices):
        ONE_ON_ONE = "ONE_ON_ONE", "One-on-one"
        GROUP = "GROUP", "Group"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mentor_sessions'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='student_sessions'
    )
    session_type = models.CharField(max_length=20, choices=SessionType.choices)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.mentor} with {self.student}"


class Booking(models.Model):
    session = models.ForeignKey(MentorshipSession, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=50, default="UNPAID")
    access_code = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Booking for {self.session}"


# ✅ NEW: Mentorship Video/Resource Model
class MentorshipVideo(models.Model):
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mentor_videos'
    )
    title = models.CharField(max_length=255)
    video_url = models.URLField(help_text="YouTube, Vimeo, or direct video link")
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Mentorship Video"
        verbose_name_plural = "Mentorship Videos"

    def __str__(self):
        return f"{self.title} by {self.mentor}"