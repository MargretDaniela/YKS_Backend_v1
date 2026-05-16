
from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from .models import (
    HomeBanner, HomeFeaturedCourse, HomeSection,
    CourseCategory, InfoPage, SiteSettings,
)


# =====================================================================
# Shared helpers
# =====================================================================

def _img(obj, field="image", size=56):
    img = getattr(obj, field, None)
    if img:
        return mark_safe(
            f'<img src="{img.url}" style="height:{size}px;border-radius:6px;'
            f'object-fit:cover;box-shadow:0 2px 6px rgba(0,0,0,0.15);"/>'
        )
    return mark_safe(
        f'<div style="width:{size}px;height:{size}px;background:#F0F4F8;'
        f'border-radius:6px;display:flex;align-items:center;'
        f'justify-content:center;color:#aaa;font-size:10px;">None</div>'
    )

def _active(obj):
    if obj.is_active:
        return mark_safe(
            '<span style="background:#E8F5EE;color:#1A7A4A;padding:3px 10px;'
            'border-radius:20px;font-size:11px;font-weight:700;">● Active</span>'
        )
    return mark_safe(
        '<span style="background:#FDECEA;color:#C0392B;padding:3px 10px;'
        'border-radius:20px;font-size:11px;font-weight:700;">● Inactive</span>'
    )

def _actions(obj):
    app  = obj._meta.app_label
    name = obj._meta.model_name
    edit_url   = reverse(f"admin:{app}_{name}_change", args=[obj.pk])
    delete_url = reverse(f"admin:{app}_{name}_delete", args=[obj.pk])
    return format_html(
        '<div style="display:flex;gap:4px;">'
        '<a href="{}" style="display:inline-flex;align-items:center;justify-content:center;'
        'width:30px;height:30px;border-radius:6px;background:#E8F5EE;color:#1A7A4A;'
        'border:1px solid #1A7A4A;text-decoration:none;font-size:13px;">'
        '<i class="fas fa-pen"></i></a>'
        '<a href="{}" style="display:inline-flex;align-items:center;justify-content:center;'
        'width:30px;height:30px;border-radius:6px;background:#FDECEA;color:#C0392B;'
        'border:1px solid #C0392B;text-decoration:none;font-size:13px;"'
        ' onclick="return confirm(\'Delete?\');">'
        '<i class="fas fa-trash"></i></a>'
        '</div>',
        edit_url, delete_url
    )

def _section_header(title, icon):
    return mark_safe(
        f'<div style="display:flex;align-items:center;gap:10px;'
        f'margin:28px 0 14px 0;padding-bottom:10px;'
        f'border-bottom:2px solid #E8ECF0;">'
        f'<span style="font-size:20px;">{icon}</span>'
        f'<span style="font-size:16px;font-weight:900;color:#001A35;'
        f'text-transform:uppercase;letter-spacing:0.5px;">{title}</span>'
        f'</div>'
    )

def _nav_card(title, desc, url, add_url=None, count=None):
    count_badge = ''
    if count is not None:
        count_badge = (
            f'<span style="background:#001A35;color:#AC7D0C;font-size:11px;'
            f'font-weight:700;padding:2px 10px;border-radius:20px;'
            f'margin-left:8px;">{count}</span>'
        )
    view_btn = format_html(
        '<a href="{}" style="font-size:11px;font-weight:600;background:#001A35;'
        'color:#AC7D0C;padding:6px 16px;border-radius:20px;text-decoration:none;'
        'border:1px solid #AC7D0C;white-space:nowrap;">View / Manage</a>',
        url
    )
    add_btn = mark_safe('')
    if add_url:
        add_btn = format_html(
            '<a href="{}" style="font-size:11px;font-weight:600;background:#F0F4F8;'
            'color:#001A35;padding:6px 16px;border-radius:20px;text-decoration:none;'
            'border:1px solid #E0E6ED;white-space:nowrap;">+ Add New</a>',
            add_url
        )
    return format_html(
        '<div style="background:#fff;border:1.5px solid #E8ECF0;border-radius:14px;'
        'padding:16px 20px;margin-bottom:12px;">'
        '<div style="display:flex;align-items:center;justify-content:space-between;'
        'flex-wrap:wrap;gap:10px;">'
        '<div>'
        '<p style="font-size:14px;font-weight:800;color:#001A35;margin:0 0 3px 0;">'
        '{}{}</p>'
        '<p style="font-size:12px;color:#999;margin:0;">{}</p>'
        '</div>'
        '<div style="display:flex;gap:8px;align-items:center;">{}{}</div>'
        '</div></div>',
        title, mark_safe(count_badge), desc, view_btn, add_btn
    )


# =====================================================================
# MAIN DASHBOARD PROXY
# =====================================================================

class MainDashboard(SiteSettings):
    class Meta:
        proxy               = True
        verbose_name        = "Main Dashboard"
        verbose_name_plural = "🏠  Main Dashboard"


@admin.register(MainDashboard)
class MainDashboardAdmin(admin.ModelAdmin):
    readonly_fields = ["main_dashboard_display"]

    def main_dashboard_display(self, obj=None):
        try:
            from courses.models import Course, Enrollment
            courses_count     = Course.objects.count()
            enrollments_count = Enrollment.objects.count()
        except Exception:
            courses_count = enrollments_count = 0

        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            users_count = User.objects.count()
        except Exception:
            users_count = 0

        try:
            from attendance.models import Attendance
            attendance_count = Attendance.objects.count()
        except Exception:
            attendance_count = 0

        try:
            from mentorship.models import MentorshipSession
            sessions_count = MentorshipSession.objects.count()
        except Exception:
            sessions_count = 0

        # Pages Dashboard button
        pages_btn = mark_safe(
            '<a href="/admin/pages/pagesdashboard/1/change/" '
            'style="display:inline-flex;align-items:center;gap:10px;'
            'background:linear-gradient(135deg,#001A35,#003166);'
            'color:#AC7D0C;padding:14px 28px;border-radius:16px;'
            'text-decoration:none;font-weight:800;font-size:15px;'
            'border:1.5px solid #AC7D0C;letter-spacing:0.3px;'
            'box-shadow:0 4px 16px rgba(0,26,53,0.18);">'
            '<i class="fas fa-layer-group" style="font-size:18px;"></i>'
            '&nbsp; Open Pages Dashboard'
            '</a>'
        )

        stats = format_html(
            '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:28px;">'
            '<div style="background:#fff;border:1.5px solid #E8ECF0;border-radius:12px;padding:14px 22px;min-width:110px;">'
            '<div style="font-size:26px;font-weight:900;color:#001A35;">{}</div>'
            '<div style="font-size:10px;color:#999;font-weight:700;text-transform:uppercase;">Users</div></div>'
            '<div style="background:#fff;border:1.5px solid #E8ECF0;border-radius:12px;padding:14px 22px;min-width:110px;">'
            '<div style="font-size:26px;font-weight:900;color:#001A35;">{}</div>'
            '<div style="font-size:10px;color:#999;font-weight:700;text-transform:uppercase;">Courses</div></div>'
            '<div style="background:#fff;border:1.5px solid #E8ECF0;border-radius:12px;padding:14px 22px;min-width:110px;">'
            '<div style="font-size:26px;font-weight:900;color:#001A35;">{}</div>'
            '<div style="font-size:10px;color:#999;font-weight:700;text-transform:uppercase;">Enrollments</div></div>'
            '<div style="background:#fff;border:1.5px solid #E8ECF0;border-radius:12px;padding:14px 22px;min-width:110px;">'
            '<div style="font-size:26px;font-weight:900;color:#001A35;">{}</div>'
            '<div style="font-size:10px;color:#999;font-weight:700;text-transform:uppercase;">Sessions</div></div>'
            '<div style="background:#fff;border:1.5px solid #E8ECF0;border-radius:12px;padding:14px 22px;min-width:110px;">'
            '<div style="font-size:26px;font-weight:900;color:#001A35;">{}</div>'
            '<div style="font-size:10px;color:#999;font-weight:700;text-transform:uppercase;">Attendance</div></div>'
            '</div>',
            users_count, courses_count, enrollments_count, sessions_count, attendance_count,
        )

        return mark_safe(
            '<div style="max-width:900px;">'
            '<div style="margin-bottom:28px;">' + str(pages_btn) + '</div>'
            + str(stats)
            + '</div>'
        )

    main_dashboard_display.short_description = ""
    fieldsets = (("", {"fields": ("main_dashboard_display",)}),)

    def get_object(self, request, object_id, from_field=None):
        return SiteSettings.get()

    def changelist_view(self, request, extra_context=None):
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect("/admin/pages/maindashboard/1/change/")

    def has_add_permission(self, request):              return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return True
    def has_view_permission(self, request, obj=None):   return True
    def get_queryset(self, request):
        return super().get_queryset(request).filter(pk=1)


# =====================================================================
# PAGES DASHBOARD PROXY
# =====================================================================

class PagesDashboard(SiteSettings):
    class Meta:
        proxy               = True
        verbose_name        = "Pages Dashboard"
        verbose_name_plural = "📋  Pages Dashboard"


@admin.register(PagesDashboard)
class PagesDashboardAdmin(admin.ModelAdmin):
    readonly_fields = ["pages_dashboard_display"]

    def pages_dashboard_display(self, obj=None):

        # Back button
        back_btn = mark_safe(
            '<a href="/admin/pages/maindashboard/1/change/" '
            'style="display:inline-flex;align-items:center;gap:8px;'
            'margin-bottom:28px;background:#F0F4F8;color:#001A35;'
            'padding:9px 20px;border-radius:24px;text-decoration:none;'
            'font-weight:700;font-size:13px;border:1.5px solid #E0E6ED;">'
            '<i class="fas fa-arrow-left"></i>&nbsp; Back to Main Dashboard'
            '</a>'
        )

        banners  = HomeBanner.objects.count()
        cats     = CourseCategory.objects.count()
        pages    = InfoPage.objects.count()
        settings = SiteSettings.objects.count()

        try:
            from courses.models import Course, Enrollment
            courses_count     = Course.objects.count()
            enrollments_count = Enrollment.objects.count()
        except Exception:
            courses_count = enrollments_count = 0

        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            users_count = User.objects.count()
        except Exception:
            users_count = 0

        try:
            from attendance.models import Attendance
            attendance_count = Attendance.objects.count()
        except Exception:
            attendance_count = 0

        try:
            from mentorship.models import MentorshipSession
            sessions_count = MentorshipSession.objects.count()
        except Exception:
            sessions_count = 0

        stats = format_html(
            '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:28px;">'
            '<div style="background:#fff;border:1.5px solid #E8ECF0;border-radius:12px;padding:14px 22px;min-width:100px;">'
            '<div style="font-size:26px;font-weight:900;color:#001A35;">{}</div>'
            '<div style="font-size:10px;color:#999;font-weight:700;text-transform:uppercase;">Banners</div></div>'
            '<div style="background:#fff;border:1.5px solid #E8ECF0;border-radius:12px;padding:14px 22px;min-width:100px;">'
            '<div style="font-size:26px;font-weight:900;color:#001A35;">{}</div>'
            '<div style="font-size:10px;color:#999;font-weight:700;text-transform:uppercase;">Categories</div></div>'
            '<div style="background:#fff;border:1.5px solid #E8ECF0;border-radius:12px;padding:14px 22px;min-width:100px;">'
            '<div style="font-size:26px;font-weight:900;color:#001A35;">{}</div>'
            '<div style="font-size:10px;color:#999;font-weight:700;text-transform:uppercase;">Courses</div></div>'
            '<div style="background:#fff;border:1.5px solid #E8ECF0;border-radius:12px;padding:14px 22px;min-width:100px;">'
            '<div style="font-size:26px;font-weight:900;color:#001A35;">{}</div>'
            '<div style="font-size:10px;color:#999;font-weight:700;text-transform:uppercase;">Enrollments</div></div>'
            '<div style="background:#fff;border:1.5px solid #E8ECF0;border-radius:12px;padding:14px 22px;min-width:100px;">'
            '<div style="font-size:26px;font-weight:900;color:#001A35;">{}</div>'
            '<div style="font-size:10px;color:#999;font-weight:700;text-transform:uppercase;">Users</div></div>'
            '<div style="background:#fff;border:1.5px solid #E8ECF0;border-radius:12px;padding:14px 22px;min-width:100px;">'
            '<div style="font-size:26px;font-weight:900;color:#001A35;">{}</div>'
            '<div style="font-size:10px;color:#999;font-weight:700;text-transform:uppercase;">Sessions</div></div>'
            '<div style="background:#fff;border:1.5px solid #E8ECF0;border-radius:12px;padding:14px 22px;min-width:100px;">'
            '<div style="font-size:26px;font-weight:900;color:{};">{}</div>'
            '<div style="font-size:10px;color:#999;font-weight:700;text-transform:uppercase;">Settings</div></div>'
            '</div>',
            banners, cats, courses_count, enrollments_count, users_count, sessions_count,
            "#1A7A4A" if settings else "#E65100",
            "✓ Set" if settings else "⚠ Missing",
        )

        home_section = (
            str(_section_header("Home Screen", "🏠")) +
            str(_nav_card("Banners",          "Hero banners on the app home screen",           "/admin/pages/homebanner/",              "/admin/pages/homebanner/add/",              banners)) +
            str(_nav_card("Featured Courses", "Courses pinned to the home screen",             "/admin/pages/homefeaturedcourse/",      "/admin/pages/homefeaturedcourse/add/",      None)) +
            str(_nav_card("Home Sections",    "Custom sections on home screen",                "/admin/pages/homesection/",             "/admin/pages/homesection/add/",             None))
        )

        courses_section = (
            str(_section_header("Courses", "🎓")) +
            str(_nav_card("All Courses",      "Manage all courses on the platform",            "/admin/courses/course/",                "/admin/courses/course/add/",                courses_count)) +
            str(_nav_card("Categories",       "Course categories shown in the app",            "/admin/pages/coursecategory/",          "/admin/pages/coursecategory/add/",          cats)) +
            str(_nav_card("Enrollments",      "View and manage student enrollments",           "/admin/courses/enrollment/",            None,                                        enrollments_count))
        )

        accounts_section = (
            str(_section_header("Accounts", "👤")) +
            str(_nav_card("All Users",        "View and manage all registered users",          "/admin/accounts/user/",                 "/admin/accounts/user/add/",                 users_count)) +
            str(_nav_card("Mentor Users",     "Manage mentor accounts",                        "/admin/accounts/mentoruser/",           "/admin/accounts/mentoruser/add/",           None)) +
            str(_nav_card("Student Users",    "Manage student accounts",                       "/admin/accounts/studentuser/",          "/admin/accounts/studentuser/add/",          None))
        )

        attendance_section = (
            str(_section_header("Attendance", "📅")) +
            str(_nav_card("Attendance Records", "Track student attendance",                    "/admin/attendance/attendance/",         "/admin/attendance/attendance/add/",         attendance_count))
        )

        sessions_section = (
            str(_section_header("Mentorship Sessions", "🧑‍🏫")) +
            str(_nav_card("Sessions",         "View and manage mentorship sessions",           "/admin/mentorship/mentorshipsession/",  "/admin/mentorship/mentorshipsession/add/",  sessions_count)) +
            str(_nav_card("Bookings",         "Manage session bookings",                       "/admin/mentorship/booking/",            "/admin/mentorship/booking/add/",            None))
        )

        info_section = (
            str(_section_header("Info Pages", "📄")) +
            str(_nav_card("About Us",          "About Us page content",                        "/admin/pages/infopage/?page_type=about",    "/admin/pages/infopage/add/", None)) +
            str(_nav_card("Terms & Conditions","Terms & Conditions page",                      "/admin/pages/infopage/?page_type=terms",    "/admin/pages/infopage/add/", None)) +
            str(_nav_card("Privacy Policy",    "Privacy Policy page",                          "/admin/pages/infopage/?page_type=privacy",  "/admin/pages/infopage/add/", None)) +
            str(_nav_card("FAQ",               "Frequently Asked Questions",                   "/admin/pages/infopage/?page_type=faq",      "/admin/pages/infopage/add/", None)) +
            str(_nav_card("Contact Us",        "Contact Us page",                              "/admin/pages/infopage/?page_type=contact",  "/admin/pages/infopage/add/", None)) +
            str(_nav_card("All Info Pages",    "View all info pages",                          "/admin/pages/infopage/",                    None,                         pages))
        )

        settings_section = (
            str(_section_header("Site Settings", "⚙️")) +
            str(_nav_card("App Settings",      "App name, logo, social links, support info",  "/admin/pages/sitesettings/",            None,                                        None))
        )

        return mark_safe(
            '<div style="max-width:920px;">'
            + str(back_btn)
            + str(stats)
            + home_section
            + courses_section
            + accounts_section
            + attendance_section
            + sessions_section
            + info_section
            + settings_section
            + '</div>'
        )

    pages_dashboard_display.short_description = ""
    fieldsets = (("", {"fields": ("pages_dashboard_display",)}),)

    def get_object(self, request, object_id, from_field=None):
        return SiteSettings.get()

    def changelist_view(self, request, extra_context=None):
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect("/admin/pages/pagesdashboard/1/change/")

    def has_add_permission(self, request):              return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return True
    def has_view_permission(self, request, obj=None):   return True
    def get_queryset(self, request):
        return super().get_queryset(request).filter(pk=1)


# =====================================================================
# HOME SCREEN models
# =====================================================================

@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display       = ["order", "title", "preview", "status", "button_text", "actions_col"]
    list_display_links = ["title"]
    list_editable      = ["order"]
    list_filter        = ["is_active"]
    search_fields      = ["title", "subtitle"]
    ordering           = ["order"]
    fieldsets = (
        ("Content",        {"fields": ("title", "subtitle", "image", "order")}),
        ("Call to Action", {"fields": ("button_text", "button_link")}),
        ("Visibility",     {"fields": ("is_active",)}),
    )
    def preview(self, obj):       return _img(obj)
    preview.short_description     = "Image"
    def status(self, obj):        return _active(obj)
    status.short_description      = "Status"
    def actions_col(self, obj):   return _actions(obj)
    actions_col.short_description = "Actions"


@admin.register(HomeFeaturedCourse)
class HomeFeaturedCourseAdmin(admin.ModelAdmin):
    list_display        = ["order", "course", "label", "status", "actions_col"]
    list_display_links  = ["course"]
    list_editable       = ["order", "label"]
    list_filter         = ["is_active"]
    ordering            = ["order"]
    autocomplete_fields = ["course"]
    def status(self, obj):        return _active(obj)
    status.short_description      = "Status"
    def actions_col(self, obj):   return _actions(obj)
    actions_col.short_description = "Actions"


@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display       = ["order", "title", "subtitle", "status", "actions_col"]
    list_display_links = ["title"]
    list_editable      = ["order"]
    list_filter        = ["is_active"]
    ordering           = ["order"]
    def status(self, obj):        return _active(obj)
    status.short_description      = "Status"
    def actions_col(self, obj):   return _actions(obj)
    actions_col.short_description = "Actions"


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display       = ["order", "name", "preview", "status", "actions_col"]
    list_display_links = ["name"]
    list_editable      = ["order"]
    list_filter        = ["is_active"]
    search_fields      = ["name"]
    ordering           = ["order"]
    fieldsets = (
        ("Category Info", {"fields": ("name", "description", "order")}),
        ("Appearance",    {"fields": ("icon", "image")}),
        ("Visibility",    {"fields": ("is_active",)}),
    )
    def preview(self, obj):       return _img(obj)
    preview.short_description     = "Image"
    def status(self, obj):        return _active(obj)
    status.short_description      = "Status"
    def actions_col(self, obj):   return _actions(obj)
    actions_col.short_description = "Actions"


@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display        = ["title", "page_type", "slug", "preview", "status", "updated_at", "actions_col"]
    list_filter         = ["is_active", "page_type"]
    search_fields       = ["title", "slug", "body"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields     = ["updated_at"]
    fieldsets = (
        ("Page Info",  {"fields": ("title", "slug", "page_type")}),
        ("Content",    {"fields": ("body", "image")}),
        ("Visibility", {"fields": ("is_active", "updated_at")}),
    )
    def preview(self, obj):       return _img(obj)
    preview.short_description     = "Image"
    def status(self, obj):        return _active(obj)
    status.short_description      = "Status"
    def actions_col(self, obj):   return _actions(obj)
    actions_col.short_description = "Actions"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("App Identity", {"fields": ("app_name", "tagline", "logo")}),
        ("Support",      {"fields": ("support_email", "support_phone")}),
        ("Social Media", {"fields": ("facebook_url", "twitter_url", "instagram_url", "whatsapp_number")}),
        ("Maintenance",  {"fields": ("maintenance_mode", "maintenance_message"), "classes": ("collapse",)}),
    )
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False