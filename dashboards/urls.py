from django.urls import path
from . import views

urlpatterns = [
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("mentor/", views.mentor_dashboard, name="mentor_dashboard"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("superadmin/", views.superadmin_dashboard, name="superadmin_dashboard"),
]