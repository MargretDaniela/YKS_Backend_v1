
# # C:\Users\Admin\Desktop\TheYKSApp\TheYKSApp\urls.py
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),

#     # ✅ Auth & User Management (Login, Register, Forgot Password, etc.)
#     path('accounts/api/', include('accounts.urls')),

#     # ✅ Course Management (List, Detail, Curriculum, Reviews, Enrollments)
#     path('courses/api/', include('courses.urls')),

#     # ✅ Home Page Content (Banners, Featured Sections, etc.)
#     path('pages/api/', include('pages.urls')),
# ]

# # ✅ Serve media & static files during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# C:\Users\Admin\Desktop\TheYKSApp\yks_config\urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/api/', include('accounts.urls')),  # ✅ Prefix handles /accounts/api/
    path('courses/api/', include('courses.urls')),
    path('pages/api/', include('pages.urls')),
    path('mentorship/api/', include('mentorship.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)