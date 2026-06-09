
# from django.http import FileResponse, Http404
# from django.utils import timezone
# from django.shortcuts import get_object_or_404
# import os   # ✅ FIX ADDED (VERY IMPORTANT)

# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.response import Response

# from .api import _course_dict  

# from .models import (
#     Category, Course, Module, Lesson,
#     Enrollment, LessonProgress, Review, Section,
# )

# from .serializers import (
#     CategoryWithCoursesSerializer,
#     CourseDetailSerializer,
#     EnrollmentSerializer,
#     EnrollSerializer,
#     MarkLessonDoneSerializer,
#     LessonProgressSerializer,
#     ReviewSerializer,
#     LessonDownloadSerializer,
# )

# # ======================================================================
# #  COURSES & CATEGORIES
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def courses_list(request):
#     categories = Category.objects.prefetch_related(
#         'courses__learning_points',
#         'courses__modules__lessons',
#         'courses__reviews',
#         'courses__enrollments',
#     ).filter(courses__is_published=True).distinct()

#     serializer = CategoryWithCoursesSerializer(
#         categories, many=True, context={'request': request}
#     )
#     return Response({'success': True, 'categories': serializer.data})


# # ======================================================================
# #  COURSE DETAIL
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def course_detail(request, course_id):
#     course = get_object_or_404(
#         Course.objects.prefetch_related(
#             'learning_points',
#             'modules__lessons',
#             'reviews__student',
#             'enrollments',
#         ),
#         id=course_id, is_published=True
#     )
#     serializer = CourseDetailSerializer(course, context={'request': request})
#     return Response({'success': True, 'course': serializer.data})


# # ======================================================================
# #  CATEGORIES
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def categories_api(request):
#     categories = Course.objects.filter(
#         is_published=True
#     ).values_list('category__name', flat=True).distinct().order_by('category__name')

#     clean_cats = [c for c in categories if c]
#     return Response({'success': True, 'categories': clean_cats})


# # ======================================================================
# #  CURRICULUM
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def course_curriculum_api(request, pk):
#     course = get_object_or_404(Course, id=pk, is_published=True)

#     sections = Module.objects.filter(course=course).prefetch_related(
#         'lessons'
#     ).order_by('order')

#     data = []
#     for s in sections:
#         data.append({
#             'id': s.id,
#             'title': s.title,
#             'description': s.description,
#             'order': s.order,
#             'lessons': [
#                 {
#                     'id': l.id,
#                     'name': l.title,
#                     'duration': l.duration,
#                     'free': l.is_free,
#                     'order': l.order,
#                 }
#                 for l in s.lessons.all()
#             ]
#         })

#     return Response({'success': True, 'course_id': pk, 'sections': data})


# # ======================================================================
# #  ENROLLMENTS
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def my_enrollments(request):
#     enrollments = Enrollment.objects.filter(
#         student=request.user, is_active=True
#     ).select_related(
#         'course__category', 'course__trainer'
#     ).prefetch_related(
#         'lesson_progress', 'course__modules__lessons'
#     )

#     serializer = EnrollmentSerializer(
#         enrollments, many=True, context={'request': request}
#     )
#     return Response({'success': True, 'enrollments': serializer.data})


# # ======================================================================
# #  ENROLL
# # ======================================================================
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def enroll(request):
#     ser = EnrollSerializer(data=request.data)
#     ser.is_valid(raise_exception=True)

#     course = get_object_or_404(
#         Course,
#         id=ser.validated_data['course_id'],
#         is_published=True
#     )

#     enrollment, created = Enrollment.objects.get_or_create(
#         student=request.user,
#         course=course,
#         defaults={'is_active': True}
#     )

#     if not created and not enrollment.is_active:
#         enrollment.is_active = True
#         enrollment.save()

#     if created:
#         lessons = Lesson.objects.filter(module__course=course)

#         LessonProgress.objects.bulk_create([
#             LessonProgress(enrollment=enrollment, lesson=lesson)
#             for lesson in lessons
#         ], ignore_conflicts=True)

#         Course.objects.filter(id=course.id).update(
#             student_count=course.student_count + 1
#         )

#     return Response({
#         'success': True,
#         'message': 'Enrolled successfully' if created else 'Already enrolled',
#         'enrollment_id': enrollment.id,
#     }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# # ======================================================================
# #  PROGRESS
# # ======================================================================
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def mark_lesson_progress(request):
#     ser = MarkLessonDoneSerializer(data=request.data)
#     ser.is_valid(raise_exception=True)

#     lesson = get_object_or_404(Lesson, id=ser.validated_data['lesson_id'])

#     # SAFE FIX (prevents crash if module is missing)
#     course = lesson.module.course if lesson.module else None

#     enrollment = get_object_or_404(
#         Enrollment,
#         student=request.user,
#         course=course,
#         is_active=True,
#     )

#     progress, _ = LessonProgress.objects.get_or_create(
#         enrollment=enrollment,
#         lesson=lesson
#     )

#     progress.is_completed = ser.validated_data['is_completed']
#     progress.last_position = ser.validated_data.get('last_position', 0)

#     if progress.is_completed and not progress.completed_at:
#         progress.completed_at = timezone.now()

#     progress.save()

#     return Response({
#         'success': True,
#         'lesson_id': lesson.id,
#         'is_completed': progress.is_completed,
#         'last_position': progress.last_position,
#         'course_progress': enrollment.progress_percentage,
#     })


# # ======================================================================
# #  COURSE PROGRESS
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def course_progress(request, course_id):
#     enrollment = get_object_or_404(
#         Enrollment,
#         student=request.user,
#         course_id=course_id,
#         is_active=True,
#     )

#     progress_records = LessonProgress.objects.filter(
#         enrollment=enrollment
#     ).select_related('lesson').order_by('lesson__order')

#     return Response({
#         'success': True,
#         'course_id': course_id,
#         'progress_percentage': enrollment.progress_percentage,
#         'lessons': [
#             {
#                 'lesson_id': p.lesson_id,
#                 'title': p.lesson.title,
#                 'is_completed': p.is_completed,
#                 'last_position': p.last_position,
#                 'completed_at': p.completed_at,
#             }
#             for p in progress_records
#         ],
#     })


# # ======================================================================
# #  REVIEWS
# # ======================================================================
# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def course_reviews(request, course_id):
#     course = get_object_or_404(Course, id=course_id, is_published=True)

#     if request.method == 'GET':
#         reviews = course.reviews.select_related('student').order_by('-created_at')
#         ser = ReviewSerializer(reviews, many=True, context={'request': request})

#         return Response({
#             'success': True,
#             'avg_rating': course.avg_rating,
#             'review_count': course.review_count,
#             'reviews': ser.data,
#         })

#     if not request.user.is_authenticated:
#         return Response(
#             {'success': False, 'error': 'Authentication required'},
#             status=status.HTTP_401_UNAUTHORIZED
#         )

#     enrollment = Enrollment.objects.filter(
#         student=request.user,
#         course=course,
#         is_active=True
#     ).first()

#     if not enrollment:
#         return Response(
#             {'success': False, 'error': 'You must be enrolled to review'},
#             status=status.HTTP_403_FORBIDDEN
#         )

#     if not enrollment.can_review():
#         return Response(
#             {'success': False, 'error': 'Complete at least 2 lessons before reviewing.'},
#             status=status.HTTP_403_FORBIDDEN
#         )

#     ser = ReviewSerializer(data=request.data, context={'request': request})
#     ser.is_valid(raise_exception=True)

#     review, created = Review.objects.update_or_create(
#         course=course,
#         student=request.user,
#         defaults={
#             'rating': ser.validated_data['rating'],
#             'comment': ser.validated_data.get('comment', ''),
#         }
#     )

#     return Response({
#         'success': True,
#         'message': 'Review submitted!' if created else 'Review updated!',
#         'review': ReviewSerializer(review).data,
#     })


# # ======================================================================
# #  LESSON DOWNLOAD INFO (FIXED MISSING VIEW)
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def lesson_download_info(request, lesson_id):
#     lesson = get_object_or_404(Lesson, id=lesson_id)

#     course = lesson.module.course if lesson.module else None

#     # Check enrollment
#     is_enrolled = Enrollment.objects.filter(
#         student=request.user,
#         course=course,
#         is_active=True
#     ).exists()

#     if not is_enrolled:
#         return Response({
#             'success': False,
#             'error': 'Enrollment required'
#         }, status=status.HTTP_403_FORBIDDEN)

#     return Response({
#         'success': True,
#         'lesson_id': lesson.id,
#         'title': lesson.title,
#         'allow_download': lesson.allow_download,
#         'video_type': lesson.video_type,
#         'download_available': lesson.allow_download and lesson.video_file is not None,
#     })

"""
courses/views.py
================
HTML dashboard views — role-aware throughout.

New in this version:
  • dashboard_module_edit handles video_file upload + video_url + resource_link
  • dashboard_module_upload_video  — AJAX endpoint for module video
  • dashboard_module_set_url       — AJAX endpoint for module external URL
  • dashboard_module_set_resource_link — AJAX endpoint for resource link
"""

import os
import json

from django.shortcuts               import render, redirect, get_object_or_404
from django.contrib                 import messages
from django.contrib.auth            import get_user_model
from django.http                    import JsonResponse
from django.views.decorators.http   import require_POST

from .models import Course, Module, Lesson, Category, Enrollment, Review

User = get_user_model()

SUPER_ADMIN = 'SUPER_ADMIN'
ADMIN       = 'ADMIN'
MENTOR      = 'MENTOR'
STUDENT     = 'STUDENT'
STAFF_ROLES = {SUPER_ADMIN, ADMIN, MENTOR}


# ======================================================================
#  ROLE HELPERS
# ======================================================================
def _role(user):             return getattr(user, 'role', STUDENT)
def _is_super_admin(user):   return _role(user) == SUPER_ADMIN
def _is_admin(user):         return _role(user) == ADMIN
def _is_mentor(user):        return _role(user) == MENTOR
def _is_staff(user):         return _role(user) in STAFF_ROLES

def _require_staff(request):
    if not request.user.is_authenticated:
        return redirect(f'/admin/login/?next={request.path}')
    if not _is_staff(request.user):
        return redirect('/admin/no-access/')
    return None

def _can_edit_course(user, course):
    r = _role(user)
    if r in {SUPER_ADMIN, ADMIN}: return True
    if r == MENTOR:               return course.trainer == user
    return False

def _can_edit_module(user, module):
    return _can_edit_course(user, module.course)


# ======================================================================
#  ROLE REDIRECTS
# ======================================================================
def redirect_by_role(user):
    if _role(user) in {SUPER_ADMIN, ADMIN, MENTOR}:
        return redirect('/admin/')
    return redirect('/admin/no-access/')

def no_access_view(request):
    return redirect('/admin/login/')


# ======================================================================
#  DASHBOARD HOME
# ======================================================================
def dashboard_home(request):
    guard = _require_staff(request)
    if guard: return guard

    user = request.user
    qs   = (Course.objects.filter(trainer=user) if _is_mentor(user)
            else Course.objects.select_related('category').order_by('-created_at'))

    return render(request, 'dashboard/home.html', {
        'courses':        qs,
        'total_courses':  qs.count(),
        'published':      qs.filter(is_published=True).count(),
        'live':           qs.filter(is_live=True).count(),
        'total_students': Enrollment.objects.filter(
            course__in=qs, payment_status='paid').count(),
        'is_super_admin': _is_super_admin(user),
        'is_admin':       _is_admin(user),
        'is_mentor':      _is_mentor(user),
    })


# ======================================================================
#  COURSE LIST
# ======================================================================
def dashboard_courses(request):
    guard = _require_staff(request)
    if guard: return guard

    user = request.user
    qs   = (Course.objects.filter(trainer=user).select_related('category', 'trainer')
            if _is_mentor(user)
            else Course.objects.select_related('category', 'trainer').order_by('-created_at'))

    return render(request, 'dashboard/courses/list.html', {
        'courses':        qs,
        'is_super_admin': _is_super_admin(user),
        'is_admin':       _is_admin(user),
        'is_mentor':      _is_mentor(user),
    })


# ======================================================================
#  CREATE COURSE
# ======================================================================
def dashboard_course_create(request):
    guard = _require_staff(request)
    if guard: return guard

    categories = Category.objects.order_by('name')
    user       = request.user

    if request.method == 'POST':
        data = request.POST
        try:
            category = Category.objects.get(pk=data.get('category_id'))
        except (Category.DoesNotExist, ValueError):
            messages.error(request, 'Please select a valid category.')
            return render(request, 'dashboard/courses/form.html', {'categories': categories})

        trainer = user if _is_mentor(user) else None
        if not _is_mentor(user) and data.get('trainer_id'):
            try:
                trainer = User.objects.get(pk=data['trainer_id'], role=MENTOR)
            except User.DoesNotExist:
                pass

        course = Course.objects.create(
            category             = category,
            title                = data.get('title', '').strip(),
            description          = data.get('description', '').strip(),
            instructor           = data.get('instructor', '').strip(),
            instructor_bio       = data.get('instructor_bio', '').strip(),
            learning_points_text = data.get('learning_points_text', '').strip(),
            amount               = data.get('amount', 0) or 0,
            currency             = data.get('currency', 'USD'),
            is_live              = 'is_live' in data,
            is_published         = 'is_published' in data,
            recording_url        = data.get('recording_url', '').strip(),
            trainer              = trainer,
        )
        if 'thumbnail' in request.FILES:
            course.thumbnail = request.FILES['thumbnail']
            course.save()

        messages.success(request, f'Course "{course.title}" created.')
        return redirect('dashboard_course_detail', pk=course.pk)

    mentors = [] if _is_mentor(user) else User.objects.filter(role=MENTOR, is_active=True)
    return render(request, 'dashboard/courses/form.html', {
        'categories':     categories,
        'mentors':        mentors,
        'is_super_admin': _is_super_admin(user),
        'is_admin':       _is_admin(user),
    })


# ======================================================================
#  EDIT COURSE
# ======================================================================
def dashboard_course_edit(request, pk):
    guard = _require_staff(request)
    if guard: return guard

    course     = get_object_or_404(Course, pk=pk)
    user       = request.user
    categories = Category.objects.order_by('name')

    if not _can_edit_course(user, course):
        messages.error(request, 'You can only edit your own courses.')
        return redirect('dashboard_courses')

    if request.method == 'POST':
        data = request.POST
        if 'category_id' in data:
            try:
                course.category = Category.objects.get(pk=data['category_id'])
            except (Category.DoesNotExist, ValueError):
                pass

        course.title                = data.get('title',                course.title).strip()
        course.description          = data.get('description',          course.description).strip()
        course.instructor           = data.get('instructor',           course.instructor).strip()
        course.instructor_bio       = data.get('instructor_bio',       course.instructor_bio).strip()
        course.learning_points_text = data.get('learning_points_text', course.learning_points_text).strip()
        course.amount               = data.get('amount', course.amount) or 0
        course.currency             = data.get('currency', course.currency)
        course.is_live              = 'is_live' in data
        course.recording_url        = data.get('recording_url', course.recording_url).strip()

        if not _is_mentor(user):
            course.is_published = 'is_published' in data

        if 'thumbnail' in request.FILES:
            if course.thumbnail:
                try:
                    old = course.thumbnail.path
                    if os.path.isfile(old): os.remove(old)
                except Exception:
                    pass
            course.thumbnail = request.FILES['thumbnail']

        course.save()
        messages.success(request, f'Course "{course.title}" updated.')
        return redirect('dashboard_course_detail', pk=course.pk)

    mentors = [] if _is_mentor(user) else User.objects.filter(role=MENTOR, is_active=True)
    return render(request, 'dashboard/courses/form.html', {
        'course':         course,
        'categories':     categories,
        'mentors':        mentors,
        'editing':        True,
        'is_super_admin': _is_super_admin(user),
        'is_admin':       _is_admin(user),
        'is_mentor':      _is_mentor(user),
    })


# ======================================================================
#  COURSE DETAIL
# ======================================================================
def dashboard_course_detail(request, pk):
    guard = _require_staff(request)
    if guard: return guard

    course  = get_object_or_404(Course.objects.select_related('category'), pk=pk)
    user    = request.user

    if _is_mentor(user) and course.trainer != user:
        messages.error(request, 'You can only view your own courses.')
        return redirect('dashboard_courses')

    modules = Module.objects.filter(course=course).prefetch_related('lessons').order_by('order')
    return render(request, 'dashboard/courses/detail.html', {
        'course':         course,
        'modules':        modules,
        'can_edit':       _can_edit_course(user, course),
        'can_publish':    not _is_mentor(user),
        'is_super_admin': _is_super_admin(user),
        'is_admin':       _is_admin(user),
        'is_mentor':      _is_mentor(user),
    })


# ======================================================================
#  DELETE COURSE  — SUPER_ADMIN only
# ======================================================================
@require_POST
def dashboard_course_delete(request, pk):
    guard = _require_staff(request)
    if guard: return guard

    if not _is_super_admin(request.user):
        messages.error(request, 'Only Super-Admins can delete courses.')
        return redirect('dashboard_courses')

    course = get_object_or_404(Course, pk=pk)
    title  = course.title
    course.delete()
    messages.success(request, f'Course "{title}" deleted.')
    return redirect('dashboard_courses')


# ======================================================================
#  MODULE CREATE
# ======================================================================
def dashboard_module_create(request, course_id):
    guard = _require_staff(request)
    if guard: return guard

    course = get_object_or_404(Course, pk=course_id)
    if not _can_edit_course(request.user, course):
        messages.error(request, 'You can only add modules to your own courses.')
        return redirect('dashboard_courses')

    if request.method == 'POST':
        data       = request.POST
        last_order = (
            Module.objects.filter(course=course)
            .order_by('-order').values_list('order', flat=True).first()
        ) or 0

        module = Module(
            course       = course,
            title        = data.get('title', '').strip() or f'Module {last_order + 1}',
            description  = data.get('description', '').strip(),
            order        = int(data.get('order', last_order + 1)),
            video_type   = data.get('video_type', Module.VideoType.NONE),
            video_url    = data.get('video_url', '').strip(),
            resource_link       = data.get('resource_link', '').strip(),
            resource_link_label = data.get('resource_link_label', '').strip(),
        )
        module.save()

        # Video file upload — pick from device, same as thumbnail
        if 'video_file' in request.FILES and module.video_type == Module.VideoType.UPLOAD:
            _save_module_video(module, request.FILES['video_file'])

        messages.success(request, 'Module added.')
        return redirect('dashboard_course_detail', pk=course_id)

    return render(request, 'dashboard/modules/form.html', {
        'course': course, 'editing': False,
    })


# ======================================================================
#  MODULE EDIT
#  Handles: title/description/order, video file upload, video URL,
#           resource link + label
# ======================================================================
def dashboard_module_edit(request, module_id):
    guard = _require_staff(request)
    if guard: return guard

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_module(request.user, module):
        messages.error(request, 'You can only edit modules in your own courses.')
        return redirect('dashboard_courses')

    if request.method == 'POST':
        data = request.POST

        module.title       = data.get('title', module.title).strip()
        module.description = data.get('description', module.description).strip()
        module.order       = int(data.get('order', module.order))

        # Resource link (any URL — YouTube, TikTok, PDF, anything)
        module.resource_link       = data.get('resource_link',       '').strip()
        module.resource_link_label = data.get('resource_link_label', '').strip()

        new_video_type = data.get('video_type', module.video_type)
        module.video_type = new_video_type

        if new_video_type == Module.VideoType.URL:
            # Instructor pasted an external link
            module.video_url  = data.get('video_url', '').strip()
            module.video_file = None   # clear file reference

        elif new_video_type == Module.VideoType.UPLOAD:
            module.video_url = ''
            if 'video_file' in request.FILES:
                # Delete old file first
                if module.video_file:
                    try:
                        old = module.video_file.path
                        if os.path.isfile(old): os.remove(old)
                    except Exception:
                        pass
                _save_module_video(module, request.FILES['video_file'])

        elif new_video_type == Module.VideoType.NONE:
            module.video_url = ''
            # Keep existing file on disk but clear reference
            module.video_file = None

        module.save()
        messages.success(request, 'Module updated.')
        return redirect('dashboard_course_detail', pk=module.course_id)

    return render(request, 'dashboard/modules/form.html', {
        'module':  module,
        'course':  module.course,
        'editing': True,
    })


# ======================================================================
#  MODULE DELETE
# ======================================================================
@require_POST
def dashboard_module_delete(request, module_id):
    guard = _require_staff(request)
    if guard: return guard

    module    = get_object_or_404(Module, pk=module_id)
    course_id = module.course_id

    if not _can_edit_module(request.user, module):
        messages.error(request, 'You can only delete modules in your own courses.')
        return redirect('dashboard_courses')

    module.delete()
    messages.success(request, 'Module deleted.')
    return redirect('dashboard_course_detail', pk=course_id)


# ======================================================================
#  MODULE REORDER  (AJAX)
# ======================================================================
@require_POST
def dashboard_modules_reorder(request, course_id):
    guard = _require_staff(request)
    if guard:
        return JsonResponse({'success': False, 'error': 'Unauthorised'}, status=403)

    course = get_object_or_404(Course, pk=course_id)
    if not _can_edit_course(request.user, course):
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

    try:
        items = json.loads(request.body)
        for item in items:
            Module.objects.filter(pk=item['id'], course_id=course_id).update(order=item['order'])
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ======================================================================
#  MODULE VIDEO UPLOAD  (AJAX — returns JSON with new video URL)
# ======================================================================
@require_POST
def dashboard_module_upload_video(request, module_id):
    """
    Accepts multipart POST with field 'video_file'.
    Saves video, updates module.video_type = 'upload'.
    Returns JSON so the edit page can refresh the player without reloading.
    """
    guard = _require_staff(request)
    if guard:
        return JsonResponse({'success': False, 'error': 'Unauthorised'}, status=403)

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_module(request.user, module):
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

    if 'video_file' not in request.FILES:
        return JsonResponse({'success': False, 'error': 'No file provided.'}, status=400)

    video_file    = request.FILES['video_file']
    allowed_types = [
        'video/mp4', 'video/webm', 'video/ogg', 'video/quicktime',
        'video/x-msvideo', 'video/x-matroska', 'video/mpeg',
    ]
    if video_file.content_type not in allowed_types:
        return JsonResponse(
            {'success': False, 'error': f'Unsupported type: {video_file.content_type}'},
            status=400)

    if module.video_file:
        try:
            if os.path.isfile(module.video_file.path):
                os.remove(module.video_file.path)
        except Exception:
            pass

    _save_module_video(module, video_file)
    module.video_type = Module.VideoType.UPLOAD
    module.video_url  = ''
    module.save()

    return JsonResponse({
        'success':   True,
        'message':   'Video uploaded.',
        'video_url': request.build_absolute_uri(module.video_file.url),
    })


# ======================================================================
#  MODULE SET EXTERNAL URL  (AJAX)
# ======================================================================
@require_POST
def dashboard_module_set_url(request, module_id):
    """JSON POST: {"video_url": "https://..."}"""
    guard = _require_staff(request)
    if guard:
        return JsonResponse({'success': False, 'error': 'Unauthorised'}, status=403)

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_module(request.user, module):
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)

    url = (body.get('video_url') or '').strip()
    if not url:
        return JsonResponse({'success': False, 'error': 'video_url required.'}, status=400)

    module.video_url  = url
    module.video_type = Module.VideoType.URL
    module.video_file = None
    module.save()

    return JsonResponse({'success': True, 'message': 'URL saved.', 'video_url': url})


# ======================================================================
#  MODULE SET RESOURCE LINK  (AJAX)
# ======================================================================
@require_POST
def dashboard_module_set_resource_link(request, module_id):
    """
    JSON POST: {"resource_link": "https://...", "resource_link_label": "Watch on TikTok"}
    Both fields optional — send empty string to clear.
    """
    guard = _require_staff(request)
    if guard:
        return JsonResponse({'success': False, 'error': 'Unauthorised'}, status=403)

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_module(request.user, module):
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)

    module.resource_link       = (body.get('resource_link')       or '').strip()
    module.resource_link_label = (body.get('resource_link_label') or '').strip()
    module.save()

    return JsonResponse({
        'success':              True,
        'message':              'Resource link saved.',
        'resource_link':        module.resource_link,
        'resource_link_label':  module.effective_resource_label,
    })


# ======================================================================
#  LESSON CREATE
# ======================================================================
def dashboard_lesson_create(request, module_id):
    guard = _require_staff(request)
    if guard: return guard

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_module(request.user, module):
        messages.error(request, 'You can only add lessons to your own courses.')
        return redirect('dashboard_courses')

    if request.method == 'POST':
        data       = request.POST
        last_order = (
            Lesson.objects.filter(module=module)
            .order_by('-order').values_list('order', flat=True).first()
        ) or 0
        next_order = int(data.get('order', last_order + 1))
        video_type = data.get('video_type', Lesson.VideoType.URL)

        lesson = Lesson.objects.create(
            module         = module,
            title          = data.get('title', '').strip() or f'Lesson {next_order}',
            order          = next_order,
            duration       = data.get('duration', '00:00').strip(),
            is_free        = 'is_free' in data,
            allow_download = 'allow_download' in data,
            video_type     = video_type,
            video_url      = data.get('video_url', '').strip()
                             if video_type == Lesson.VideoType.URL else '',
        )

        if 'video_file' in request.FILES and video_type == Lesson.VideoType.UPLOAD:
            _save_lesson_video(lesson, request.FILES['video_file'])

        messages.success(request, f'Lesson "{lesson.title}" created.')
        return redirect('dashboard_course_detail', pk=module.course_id)

    return render(request, 'dashboard/lessons/form.html', {
        'module': module, 'course': module.course, 'editing': False,
    })


# ======================================================================
#  LESSON EDIT
# ======================================================================
def dashboard_lesson_edit(request, lesson_id):
    guard = _require_staff(request)
    if guard: return guard

    lesson = get_object_or_404(Lesson, pk=lesson_id)
    module = lesson.module

    if not _can_edit_module(request.user, module):
        messages.error(request, 'You can only edit lessons in your own courses.')
        return redirect('dashboard_courses')

    if request.method == 'POST':
        data = request.POST

        lesson.title          = data.get('title', lesson.title).strip()
        lesson.order          = int(data.get('order', lesson.order))
        lesson.duration       = data.get('duration', lesson.duration).strip()
        lesson.is_free        = 'is_free' in data
        lesson.allow_download = 'allow_download' in data

        new_video_type = data.get('video_type', lesson.video_type)
        lesson.video_type = new_video_type

        if new_video_type == Lesson.VideoType.URL:
            lesson.video_url  = data.get('video_url', '').strip()
            lesson.video_file = None
        elif new_video_type == Lesson.VideoType.UPLOAD:
            lesson.video_url = ''
            if 'video_file' in request.FILES:
                if lesson.video_file:
                    try:
                        old = lesson.video_file.path
                        if os.path.isfile(old): os.remove(old)
                    except Exception:
                        pass
                _save_lesson_video(lesson, request.FILES['video_file'])

        lesson.save()
        messages.success(request, f'Lesson "{lesson.title}" updated.')
        return redirect('dashboard_course_detail', pk=module.course_id)

    return render(request, 'dashboard/lessons/form.html', {
        'lesson':  lesson,
        'module':  module,
        'course':  module.course,
        'editing': True,
    })


# ======================================================================
#  LESSON DELETE
# ======================================================================
@require_POST
def dashboard_lesson_delete(request, lesson_id):
    guard = _require_staff(request)
    if guard: return guard

    lesson    = get_object_or_404(Lesson, pk=lesson_id)
    course_id = lesson.module.course_id

    if not _can_edit_module(request.user, lesson.module):
        messages.error(request, 'You can only delete lessons in your own courses.')
        return redirect('dashboard_courses')

    if lesson.video_file:
        try:
            if os.path.isfile(lesson.video_file.path):
                os.remove(lesson.video_file.path)
        except Exception:
            pass

    lesson.delete()
    messages.success(request, 'Lesson deleted.')
    return redirect('dashboard_course_detail', pk=course_id)


# ======================================================================
#  LESSON REORDER  (AJAX)
# ======================================================================
@require_POST
def dashboard_lessons_reorder(request, module_id):
    guard = _require_staff(request)
    if guard:
        return JsonResponse({'success': False, 'error': 'Unauthorised'}, status=403)

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_module(request.user, module):
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

    try:
        items = json.loads(request.body)
        for item in items:
            Lesson.objects.filter(pk=item['id'], module_id=module_id).update(order=item['order'])
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ======================================================================
#  LESSON VIDEO UPLOAD  (AJAX)
# ======================================================================
@require_POST
def dashboard_lesson_upload_video(request, lesson_id):
    guard = _require_staff(request)
    if guard:
        return JsonResponse({'success': False, 'error': 'Unauthorised'}, status=403)

    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if not _can_edit_module(request.user, lesson.module):
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

    if 'video_file' not in request.FILES:
        return JsonResponse({'success': False, 'error': 'No file provided.'}, status=400)

    video_file    = request.FILES['video_file']
    allowed_types = [
        'video/mp4', 'video/webm', 'video/ogg', 'video/quicktime',
        'video/x-msvideo', 'video/x-matroska', 'video/mpeg',
    ]
    if video_file.content_type not in allowed_types:
        return JsonResponse(
            {'success': False, 'error': f'Unsupported type: {video_file.content_type}'},
            status=400)

    if lesson.video_file:
        try:
            if os.path.isfile(lesson.video_file.path):
                os.remove(lesson.video_file.path)
        except Exception:
            pass

    _save_lesson_video(lesson, video_file)
    lesson.video_type = Lesson.VideoType.UPLOAD
    lesson.video_url  = ''
    lesson.save()

    return JsonResponse({
        'success':   True,
        'message':   'Video uploaded.',
        'video_url': request.build_absolute_uri(lesson.video_file.url),
    })


# ======================================================================
#  LESSON SET EXTERNAL URL  (AJAX)
# ======================================================================
@require_POST
def dashboard_lesson_set_url(request, lesson_id):
    guard = _require_staff(request)
    if guard:
        return JsonResponse({'success': False, 'error': 'Unauthorised'}, status=403)

    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if not _can_edit_module(request.user, lesson.module):
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)

    url = (body.get('video_url') or '').strip()
    if not url:
        return JsonResponse({'success': False, 'error': 'video_url required.'}, status=400)

    lesson.video_url  = url
    lesson.video_type = Lesson.VideoType.URL
    lesson.video_file = None
    lesson.save()

    return JsonResponse({'success': True, 'message': 'URL saved.', 'video_url': url})


# ======================================================================
#  PRIVATE HELPERS
# ======================================================================
def _save_module_video(module, uploaded_file):
    """Save an uploaded video file to the module."""
    module.video_file.save(uploaded_file.name, uploaded_file, save=False)


def _save_lesson_video(lesson, uploaded_file):
    """Save an uploaded video file to the lesson."""
    lesson.video_file.save(uploaded_file.name, uploaded_file, save=False)