# attendance/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone


class Attendance(models.Model):

    class Status(models.TextChoices):
        PRESENT  = 'PRESENT',  'Present'
        ABSENT   = 'ABSENT',   'Absent'
        LATE     = 'LATE',     'Late'
        EXCUSED  = 'EXCUSED',  'Excused'

    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendance_records_as_mentor',
        limit_choices_to={'role': 'MENTOR'},
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendance_records_as_student',
        limit_choices_to={'role': 'STUDENT'},
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='attendance_records',
        null=True,
        blank=True,
        help_text='The course this attendance record belongs to.',
    )
    date   = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PRESENT,
    )
    notes = models.TextField(blank=True, help_text='Optional notes about this record.')

    class Meta:
        verbose_name        = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        ordering            = ['-date', 'student__full_name']
        unique_together     = ('mentor', 'student', 'course', 'date')

    def __str__(self):
        return (
            f'{self.student} — {self.course or "General"} '
            f'[{self.date}] {self.get_status_display()}'
        )