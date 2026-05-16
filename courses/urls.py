
# # C:\Users\Admin\Desktop\TheYKSApp\courses\urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     # ── 📚 COURSE LIST & DETAIL ─────────────────────────────────
#     path('courses/', views.courses_list_api, name='course-list'),
#     path('courses/<int:pk>/', views.course_detail_api, name='course-detail'),
    
#     # ── 📖 CURRICULUM & LESSONS ─────────────────────────────────
#     path('courses/<int:pk>/curriculum/', views.course_curriculum_api, name='course-curriculum'),
    
#     # ── ⭐ REVIEWS ──────────────────────────────────────────────
#     path('courses/<int:pk>/reviews/', views.course_reviews_api, name='course-reviews'),
    
#     # ── 🎓 ENROLLMENTS ─────────────────────────────────────────
#     path('enrollments/', views.my_enrollments_api, name='my-enrollments'),
    
#     # ── 📂 CATEGORIES ──────────────────────────────────────────
#     path('categories/', views.categories_api, name='categories'),
# ]

from django.urls import path
from . import views, api

app_name = 'courses'

urlpatterns = [
    # ── 📚 COURSES & CATEGORIES (Student/Public) ───────────────────────
    path('courses/',                        views.courses_list,           name='courses-list'),
    path('courses/<int:course_id>/',        views.course_detail,          name='course-detail'),
    path('courses/<int:course_id>/curriculum/', views.course_curriculum_api, name='course-curriculum'),
    path('categories/',                     views.categories_api,         name='categories'),

    # ── 🎓 ENROLLMENTS (Student) ───────────────────────────────────────
    path('enrollments/',                    views.my_enrollments,         name='my-enrollments'),
    path('enroll/',                         views.enroll,                 name='enroll'),

    # ── 📊 PROGRESS TRACKING (Student) ─────────────────────────────────
    path('progress/',                       views.mark_lesson_progress,   name='mark-progress'),
    path('progress/<int:course_id>/',       views.course_progress,        name='course-progress'),

    # ── ⭐ REVIEWS (Student/Public) ────────────────────────────────────
    path('courses/<int:course_id>/reviews/', views.course_reviews,        name='course-reviews'),

    # ── 📥 VIDEO DOWNLOADS (Student) ───────────────────────────────────
    path('lessons/<int:lesson_id>/download-info/', views.lesson_download_info, name='lesson-download-info'),

    # ── 🛠️ LESSON MANAGEMENT (Mentor/Admin Only) ──────────────────────
    # These endpoints were missing from your original urls.py
    path('lessons/<int:lesson_id>/upload-video/',  api.upload_lesson_video,    name='upload-lesson-video'),
    path('lessons/<int:lesson_id>/set-url/',       api.set_lesson_video_url,   name='set-lesson-video-url'),
    path('courses/<int:course_id>/create-lesson/', api.create_lesson,          name='create-lesson'),
    path('lessons/<int:lesson_id>/update/',        api.update_lesson,          name='update-lesson'),
]