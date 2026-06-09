# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.utils.html import format_html
# from django.urls import reverse
# from django.utils.safestring import mark_safe
# from django.core.mail import send_mail
# from django.conf import settings
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

#     CUSTOM_ADMIN_FIELDS = ('password_display',)

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

#         all_custom_fields = set(self.CUSTOM_ADMIN_FIELDS)
#         all_custom_fields.update(['date_joined', 'last_login'])

#         if 'fields' in kwargs and kwargs['fields']:
#             kwargs['fields'] = tuple(
#                 f for f in kwargs['fields']
#                 if f not in all_custom_fields
#             )

#         return super().get_form(request, obj, **kwargs)

#     def save_model(self, request, obj, form, change):
#         """
#         DEBUG VERSION: Aggressive logging to trace email flow
#         """
#         print(f"\n [DEBUG] save_model() called")
#         print(f"   - change={change} (False = new user)")
#         print(f"   - obj.email={obj.email}")
#         print(f"   - obj.role={getattr(obj, 'role', 'N/A')}")
#         print(f"   - form.cleaned_data keys: {list(getattr(form, 'cleaned_data', {}).keys())}")
        
#         # Capture plain password BEFORE hashing
#         plain_password = None
#         cleaned_data = getattr(form, 'cleaned_data', {})
#         plain_password = cleaned_data.get('password1') or cleaned_data.get('password')
#         print(f"   - plain_password captured: {'YES' if plain_password else 'NO'}")

#         # Save to DB
#         print(f"   - Calling super().save_model()...")
#         super().save_model(request, obj, form, change)
#         print(f"   - User saved to database")

#         # Send email only on first creation
#         if not change and plain_password and obj.email:
#             print(f"   - Conditions met: sending email...")
#             self._send_credentials_email(request, obj, plain_password)
#         else:
#             reason = []
#             if change: reason.append("editing existing user")
#             if not plain_password: reason.append("no password captured")
#             if not obj.email: reason.append("no email")
#             print(f"   - ⏭ Skipping email: {', '.join(reason)}")
#         print(f"🔍 [DEBUG] save_model() complete\n")

#     def _send_credentials_email(self, request, user, password):
#         """Send welcome email with name, initials, email & password"""
#         initials = ""
#         if user.full_name:
#             parts = user.full_name.strip().split()
#             initials = ".".join([p[0].upper() for p in parts[:2]])
#             if len(parts) == 1:
#                 initials = parts[0][0].upper() + "."
        
#         role_label = getattr(user, 'role', 'User').replace('_', ' ').title()
#         subject = f"Welcome to TheYKSApp - Your {role_label} Account"
        
#         message = (
#             f"Dear {user.full_name} ({initials}),\n\n"
#             f"Your {role_label} account has been successfully created.\n\n"
#             f"Login Email: {user.email}\n"
#             f"Temporary Password: {password}\n\n"
#             "Please log in and change your password immediately for security.\n\n"
#             "Best regards,\n"
#             "The YKSApp Team"
#         )

#         print(f"\n [EMAIL] Attempting to send to {user.email}")
#         print(f"   Subject: {subject}")
#         print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
#         print(f"   Backend: {settings.EMAIL_BACKEND}")
        
#         try:
#             send_mail(
#                 subject=subject,
#                 message=message,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[user.email],
#                 fail_silently=False,
#             )
#             print(f" [EMAIL] send_mail() returned successfully")
#             self.message_user(
#                 request,
#                 f" {role_label} created & credentials email sent to {user.email}.",
#                 level='INFO'
#             )
#         except Exception as e:
#             import traceback
#             print(f" [EMAIL] CRITICAL FAILURE:")
#             print(f"   Error: {type(e).__name__}: {str(e)}")
#             print(f"   Traceback:\n{traceback.format_exc()}")
#             self.message_user(
#                 request,
#                 f"{role_label} created, but email failed: {e}",
#                 level='ERROR'
#             )


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
#         form = super().get_form(request, obj, **kwargs)
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

# accounts/admin.py

# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from .models import User


# ======================================================================
#  EYE-TOGGLE PASSWORD WIDGET
# ======================================================================
class EyePasswordInput(forms.PasswordInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs['id'] = f'id_{name}'
        attrs['style'] = (
            'width:100%;padding:8px 44px 8px 10px;'
            'border:1px solid #ccc;border-radius:6px;'
            'font-size:14px;box-sizing:border-box;'
        )
        input_html = super().render(name, value, attrs, renderer)
        btn_id = f'eye_{name}'
        html = (
            f'<div style="position:relative;display:inline-block;width:100%;max-width:400px;">'
            f'  {input_html}'
            f'  <button type="button" id="{btn_id}" title="Show / hide password"'
            f'    style="position:absolute;right:10px;top:50%;transform:translateY(-50%);'
            f'           background:none;border:none;cursor:pointer;padding:2px;'
            f'           display:flex;align-items:center;"'
            f'    onclick="toggleEyePassword(\'id_{name}\', \'{btn_id}\')">'
            f'    <i class="fa fa-eye" style="font-size:16px;color:#666;"></i>'
            f'  </button>'
            f'</div>'
            f'<script>'
            f'if (!window._eyeToggleDefined) {{'
            f'  window._eyeToggleDefined = true;'
            f'  window.toggleEyePassword = function(inputId, btnId) {{'
            f'    var i = document.getElementById(inputId);'
            f'    var icon = document.querySelector("#" + btnId + " i");'
            f'    if (i.type === "password") {{'
            f'      i.type = "text";'
            f'      icon.classList.remove("fa-eye");'
            f'      icon.classList.add("fa-eye-slash");'
            f'    }} else {{'
            f'      i.type = "password";'
            f'      icon.classList.remove("fa-eye-slash");'
            f'      icon.classList.add("fa-eye");'
            f'    }}'
            f'  }};'
            f'}}'
            f'</script>'
        )
        return mark_safe(html)


# ======================================================================
#  PROXY MODELS
# ======================================================================
class AdminUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

class MentorUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Mentor'
        verbose_name_plural = 'Mentors'

class StudentUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


# ======================================================================
#  BASE USER ADMIN
# ======================================================================
class BaseUserAdmin(UserAdmin):

    CUSTOM_ADMIN_FIELDS = ('password_display',)

    def role_badge(self, obj):
        colors = {
            'SUPER_ADMIN': ('#001A35', '#D4A017', 'Super Admin'),
            'ADMIN':       ('#002147', '#6EA8FE', 'Admin'),
            'MENTOR':      ('#1A3A1A', '#6FCF97', 'Mentor'),
            'STUDENT':     ('#1A1A3A', '#A78BFA', 'Student'),
        }
        bg, color, label = colors.get(obj.role, ('#333', '#fff', obj.role))
        return format_html(
            '<span style="background:{};color:{};padding:3px 12px;'
            'border-radius:20px;font-size:11px;font-weight:700;'
            'letter-spacing:0.5px;text-transform:uppercase;">{}</span>',
            bg, color, label,
        )
    role_badge.short_description = 'Role'
    role_badge.admin_order_field = 'role'

    def status_badge(self, obj):
        if obj.is_active:
            return mark_safe(
                '<span style="background:#E8F5EE;color:#1A7A4A;'
                'padding:3px 10px;border-radius:20px;'
                'font-size:11px;font-weight:700;">Active</span>')
        return mark_safe(
            '<span style="background:#FDECEA;color:#C0392B;'
            'padding:3px 10px;border-radius:20px;'
            'font-size:11px;font-weight:700;">Inactive</span>')
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'is_active'

    def action_buttons(self, obj):
        app        = obj._meta.app_label
        name       = obj._meta.model_name
        view_url   = reverse('admin:%s_%s_change' % (app, name), args=[obj.pk])
        delete_url = reverse('admin:%s_%s_delete' % (app, name), args=[obj.pk])
        modal_id   = f'del_modal_{obj.pk}'

        return format_html(
            # ── Row of 3 icon buttons ──────────────────────────────────
            '<div style="display:flex;gap:6px;align-items:center;">'

            # View
            '<a href="{0}" title="View"'
            ' style="display:inline-flex;align-items:center;justify-content:center;'
            'width:32px;height:32px;border-radius:8px;'
            'background:#F0F2F5;color:#1D3557;border:1.5px solid #1D3557;'
            'text-decoration:none;font-size:13px;"'
            ' onmouseover="this.style.background=\'#1D3557\';this.style.color=\'#F0F2F5\';"'
            ' onmouseout="this.style.background=\'#F0F2F5\';this.style.color=\'#1D3557\';">'
            '<i class="fas fa-eye"></i></a>'

            # Edit
            '<a href="{0}" title="Edit"'
            ' style="display:inline-flex;align-items:center;justify-content:center;'
            'width:32px;height:32px;border-radius:8px;'
            'background:#F0F2F5;color:#B8860B;border:1.5px solid #B8860B;'
            'text-decoration:none;font-size:13px;"'
            ' onmouseover="this.style.background=\'#B8860B\';this.style.color=\'#ffffff\';"'
            ' onmouseout="this.style.background=\'#F0F2F5\';this.style.color=\'#B8860B\';">'
            '<i class="fas fa-pen"></i></a>'

            # Delete — opens modal
            '<button type="button" title="Delete"'
            ' onclick="document.getElementById(\'{2}\').style.display=\'flex\';"'
            ' style="display:inline-flex;align-items:center;justify-content:center;'
            'width:32px;height:32px;border-radius:8px;'
            'background:#F0F2F5;color:#C0392B;border:1.5px solid #C0392B;'
            'cursor:pointer;font-size:13px;"'
            ' onmouseover="this.style.background=\'#C0392B\';this.style.color=\'#ffffff\';"'
            ' onmouseout="this.style.background=\'#F0F2F5\';this.style.color=\'#C0392B\';">'
            '<i class="fas fa-trash"></i></button>'
            '</div>'

            # ── Modal backdrop ─────────────────────────────────────────
            '<div id="{2}" style="display:none;position:fixed;inset:0;z-index:99999;'
            'align-items:center;justify-content:center;'
            'background:rgba(29,53,87,0.55);backdrop-filter:blur(3px);">'

            # Modal card
            '<div style="background:#ffffff;border-radius:16px;'
            'box-shadow:0 20px 60px rgba(29,53,87,0.25);'
            'padding:40px 36px 32px;max-width:400px;width:90%;'
            'text-align:center;position:relative;box-sizing:border-box;">'

            # Top accent bar
            '<div style="position:absolute;top:0;left:0;right:0;height:5px;'
            'background:linear-gradient(90deg,#1D3557,#B8860B);'
            'border-radius:16px 16px 0 0;"></div>'

            # Icon circle
            '<div style="width:64px;height:64px;border-radius:50%;'
            'background:#FFF3F3;border:2px solid #C0392B;'
            'display:flex;align-items:center;justify-content:center;margin:0 auto 20px;">'
            '<i class="fas fa-trash" style="font-size:24px;color:#C0392B;"></i>'
            '</div>'

            # Title
            '<p style="margin:0 0 10px;font-size:19px;font-weight:700;'
            'color:#1D3557;letter-spacing:0.2px;">Delete User</p>'

            # Message
            '<p style="margin:0 0 30px;font-size:13.5px;color:#6B7280;line-height:1.65;">'
            'Are you sure you want to delete this user?<br>'
            '<span style="color:#C0392B;font-weight:600;">This action cannot be undone.</span>'
            '</p>'

            # Buttons row — both same width via flex
            '<div style="display:flex;gap:12px;justify-content:center;">'

            # Cancel — fixed min-width so both buttons match
            '<button type="button"'
            ' onclick="document.getElementById(\'{2}\').style.display=\'none\';"'
            ' style="min-width:130px;padding:11px 20px;border-radius:8px;'
            'font-size:13.5px;font-weight:600;white-space:nowrap;'
            'background:#F0F2F5;color:#1D3557;border:1.5px solid #1D3557;cursor:pointer;"'
            ' onmouseover="this.style.background=\'#1D3557\';this.style.color=\'#ffffff\';"'
            ' onmouseout="this.style.background=\'#F0F2F5\';this.style.color=\'#1D3557\';">'
            'Cancel'
            '</button>'

            # Yes Delete — same min-width, no wrapping
            '<a href="{1}"'
            ' style="min-width:130px;padding:11px 20px;border-radius:8px;'
            'font-size:13.5px;font-weight:600;white-space:nowrap;'
            'background:#C0392B;color:#ffffff;border:1.5px solid #C0392B;'
            'text-decoration:none;display:inline-flex;'
            'align-items:center;justify-content:center;gap:7px;box-sizing:border-box;"'
            ' onmouseover="this.style.background=\'#a93226\';this.style.borderColor=\'#a93226\';"'
            ' onmouseout="this.style.background=\'#C0392B\';this.style.borderColor=\'#C0392B\';">'
            '<i class="fas fa-trash" style="font-size:12px;"></i>Yes, Delete'
            '</a>'

            '</div>'   # buttons row
            '</div>'   # modal card
            '</div>',  # modal backdrop

            view_url, delete_url, modal_id,
        )
    action_buttons.short_description = 'Actions'

    def password_display(self, obj):
        pk = obj.pk
        return mark_safe(
            f'<div style="display:flex;align-items:center;gap:10px;max-width:420px;">'
            f'  <input id="phash_{pk}" type="password" value="{obj.password}" readonly'
            f'    style="flex:1;padding:8px 12px;border:1px solid #ddd;border-radius:6px;'
            f'           font-family:monospace;font-size:13px;background:#f8f8f8;'
            f'           color:#333;outline:none;"/>'
            f'  <button type="button" id="phash_btn_{pk}" title="Show password"'
            f'    style="padding:7px 10px;border:1px solid #1A56DB;border-radius:6px;'
            f'           background:#E8F0FE;color:#1A56DB;cursor:pointer;'
            f'           display:flex;align-items:center;justify-content:center;"'
            f'    onclick="toggleEyePassword(\'phash_{pk}\', \'phash_btn_{pk}\')">'
            f'    <i class="fa fa-eye" style="font-size:16px;"></i>'
            f'  </button>'
            f'</div>'
            f'<p style="margin-top:6px;font-size:11px;color:#888;">'
            f'  Hashed value — to change it use the'
            f'  <a href="password/">password change form</a>.'
            f'</p>'
        )
    password_display.short_description = 'Password'

    list_display   = ['full_name', 'email', 'role_badge', 'status_badge',
                      'date_joined', 'action_buttons']
    list_filter    = ['is_active', 'date_joined']
    search_fields  = ['email', 'full_name']
    ordering       = ['-date_joined']
    list_per_page  = 20
    date_hierarchy = 'date_joined'

    fieldsets = (
        ('Login Credentials',    {'fields': ('email', 'password_display')}),
        ('Personal Information', {'fields': ('full_name',)}),
        ('Role and Access',      {'fields': ('role', 'is_active',
                                             'is_staff', 'is_superuser')}),
        ('Important Dates',      {'fields': ('date_joined', 'last_login'),
                                  'classes': ('collapse',)}),
    )
    readonly_fields = ['date_joined', 'last_login', 'password_display']

    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields':  ('full_name', 'email', 'role',
                        'password1', 'password2', 'is_active'),
        }),
    )

    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, '%d user(s) activated.' % updated)
    activate_users.short_description = 'Activate selected users'

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, '%d user(s) deactivated.' % updated)
    deactivate_users.short_description = 'Deactivate selected users'

    def get_form(self, request, obj=None, **kwargs):
        kwargs.setdefault('exclude', [])
        if isinstance(kwargs['exclude'], tuple):
            kwargs['exclude'] = list(kwargs['exclude'])
        if 'password' not in kwargs['exclude']:
            kwargs['exclude'].append('password')
        all_custom = set(self.CUSTOM_ADMIN_FIELDS) | {'date_joined', 'last_login'}
        if 'fields' in kwargs and kwargs['fields']:
            kwargs['fields'] = tuple(
                f for f in kwargs['fields'] if f not in all_custom)
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            for fname in ('password1', 'password2'):
                if fname in form.base_fields:
                    form.base_fields[fname].widget = EyePasswordInput(
                        attrs={'autocomplete': 'new-password'})
        return form

    def save_model(self, request, obj, form, change):
        cleaned        = getattr(form, 'cleaned_data', {})
        plain_password = cleaned.get('password1') or cleaned.get('password')
        super().save_model(request, obj, form, change)
        if not change and plain_password and obj.email:
            self._send_credentials_email(request, obj, plain_password)

    def _send_credentials_email(self, request, user, password):
        initials = ''
        if user.full_name:
            parts    = user.full_name.strip().split()
            initials = '.'.join(p[0].upper() for p in parts[:2])
            if len(parts) == 1:
                initials = parts[0][0].upper() + '.'
        role_label = getattr(user, 'role', 'User').replace('_', ' ').title()
        subject    = f'Welcome to TheYKSApp — Your {role_label} Account'
        message    = (
            f'Dear {user.full_name} ({initials}),\n\n'
            f'Your {role_label} account has been created.\n\n'
            f'Login Email:        {user.email}\n'
            f'Temporary Password: {password}\n\n'
            'Please log in and change your password immediately.\n\n'
            'Best regards,\nThe YKSApp Team'
        )
        try:
            send_mail(subject, message,
                      settings.DEFAULT_FROM_EMAIL, [user.email],
                      fail_silently=False)
            self.message_user(
                request,
                f'{role_label} created — credentials sent to {user.email}.')
        except Exception as e:
            self.message_user(
                request,
                f'{role_label} created, but email failed: {e}',
                level='ERROR')


# ======================================================================
#  MAIN USER ADMIN
# ======================================================================
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['full_name', 'email', 'role_badge', 'status_badge',
                    'date_joined', 'action_buttons']
    list_filter  = ['role', 'is_active', 'date_joined']
    actions      = BaseUserAdmin.actions + ['make_mentor', 'make_admin']

    def make_mentor(self, request, queryset):
        for u in queryset:
            u.role = 'MENTOR'
            u.save()
        self.message_user(request, '%d user(s) set as Mentor.' % queryset.count())
    make_mentor.short_description = 'Set selected as Mentor'

    def make_admin(self, request, queryset):
        for u in queryset:
            u.role = 'ADMIN'
            u.save()
        self.message_user(request, '%d user(s) set as Admin.' % queryset.count())
    make_admin.short_description = 'Set selected as Admin'

    def get_queryset(self, request):
        qs   = super().get_queryset(request)
        role = getattr(request.user, 'role', None)
        if role == 'SUPER_ADMIN': return qs
        if role == 'ADMIN':       return qs.filter(role__in=['MENTOR', 'STUDENT'])
        if role == 'MENTOR':      return qs.filter(role='STUDENT')
        return qs.filter(pk=request.user.pk)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        role = getattr(request.user, 'role', None)
        if role == 'ADMIN':
            if 'role' in form.base_fields:
                form.base_fields['role'].choices = [
                    ('MENTOR',  'Mentor'),
                    ('STUDENT', 'Student'),
                ]
            for f in ['is_staff', 'is_superuser']:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True
        elif role == 'MENTOR':
            for f in list(form.base_fields):
                if f not in ['full_name', 'email']:
                    form.base_fields[f].disabled = True
        return form

    def has_delete_permission(self, request, obj=None):
        return getattr(request.user, 'role', None) == 'SUPER_ADMIN'


# ======================================================================
#  MENTOR ADMIN
# ======================================================================
@admin.register(MentorUser)
class MentorUserAdmin(BaseUserAdmin):
    list_display = ['full_name', 'email', 'status_badge',
                    'date_joined', 'action_buttons']

    add_fieldsets = (
        ('Create Mentor Account', {
            'classes': ('wide',),
            'fields':  ('full_name', 'email',
                        'password1', 'password2', 'is_active'),
        }),
    )

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['role_banner'] = mark_safe(
            '<div style="background:#E8F5EE;border-left:4px solid #1A7A4A;'
            'padding:12px 16px;border-radius:6px;margin-bottom:16px;'
            'font-size:13px;color:#1A3A1A;">'
            '<strong>Mentor account</strong> — role is automatically set '
            'to <strong>Mentor</strong>. No need to select a role.'
            '</div>')
        return super().add_view(request, form_url, extra_context)

    def get_queryset(self, request):
        return super(UserAdmin, self).get_queryset(request).filter(role='MENTOR')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.role = 'MENTOR'
        super().save_model(request, obj, form, change)

    def has_module_perms(self, request):              return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']
    def has_view_permission(self, request, obj=None): return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']
    def has_change_permission(self, request, obj=None): return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']
    def has_delete_permission(self, request, obj=None): return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']
    def has_add_permission(self, request):            return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']


# ======================================================================
#  ADMIN USER ADMIN
# ======================================================================
@admin.register(AdminUser)
class AdminUserAdmin(BaseUserAdmin):
    list_display = ['full_name', 'email', 'status_badge',
                    'date_joined', 'action_buttons']

    add_fieldsets = (
        ('Create Admin Account', {
            'classes': ('wide',),
            'fields':  ('full_name', 'email',
                        'password1', 'password2', 'is_active'),
        }),
    )

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['role_banner'] = mark_safe(
            '<div style="background:#E8F0FE;border-left:4px solid #1A56DB;'
            'padding:12px 16px;border-radius:6px;margin-bottom:16px;'
            'font-size:13px;color:#002147;">'
            '<strong>Admin account</strong> — role is automatically set '
            'to <strong>Admin</strong>. No need to select a role.'
            '</div>')
        return super().add_view(request, form_url, extra_context)

    def get_queryset(self, request):
        return super(UserAdmin, self).get_queryset(request).filter(role='ADMIN')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.role = 'ADMIN'
        super().save_model(request, obj, form, change)

    def has_module_perms(self, request):              return getattr(request.user, 'role', None) == 'SUPER_ADMIN'
    def has_view_permission(self, request, obj=None): return getattr(request.user, 'role', None) == 'SUPER_ADMIN'
    def has_change_permission(self, request, obj=None): return getattr(request.user, 'role', None) == 'SUPER_ADMIN'
    def has_delete_permission(self, request, obj=None): return getattr(request.user, 'role', None) == 'SUPER_ADMIN'
    def has_add_permission(self, request):            return getattr(request.user, 'role', None) == 'SUPER_ADMIN'


# ======================================================================
#  STUDENT ADMIN
# ======================================================================
@admin.register(StudentUser)
class StudentUserAdmin(BaseUserAdmin):
    list_display = ['full_name', 'email', 'status_badge',
                    'date_joined', 'action_buttons']

    add_fieldsets = (
        ('Create Student Account', {
            'classes': ('wide',),
            'fields':  ('full_name', 'email',
                        'password1', 'password2', 'is_active'),
        }),
    )

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['role_banner'] = mark_safe(
            '<div style="background:#F3F0FF;border-left:4px solid #7C5CFC;'
            'padding:12px 16px;border-radius:6px;margin-bottom:16px;'
            'font-size:13px;color:#1A1A3A;">'
            '<strong>Student account</strong> — role is automatically set '
            'to <strong>Student</strong>. No need to select a role.'
            '</div>')
        return super().add_view(request, form_url, extra_context)

    def get_queryset(self, request):
        return super(UserAdmin, self).get_queryset(request).filter(role='STUDENT')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.role = 'STUDENT'
        super().save_model(request, obj, form, change)

    def has_module_perms(self, request):              return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN', 'MENTOR']
    def has_view_permission(self, request, obj=None): return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN', 'MENTOR']
    def has_change_permission(self, request, obj=None): return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN', 'MENTOR']
    def has_delete_permission(self, request, obj=None): return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']
    def has_add_permission(self, request):            return getattr(request.user, 'role', None) in ['SUPER_ADMIN', 'ADMIN']