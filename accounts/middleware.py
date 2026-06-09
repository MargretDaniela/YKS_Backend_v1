# from django.shortcuts import redirect


# class RoleBasedAccessMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     ALLOWED_PATHS = [
#         "/admin/login/",
#         "/admin/logout/",
#         "/admin/jsi18n/",
#         "/admin/password_reset/",
#         "/admin/password_reset/done/",
#     ]

#     def __call__(self, request):
#         if request.path.startswith("/admin/"):
#             # Always allow static files and auth pages
#             if (request.path in self.ALLOWED_PATHS
#                     or request.path.startswith("/admin/static/")
#                     or request.path.startswith("/static/")):
#                 return self.get_response(request)

#             # Not logged in at all
#             if not request.user.is_authenticated:
#                 return redirect(f"/admin/login/?next={request.path}")

#             # Logged in but session expired or invalid
#             if not request.user.is_active:
#                 return redirect("/admin/login/")

#             # Wrong role — block access
#             allowed_roles = ["SUPER_ADMIN", "superadmin", "ADMIN", "MENTOR"]
#             if not hasattr(request.user, 'role') or request.user.role not in allowed_roles:
#                 return redirect("/admin/login/")

#             # Not staff — block access
#             if not request.user.is_staff:
#                 return redirect("/admin/login/")

#         return self.get_response(request)

# accounts/middleware.py
from django.shortcuts import redirect


class RoleBasedAccessMiddleware:
    """
    Handles two things:
    1. Blocks anyone without the right role/staff status from /admin/
    2. For MENTORs specifically, restricts which admin pages they can visit
    """

    ALLOWED_PATHS = [
        "/admin/login/",
        "/admin/logout/",
        "/admin/jsi18n/",
        "/admin/password_reset/",
        "/admin/password_reset/done/",
    ]

    # Mentors are never allowed here — redirected to dashboard
    MENTOR_BLOCKED = [
        "/admin/payments/",
        "/admin/accounts/user/add/",
        "/admin/accounts/adminuser/",
        "/admin/accounts/mentoruser/",
        "/admin/auth/",
    ]

    # Mentors are only allowed these prefixes
    MENTOR_ALLOWED = [
        "/admin/",                         # dashboard index
        "/admin/login/",
        "/admin/logout/",
        "/admin/jsi18n/",
        "/admin/courses/",                 # their own courses, categories, modules, lessons
        "/admin/mentorship/",              # their sessions, bookings, videos
        "/admin/attendance/",              # their attendance records
        "/admin/accounts/studentuser/",    # view students only
        "/admin/accounts/user/",           # view users (get_queryset limits results)
        "/admin/password_change/",
        "/admin/autocomplete/",            # needed for related field dropdowns
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if not path.startswith("/admin/"):
            return self.get_response(request)

        # Always allow static files and core auth pages
        if (path in self.ALLOWED_PATHS
                or path.startswith("/admin/static/")
                or path.startswith("/static/")):
            return self.get_response(request)

        # Not logged in — send to login
        if not request.user.is_authenticated:
            return redirect(f"/admin/login/?next={path}")

        # Inactive account — send to login
        if not request.user.is_active:
            return redirect("/admin/login/")

        # Wrong role entirely — block
        allowed_roles = ["SUPER_ADMIN", "ADMIN", "MENTOR"]
        role = getattr(request.user, "role", None)
        if role not in allowed_roles:
            return redirect("/admin/login/")

        # Not staff — block
        if not request.user.is_staff:
            return redirect("/admin/login/")

        # ── MENTOR-specific path restrictions ──────────────────────
        if role == "MENTOR":
            # Block forbidden paths first
            for blocked in self.MENTOR_BLOCKED:
                if path.startswith(blocked):
                    return redirect("/admin/")

            # Allow only whitelisted prefixes
            allowed = any(path.startswith(p) for p in self.MENTOR_ALLOWED)
            if not allowed:
                return redirect("/admin/")

        return self.get_response(request)