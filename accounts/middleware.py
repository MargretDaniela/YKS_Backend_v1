from django.shortcuts import redirect


class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    ALLOWED_PATHS = [
        "/admin/login/",
        "/admin/logout/",
        "/admin/jsi18n/",
        "/admin/password_reset/",
        "/admin/password_reset/done/",
    ]

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            # Always allow static files and auth pages
            if (request.path in self.ALLOWED_PATHS
                    or request.path.startswith("/admin/static/")
                    or request.path.startswith("/static/")):
                return self.get_response(request)

            # Not logged in at all
            if not request.user.is_authenticated:
                return redirect(f"/admin/login/?next={request.path}")

            # Logged in but session expired or invalid
            if not request.user.is_active:
                return redirect("/admin/login/")

            # Wrong role — block access
            allowed_roles = ["SUPER_ADMIN", "superadmin", "ADMIN", "MENTOR"]
            if not hasattr(request.user, 'role') or request.user.role not in allowed_roles:
                return redirect("/admin/login/")

            # Not staff — block access
            if not request.user.is_staff:
                return redirect("/admin/login/")

        return self.get_response(request)