# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.utils.html import format_html
# from django.urls import reverse
# from django.utils.safestring import mark_safe
# from .models import User


# # =====================================================================
# # PROXY MODELS
# # =====================================================================

# class AdminUser(User):
#     class Meta:
#         proxy               = True
#         verbose_name        = "Admin"
#         verbose_name_plural = "Admins"

# class MentorUser(User):
#     class Meta:
#         proxy               = True
#         verbose_name        = "Mentor"
#         verbose_name_plural = "Mentors"

# class StudentUser(User):
#     class Meta:
#         proxy               = True
#         verbose_name        = "Student"
#         verbose_name_plural = "Students"


# # =====================================================================
# # BASE ADMIN
# # =====================================================================

# class BaseUserAdmin(UserAdmin):

#     def role_badge(self, obj):
#         colors = {
#             "SUPER_ADMIN": ("#001A35", "#D4A017", "Super Admin"),
#             "ADMIN":       ("#002147", "#6EA8FE", "Admin"),
#             "MENTOR":      ("#1A3A1A", "#6FCF97", "Mentor"),
#             "STUDENT":     ("#1A1A3A", "#A78BFA", "Student"),
#         }
#         bg, color, label = colors.get(obj.role, ("#333", "#fff", obj.role))
#         return format_html(
#             '<span style="background:{};color:{};padding:3px 12px;'
#             'border-radius:20px;font-size:11px;font-weight:700;'
#             'letter-spacing:0.5px;text-transform:uppercase;">{}</span>',
#             bg, color, label
#         )
#     role_badge.short_description = "Role"
#     role_badge.admin_order_field = "role"

#     def status_badge(self, obj):
#         if obj.is_active:
#             return mark_safe(
#                 '<span style="background:#E8F5EE;color:#1A7A4A;'
#                 'padding:3px 10px;border-radius:20px;'
#                 'font-size:11px;font-weight:700;">Active</span>'
#             )
#         return mark_safe(
#             '<span style="background:#FDECEA;color:#C0392B;'
#             'padding:3px 10px;border-radius:20px;'
#             'font-size:11px;font-weight:700;">Inactive</span>'
#         )
#     status_badge.short_description = "Status"
#     status_badge.admin_order_field = "is_active"

#     def action_buttons(self, obj):
#         app        = obj._meta.app_label
#         name       = obj._meta.model_name
#         view_url   = reverse("admin:%s_%s_change" % (app, name), args=[obj.pk])
#         delete_url = reverse("admin:%s_%s_delete" % (app, name), args=[obj.pk])
#         return format_html(
#             '<div style="display:flex;gap:4px;align-items:center;">'
#             '<a href="{0}" title="View" style="'
#             'display:inline-flex;align-items:center;justify-content:center;'
#             'width:30px;height:30px;border-radius:6px;'
#             'background:#E8F0FE;color:#1A56DB;border:1px solid #1A56DB;'
#             'text-decoration:none;font-size:13px;">'
#             '<i class="fas fa-eye"></i></a>'
#             '<a href="{0}" title="Edit" style="'
#             'display:inline-flex;align-items:center;justify-content:center;'
#             'width:30px;height:30px;border-radius:6px;'
#             'background:#E8F5EE;color:#1A7A4A;border:1px solid #1A7A4A;'
#             'text-decoration:none;font-size:13px;">'
#             '<i class="fas fa-pen"></i></a>'
#             '<a href="{1}" title="Delete" style="'
#             'display:inline-flex;align-items:center;justify-content:center;'
#             'width:30px;height:30px;border-radius:6px;'
#             'background:#FDECEA;color:#C0392B;border:1px solid #C0392B;'
#             'text-decoration:none;font-size:13px;" '
#             'onclick="return confirm(\'Delete this user?\');">'
#             '<i class="fas fa-trash"></i></a>'
#             '</div>',
#             view_url, delete_url
#         )
#     action_buttons.short_description = "Actions"

#     def password_display(self, obj):
#         return mark_safe('''
#             <div style="display:flex;align-items:center;gap:10px;max-width:420px;">
#                 <input
#                     id="pwd_display_{pk}"
#                     type="password"
#                     value="{pwd}"
#                     readonly
#                     style="flex:1;padding:8px 12px;border:1px solid #ddd;
#                            border-radius:6px;font-family:monospace;font-size:13px;
#                            background:#f8f8f8;color:#333;outline:none;"
#                 />
#                 <button
#                     type="button"
#                     onclick="
#                         var f = document.getElementById('pwd_display_{pk}');
#                         var i = document.getElementById('eye_icon_{pk}');
#                         if (f.type === 'password') {{
#                             f.type = 'text';
#                             i.className = 'fas fa-eye-slash';
#                         }} else {{
#                             f.type = 'password';
#                             i.className = 'fas fa-eye';
#                         }}
#                     "
#                     style="padding:8px 12px;border:1px solid #1A56DB;border-radius:6px;
#                            background:#E8F0FE;color:#1A56DB;cursor:pointer;
#                            font-size:14px;display:flex;align-items:center;gap:6px;"
#                     title="Show / Hide password"
#                 >
#                     <i id="eye_icon_{pk}" class="fas fa-eye"></i>
#                 </button>
#             </div>
#             <p style="margin-top:6px;font-size:11px;color:#888;">
#                 This is the hashed password stored in the database.
#                 To change it use the
#                 <a href="password/">password change form</a>.
#             </p>
#         '''.format(pk=obj.pk, pwd=obj.password))
#     password_display.short_description = "Password"

#     list_display   = ["full_name", "email", "role_badge", "status_badge", "date_joined", "action_buttons"]
#     list_filter    = ["is_active", "date_joined"]
#     search_fields  = ["email", "full_name"]
#     ordering       = ["-date_joined"]
#     list_per_page  = 20
#     date_hierarchy = "date_joined"

#     fieldsets = (
#         ("Login Credentials",    {"fields": ("email", "password_display")}),
#         ("Personal Information", {"fields": ("full_name",)}),
#         ("Role and Access",      {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
#         ("Important Dates",      {"fields": ("date_joined", "last_login"), "classes": ("collapse",)}),
#     )
#     readonly_fields = ["date_joined", "last_login", "password_display"]

#     add_fieldsets = (
#         ("Create New User", {
#             "classes": ("wide",),
#             "fields":  ("full_name", "email", "role", "password1", "password2", "is_active"),
#         }),
#     )

#     actions = ["activate_users", "deactivate_users"]

#     def activate_users(self, request, queryset):
#         updated = queryset.update(is_active=True)
#         self.message_user(request, "%d user(s) activated." % updated)
#     activate_users.short_description = "Activate selected users"

#     def deactivate_users(self, request, queryset):
#         updated = queryset.update(is_active=False)
#         self.message_user(request, "%d user(s) deactivated." % updated)
#     deactivate_users.short_description = "Deactivate selected users"

#     def get_form(self, request, obj=None, **kwargs):
#         kwargs.setdefault('exclude', [])
#         if isinstance(kwargs['exclude'], tuple):
#             kwargs['exclude'] = list(kwargs['exclude'])
#         if 'password' not in kwargs['exclude']:
#             kwargs['exclude'].append('password')
#         return super().get_form(request, obj, **kwargs)


# # =====================================================================
# # MAIN USER ADMIN
# # =====================================================================

# @admin.register(User)
# class CustomUserAdmin(BaseUserAdmin):

#     list_display = ["full_name", "email", "role_badge", "status_badge", "date_joined", "action_buttons"]
#     list_filter  = ["role", "is_active", "date_joined"]
#     actions      = BaseUserAdmin.actions + ["make_mentor", "make_admin"]

#     def make_mentor(self, request, queryset):
#         for user in queryset:
#             user.role = "MENTOR"
#             user.save()
#         self.message_user(request, "%d user(s) set as Mentor." % queryset.count())
#     make_mentor.short_description = "Set selected as Mentor"

#     def make_admin(self, request, queryset):
#         for user in queryset:
#             user.role = "ADMIN"
#             user.save()
#         self.message_user(request, "%d user(s) set as Admin." % queryset.count())
#     make_admin.short_description = "Set selected as Admin"

#     def get_queryset(self, request):
#         qs   = super().get_queryset(request)
#         role = getattr(request.user, 'role', None)
#         if role == "SUPER_ADMIN":
#             return qs
#         if role == "ADMIN":
#             return qs.filter(role__in=["MENTOR", "STUDENT"])
#         if role == "MENTOR":
#             return qs.filter(role="STUDENT")
#         return qs.filter(pk=request.user.pk)

#     def get_form(self, request, obj=None, **kwargs):
#         kwargs.setdefault('exclude', [])
#         if isinstance(kwargs['exclude'], tuple):
#             kwargs['exclude'] = list(kwargs['exclude'])
#         if 'password' not in kwargs['exclude']:
#             kwargs['exclude'].append('password')

#         form = super(BaseUserAdmin, self).get_form(request, obj, **kwargs)
#         role = getattr(request.user, 'role', None)
#         if role == "ADMIN":
#             if "role" in form.base_fields:
#                 form.base_fields["role"].choices = [
#                     ("MENTOR",  "Mentor"),
#                     ("STUDENT", "Student"),
#                 ]
#             for field in ["is_staff", "is_superuser"]:
#                 if field in form.base_fields:
#                     form.base_fields[field].disabled = True
#         elif role == "MENTOR":
#             allowed = ["full_name", "email"]
#             for field in list(form.base_fields.keys()):
#                 if field not in allowed:
#                     form.base_fields[field].disabled = True
#         return form

#     def has_delete_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) == "SUPER_ADMIN"


# # =====================================================================
# # ADMIN PROXY
# # =====================================================================

# @admin.register(AdminUser)
# class AdminUserAdmin(BaseUserAdmin):
#     list_display = ["full_name", "email", "status_badge", "date_joined", "action_buttons"]

#     def get_queryset(self, request):
#         return super(UserAdmin, self).get_queryset(request).filter(role="ADMIN")

#     def has_module_perms(self, request):
#         return getattr(request.user, 'role', None) == "SUPER_ADMIN"

#     def has_view_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) == "SUPER_ADMIN"

#     def has_change_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) == "SUPER_ADMIN"

#     def has_delete_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) == "SUPER_ADMIN"

#     def has_add_permission(self, request):
#         return getattr(request.user, 'role', None) == "SUPER_ADMIN"


# # =====================================================================
# # MENTOR PROXY
# # =====================================================================

# @admin.register(MentorUser)
# class MentorUserAdmin(BaseUserAdmin):
#     list_display = ["full_name", "email", "status_badge", "date_joined", "action_buttons"]

#     def get_queryset(self, request):
#         return super(UserAdmin, self).get_queryset(request).filter(role="MENTOR")

#     def has_module_perms(self, request):
#         return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]

#     def has_view_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]

#     def has_change_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]

#     def has_delete_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]

#     def has_add_permission(self, request):
#         return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]


# # =====================================================================
# # STUDENT PROXY
# # =====================================================================

# @admin.register(StudentUser)
# class StudentUserAdmin(BaseUserAdmin):
#     list_display = ["full_name", "email", "status_badge", "date_joined", "action_buttons"]

#     def get_queryset(self, request):
#         return super(UserAdmin, self).get_queryset(request).filter(role="STUDENT")

#     def has_module_perms(self, request):
#         return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN", "MENTOR"]

#     def has_view_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN", "MENTOR"]

#     def has_change_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN", "MENTOR"]

#     def has_delete_permission(self, request, obj=None):
#         return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]

#     def has_add_permission(self, request):
#         return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from django.conf import settings
from .models import User


# =====================================================================
# PROXY MODELS
# =====================================================================

class AdminUser(User):
    class Meta:
        proxy               = True
        verbose_name        = "Admin"
        verbose_name_plural = "Admins"

class MentorUser(User):
    class Meta:
        proxy               = True
        verbose_name        = "Mentor"
        verbose_name_plural = "Mentors"

class StudentUser(User):
    class Meta:
        proxy               = True
        verbose_name        = "Student"
        verbose_name_plural = "Students"


# =====================================================================
# BASE ADMIN
# =====================================================================

class BaseUserAdmin(UserAdmin):

    CUSTOM_ADMIN_FIELDS = ('password_display',)

    def role_badge(self, obj):
        colors = {
            "SUPER_ADMIN": ("#001A35", "#D4A017", "Super Admin"),
            "ADMIN":       ("#002147", "#6EA8FE", "Admin"),
            "MENTOR":      ("#1A3A1A", "#6FCF97", "Mentor"),
            "STUDENT":     ("#1A1A3A", "#A78BFA", "Student"),
        }
        bg, color, label = colors.get(obj.role, ("#333", "#fff", obj.role))
        return format_html(
            '<span style="background:{};color:{};padding:3px 12px;'
            'border-radius:20px;font-size:11px;font-weight:700;'
            'letter-spacing:0.5px;text-transform:uppercase;">{}</span>',
            bg, color, label
        )
    role_badge.short_description = "Role"
    role_badge.admin_order_field = "role"

    def status_badge(self, obj):
        if obj.is_active:
            return mark_safe(
                '<span style="background:#E8F5EE;color:#1A7A4A;'
                'padding:3px 10px;border-radius:20px;'
                'font-size:11px;font-weight:700;">Active</span>'
            )
        return mark_safe(
            '<span style="background:#FDECEA;color:#C0392B;'
            'padding:3px 10px;border-radius:20px;'
            'font-size:11px;font-weight:700;">Inactive</span>'
        )
    status_badge.short_description = "Status"
    status_badge.admin_order_field = "is_active"

    def action_buttons(self, obj):
        app        = obj._meta.app_label
        name       = obj._meta.model_name
        view_url   = reverse("admin:%s_%s_change" % (app, name), args=[obj.pk])
        delete_url = reverse("admin:%s_%s_delete" % (app, name), args=[obj.pk])
        return format_html(
            '<div style="display:flex;gap:4px;align-items:center;">'
            '<a href="{0}" title="View" style="'
            'display:inline-flex;align-items:center;justify-content:center;'
            'width:30px;height:30px;border-radius:6px;'
            'background:#E8F0FE;color:#1A56DB;border:1px solid #1A56DB;'
            'text-decoration:none;font-size:13px;">'
            '<i class="fas fa-eye"></i></a>'
            '<a href="{0}" title="Edit" style="'
            'display:inline-flex;align-items:center;justify-content:center;'
            'width:30px;height:30px;border-radius:6px;'
            'background:#E8F5EE;color:#1A7A4A;border:1px solid #1A7A4A;'
            'text-decoration:none;font-size:13px;">'
            '<i class="fas fa-pen"></i></a>'
            '<a href="{1}" title="Delete" style="'
            'display:inline-flex;align-items:center;justify-content:center;'
            'width:30px;height:30px;border-radius:6px;'
            'background:#FDECEA;color:#C0392B;border:1px solid #C0392B;'
            'text-decoration:none;font-size:13px;" '
            'onclick="return confirm(\'Delete this user?\');">'
            '<i class="fas fa-trash"></i></a>'
            '</div>',
            view_url, delete_url
        )
    action_buttons.short_description = "Actions"

    def password_display(self, obj):
        return mark_safe('''
            <div style="display:flex;align-items:center;gap:10px;max-width:420px;">
                <input
                    id="pwd_display_{pk}"
                    type="password"
                    value="{pwd}"
                    readonly
                    style="flex:1;padding:8px 12px;border:1px solid #ddd;
                           border-radius:6px;font-family:monospace;font-size:13px;
                           background:#f8f8f8;color:#333;outline:none;"
                />
                <button
                    type="button"
                    onclick="
                        var f = document.getElementById('pwd_display_{pk}');
                        var i = document.getElementById('eye_icon_{pk}');
                        if (f.type === 'password') {{
                            f.type = 'text';
                            i.className = 'fas fa-eye-slash';
                        }} else {{
                            f.type = 'password';
                            i.className = 'fas fa-eye';
                        }}
                    "
                    style="padding:8px 12px;border:1px solid #1A56DB;border-radius:6px;
                           background:#E8F0FE;color:#1A56DB;cursor:pointer;
                           font-size:14px;display:flex;align-items:center;gap:6px;"
                    title="Show / Hide password"
                >
                    <i id="eye_icon_{pk}" class="fas fa-eye"></i>
                </button>
            </div>
            <p style="margin-top:6px;font-size:11px;color:#888;">
                This is the hashed password stored in the database.
                To change it use the
                <a href="password/">password change form</a>.
            </p>
        '''.format(pk=obj.pk, pwd=obj.password))
    password_display.short_description = "Password"

    list_display   = ["full_name", "email", "role_badge", "status_badge", "date_joined", "action_buttons"]
    list_filter    = ["is_active", "date_joined"]
    search_fields  = ["email", "full_name"]
    ordering       = ["-date_joined"]
    list_per_page  = 20
    date_hierarchy = "date_joined"

    fieldsets = (
        ("Login Credentials",    {"fields": ("email", "password_display")}),
        ("Personal Information", {"fields": ("full_name",)}),
        ("Role and Access",      {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
        ("Important Dates",      {"fields": ("date_joined", "last_login"), "classes": ("collapse",)}),
    )
    readonly_fields = ["date_joined", "last_login", "password_display"]

    add_fieldsets = (
        ("Create New User", {
            "classes": ("wide",),
            "fields":  ("full_name", "email", "role", "password1", "password2", "is_active"),
        }),
    )

    actions = ["activate_users", "deactivate_users"]

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, "%d user(s) activated." % updated)
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, "%d user(s) deactivated." % updated)
    deactivate_users.short_description = "Deactivate selected users"

    def get_form(self, request, obj=None, **kwargs):
        kwargs.setdefault('exclude', [])
        if isinstance(kwargs['exclude'], tuple):
            kwargs['exclude'] = list(kwargs['exclude'])
        if 'password' not in kwargs['exclude']:
            kwargs['exclude'].append('password')

        all_custom_fields = set(self.CUSTOM_ADMIN_FIELDS)
        all_custom_fields.update(['date_joined', 'last_login'])

        if 'fields' in kwargs and kwargs['fields']:
            kwargs['fields'] = tuple(
                f for f in kwargs['fields']
                if f not in all_custom_fields
            )

        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        DEBUG VERSION: Aggressive logging to trace email flow
        """
        print(f"\n [DEBUG] save_model() called")
        print(f"   - change={change} (False = new user)")
        print(f"   - obj.email={obj.email}")
        print(f"   - obj.role={getattr(obj, 'role', 'N/A')}")
        print(f"   - form.cleaned_data keys: {list(getattr(form, 'cleaned_data', {}).keys())}")
        
        # Capture plain password BEFORE hashing
        plain_password = None
        cleaned_data = getattr(form, 'cleaned_data', {})
        plain_password = cleaned_data.get('password1') or cleaned_data.get('password')
        print(f"   - plain_password captured: {'YES' if plain_password else 'NO'}")

        # Save to DB
        print(f"   - Calling super().save_model()...")
        super().save_model(request, obj, form, change)
        print(f"   - User saved to database")

        # Send email only on first creation
        if not change and plain_password and obj.email:
            print(f"   - Conditions met: sending email...")
            self._send_credentials_email(request, obj, plain_password)
        else:
            reason = []
            if change: reason.append("editing existing user")
            if not plain_password: reason.append("no password captured")
            if not obj.email: reason.append("no email")
            print(f"   - ⏭ Skipping email: {', '.join(reason)}")
        print(f"🔍 [DEBUG] save_model() complete\n")

    def _send_credentials_email(self, request, user, password):
        """Send welcome email with name, initials, email & password"""
        initials = ""
        if user.full_name:
            parts = user.full_name.strip().split()
            initials = ".".join([p[0].upper() for p in parts[:2]])
            if len(parts) == 1:
                initials = parts[0][0].upper() + "."
        
        role_label = getattr(user, 'role', 'User').replace('_', ' ').title()
        subject = f"Welcome to TheYKSApp - Your {role_label} Account"
        
        message = (
            f"Dear {user.full_name} ({initials}),\n\n"
            f"Your {role_label} account has been successfully created.\n\n"
            f"Login Email: {user.email}\n"
            f"Temporary Password: {password}\n\n"
            "Please log in and change your password immediately for security.\n\n"
            "Best regards,\n"
            "The YKSApp Team"
        )

        print(f"\n [EMAIL] Attempting to send to {user.email}")
        print(f"   Subject: {subject}")
        print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"   Backend: {settings.EMAIL_BACKEND}")
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            print(f" [EMAIL] send_mail() returned successfully")
            self.message_user(
                request,
                f" {role_label} created & credentials email sent to {user.email}.",
                level='INFO'
            )
        except Exception as e:
            import traceback
            print(f" [EMAIL] CRITICAL FAILURE:")
            print(f"   Error: {type(e).__name__}: {str(e)}")
            print(f"   Traceback:\n{traceback.format_exc()}")
            self.message_user(
                request,
                f"{role_label} created, but email failed: {e}",
                level='ERROR'
            )


# =====================================================================
# MAIN USER ADMIN
# =====================================================================

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ["full_name", "email", "role_badge", "status_badge", "date_joined", "action_buttons"]
    list_filter  = ["role", "is_active", "date_joined"]
    actions      = BaseUserAdmin.actions + ["make_mentor", "make_admin"]

    def make_mentor(self, request, queryset):
        for user in queryset:
            user.role = "MENTOR"
            user.save()
        self.message_user(request, "%d user(s) set as Mentor." % queryset.count())
    make_mentor.short_description = "Set selected as Mentor"

    def make_admin(self, request, queryset):
        for user in queryset:
            user.role = "ADMIN"
            user.save()
        self.message_user(request, "%d user(s) set as Admin." % queryset.count())
    make_admin.short_description = "Set selected as Admin"

    def get_queryset(self, request):
        qs   = super().get_queryset(request)
        role = getattr(request.user, 'role', None)
        if role == "SUPER_ADMIN":
            return qs
        if role == "ADMIN":
            return qs.filter(role__in=["MENTOR", "STUDENT"])
        if role == "MENTOR":
            return qs.filter(role="STUDENT")
        return qs.filter(pk=request.user.pk)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        role = getattr(request.user, 'role', None)
        if role == "ADMIN":
            if "role" in form.base_fields:
                form.base_fields["role"].choices = [
                    ("MENTOR",  "Mentor"),
                    ("STUDENT", "Student"),
                ]
            for field in ["is_staff", "is_superuser"]:
                if field in form.base_fields:
                    form.base_fields[field].disabled = True
        elif role == "MENTOR":
            allowed = ["full_name", "email"]
            for field in list(form.base_fields.keys()):
                if field not in allowed:
                    form.base_fields[field].disabled = True
        return form

    def has_delete_permission(self, request, obj=None):
        return getattr(request.user, 'role', None) == "SUPER_ADMIN"


# =====================================================================
# ADMIN PROXY
# =====================================================================

@admin.register(AdminUser)
class AdminUserAdmin(BaseUserAdmin):
    list_display = ["full_name", "email", "status_badge", "date_joined", "action_buttons"]

    def get_queryset(self, request):
        return super(UserAdmin, self).get_queryset(request).filter(role="ADMIN")

    def has_module_perms(self, request):
        return getattr(request.user, 'role', None) == "SUPER_ADMIN"

    def has_view_permission(self, request, obj=None):
        return getattr(request.user, 'role', None) == "SUPER_ADMIN"

    def has_change_permission(self, request, obj=None):
        return getattr(request.user, 'role', None) == "SUPER_ADMIN"

    def has_delete_permission(self, request, obj=None):
        return getattr(request.user, 'role', None) == "SUPER_ADMIN"

    def has_add_permission(self, request):
        return getattr(request.user, 'role', None) == "SUPER_ADMIN"


# =====================================================================
# MENTOR PROXY
# =====================================================================

@admin.register(MentorUser)
class MentorUserAdmin(BaseUserAdmin):
    list_display = ["full_name", "email", "status_badge", "date_joined", "action_buttons"]

    def get_queryset(self, request):
        return super(UserAdmin, self).get_queryset(request).filter(role="MENTOR")

    def has_module_perms(self, request):
        return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]

    def has_view_permission(self, request, obj=None):
        return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]

    def has_change_permission(self, request, obj=None):
        return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]

    def has_delete_permission(self, request, obj=None):
        return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]

    def has_add_permission(self, request):
        return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]


# =====================================================================
# STUDENT PROXY
# =====================================================================

@admin.register(StudentUser)
class StudentUserAdmin(BaseUserAdmin):
    list_display = ["full_name", "email", "status_badge", "date_joined", "action_buttons"]

    def get_queryset(self, request):
        return super(UserAdmin, self).get_queryset(request).filter(role="STUDENT")

    def has_module_perms(self, request):
        return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN", "MENTOR"]

    def has_view_permission(self, request, obj=None):
        return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN", "MENTOR"]

    def has_change_permission(self, request, obj=None):
        return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN", "MENTOR"]

    def has_delete_permission(self, request, obj=None):
        return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]

    def has_add_permission(self, request):
        return getattr(request.user, 'role', None) in ["SUPER_ADMIN", "ADMIN"]