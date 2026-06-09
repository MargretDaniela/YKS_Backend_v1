
# from django.urls import path
# from . import views, api

# app_name = 'courses'

# urlpatterns = [
#     # ── 📚 COURSES & CATEGORIES (Student/Public) ───────────────────────
#     path('courses/',                        views.courses_list,           name='courses-list'),
#     path('courses/<int:course_id>/',        views.course_detail,          name='course-detail'),
#     path('courses/<int:course_id>/curriculum/', views.course_curriculum_api, name='course-curriculum'),
#     path('categories/',                     views.categories_api,         name='categories'),

#     # ── 🎓 ENROLLMENTS (Student) ───────────────────────────────────────
#     path('enrollments/',                    views.my_enrollments,         name='my-enrollments'),
#     path('enroll/',                         views.enroll,                 name='enroll'),

#     # ── 📊 PROGRESS TRACKING (Student) ─────────────────────────────────
#     path('progress/',                       views.mark_lesson_progress,   name='mark-progress'),
#     path('progress/<int:course_id>/',       views.course_progress,        name='course-progress'),

#     # ── ⭐ REVIEWS (Student/Public) ────────────────────────────────────
#     path('courses/<int:course_id>/reviews/', views.course_reviews,        name='course-reviews'),

#     # ── 📥 VIDEO DOWNLOADS (Student) ───────────────────────────────────
#     path('lessons/<int:lesson_id>/download-info/', views.lesson_download_info, name='lesson-download-info'),

#     # ── 🛠️ LESSON MANAGEMENT (Mentor/Admin Only) ──────────────────────
#     # These endpoints were missing from your original urls.py
#     path('lessons/<int:lesson_id>/upload-video/',  api.upload_lesson_video,    name='upload-lesson-video'),
#     path('lessons/<int:lesson_id>/set-url/',       api.set_lesson_video_url,   name='set-lesson-video-url'),
#     path('courses/<int:course_id>/create-lesson/', api.create_lesson,          name='create-lesson'),
#     path('lessons/<int:lesson_id>/update/',        api.update_lesson,          name='update-lesson'),
# ]

"""
courses/urls.py
===============
Include in your project urls.py:
    path('', include('courses.urls')),
"""

from django.urls import path
from . import api, views

urlpatterns = [

    # ==================================================================
    #  PUBLIC REST API  — consumed by the Flutter app
    # ==================================================================

    path('api/courses/',
         api.courses_list_api,
         name='api_courses_list'),

    path('api/courses/<int:pk>/',
         api.course_detail_api,
         name='api_course_detail'),

    # Curriculum: returns modules + lessons + module video + resource link
    path('api/courses/<int:pk>/curriculum/',
         api.course_curriculum_api,
         name='api_course_curriculum'),

    path('api/courses/<int:pk>/reviews/',
         api.course_reviews_api,
         name='api_course_reviews'),

    path('api/categories/',
         api.categories_api,
         name='api_categories'),

    path('api/my-enrollments/',
         api.my_enrollments_api,
         name='api_my_enrollments'),


    # ==================================================================
    #  DASHBOARD REST API  — Flutter admin panel / JS dashboard
    # ==================================================================

    # ── Courses ───────────────────────────────────────────────────────
    path('api/dashboard/courses/',
         api.dashboard_courses_list,
         name='api_dashboard_courses_list'),

    path('api/dashboard/courses/create/',
         api.dashboard_create_course,
         name='api_dashboard_create_course'),

    path('api/dashboard/courses/<int:pk>/update/',
         api.dashboard_update_course,
         name='api_dashboard_update_course'),

    path('api/dashboard/courses/<int:pk>/delete/',
         api.dashboard_delete_course,
         name='api_dashboard_delete_course'),

    path('api/dashboard/courses/<int:course_id>/curriculum/',
         api.dashboard_full_curriculum,
         name='api_dashboard_full_curriculum'),

    # ── Modules ───────────────────────────────────────────────────────
    path('api/dashboard/courses/<int:course_id>/modules/',
         api.dashboard_modules_list,
         name='api_dashboard_modules_list'),

    path('api/dashboard/courses/<int:course_id>/modules/create/',
         api.dashboard_create_module,
         name='api_dashboard_create_module'),

    path('api/dashboard/courses/<int:course_id>/modules/reorder/',
         api.dashboard_reorder_modules,
         name='api_dashboard_reorder_modules'),

    path('api/dashboard/modules/<int:module_id>/update/',
         api.dashboard_update_module,
         name='api_dashboard_update_module'),

    path('api/dashboard/modules/<int:module_id>/delete/',
         api.dashboard_delete_module,
         name='api_dashboard_delete_module'),

    # Module video — upload file from device
    path('api/dashboard/modules/<int:module_id>/upload-video/',
         api.upload_module_video,
         name='api_upload_module_video'),

    # Module video — set external URL
    path('api/dashboard/modules/<int:module_id>/set-video-url/',
         api.set_module_video_url,
         name='api_set_module_video_url'),

    # Module resource link — set any external URL
    path('api/dashboard/modules/<int:module_id>/set-resource-link/',
         api.set_module_resource_link,
         name='api_set_module_resource_link'),

    # ── Lessons ───────────────────────────────────────────────────────
    path('api/dashboard/modules/<int:module_id>/lessons/',
         api.dashboard_lessons_list,
         name='api_dashboard_lessons_list'),

    path('api/dashboard/modules/<int:module_id>/lessons/create/',
         api.dashboard_create_lesson,
         name='api_dashboard_create_lesson'),

    path('api/dashboard/modules/<int:module_id>/lessons/reorder/',
         api.dashboard_reorder_lessons,
         name='api_dashboard_reorder_lessons'),

    path('api/dashboard/lessons/<int:lesson_id>/update/',
         api.dashboard_update_lesson,
         name='api_dashboard_update_lesson'),

    path('api/dashboard/lessons/<int:lesson_id>/delete/',
         api.dashboard_delete_lesson,
         name='api_dashboard_delete_lesson'),

    # Lesson video — upload file from device
    path('api/dashboard/lessons/<int:lesson_id>/upload-video/',
         api.upload_lesson_video,
         name='api_upload_lesson_video'),

    # Lesson video — set external URL
    path('api/dashboard/lessons/<int:lesson_id>/set-video-url/',
         api.set_lesson_video_url,
         name='api_set_lesson_video_url'),


    # ==================================================================
    #  WEB DASHBOARD VIEWS  (HTML — browser-based admin panel)
    # ==================================================================

    path('dashboard/',
         views.dashboard_home,
         name='dashboard_home'),

    path('dashboard/courses/',
         views.dashboard_courses,
         name='dashboard_courses'),

    path('dashboard/courses/create/',
         views.dashboard_course_create,
         name='dashboard_course_create'),

    path('dashboard/courses/<int:pk>/',
         views.dashboard_course_detail,
         name='dashboard_course_detail'),

    path('dashboard/courses/<int:pk>/edit/',
         views.dashboard_course_edit,
         name='dashboard_course_edit'),

    path('dashboard/courses/<int:pk>/delete/',
         views.dashboard_course_delete,
         name='dashboard_course_delete'),

    # ── Module views ──────────────────────────────────────────────────
    path('dashboard/courses/<int:course_id>/modules/create/',
         views.dashboard_module_create,
         name='dashboard_module_create'),

    path('dashboard/modules/<int:module_id>/edit/',
         views.dashboard_module_edit,
         name='dashboard_module_edit'),

    path('dashboard/modules/<int:module_id>/delete/',
         views.dashboard_module_delete,
         name='dashboard_module_delete'),

    path('dashboard/courses/<int:course_id>/modules/reorder/',
         views.dashboard_modules_reorder,
         name='dashboard_modules_reorder'),

    # Module video upload (AJAX)
    path('dashboard/modules/<int:module_id>/upload-video/',
         views.dashboard_module_upload_video,
         name='dashboard_module_upload_video'),

    # Module set URL (AJAX)
    path('dashboard/modules/<int:module_id>/set-url/',
         views.dashboard_module_set_url,
         name='dashboard_module_set_url'),

    # Module resource link (AJAX)
    path('dashboard/modules/<int:module_id>/set-resource-link/',
         views.dashboard_module_set_resource_link,
         name='dashboard_module_set_resource_link'),

    # ── Lesson views ──────────────────────────────────────────────────
    path('dashboard/modules/<int:module_id>/lessons/create/',
         views.dashboard_lesson_create,
         name='dashboard_lesson_create'),

    path('dashboard/lessons/<int:lesson_id>/edit/',
         views.dashboard_lesson_edit,
         name='dashboard_lesson_edit'),

    path('dashboard/lessons/<int:lesson_id>/delete/',
         views.dashboard_lesson_delete,
         name='dashboard_lesson_delete'),

    path('dashboard/modules/<int:module_id>/lessons/reorder/',
         views.dashboard_lessons_reorder,
         name='dashboard_lessons_reorder'),

    path('dashboard/lessons/<int:lesson_id>/upload-video/',
         views.dashboard_lesson_upload_video,
         name='dashboard_lesson_upload_video'),

    path('dashboard/lessons/<int:lesson_id>/set-url/',
         views.dashboard_lesson_set_url,
         name='dashboard_lesson_set_url'),

    # ── Role redirect / no-access ─────────────────────────────────────
    path('admin/no-access/',
         views.no_access_view,
         name='no_access'),
]