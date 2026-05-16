from django.contrib.admin import AdminSite


class YouthKeyAdminSite(AdminSite):
    site_header = "Youth Key Series"
    site_title = "Youth Key Admin"
    index_title = "Dashboard"

    def has_permission(self, request):
        if not request.user.is_authenticated:
            return False
        if not request.user.is_active:
            return False
        return request.user.role in ["SUPER_ADMIN", "superadmin", "ADMIN", "MENTOR"]