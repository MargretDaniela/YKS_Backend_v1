
# from django.db import models
# from django.conf import settings


# class Course(models.Model):
#     title           = models.CharField(max_length=255)
#     description     = models.TextField()
#     trainer         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     category        = models.CharField(max_length=100)
#     price           = models.DecimalField(max_digits=10, decimal_places=2)
#     is_live         = models.BooleanField(default=True)
#     start_date      = models.DateField()
#     end_date        = models.DateField()
#     recording_url   = models.URLField(blank=True)
#     thumbnail       = models.ImageField(upload_to='course_thumbnails/', blank=True)

#     # ✅ New fields
#     learning_points = models.TextField(
#         blank=True,
#         help_text='Enter each point on a new line. Example:\nUnderstand leadership\nBuild confidence'
#     )
#     instructor_bio  = models.TextField(
#         blank=True,
#         help_text='Short bio shown on course detail page'
#     )

#     class Meta:
#         ordering = ['category', 'title']

#     def __str__(self):
#         return self.title

#     def get_learning_points(self):
#         return [p.strip() for p in self.learning_points.split('\n') if p.strip()]

#     def get_average_rating(self):
#         reviews = self.reviews.all()
#         if not reviews:
#             return 0.0
#         return round(sum(r.rating for r in reviews) / reviews.count(), 1)

#     def get_student_count(self):
#         return self.enrollment_set.filter(payment_status='paid').count()


# class Section(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
#     title  = models.CharField(max_length=255)
#     order  = models.PositiveIntegerField(default=0)

#     class Meta:
#         ordering = ['order']

#     def __str__(self):
#         return f"{self.course.title} — {self.title}"


# class Lesson(models.Model):
#     section   = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lessons')
#     title     = models.CharField(max_length=255)
#     duration  = models.CharField(max_length=20, default='00:00')
#     is_free   = models.BooleanField(default=False)
#     order     = models.PositiveIntegerField(default=0)
#     video_url = models.URLField(blank=True)

#     class Meta:
#         ordering = ['order']

#     def __str__(self):
#         return f"{self.section.title} — {self.title}"


# class Review(models.Model):
#     course     = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
#     user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     rating     = models.IntegerField(default=5)
#     comment    = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering      = ['-created_at']
#         unique_together = ['course', 'user']

#     def __str__(self):
#         return f"{self.user} → {self.course.title} ({self.rating}★)"


# class Enrollment(models.Model):
#     user                = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     course              = models.ForeignKey(Course, on_delete=models.CASCADE)
#     payment_status      = models.CharField(max_length=50)
#     progress_percentage = models.IntegerField(default=0)
#     completed_lessons   = models.IntegerField(default=0)   # ✅ track lessons done
#     completed           = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user} - {self.course}"

#     def can_review(self):
#         # ✅ Student can review after completing at least 2 lessons
#         return self.completed_lessons >= 2

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models import Avg
import os


# ======================================================================
#  FILE PATH HELPERS
# ======================================================================
def course_thumbnail_path(instance, filename):
    return f'courses/{instance.id}/thumbnail/{filename}'


def lesson_video_path(instance, filename):
    return f'courses/lessons/{instance.id}/video/{filename}'


# ======================================================================
#  CATEGORY
# ======================================================================
class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    icon = models.CharField(
        max_length=60,
        blank=True,
        help_text='Flutter icon name e.g. self_improvement'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


# ======================================================================
#  COURSE
# ======================================================================
class Course(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    category_text = models.CharField(
        max_length=100,
        blank=True,
        help_text='Legacy text category (if FK not set)'
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    instructor = models.CharField(max_length=150, blank=True)

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses_trained'
    )

    instructor_bio = models.TextField(blank=True)

    learning_points_text = models.TextField(blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='USD')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    is_live = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    recording_url = models.URLField(blank=True)

    thumbnail = models.ImageField(
        upload_to=course_thumbnail_path,
        null=True,
        blank=True
    )

    student_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    # ---------------- PROPERTIES ----------------
    @property
    def price_display(self):
        symbols = {'USD': 'US$', 'UGX': 'UGX ', 'KES': 'KES '}
        symbol = symbols.get(self.currency, f'{self.currency} ')
        return f'{symbol}{self.amount:,.2f}'

    @property
    def avg_rating(self):
        agg = self.reviews.aggregate(avg=Avg('rating'))
        return round(agg['avg'] or 0, 1)

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def thumbnail_url(self):
        return self.thumbnail.url if self.thumbnail else None

    def get_learning_points(self):
        return [
            p.strip()
            for p in self.learning_points_text.split('\n')
            if p.strip()
        ]

    def get_student_count(self):
        return self.enrollments.filter(payment_status='paid').count()


# ======================================================================
#  LEARNING POINT
# ======================================================================
class LearningPoint(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='learning_points'
    )
    point = models.CharField(max_length=300)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.course.title} — {self.point[:60]}'


# ======================================================================
#  MODULE
# ======================================================================
class Module(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.course.title} › {self.title}'


Section = Module


# ======================================================================
#  LESSON
# ======================================================================
class Lesson(models.Model):

    class VideoType(models.TextChoices):
        URL = 'url', 'External URL'
        UPLOAD = 'upload', 'Uploaded File'

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons',
        null=True,
        blank=True
    )

    title = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField(default=0)

    duration = models.CharField(max_length=20, default='00:00', blank=True)
    is_free = models.BooleanField(default=False)

    video_type = models.CharField(
        max_length=10,
        choices=VideoType.choices,
        default=VideoType.URL
    )

    video_url = models.URLField(blank=True, default='')

    video_file = models.FileField(
        upload_to=lesson_video_path,
        null=True,
        blank=True
    )

    allow_download = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.module} › {self.title}'

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def video_source(self):
        if self.video_type == self.VideoType.UPLOAD and self.video_file:
            return self.video_file.url
        return self.video_url


# ======================================================================
#  ENROLLMENT
# ======================================================================
class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        null=True,
        blank=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    enrolled_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    payment_status = models.CharField(max_length=50, blank=True)
    progress_percentage = models.IntegerField(default=0)
    completed_lessons = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student} → {self.course.title}'

    @property
    def user(self):
        return self.student


# ======================================================================
#  LESSON PROGRESS
# ======================================================================
class LessonProgress(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='lesson_progress'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress_records'
    )

    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_position = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('enrollment', 'lesson')


# ======================================================================
# ======================================================================
#  REVIEW
# ======================================================================
class Review(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_reviews',
        null=True,
        blank=True
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    comment    = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('course', 'student')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student} → {self.course.title} ({self.rating}★)'

    # ❌ DELETE the @property user — this was causing the error
    # Django saw 'user' as a field reference in old migrations