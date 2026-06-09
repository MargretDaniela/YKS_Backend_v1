# mentorship/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import MentorshipSession, Booking, MentorshipVideo


def _role(request):
    return getattr(request.user, 'role', None)


# ======================================================================
#  BOOKING INLINE  (read-only inside MentorshipSession)
# ======================================================================
class BookingInline(admin.TabularInline):
    model           = Booking
    extra           = 0
    readonly_fields = ['session', 'payment_status', 'access_code']
    can_delete      = False

    def has_add_permission(self, request, obj=None):
        return False   # nobody creates bookings from admin — students do it


# ======================================================================
#  MENTORSHIP SESSION ADMIN
# ======================================================================
@admin.register(MentorshipSession)
class MentorshipSessionAdmin(admin.ModelAdmin):
    list_display  = [
        'mentor', 'student', 'session_type_badge',
        'date', 'time', 'status_badge', 'meeting_link_display',
    ]
    list_filter   = ['status', 'session_type', 'date']
    search_fields = ['mentor__full_name', 'mentor__email',
                     'student__full_name', 'student__email']
    ordering      = ['-date', '-time']
    list_per_page = 25
    inlines       = [BookingInline]

    fieldsets = (
        ('Session Details', {
            'fields': ('mentor', 'student', 'session_type', 'date', 'time'),
        }),
        ('Status & Meeting', {
            'fields': ('status', 'meeting_link', 'notes'),
        }),
    )

    # ── Display helpers ──────────────────────────────────────────────
    @admin.display(description='Type')
    def session_type_badge(self, obj):
        color = '#1A56DB' if obj.session_type == 'ONE_ON_ONE' else '#7C5CFC'
        label = obj.get_session_type_display()
        return format_html(
            '<span style="background:{0}22;color:{0};padding:3px 10px;'
            'border-radius:20px;font-size:11px;font-weight:700;">{1}</span>',
            color, label,
        )

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'PENDING':   '#E6A817',
            'APPROVED':  '#1A7A4A',
            'COMPLETED': '#1A56DB',
            'CANCELLED': '#C0392B',
        }
        color = colors.get(obj.status, '#888')
        return format_html(
            '<span style="background:{0}22;color:{0};padding:3px 10px;'
            'border-radius:20px;font-size:11px;font-weight:700;">{1}</span>',
            color, obj.get_status_display(),
        )

    @admin.display(description='Meeting Link')
    def meeting_link_display(self, obj):
        if obj.meeting_link:
            return format_html(
                '<a href="{}" target="_blank" '
                'style="color:#1A56DB;font-size:12px;">Open Link</a>',
                obj.meeting_link,
            )
        return mark_safe('<span style="color:#bbb;">—</span>')

    # ── Permissions ──────────────────────────────────────────────────
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if _role(request) == 'MENTOR':
            return qs.filter(mentor=request.user)
        return qs

    def has_view_permission(self, request, obj=None):
        return _role(request) in ['SUPER_ADMIN', 'ADMIN', 'MENTOR']

    def has_add_permission(self, request):
        # Mentors cannot create sessions — students request them
        return _role(request) in ['SUPER_ADMIN', 'ADMIN']

    def has_change_permission(self, request, obj=None):
        if _role(request) == 'MENTOR':
            # Mentor can only update status/meeting link on their own sessions
            if obj is not None:
                return obj.mentor == request.user
            return True
        return _role(request) in ['SUPER_ADMIN', 'ADMIN']

    def has_delete_permission(self, request, obj=None):
        return _role(request) in ['SUPER_ADMIN', 'ADMIN']

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if _role(request) == 'MENTOR':
            # Mentors cannot reassign mentor/student — only manage status & link
            return [f for f in fields if f not in ['mentor', 'student', 'session_type']]
        return fields

    def get_readonly_fields(self, request, obj=None):
        if _role(request) == 'MENTOR':
            return ['mentor', 'student', 'session_type', 'date', 'time']
        return []


# ======================================================================
#  BOOKING ADMIN  (view-only for mentors)
# ======================================================================
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['session', 'payment_status', 'access_code']
    list_filter   = ['payment_status']
    search_fields = ['session__mentor__full_name', 'session__student__full_name']
    ordering      = ['session__date']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if _role(request) == 'MENTOR':
            return qs.filter(session__mentor=request.user)
        return qs

    def has_view_permission(self, request, obj=None):
        return _role(request) in ['SUPER_ADMIN', 'ADMIN', 'MENTOR']

    # Mentors cannot create or edit bookings — students do that
    def has_add_permission(self, request):
        return _role(request) in ['SUPER_ADMIN', 'ADMIN']

    def has_change_permission(self, request, obj=None):
        return _role(request) in ['SUPER_ADMIN', 'ADMIN']

    def has_delete_permission(self, request, obj=None):
        return _role(request) in ['SUPER_ADMIN', 'ADMIN']


# ======================================================================
#  MENTORSHIP VIDEO ADMIN
# ======================================================================
@admin.register(MentorshipVideo)
class MentorshipVideoAdmin(admin.ModelAdmin):
    list_display  = ['title', 'mentor', 'category', 'is_active', 'created_at',
                     'video_link_display']
    list_filter   = ['is_active', 'category']
    search_fields = ['title', 'mentor__full_name', 'mentor__email']
    ordering      = ['-created_at']
    list_editable = ['is_active']

    fieldsets = (
        ('Video Info', {
            'fields': ('mentor', 'title', 'description', 'category', 'is_active'),
        }),
        ('Video Link', {
            'fields': ('video_url',),
        }),
    )

    @admin.display(description='Video')
    def video_link_display(self, obj):
        if obj.video_url:
            return format_html(
                '<a href="{}" target="_blank" style="color:#1A56DB;">Watch</a>',
                obj.video_url,
            )
        return '—'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if _role(request) == 'MENTOR':
            return qs.filter(mentor=request.user)
        return qs

    def has_view_permission(self, request, obj=None):
        return _role(request) in ['SUPER_ADMIN', 'ADMIN', 'MENTOR']

    def has_add_permission(self, request):
        return _role(request) in ['SUPER_ADMIN', 'ADMIN', 'MENTOR']

    def has_change_permission(self, request, obj=None):
        if _role(request) == 'MENTOR' and obj is not None:
            return obj.mentor == request.user
        return _role(request) in ['SUPER_ADMIN', 'ADMIN', 'MENTOR']

    def has_delete_permission(self, request, obj=None):
        return _role(request) in ['SUPER_ADMIN', 'ADMIN']