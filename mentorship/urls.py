# C:\Users\Admin\Desktop\TheYKSApp\mentorship\urls.py
from django.urls import path
from . import api

urlpatterns = [
    # 🎥 Videos
    path('videos/', api.video_list_api, name='mentor-videos'),
    
    # 📅 Sessions & Bookings
    path('sessions/', api.session_list_api, name='mentor-sessions'),
    path('bookings/', api.booking_list_api, name='mentor-bookings'),
]