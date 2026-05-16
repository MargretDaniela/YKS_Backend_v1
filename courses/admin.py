
# from django import forms
# from django.contrib import admin
# from django.utils.html import format_html, mark_safe
# from .models import Course, Section, Lesson, Review, Enrollment


# # ── Dynamic category choices from pages.CourseCategory ───────────────
# def _category_choices():
#     try:
#         from pages.models import CourseCategory
#         cats = CourseCategory.objects.filter(is_active=True).order_by('order', 'name')
#         choices = [('', '— Select Category —')] + [(c.name, c.name) for c in cats]
#         return choices
#     except Exception:
#         return [('', '— No categories found —')]


# def _trainer_choices():
#     try:
#         from django.contrib.auth import get_user_model
#         User = get_user_model()
#         trainers = User.objects.filter(
#             role__in=['SUPER_ADMIN', 'ADMIN', 'MENTOR']
#         ).order_by('full_name')
#         return [('', '— Select Trainer —')] + [(u.pk, f"{u.full_name} ({u.role})") for u in trainers]
#     except Exception:
#         return [('', '— No trainers found —')]


# # ======================================================================
# #  INLINES
# # ======================================================================
# class LessonInline(admin.TabularInline):
#     model  = Lesson
#     extra  = 1
#     fields = ['order', 'title', 'duration', 'is_free', 'video_url']


# class SectionInline(admin.StackedInline):
#     model  = Section
#     extra  = 1
#     fields = ['order', 'title']


# # ======================================================================
# #  COURSE FORM
# # ======================================================================
# class CourseAdminForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['category'].widget = forms.Select(choices=_category_choices())
#         self.fields['category'].help_text = 'Categories are managed in Pages Dashboard → Categories'
#         self.fields['trainer'].widget = forms.Select(choices=_trainer_choices())
#         self.fields['trainer'].help_text = 'Only Admins and Mentors are shown'
#         # ✅ Help text for new fields
#         self.fields['learning_points'].help_text = (
#             'Enter each learning point on a new line. Example:\n'
#             'Understand leadership principles\n'
#             'Build confidence as a young leader'
#         )
#         self.fields['instructor_bio'].help_text = (
#             'Short bio shown on the course detail page in the app.'
#         )

#     class Meta:
#         model  = Course
#         fields = '__all__'
#         widgets = {
#             'description':     forms.Textarea(attrs={'rows': 5}),
#             'learning_points': forms.Textarea(attrs={  # ✅ nice textarea
#                 'rows': 8,
#                 'placeholder': (
#                     'Understand leadership principles\n'
#                     'Build confidence as a young leader\n'
#                     'Apply skills in real-world situations\n'
#                     'Develop your personal brand'
#                 ),
#             }),
#             'instructor_bio':  forms.Textarea(attrs={'rows': 4}),  # ✅
#         }


# # ======================================================================
# #  COURSE ADMIN
# # ======================================================================
# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     form = CourseAdminForm

#     list_display  = ['title', 'category_badge', 'trainer', 'price_display',
#                      'is_live', 'start_date', 'end_date', 'thumbnail_preview', 'actions_col']
#     list_filter   = ['is_live', 'category', 'start_date']
#     search_fields = ['title', 'description', 'category']
#     ordering      = ['category', 'title']
#     list_per_page = 20
#     inlines       = [SectionInline]

#     fieldsets = (
#         ('Course Info', {
#             'fields': (
#                 'title',
#                 'description',
#                 'category',
#                 'trainer',
#                 'instructor_bio',    # ✅ real instructor bio
#                 'learning_points',  # ✅ real learning points
#             )
#         }),
#         ('Pricing & Schedule', {
#             'fields': ('price', 'start_date', 'end_date', 'is_live')
#         }),
#         ('Media', {
#             'fields': ('thumbnail', 'recording_url')
#         }),
#     )

#     def category_badge(self, obj):
#         return format_html(
#             '<span style="background:#E8F0FE;color:#1A56DB;padding:3px 10px;'
#             'border-radius:20px;font-size:11px;font-weight:700;">{}</span>',
#             obj.category or '—'
#         )
#     category_badge.short_description = 'Category'
#     category_badge.admin_order_field = 'category'

#     def price_display(self, obj):
#         return format_html(
#             '<span style="font-weight:700;color:#001A35;">US${}</span>',
#             f'{obj.price:.2f}'
#         )
#     price_display.short_description = 'Price'
#     price_display.admin_order_field = 'price'

#     def thumbnail_preview(self, obj):
#         if obj.thumbnail:
#             return mark_safe(
#                 f'<img src="{obj.thumbnail.url}" style="height:40px;width:60px;'
#                 f'object-fit:cover;border-radius:6px;"/>'
#             )
#         return mark_safe('<span style="color:#aaa;font-size:11px;">No image</span>')
#     thumbnail_preview.short_description = 'Thumbnail'

#     def actions_col(self, obj):
#         from django.urls import reverse
#         edit_url   = reverse('admin:courses_course_change', args=[obj.pk])
#         delete_url = reverse('admin:courses_course_delete', args=[obj.pk])
#         return format_html(
#             '<div style="display:flex;gap:4px;">'
#             '<a href="{}" style="display:inline-flex;align-items:center;justify-content:center;'
#             'width:30px;height:30px;border-radius:6px;background:#E8F5EE;color:#1A7A4A;'
#             'border:1px solid #1A7A4A;text-decoration:none;font-size:13px;">'
#             '<i class="fas fa-pen"></i></a>'
#             '<a href="{}" style="display:inline-flex;align-items:center;justify-content:center;'
#             'width:30px;height:30px;border-radius:6px;background:#FDECEA;color:#C0392B;'
#             'border:1px solid #C0392B;text-decoration:none;font-size:13px;"'
#             ' onclick="return confirm(\'Delete this course?\');">'
#             '<i class="fas fa-trash"></i></a>'
#             '</div>',
#             edit_url, delete_url
#         )
#     actions_col.short_description = 'Actions'

#     def has_module_perms(self, request):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_view_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_add_permission(self, request):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_change_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_delete_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) == 'SUPER_ADMIN'


# # ======================================================================
# #  SECTION ADMIN
# # ======================================================================
# @admin.register(Section)
# class SectionAdmin(admin.ModelAdmin):
#     list_display  = ['course', 'title', 'order']
#     list_filter   = ['course']
#     search_fields = ['title', 'course__title']
#     ordering      = ['course', 'order']
#     inlines       = [LessonInline]

#     def has_module_perms(self, request):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_view_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_add_permission(self, request):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_change_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_delete_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) == 'SUPER_ADMIN'


# # ======================================================================
# #  LESSON ADMIN
# # ======================================================================
# @admin.register(Lesson)
# class LessonAdmin(admin.ModelAdmin):
#     list_display  = ['title', 'section', 'duration', 'is_free', 'order']
#     list_filter   = ['is_free', 'section__course']
#     search_fields = ['title', 'section__title', 'section__course__title']
#     ordering      = ['section__course', 'section__order', 'order']

#     def has_module_perms(self, request):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_view_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_add_permission(self, request):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_change_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_delete_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) == 'SUPER_ADMIN'


# # ======================================================================
# #  REVIEW ADMIN
# # ======================================================================
# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display  = ['user', 'course', 'rating_stars', 'created_at']
#     list_filter   = ['rating', 'course']
#     search_fields = ['user__email', 'user__full_name', 'course__title', 'comment']
#     ordering      = ['-created_at']

#     def rating_stars(self, obj):
#         stars = '★' * obj.rating + '☆' * (5 - obj.rating)
#         color = '#E6A817' if obj.rating >= 4 else '#C0392B'
#         return format_html(
#             '<span style="color:{};font-size:14px;">{}</span>', color, stars
#         )
#     rating_stars.short_description = 'Rating'

#     def has_module_perms(self, request):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_view_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_add_permission(self, request):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_change_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_delete_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) == 'SUPER_ADMIN'


# # ======================================================================
# #  ENROLLMENT ADMIN
# # ======================================================================
# @admin.register(Enrollment)
# class EnrollmentAdmin(admin.ModelAdmin):
#     list_display  = ['user', 'course', 'payment_status', 'progress_bar',
#                      'completed_lessons', 'completed', 'actions_col']
#     list_filter   = ['payment_status', 'completed', 'course__category']
#     search_fields = ['user__email', 'user__full_name', 'course__title']
#     ordering      = ['-pk']
#     list_per_page = 25
#     autocomplete_fields = ['course']

#     fieldsets = (
#         ('Enrollment Info', {
#             'fields': ('user', 'course', 'payment_status')
#         }),
#         ('Progress', {
#             'fields': (
#                 'progress_percentage',
#                 'completed_lessons',  # ✅ shown so admin can set for testing
#                 'completed',
#             )
#         }),
#     )

#     def progress_bar(self, obj):
#         pct   = obj.progress_percentage or 0
#         color = '#1A7A4A' if pct >= 80 else '#E6A817' if pct >= 40 else '#C0392B'
#         return mark_safe(
#             f'<div style="display:flex;align-items:center;gap:8px;">'
#             f'<div style="width:80px;height:8px;background:#eee;border-radius:4px;overflow:hidden;">'
#             f'<div style="width:{pct}%;height:100%;background:{color};border-radius:4px;"></div>'
#             f'</div>'
#             f'<span style="font-size:11px;font-weight:700;color:{color};">{pct}%</span>'
#             f'</div>'
#         )
#     progress_bar.short_description = 'Progress'

#     def actions_col(self, obj):
#         from django.urls import reverse
#         edit_url   = reverse('admin:courses_enrollment_change', args=[obj.pk])
#         delete_url = reverse('admin:courses_enrollment_delete', args=[obj.pk])
#         return format_html(
#             '<div style="display:flex;gap:4px;">'
#             '<a href="{}" style="display:inline-flex;align-items:center;justify-content:center;'
#             'width:30px;height:30px;border-radius:6px;background:#E8F5EE;color:#1A7A4A;'
#             'border:1px solid #1A7A4A;text-decoration:none;font-size:13px;">'
#             '<i class="fas fa-pen"></i></a>'
#             '<a href="{}" style="display:inline-flex;align-items:center;justify-content:center;'
#             'width:30px;height:30px;border-radius:6px;background:#FDECEA;color:#C0392B;'
#             'border:1px solid #C0392B;text-decoration:none;font-size:13px;"'
#             ' onclick="return confirm(\'Delete this enrollment?\');">'
#             '<i class="fas fa-trash"></i></a>'
#             '</div>',
#             edit_url, delete_url
#         )
#     actions_col.short_description = 'Actions'

#     def has_module_perms(self, request):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_view_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_add_permission(self, request):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_change_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']

#     def has_delete_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) == 'SUPER_ADMIN'

# C:\Users\Admin\Desktop\TheYKSApp\courses\admin.py

from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django import forms
from .models import (
    Category, Course, LearningPoint, Module, Lesson,
    Enrollment, LessonProgress, Review,
)


# ======================================================================
#  INLINES
# ======================================================================
class LearningPointInline(admin.TabularInline):
    model  = LearningPoint
    extra  = 3
    fields = ['point', 'order']


class LessonInline(admin.TabularInline):
    model  = Lesson
    extra  = 1
    fields = [
        'order', 'title', 'duration', 'is_free',
        'video_type', 'video_url', 'video_file', 'allow_download',
    ]


class ModuleInline(admin.StackedInline):
    model            = Module
    extra            = 1
    fields           = ['title', 'description', 'order']
    show_change_link = True  # click through to add lessons inside


# ======================================================================
#  CATEGORY
# ======================================================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'icon', 'course_count']
    search_fields = ['name']

    @admin.display(description='Courses')
    def course_count(self, obj):
        return obj.courses.count()


# ======================================================================
#  COURSE FORM
# ======================================================================
class CourseAdminForm(forms.ModelForm):
    class Meta:
        model  = Course
        # ✅ Only fields that ACTUALLY exist on the Course model
        fields = [
            'category', 'title', 'description',
            'instructor', 'instructor_bio',
            'amount', 'currency',
            'start_date', 'end_date', 'is_live',
            'thumbnail', 'is_published', 'student_count',
        ]
        widgets = {
            'description':    forms.Textarea(attrs={'rows': 5}),
            'instructor_bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instructor_bio' in self.fields:
            self.fields['instructor_bio'].help_text = (
                'Short bio shown on the course detail page in the app.'
            )


# ======================================================================
#  COURSE
# ======================================================================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm

    list_display = [
        'title', 'category_badge', 'instructor',
        'price_display', 'is_live', 'is_published',
        'start_date', 'student_count',
        'avg_rating_display', 'thumbnail_preview',
    ]
    list_filter   = ['is_published', 'is_live', 'category']
    search_fields = ['title', 'description', 'instructor', 'category__name']
    ordering      = ['-created_at']
    list_per_page = 20
    list_editable = ['is_published', 'is_live']

    # ✅ learning_points is a related model → use LearningPointInline
    # ✅ modules are related → use ModuleInline
    inlines = [LearningPointInline, ModuleInline]

    fieldsets = (
        ('Course Info', {
            'fields': (
                'category', 'title', 'description',
                'instructor', 'instructor_bio',
            )
        }),
        ('Pricing & Schedule', {
            'fields': (
                'amount', 'currency',
                'start_date', 'end_date',
                'is_live', 'is_published',
            )
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('Stats', {
            'fields': ('student_count',),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Category')
    def category_badge(self, obj):
        cat = obj.category.name if obj.category else '—'
        return format_html(
            '<span style="background:#E8F0FE;color:#1A56DB;padding:3px 10px;'
            'border-radius:20px;font-size:11px;font-weight:700;">{}</span>',
            cat
        )

    @admin.display(description='Price')
    def price_display(self, obj):
        return format_html(
            '<span style="font-weight:700;color:#001A35;">US${:.2f}</span>',
            float(obj.amount or 0)
        )

    @admin.display(description='Rating')
    def avg_rating_display(self, obj):
        return obj.avg_rating

    @admin.display(description='Thumb')
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return mark_safe(
                f'<img src="{obj.thumbnail.url}" '
                f'style="height:40px;width:60px;object-fit:cover;border-radius:6px;"/>'
            )
        return mark_safe('<span style="color:#aaa;font-size:11px;">No image</span>')

    # Role-based permissions
    def _has_role(self, request, roles):
        return getattr(request.user, 'role', None) in roles

    def has_view_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_add_permission(self, request):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_change_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_delete_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN'])


# ======================================================================
#  MODULE
# ======================================================================
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display  = ['title', 'course', 'order', 'lesson_count']
    list_filter   = ['course']
    search_fields = ['title', 'course__title']
    ordering      = ['course', 'order']
    inlines       = [LessonInline]

    @admin.display(description='Lessons')
    def lesson_count(self, obj):
        return obj.lessons.count()

    def _has_role(self, request, roles):
        return getattr(request.user, 'role', None) in roles

    def has_view_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_add_permission(self, request):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_change_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_delete_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN'])


# ======================================================================
#  LESSON
# ======================================================================
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'module', 'order', 'duration',
        'is_free', 'video_type', 'allow_download',
    ]
    list_filter   = ['is_free', 'video_type', 'allow_download', 'module__course']
    search_fields = ['title', 'module__title', 'module__course__title']
    ordering      = ['module__course', 'module__order', 'order']
    list_editable = ['is_free', 'allow_download', 'order']

    fieldsets = (
        ('Basic', {
            'fields': ('module', 'title', 'order', 'duration', 'is_free')
        }),
        ('Video', {
            'fields': ('video_type', 'video_url', 'video_file'),
            'description': (
                'Choose URL for YouTube/Vimeo links, '
                'or Upload to store the file on the server.'
            ),
        }),
        ('Download', {
            'fields': ('allow_download',)
        }),
    )

    def _has_role(self, request, roles):
        return getattr(request.user, 'role', None) in roles

    def has_view_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_add_permission(self, request):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_change_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_delete_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN'])


# ======================================================================
#  REVIEW
# ======================================================================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ['student', 'course', 'rating_stars', 'created_at']
    list_filter   = ['rating', 'course']
    search_fields = ['student__email', 'course__title', 'comment']
    ordering      = ['-created_at']

    @admin.display(description='Rating')
    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        color = '#E6A817' if obj.rating >= 4 else '#C0392B'
        return format_html(
            '<span style="color:{};font-size:14px;">{}</span>',
            color, stars
        )

    def _has_role(self, request, roles):
        return getattr(request.user, 'role', None) in roles

    def has_view_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_add_permission(self, request):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_change_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_delete_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN'])


# ======================================================================
#  ENROLLMENT
# ✅ Only fields that exist on the Enrollment model we built:
#    student, course, enrolled_at, is_active
#    + progress_percentage is a @property
# ======================================================================
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display  = [
        'student', 'course', 'enrolled_at',
        'is_active', 'progress_bar',
    ]
    list_filter   = ['is_active', 'course__category']
    search_fields = ['student__email', 'course__title']
    ordering      = ['-enrolled_at']
    list_per_page = 25
    readonly_fields = ['enrolled_at', 'progress_display']

    fieldsets = (
        ('Enrollment Info', {
            'fields': ('student', 'course', 'is_active', 'enrolled_at')
        }),
        ('Progress', {
            'fields': ('progress_display',)
        }),
    )

    @admin.display(description='Progress')
    def progress_bar(self, obj):
        pct   = obj.progress_percentage
        color = '#1A7A4A' if pct >= 80 else '#E6A817' if pct >= 40 else '#C0392B'
        return mark_safe(
            f'<div style="display:flex;align-items:center;gap:8px;">'
            f'<div style="width:80px;height:8px;background:#eee;'
            f'border-radius:4px;overflow:hidden;">'
            f'<div style="width:{pct}%;height:100%;background:{color};'
            f'border-radius:4px;"></div></div>'
            f'<span style="font-size:11px;font-weight:700;color:{color};">'
            f'{pct}%</span></div>'
        )

    @admin.display(description='Progress %')
    def progress_display(self, obj):
        return f'{obj.progress_percentage}%'

    def _has_role(self, request, roles):
        return getattr(request.user, 'role', None) in roles

    def has_view_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_add_permission(self, request):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_change_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN', 'ADMIN'])

    def has_delete_permission(self, request, obj=None):
        return self._has_role(request, ['SUPER_ADMIN'])


# ======================================================================
#  LESSON PROGRESS  (read-only audit view)
# ======================================================================
@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display    = ['enrollment', 'lesson', 'is_completed',
                       'last_position', 'completed_at']
    list_filter     = ['is_completed', 'enrollment__course']
    search_fields   = ['enrollment__student__email', 'lesson__title']
    readonly_fields = ['enrollment', 'lesson', 'is_completed',
                       'completed_at', 'last_position']
    ordering        = ['-completed_at']

    # No adding or deleting — progress is system-managed
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False