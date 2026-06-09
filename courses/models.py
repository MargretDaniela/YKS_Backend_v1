
# from django.db import models
# from django.conf import settings
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.utils import timezone
# from django.db.models import Avg
# import os


# # ======================================================================
# #  FILE PATH HELPERS
# # ======================================================================
# def course_thumbnail_path(instance, filename):
#     return f'courses/{instance.id}/thumbnail/{filename}'


# def lesson_video_path(instance, filename):
#     return f'courses/lessons/{instance.id}/video/{filename}'


# # ======================================================================
# #  CATEGORY
# # ======================================================================
# class Category(models.Model):
#     name = models.CharField(max_length=120, unique=True)
#     icon = models.CharField(
#         max_length=60,
#         blank=True,
#         help_text='Flutter icon name e.g. self_improvement'
#     )
#     created_at = models.DateTimeField(default=timezone.now)

#     class Meta:
#         verbose_name_plural = 'Categories'
#         ordering = ['name']

#     def __str__(self):
#         return self.name


# # ======================================================================
# #  COURSE
# # ======================================================================
# class Course(models.Model):
#     category = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE,
#         related_name='courses'
#     )
#     category_text = models.CharField(
#         max_length=100,
#         blank=True,
#         help_text='Legacy text category (if FK not set)'
#     )

#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     instructor = models.CharField(max_length=150, blank=True)

#     trainer = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='courses_trained'
#     )

#     instructor_bio = models.TextField(blank=True)

#     learning_points_text = models.TextField(blank=True)

#     amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     currency = models.CharField(max_length=10, default='USD')
#     price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

#     start_date = models.DateField(null=True, blank=True)
#     end_date = models.DateField(null=True, blank=True)

#     is_live = models.BooleanField(default=False)
#     is_published = models.BooleanField(default=False)
#     recording_url = models.URLField(blank=True)

#     thumbnail = models.ImageField(
#         upload_to=course_thumbnail_path,
#         null=True,
#         blank=True
#     )

#     student_count = models.PositiveIntegerField(default=0)

#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return self.title

#     def save(self, *args, **kwargs):
#         self.updated_at = timezone.now()
#         super().save(*args, **kwargs)

#     # ---------------- PROPERTIES ----------------
#     @property
#     def price_display(self):
#         symbols = {'USD': 'US$', 'UGX': 'UGX ', 'KES': 'KES '}
#         symbol = symbols.get(self.currency, f'{self.currency} ')
#         return f'{symbol}{self.amount:,.2f}'

#     @property
#     def avg_rating(self):
#         agg = self.reviews.aggregate(avg=Avg('rating'))
#         return round(agg['avg'] or 0, 1)

#     @property
#     def review_count(self):
#         return self.reviews.count()

#     @property
#     def thumbnail_url(self):
#         return self.thumbnail.url if self.thumbnail else None

#     def get_learning_points(self):
#         return [
#             p.strip()
#             for p in self.learning_points_text.split('\n')
#             if p.strip()
#         ]

#     def get_student_count(self):
#         return self.enrollments.filter(payment_status='paid').count()


# # ======================================================================
# #  LEARNING POINT
# # ======================================================================
# class LearningPoint(models.Model):
#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         related_name='learning_points'
#     )
#     point = models.CharField(max_length=300)
#     order = models.PositiveSmallIntegerField(default=0)

#     class Meta:
#         ordering = ['order']

#     def __str__(self):
#         return f'{self.course.title} — {self.point[:60]}'


# # ======================================================================
# #  MODULE
# # ======================================================================
# class Module(models.Model):
#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         related_name='modules'
#     )
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     order = models.PositiveSmallIntegerField(default=0)
#     created_at = models.DateTimeField(default=timezone.now)

#     class Meta:
#         ordering = ['order']

#     def __str__(self):
#         return f'{self.course.title} › {self.title}'


# Section = Module


# # ======================================================================
# #  LESSON
# # ======================================================================
# class Lesson(models.Model):

#     class VideoType(models.TextChoices):
#         URL = 'url', 'External URL'
#         UPLOAD = 'upload', 'Uploaded File'

#     module = models.ForeignKey(
#         Module,
#         on_delete=models.CASCADE,
#         related_name='lessons',
#         null=True,
#         blank=True
#     )

#     title = models.CharField(max_length=255)
#     order = models.PositiveSmallIntegerField(default=0)

#     duration = models.CharField(max_length=20, default='00:00', blank=True)
#     is_free = models.BooleanField(default=False)

#     video_type = models.CharField(
#         max_length=10,
#         choices=VideoType.choices,
#         default=VideoType.URL
#     )

#     video_url = models.URLField(blank=True, default='')

#     video_file = models.FileField(
#         upload_to=lesson_video_path,
#         null=True,
#         blank=True
#     )

#     allow_download = models.BooleanField(default=False)

#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['order']

#     def __str__(self):
#         return f'{self.module} › {self.title}'

#     def save(self, *args, **kwargs):
#         self.updated_at = timezone.now()
#         super().save(*args, **kwargs)

#     @property
#     def video_source(self):
#         if self.video_type == self.VideoType.UPLOAD and self.video_file:
#             return self.video_file.url
#         return self.video_url


# # ======================================================================
# #  ENROLLMENT
# # ======================================================================
# class Enrollment(models.Model):
#     student = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='enrollments',
#         null=True,
#         blank=True
#     )
#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         related_name='enrollments'
#     )

#     enrolled_at = models.DateTimeField(default=timezone.now)
#     is_active = models.BooleanField(default=True)

#     payment_status = models.CharField(max_length=50, blank=True)
#     progress_percentage = models.IntegerField(default=0)
#     completed_lessons = models.IntegerField(default=0)
#     completed = models.BooleanField(default=False)

#     class Meta:
#         unique_together = ('student', 'course')

#     def __str__(self):
#         return f'{self.student} → {self.course.title}'

#     @property
#     def user(self):
#         return self.student


# # ======================================================================
# #  LESSON PROGRESS
# # ======================================================================
# class LessonProgress(models.Model):
#     enrollment = models.ForeignKey(
#         Enrollment,
#         on_delete=models.CASCADE,
#         related_name='lesson_progress'
#     )
#     lesson = models.ForeignKey(
#         Lesson,
#         on_delete=models.CASCADE,
#         related_name='progress_records'
#     )

#     is_completed = models.BooleanField(default=False)
#     completed_at = models.DateTimeField(null=True, blank=True)
#     last_position = models.PositiveIntegerField(default=0)

#     class Meta:
#         unique_together = ('enrollment', 'lesson')


# # ======================================================================
# # ======================================================================
# #  REVIEW
# # ======================================================================
# class Review(models.Model):
#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         related_name='reviews'
#     )
#     student = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='course_reviews',
#         null=True,
#         blank=True
#     )
#     rating = models.PositiveSmallIntegerField(
#         validators=[MinValueValidator(1), MaxValueValidator(5)],
#         default=5
#     )
#     comment    = models.TextField(blank=True, default='')
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(default=timezone.now)

#     class Meta:
#         unique_together = ('course', 'student')
#         ordering = ['-created_at']

#     def __str__(self):
#         return f'{self.student} → {self.course.title} ({self.rating}★)'

#     # ❌ DELETE the @property user — this was causing the error
#     # Django saw 'user' as a field reference in old migrations

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
    ext = os.path.splitext(filename)[1]
    return f'courses/{instance.pk}/thumbnail/thumb{ext}'


def module_video_path(instance, filename):
    """Uploaded video for a Module — stored under courses/modules/{id}/"""
    ext = os.path.splitext(filename)[1]
    return f'courses/modules/{instance.pk}/video/video{ext}'


def lesson_video_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f'courses/lessons/{instance.pk}/video/video{ext}'


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

    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    instructor  = models.CharField(max_length=150, blank=True)

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses_trained'
    )

    instructor_bio        = models.TextField(blank=True)
    learning_points_text  = models.TextField(
        blank=True,
        help_text='One learning point per line'
    )

    amount   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='USD')
    price    = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    start_date = models.DateField(null=True, blank=True)
    end_date   = models.DateField(null=True, blank=True)

    is_live      = models.BooleanField(default=False)
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

    # ── Computed helpers ─────────────────────────────────────────────
    @property
    def price_display(self):
        symbols = {'USD': 'US$', 'UGX': 'UGX ', 'KES': 'KES '}
        symbol  = symbols.get(self.currency, f'{self.currency} ')
        return f'{symbol}{self.amount:,.2f}'

    @property
    def avg_rating(self):
        agg = self.reviews.aggregate(avg=Avg('rating'))
        return round(agg['avg'] or 0, 1)

    def get_average_rating(self):
        return self.avg_rating

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def thumbnail_url(self):
        return self.thumbnail.url if self.thumbnail else None

    def get_learning_points(self):
        return [p.strip() for p in self.learning_points_text.split('\n') if p.strip()]

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
#
#  Each module can optionally carry:
#    • video_file   — a video uploaded directly from the admin dashboard
#    • video_url    — an external video link (YouTube embed, Vimeo, CDN…)
#    • resource_link — any free-form URL the instructor wants students to
#                      visit (YouTube, TikTok, a PDF, a website — anything)
#
#  video_file takes priority when both are set (video_source property).
#  resource_link is completely optional and independent.
# ======================================================================
class Module(models.Model):

    class VideoType(models.TextChoices):
        URL    = 'url',    'External URL'
        UPLOAD = 'upload', 'Uploaded File'
        NONE   = 'none',   'No Video'

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules'
    )
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order       = models.PositiveSmallIntegerField(default=0)
    created_at  = models.DateTimeField(default=timezone.now)

    # ── Video (uploaded file OR external URL) ────────────────────────
    video_type = models.CharField(
        max_length=10,
        choices=VideoType.choices,
        default=VideoType.NONE,
        help_text='Choose "Uploaded File" to upload a video from your device, '
                  'or "External URL" to paste a link.'
    )
    video_file = models.FileField(
        upload_to=module_video_path,
        null=True,
        blank=True,
        help_text='Upload a video file (MP4, WebM, MOV …). '
                  'Leave blank if using an external URL.'
    )
    video_url = models.URLField(
        blank=True,
        default='',
        help_text='Paste a YouTube embed, Vimeo, or any direct video URL. '
                  'Used only when Video Type is "External URL".'
    )

    # ── Resource link (optional — any URL) ───────────────────────────
    resource_link = models.URLField(
        blank=True,
        default='',
        help_text='Optional. Any URL you want students to visit — '
                  'YouTube, TikTok, a PDF, a website, anything.'
    )
    resource_link_label = models.CharField(
        max_length=120,
        blank=True,
        default='',
        help_text='Button label shown to students, e.g. "Watch on YouTube" '
                  'or "Download worksheet". Defaults to the URL if left blank.'
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.course.title} › Module {self.order}: {self.title}'

    # ── Helpers ───────────────────────────────────────────────────────
    @property
    def video_source(self):
        """Return the playable video URL regardless of type."""
        if self.video_type == self.VideoType.UPLOAD and self.video_file:
            return self.video_file.url
        if self.video_type == self.VideoType.URL and self.video_url:
            return self.video_url
        return ''

    def get_video_url(self, request=None):
        """Absolute URL for API responses."""
        src = self.video_source
        if src and request and src.startswith('/'):
            return request.build_absolute_uri(src)
        return src

    @property
    def has_video(self):
        return bool(self.video_source)

    @property
    def has_resource_link(self):
        return bool(self.resource_link)

    @property
    def effective_resource_label(self):
        return self.resource_link_label.strip() or self.resource_link


# Alias kept for backward-compat
Section = Module


# ======================================================================
#  LESSON
# ======================================================================
class Lesson(models.Model):

    class VideoType(models.TextChoices):
        URL    = 'url',    'External URL'
        UPLOAD = 'upload', 'Uploaded File'

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons',
        null=True,
        blank=True
    )

    title    = models.CharField(max_length=255)
    order    = models.PositiveSmallIntegerField(default=0)
    duration = models.CharField(max_length=20, default='00:00', blank=True)
    is_free  = models.BooleanField(default=False)

    video_type = models.CharField(
        max_length=10,
        choices=VideoType.choices,
        default=VideoType.URL
    )
    video_url  = models.URLField(blank=True, default='')
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
        return f'{self.module} › Lesson {self.order}: {self.title}'

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def video_source(self):
        if self.video_type == self.VideoType.UPLOAD and self.video_file:
            return self.video_file.url
        return self.video_url

    def get_video_url(self, request=None):
        src = self.video_source
        if src and request and src.startswith('/'):
            return request.build_absolute_uri(src)
        return src or ''


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

    enrolled_at         = models.DateTimeField(default=timezone.now)
    is_active           = models.BooleanField(default=True)
    payment_status      = models.CharField(max_length=50, blank=True)
    progress_percentage = models.IntegerField(default=0)
    completed_lessons   = models.IntegerField(default=0)
    completed           = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student} → {self.course.title}'

    @property
    def user(self):
        return self.student

    def can_review(self):
        return self.completed_lessons >= 2


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

    is_completed  = models.BooleanField(default=False)
    completed_at  = models.DateTimeField(null=True, blank=True)
    last_position = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('enrollment', 'lesson')


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
        ordering        = ['-created_at']

    def __str__(self):
        return f'{self.student} → {self.course.title} ({self.rating}★)'