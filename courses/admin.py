
# # courses/admin.py
# """
# Merged admin — combines:
#   • Role-based permissions (SUPER_ADMIN / ADMIN / MENTOR)
#   • Progress bars, star ratings, category badges, thumbnail previews
#   • Module video upload (pick file from disk) + external URL
#   • Module resource link (any URL — YouTube, TikTok, PDF, website…)
#   • Lesson video upload + URL
#   • LearningPoint, Enrollment, LessonProgress, Review admins
# """

# from django.contrib import admin
# from django.utils.html import format_html, mark_safe
# from django import forms

# from .models import (
#     Category, Course, LearningPoint,
#     Module, Lesson,
#     Enrollment, LessonProgress, Review,
# )


# # ======================================================================
# #  ROLE HELPER  (shared by all admin classes)
# # ======================================================================
# def _has_role(request, roles):
#     return getattr(request.user, 'role', None) in roles


# # ======================================================================
# #  VIDEO / LINK PREVIEW HELPERS
# # ======================================================================
# def _video_preview_html(obj):
#     """Render a small inline <video> player if the object has a video."""
#     src = getattr(obj, 'video_source', '') or ''
#     if not src:
#         return mark_safe('<span style="color:#aaa;font-size:12px;">No video yet.</span>')
#     return format_html(
#         '<video src="{}" controls '
#         'style="max-width:280px;max-height:170px;border-radius:8px;'
#         'margin-top:6px;border:1px solid #ddd;"></video>',
#         src,
#     )


# def _link_preview_html(url, label=''):
#     if not url:
#         return mark_safe('<span style="color:#aaa;font-size:12px;">—</span>')
#     text = (label or '').strip() or url
#     return format_html(
#         '<a href="{}" target="_blank" rel="noopener" '
#         'style="color:#1A56DB;text-decoration:underline;font-size:13px;">'
#         '🔗 {}</a>',
#         url, text,
#     )


# # ======================================================================
# #  LESSON INLINE  (used inside ModuleAdmin)
# # ======================================================================
# class LessonInline(admin.StackedInline):
#     model            = Lesson
#     extra            = 1
#     show_change_link = True
#     ordering         = ['order']
#     fields           = (
#         'order', 'title', 'duration', 'is_free', 'allow_download',
#         'video_type', 'video_file', 'video_url',
#     )

#     def get_extra(self, request, obj=None, **kwargs):
#         # Show 1 blank form when no lessons exist, 0 otherwise
#         return 0 if (obj and obj.lessons.exists()) else 1


# # ======================================================================
# #  MODULE INLINE  (used inside CourseAdmin)
# # ======================================================================
# class ModuleInline(admin.StackedInline):
#     model            = Module
#     extra            = 1
#     show_change_link = True   # "click to add lessons inside"
#     ordering         = ['order']
#     readonly_fields  = ('video_preview', 'resource_link_preview')

#     fields = (
#         'title', 'description', 'order',
#         # video
#         'video_type', 'video_file', 'video_url', 'video_preview',
#         # resource link
#         'resource_link', 'resource_link_label', 'resource_link_preview',
#     )

#     def get_fieldsets(self, request, obj=None):
#         return [
#             ('📋 Module Info', {
#                 'fields': ('title', 'description', 'order'),
#             }),
#             ('🎬 Module Video', {
#                 'fields': ('video_type', 'video_file', 'video_url', 'video_preview'),
#                 'description': (
#                     '<p style="color:#555;font-size:13px;margin:6px 0 10px;">'
#                     '<strong>Uploaded File</strong> — pick a video from your device '
#                     '(MP4, WebM, MOV …).<br>'
#                     '<strong>External URL</strong> — paste any video link.<br>'
#                     'Leave as <strong>No Video</strong> if not applicable.</p>'
#                 ),
#             }),
#             ('🔗 Resource Link (optional)', {
#                 'fields': (
#                     'resource_link', 'resource_link_label', 'resource_link_preview',
#                 ),
#                 'description': (
#                     '<p style="color:#555;font-size:13px;margin:6px 0 10px;">'
#                     'Any URL you want students to visit — YouTube, TikTok, '
#                     'a PDF, a Google Doc, a website. Completely optional.</p>'
#                 ),
#                 'classes': ('collapse',),
#             }),
#         ]

#     def video_preview(self, obj):
#         if not obj or not obj.pk:
#             return 'Save the module first to see a preview.'
#         return _video_preview_html(obj)
#     video_preview.short_description = '▶ Video Preview'

#     def resource_link_preview(self, obj):
#         if not obj or not obj.pk:
#             return '—'
#         return _link_preview_html(obj.resource_link, obj.resource_link_label)
#     resource_link_preview.short_description = '🔗 Link Preview'


# # ======================================================================
# #  LEARNING POINT INLINE
# # ======================================================================
# class LearningPointInline(admin.TabularInline):
#     model    = LearningPoint
#     extra    = 3
#     fields   = ['point', 'order']
#     ordering = ['order']


# # ======================================================================
# #  CATEGORY ADMIN
# # ======================================================================
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display  = ['name', 'icon', 'course_count', 'created_at']
#     search_fields = ['name']
#     ordering      = ['name']

#     @admin.display(description='Courses')
#     def course_count(self, obj):
#         return obj.courses.count()


# # ======================================================================
# #  COURSE FORM
# # ======================================================================
# class CourseAdminForm(forms.ModelForm):
#     class Meta:
#         model  = Course
#         fields = [
#             'category', 'title', 'description',
#             'instructor', 'trainer', 'instructor_bio',
#             'learning_points_text',
#             'amount', 'currency', 'price',
#             'start_date', 'end_date', 'is_live', 'recording_url',
#             'thumbnail', 'is_published', 'student_count',
#         ]
#         widgets = {
#             'description':          forms.Textarea(attrs={'rows': 5}),
#             'instructor_bio':       forms.Textarea(attrs={'rows': 4}),
#             'learning_points_text': forms.Textarea(attrs={'rows': 5}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if 'instructor_bio' in self.fields:
#             self.fields['instructor_bio'].help_text = (
#                 'Short bio shown on the course detail page in the app.'
#             )
#         if 'learning_points_text' in self.fields:
#             self.fields['learning_points_text'].help_text = (
#                 'One learning point per line. Shown as bullet points in the app.'
#             )


# # ======================================================================
# #  COURSE ADMIN
# # ======================================================================
# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     form = CourseAdminForm

#     list_display = [
#         'title', 'category_badge', 'instructor',
#         'price_display', 'is_live', 'is_published',
#         'start_date', 'student_count',
#         'avg_rating_display', 'thumbnail_preview',
#     ]
#     list_filter   = ['is_published', 'is_live', 'category']
#     search_fields = ['title', 'description', 'instructor', 'category__name']
#     ordering      = ['-created_at']
#     list_per_page = 20
#     list_editable = ['is_published', 'is_live']

#     readonly_fields = ['thumbnail_preview', 'created_at', 'updated_at']

#     inlines = [LearningPointInline, ModuleInline]

#     fieldsets = (
#         (' Course Info', {
#             'fields': (
#                 'category', 'title', 'description',
#                 'instructor', 'trainer', 'instructor_bio',
#                 'learning_points_text',
#             ),
#         }),
#         (' Pricing & Schedule', {
#             'fields': (
#                 'amount', 'currency', 'price',
#                 'start_date', 'end_date',
#                 'is_live', 'recording_url',
#             ),
#         }),
#         (' Thumbnail', {
#             'fields': ('thumbnail', 'thumbnail_preview'),
#         }),
#         (' Publishing', {
#             'fields': ('is_published', 'student_count'),
#         }),
#         (' Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',),
#         }),
#     )

#     # ── Display helpers ──────────────────────────────────────────────
#     @admin.display(description='Category')
#     def category_badge(self, obj):
#         cat = obj.category.name if obj.category else '—'
#         return format_html(
#             '<span style="background:#E8F0FE;color:#1A56DB;padding:3px 10px;'
#             'border-radius:20px;font-size:11px;font-weight:700;">{}</span>',
#             cat,
#         )

#     @admin.display(description='Price')
#     def price_display(self, obj):
#         return format_html(
#             '<span style="font-weight:700;color:#001A35;">US${:.2f}</span>',
#             float(obj.amount or 0),
#         )

#     @admin.display(description='Rating')
#     def avg_rating_display(self, obj):
#         return obj.avg_rating

#     @admin.display(description='Thumb')
#     def thumbnail_preview(self, obj):
#         if obj.thumbnail:
#             return mark_safe(
#                 f'<img src="{obj.thumbnail.url}" '
#                 f'style="height:48px;width:72px;object-fit:cover;'
#                 f'border-radius:6px;border:1px solid #ddd;"/>'
#             )
#         return mark_safe('<span style="color:#aaa;font-size:11px;">No image</span>')

#     # ── Role-based permissions ────────────────────────────────────────
#     def has_view_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])

#     def has_add_permission(self, request):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])

#     def has_change_permission(self, request, obj=None):
#         # Mentors can only edit their own courses
#         if _has_role(request, ['MENTOR']) and obj is not None:
#             return obj.trainer == request.user
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])

#     def has_delete_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN'])

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if _has_role(request, ['MENTOR']):
#             return qs.filter(trainer=request.user)
#         return qs


# # ======================================================================
# #  MODULE ADMIN  (standalone — also reachable via Course inline link)
# # ======================================================================
# @admin.register(Module)
# class ModuleAdmin(admin.ModelAdmin):
#     list_display  = [
#         'title', 'course', 'order',
#         'video_status', 'resource_status', 'lesson_count', 'created_at',
#     ]
#     list_filter   = ['course', 'video_type']
#     search_fields = ['title', 'course__title']
#     ordering      = ['course', 'order']
#     readonly_fields = ['video_preview', 'resource_link_preview']

#     inlines = [LessonInline]

#     fieldsets = [
#         ('📋 Module Info', {
#             'fields': ('course', 'title', 'description', 'order'),
#         }),
#         ('🎬 Module Video', {
#             'fields': (
#                 'video_type',
#                 'video_file',
#                 'video_url',
#                 'video_preview',
#             ),
#             'description': (
#                 '<p style="color:#555;font-size:13px;margin:6px 0 12px;">'
#                 'Choose <strong>Uploaded File</strong> to pick a video from '
#                 'your device and store it on the server.<br>'
#                 'Choose <strong>External URL</strong> to paste any video link '
#                 '(YouTube embed, Vimeo, CDN, etc.).<br>'
#                 'The video plays directly in the student app for this module.'
#                 '</p>'
#             ),
#         }),
#         ('🔗 Resource Link (optional)', {
#             'fields': (
#                 'resource_link',
#                 'resource_link_label',
#                 'resource_link_preview',
#             ),
#             'description': (
#                 '<p style="color:#555;font-size:13px;margin:6px 0 12px;">'
#                 'Add any link — YouTube, TikTok, a PDF, a website, anything. '
#                 'Students see a tap-able button that opens the link. '
#                 'Leave blank if not needed.</p>'
#             ),
#             'classes': ('collapse',),
#         }),
#     ]

#     # ── List column helpers ──────────────────────────────────────────
#     @admin.display(description='Video')
#     def video_status(self, obj):
#         if obj.has_video:
#             return format_html(
#                 '<span style="color:green;font-weight:bold;">✔ {}</span>',
#                 obj.get_video_type_display(),
#             )
#         return format_html('<span style="color:#bbb;">No video</span>')

#     @admin.display(description='Resource Link')
#     def resource_status(self, obj):
#         if obj.has_resource_link:
#             return format_html(
#                 '<a href="{}" target="_blank" '
#                 'style="color:#1A56DB;font-size:12px;">🔗 Open</a>',
#                 obj.resource_link,
#             )
#         return format_html('<span style="color:#bbb;">—</span>')

#     @admin.display(description='Lessons')
#     def lesson_count(self, obj):
#         return obj.lessons.count()

#     # ── Read-only field renderers ─────────────────────────────────────
#     def video_preview(self, obj):
#         return _video_preview_html(obj)
#     video_preview.short_description = '▶ Video Preview'

#     def resource_link_preview(self, obj):
#         return _link_preview_html(obj.resource_link, obj.resource_link_label)
#     resource_link_preview.short_description = '🔗 Link Preview'

#     # ── Role-based permissions ────────────────────────────────────────
#     def has_view_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])

#     def has_add_permission(self, request):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])

#     def has_change_permission(self, request, obj=None):
#         if _has_role(request, ['MENTOR']) and obj is not None:
#             return obj.course.trainer == request.user
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])

#     def has_delete_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if _has_role(request, ['MENTOR']):
#             return qs.filter(course__trainer=request.user)
#         return qs


# # ======================================================================
# #  LESSON ADMIN  (standalone)
# # ======================================================================
# @admin.register(Lesson)
# class LessonAdmin(admin.ModelAdmin):
#     list_display  = [
#         'title', 'module', 'order', 'duration',
#         'is_free', 'video_type', 'allow_download',
#     ]
#     list_filter   = ['is_free', 'video_type', 'allow_download', 'module__course']
#     search_fields = ['title', 'module__title', 'module__course__title']
#     ordering      = ['module__course', 'module__order', 'order']
#     list_editable = ['is_free', 'allow_download', 'order']
#     readonly_fields = ['video_preview']

#     fieldsets = (
#         ('📖 Lesson Info', {
#             'fields': ('module', 'title', 'order', 'duration',
#                        'is_free', 'allow_download'),
#         }),
#         ('🎬 Video', {
#             'fields': ('video_type', 'video_file', 'video_url', 'video_preview'),
#             'description': (
#                 '<p style="color:#555;font-size:13px;margin:6px 0 10px;">'
#                 'Upload a video file from your device or paste an external URL. '
#                 'Uploaded files are stored on the server and streamed to students.'
#                 '</p>'
#             ),
#         }),
#     )

#     def video_preview(self, obj):
#         return _video_preview_html(obj)
#     video_preview.short_description = '▶ Video Preview'

#     # ── Role-based permissions ────────────────────────────────────────
#     def has_view_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])

#     def has_add_permission(self, request):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])

#     def has_change_permission(self, request, obj=None):
#         if _has_role(request, ['MENTOR']) and obj is not None:
#             return obj.module.course.trainer == request.user
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])

#     def has_delete_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if _has_role(request, ['MENTOR']):
#             return qs.filter(module__course__trainer=request.user)
#         return qs


# # ======================================================================
# #  REVIEW ADMIN
# # ======================================================================
# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display  = ['student', 'course', 'rating_stars', 'created_at']
#     list_filter   = ['rating', 'course']
#     search_fields = ['student__email', 'course__title', 'comment']
#     ordering      = ['-created_at']

#     @admin.display(description='Rating')
#     def rating_stars(self, obj):
#         stars = '★' * obj.rating + '☆' * (5 - obj.rating)
#         color = '#E6A817' if obj.rating >= 4 else '#C0392B'
#         return format_html(
#             '<span style="color:{};font-size:15px;">{}</span>', color, stars,
#         )

#     def has_view_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])

#     def has_add_permission(self, request):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])

#     def has_change_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])

#     def has_delete_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN'])


# # ======================================================================
# #  ENROLLMENT ADMIN
# # ======================================================================
# @admin.register(Enrollment)
# class EnrollmentAdmin(admin.ModelAdmin):
#     list_display  = [
#         'student', 'course', 'payment_status',
#         'progress_bar', 'completed', 'enrolled_at',
#     ]
#     list_filter   = ['payment_status', 'completed', 'course__category']
#     search_fields = ['student__email', 'course__title']
#     ordering      = ['-enrolled_at']
#     list_per_page = 25
#     readonly_fields = ['enrolled_at', 'progress_display']

#     fieldsets = (
#         ('Enrollment Info', {
#             'fields': ('student', 'course', 'payment_status',
#                        'is_active', 'enrolled_at'),
#         }),
#         ('Progress', {
#             'fields': ('progress_percentage', 'completed_lessons',
#                        'completed', 'progress_display'),
#         }),
#     )

#     @admin.display(description='Progress')
#     def progress_bar(self, obj):
#         pct   = obj.progress_percentage
#         color = '#1A7A4A' if pct >= 80 else '#E6A817' if pct >= 40 else '#C0392B'
#         return mark_safe(
#             f'<div style="display:flex;align-items:center;gap:8px;">'
#             f'<div style="width:80px;height:8px;background:#eee;'
#             f'border-radius:4px;overflow:hidden;">'
#             f'<div style="width:{pct}%;height:100%;background:{color};'
#             f'border-radius:4px;"></div></div>'
#             f'<span style="font-size:11px;font-weight:700;color:{color};">'
#             f'{pct}%</span></div>'
#         )

#     @admin.display(description='Progress %')
#     def progress_display(self, obj):
#         return f'{obj.progress_percentage}%'

#     def has_view_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])

#     def has_add_permission(self, request):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])

#     def has_change_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])

#     def has_delete_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN'])


# # ======================================================================
# #  LESSON PROGRESS  (read-only audit view)
# # ======================================================================
# @admin.register(LessonProgress)
# class LessonProgressAdmin(admin.ModelAdmin):
#     list_display  = ['enrollment', 'lesson', 'is_completed',
#                      'last_position', 'completed_at']
#     list_filter   = ['is_completed', 'enrollment__course']
#     search_fields = ['enrollment__student__email', 'lesson__title']
#     readonly_fields = ['enrollment', 'lesson', 'is_completed',
#                        'completed_at', 'last_position']
#     ordering      = ['-completed_at']

#     def has_add_permission(self, request):
#         return False   # progress is system-managed only

#     def has_delete_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN'])

#     def has_view_permission(self, request, obj=None):
#         return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])

#     def has_change_permission(self, request, obj=None):
#         return False

# courses/admin.py
from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django import forms
from .models import (
    Category, Course, LearningPoint,
    Module, Lesson, Enrollment, LessonProgress, Review,
)

def _has_role(request, roles):
    return getattr(request.user, 'role', None) in roles

def _video_preview_html(obj):
    src = getattr(obj, 'video_source', '') or ''
    if not src:
        return mark_safe('<span style="color:#aaa;font-size:12px;">No video yet.</span>')
    return format_html(
        '<video src="{}" controls style="max-width:280px;max-height:170px;border-radius:8px;margin-top:6px;border:1px solid #ddd;"></video>',
        src,
    )

def _link_preview_html(url, label=''):
    if not url:
        return mark_safe('<span style="color:#aaa;font-size:12px;">-</span>')
    text = (label or '').strip() or url
    return format_html(
        '<a href="{}" target="_blank" rel="noopener" style="color:#1A56DB;text-decoration:underline;font-size:13px;">{}</a>',
        url, text,
    )

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1
    show_change_link = True
    ordering = ['order']
    fields = ('order', 'title', 'duration', 'is_free', 'allow_download', 'video_type', 'video_file', 'video_url')
    def get_extra(self, request, obj=None, **kwargs):
        return 0 if (obj and obj.lessons.exists()) else 1

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1
    show_change_link = True
    ordering = ['order']
    readonly_fields = ('video_preview', 'resource_link_preview')
    fields = ('title', 'description', 'order', 'video_type', 'video_file', 'video_url', 'video_preview', 'resource_link', 'resource_link_label', 'resource_link_preview')
    def video_preview(self, obj):
        if not obj or not obj.pk:
            return 'Save the module first to see a preview.'
        return _video_preview_html(obj)
    video_preview.short_description = 'Video Preview'
    def resource_link_preview(self, obj):
        if not obj or not obj.pk:
            return mark_safe('<span style="color:#aaa;">-</span>')
        return _link_preview_html(obj.resource_link, obj.resource_link_label)
    resource_link_preview.short_description = 'Link Preview'

class LearningPointInline(admin.TabularInline):
    model = LearningPoint
    extra = 3
    fields = ['point', 'order']
    ordering = ['order']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'course_count', 'created_at']
    search_fields = ['name']
    ordering = ['name']
    @admin.display(description='Courses')
    def course_count(self, obj):
        return obj.courses.count()
    def has_view_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])
    def has_add_permission(self, request):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])
    def has_change_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])
    def has_delete_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN'])

class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['category', 'title', 'description', 'instructor', 'trainer', 'instructor_bio', 'learning_points_text', 'amount', 'currency', 'price', 'start_date', 'end_date', 'is_live', 'recording_url', 'thumbnail', 'is_published', 'student_count']
        widgets = {'description': forms.Textarea(attrs={'rows': 5}), 'instructor_bio': forms.Textarea(attrs={'rows': 4}), 'learning_points_text': forms.Textarea(attrs={'rows': 5})}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ['title', 'category_badge', 'instructor', 'price_display', 'is_live', 'is_published', 'start_date', 'student_count', 'avg_rating_display', 'thumbnail_preview']
    list_filter = ['is_published', 'is_live', 'category']
    search_fields = ['title', 'description', 'instructor', 'category__name']
    ordering = ['-created_at']
    list_per_page = 20
    list_editable = ['is_published', 'is_live']
    readonly_fields = ['thumbnail_preview', 'created_at', 'updated_at']
    inlines = [LearningPointInline, ModuleInline]
    fieldsets = (
        ('Course Info', {'fields': ('category', 'title', 'description', 'instructor', 'trainer', 'instructor_bio', 'learning_points_text')}),
        ('Pricing & Schedule', {'fields': ('amount', 'currency', 'price', 'start_date', 'end_date', 'is_live', 'recording_url')}),
        ('Thumbnail', {'fields': ('thumbnail', 'thumbnail_preview')}),
        ('Publishing', {'fields': ('is_published', 'student_count')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    @admin.display(description='Category')
    def category_badge(self, obj):
        cat = obj.category.name if obj.category else '-'
        return format_html('<span style="background:#E8F0FE;color:#1A56DB;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">{}</span>', cat)
    @admin.display(description='Price')
    def price_display(self, obj):
        return format_html('<span style="font-weight:700;color:#001A35;">US${:.2f}</span>', float(obj.amount or 0))
    @admin.display(description='Rating')
    def avg_rating_display(self, obj):
        return obj.avg_rating
    @admin.display(description='Thumb')
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail.url}" style="height:48px;width:72px;object-fit:cover;border-radius:6px;border:1px solid #ddd;"/>')
        return mark_safe('<span style="color:#aaa;font-size:11px;">No image</span>')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if _has_role(request, ['MENTOR']):
            return qs.filter(trainer=request.user)
        return qs
    def has_view_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])
    def has_add_permission(self, request):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])
    def has_change_permission(self, request, obj=None):
        if _has_role(request, ['MENTOR']) and obj is not None:
            return obj.trainer == request.user
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])
    def has_delete_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN'])

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'video_status', 'resource_status', 'lesson_count', 'created_at']
    list_filter = ['course', 'video_type']
    search_fields = ['title', 'course__title']
    ordering = ['course', 'order']
    readonly_fields = ['video_preview', 'resource_link_preview']
    inlines = [LessonInline]
    fieldsets = [
        ('Module Info', {'fields': ('course', 'title', 'description', 'order')}),
        ('Module Video', {'fields': ('video_type', 'video_file', 'video_url', 'video_preview')}),
        ('Resource Link (optional)', {'fields': ('resource_link', 'resource_link_label', 'resource_link_preview'), 'classes': ('collapse',)}),
    ]
    @admin.display(description='Video')
    def video_status(self, obj):
        if obj.has_video:
            return format_html('<span style="color:green;font-weight:bold;">Yes ({})</span>', obj.get_video_type_display())
        return format_html('<span style="color:#bbb;">No video</span>')
    @admin.display(description='Resource Link')
    def resource_status(self, obj):
        if obj.has_resource_link:
            return format_html('<a href="{}" target="_blank" style="color:#1A56DB;font-size:12px;">Open</a>', obj.resource_link)
        return format_html('<span style="color:#bbb;">-</span>')
    @admin.display(description='Lessons')
    def lesson_count(self, obj):
        return obj.lessons.count()
    def video_preview(self, obj):
        return _video_preview_html(obj)
    video_preview.short_description = 'Video Preview'
    def resource_link_preview(self, obj):
        return _link_preview_html(obj.resource_link, obj.resource_link_label)
    resource_link_preview.short_description = 'Link Preview'
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if _has_role(request, ['MENTOR']):
            return qs.filter(course__trainer=request.user)
        return qs
    def has_view_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])
    def has_add_permission(self, request):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])
    def has_change_permission(self, request, obj=None):
        if _has_role(request, ['MENTOR']) and obj is not None:
            return obj.course.trainer == request.user
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])
    def has_delete_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'order', 'duration', 'is_free', 'video_type', 'allow_download']
    list_filter = ['is_free', 'video_type', 'allow_download', 'module__course']
    search_fields = ['title', 'module__title', 'module__course__title']
    ordering = ['module__course', 'module__order', 'order']
    list_editable = ['is_free', 'allow_download', 'order']
    readonly_fields = ['video_preview']
    fieldsets = (
        ('Lesson Info', {'fields': ('module', 'title', 'order', 'duration', 'is_free', 'allow_download')}),
        ('Video', {'fields': ('video_type', 'video_file', 'video_url', 'video_preview')}),
    )
    def video_preview(self, obj):
        return _video_preview_html(obj)
    video_preview.short_description = 'Video Preview'
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if _has_role(request, ['MENTOR']):
            return qs.filter(module__course__trainer=request.user)
        return qs
    def has_view_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])
    def has_add_permission(self, request):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])
    def has_change_permission(self, request, obj=None):
        if _has_role(request, ['MENTOR']) and obj is not None:
            return obj.module.course.trainer == request.user
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])
    def has_delete_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'payment_status', 'progress_bar', 'completed', 'enrolled_at']
    list_filter = ['payment_status', 'completed', 'course__category']
    search_fields = ['student__email', 'course__title']
    ordering = ['-enrolled_at']
    list_per_page = 25
    readonly_fields = ['enrolled_at', 'progress_display']
    fieldsets = (
        ('Enrollment Info', {'fields': ('student', 'course', 'payment_status', 'is_active', 'enrolled_at')}),
        ('Progress', {'fields': ('progress_percentage', 'completed_lessons', 'completed', 'progress_display')}),
    )
    @admin.display(description='Progress')
    def progress_bar(self, obj):
        pct = obj.progress_percentage
        color = '#1A7A4A' if pct >= 80 else '#E6A817' if pct >= 40 else '#C0392B'
        return mark_safe(f'<div style="display:flex;align-items:center;gap:8px;"><div style="width:80px;height:8px;background:#eee;border-radius:4px;overflow:hidden;"><div style="width:{pct}%;height:100%;background:{color};border-radius:4px;"></div></div><span style="font-size:11px;font-weight:700;color:{color};">{pct}%</span></div>')
    @admin.display(description='Progress %')
    def progress_display(self, obj):
        return f'{obj.progress_percentage}%'
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if _has_role(request, ['MENTOR']):
            # Mentor sees enrollments for their own courses only
            return qs.filter(course__trainer=request.user)
        return qs
    def has_view_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN', 'MENTOR'])
    def has_add_permission(self, request):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])
    def has_change_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])
    def has_delete_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN'])

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'rating_stars', 'created_at']
    list_filter = ['rating', 'course']
    search_fields = ['student__email', 'course__title', 'comment']
    ordering = ['-created_at']
    @admin.display(description='Rating')
    def rating_stars(self, obj):
        stars = '*' * obj.rating + '-' * (5 - obj.rating)
        color = '#E6A817' if obj.rating >= 4 else '#C0392B'
        return format_html('<span style="color:{};font-size:15px;">{}</span>', color, stars)
    def has_view_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])
    def has_add_permission(self, request):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])
    def has_change_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])
    def has_delete_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN'])

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'is_completed', 'last_position', 'completed_at']
    list_filter = ['is_completed', 'enrollment__course']
    search_fields = ['enrollment__student__email', 'lesson__title']
    readonly_fields = ['enrollment', 'lesson', 'is_completed', 'completed_at', 'last_position']
    ordering = ['-completed_at']
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN'])
    def has_view_permission(self, request, obj=None):
        return _has_role(request, ['SUPER_ADMIN', 'ADMIN'])
    def has_change_permission(self, request, obj=None):
        return False