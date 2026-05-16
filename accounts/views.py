from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()


def redirect_by_role(user):
    if user.role in ["SUPER_ADMIN", "superadmin", "ADMIN"]:
        return redirect("/admin/")
    elif user.role == "MENTOR":
        return redirect("/admin/")
    else:
        return redirect("/admin/no-access/")


def no_access_view(request):
    return redirect("/admin/login/")