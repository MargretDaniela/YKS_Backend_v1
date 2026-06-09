# attendance/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Attendance


def _role(request):
    return getattr(request.user, 'role', None)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display  = [
        'student', 'course', 'mentor', 'date',
        'status_badge', 'notes_short',
    ]
    list_filter   = ['status', 'date', 'course']
    search_fields = [
        'student__full_name', 'student__email',
        'mentor__full_name',  'course__title',
    ]
    ordering      = ['-date', 'student__full_name']
    list_per_page = 30
    date_hierarchy = 'date'

    fieldsets = (
        ('Record', {
            'fields': ('mentor', 'student', 'course', 'date', 'status', 'notes'),
        }),
    )

    # ── Display helpers ──────────────────────────────────────────────
    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'PRESENT': '#1A7A4A',
            'ABSENT':  '#C0392B',
            'LATE':    '#E6A817',
            'EXCUSED': '#1A56DB',
        }
        color = colors.get(obj.status, '#888')
        return format_html(
            '<span style="background:{0}22;color:{0};padding:3px 10px;'
            'border-radius:20px;font-size:11px;font-weight:700;">{1}</span>',
            color, obj.get_status_display(),
        )

    @admin.display(description='Notes')
    def notes_short(self, obj):
        if obj.notes:
            return obj.notes[:60] + ('…' if len(obj.notes) > 60 else '')
        return mark_safe('<span style="color:#bbb;">—</span>')

    # ── Permissions ──────────────────────────────────────────────────
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if _role(request) == 'MENTOR':
            # Mentor only sees attendance records they created
            return qs.filter(mentor=request.user)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if _role(request) == 'MENTOR':
            # Lock the mentor field to the logged-in mentor
            if 'mentor' in form.base_fields:
                form.base_fields['mentor'].initial  = request.user
                form.base_fields['mentor'].disabled = True
            # Only show students enrolled in this mentor's courses
            if 'student' in form.base_fields:
                from django.contrib.auth import get_user_model
                from courses.models import Enrollment
                User = get_user_model()
                enrolled_ids = Enrollment.objects.filter(
                    course__trainer=request.user,
                    payment_status='paid',
                ).values_list('student_id', flat=True)
                form.base_fields['student'].queryset = User.objects.filter(
                    pk__in=enrolled_ids)
            # Only show this mentor's courses
            if 'course' in form.base_fields:
                from courses.models import Course
                form.base_fields['course'].queryset = Course.objects.filter(
                    trainer=request.user)
        return form

    def has_view_permission(self, request, obj=None):
        return _role(request) in ['SUPER_ADMIN', 'ADMIN', 'MENTOR']

    def has_add_permission(self, request):
        return _role(request) in ['SUPER_ADMIN', 'ADMIN', 'MENTOR']

    def has_change_permission(self, request, obj=None):
        if _role(request) == 'MENTOR' and obj is not None:
            return obj.mentor == request.user
        return _role(request) in ['SUPER_ADMIN', 'ADMIN', 'MENTOR']

    def has_delete_permission(self, request, obj=None):
        if _role(request) == 'MENTOR' and obj is not None:
            return obj.mentor == request.user
        return _role(request) in ['SUPER_ADMIN', 'ADMIN']