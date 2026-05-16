from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.mentor_home, name="mentor_dashboard"),
]