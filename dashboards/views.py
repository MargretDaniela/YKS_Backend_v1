
# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .decorators import role_required  # we'll add this below

@login_required
@role_required("student")
def student_dashboard(request):
    return render(request, "dashboards/student.html")

@login_required
@role_required("mentor")
def mentor_dashboard(request):
    return render(request, "dashboards/mentor.html")

@login_required
@role_required("admin")
def admin_dashboard(request):
    return render(request, "dashboards/admin.html")

@login_required
@role_required("superadmin")
def superadmin_dashboard(request):
    return render(request, "dashboards/superadmin.html")