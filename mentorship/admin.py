from django.contrib import admin

# Register your models here.
from .models import MentorshipSession, Booking

admin.site.register(MentorshipSession)
admin.site.register(Booking)