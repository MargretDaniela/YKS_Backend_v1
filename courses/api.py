
# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status

# from .models import Course, Module as Section, Lesson, Review, Enrollment
# from .serializers import LessonSerializer


# # ======================================================================
# #  HELPER — Build standardized course dict for API responses
# # ======================================================================
# def _course_dict(course, request=None):
#     # Thumbnail URL
#     thumbnail_url = None
#     if course.thumbnail:
#         thumbnail_url = (
#             request.build_absolute_uri(course.thumbnail.url)
#             if request else course.thumbnail.url
#         )

#     # Category (FK safe)
#     cat_obj = course.category
#     cat_name = getattr(cat_obj, 'name', 'General') if cat_obj else 'General'

#     # Instructor & Bio
#     trainer = getattr(course, 'trainer', None)
#     instructor_name = (
#         getattr(trainer, 'full_name', None) or getattr(trainer, 'email', 'Youth K.E.Y')
#         if trainer else (course.instructor or 'Youth K.E.Y')
#     )
#     instructor_bio = course.instructor_bio or (
#         f"{instructor_name} is a highly experienced coach helping youth across Africa, "
#         f"specialising in {cat_name.lower()}."
#     )

#     # Pricing & Stats
#     price_val = float(getattr(course, 'price', course.amount) or 0)
#     avg_rating = course.get_average_rating()
#     review_count = course.reviews.count()
#     student_count = course.get_student_count()
#     learning_points = course.get_learning_points()

#     return {
#         'id':               course.pk,
#         'title':            course.title,
#         'description':      course.description,
#         'category':         cat_name,
#         'instructor':       instructor_name,
#         'instructor_bio':   instructor_bio,
#         'price':            f'US${price_val:.2f}',
#         'price_raw':        price_val,
#         'is_live':          course.is_live,
#         'is_published':     course.is_published,
#         'start_date':       str(course.start_date) if course.start_date else None,
#         'end_date':         str(course.end_date) if course.end_date else None,
#         'recording_url':    course.recording_url or '',
#         'thumbnail':        thumbnail_url,
#         'learning_points':  learning_points,
#         'avg_rating':       avg_rating,
#         'review_count':     review_count,
#         'student_count':    student_count,
#     }


# # ======================================================================
# #  COURSE LIST
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def courses_list_api(request):
#     courses = Course.objects.filter(is_published=True).select_related('category', 'trainer').order_by('-created_at')
#     grouped = {}
#     for course in courses:
#         cat = course.category.name if course.category else 'General'
#         if cat not in grouped:
#             grouped[cat] = []
#         grouped[cat].append(_course_dict(course, request))

#     return Response({
#         'success': True,
#         'categories': [
#             {'category': cat, 'courses': courses_list}
#             for cat, courses_list in grouped.items()
#         ],
#     })


# # ======================================================================
# #  COURSE DETAIL
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def course_detail_api(request, pk):
#     course = get_object_or_404(
#         Course.objects.select_related('category', 'trainer'),
#         pk=pk, is_published=True
#     )
#     return Response({'success': True, 'course': _course_dict(course, request)})


# # ======================================================================
# #  CURRICULUM
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def course_curriculum_api(request, pk):
#     try:
#         sections = Section.objects.filter(course_id=pk).prefetch_related('lessons').order_by('order')
#         data = [{
#             'id': s.id,
#             'title': s.title,
#             'order': s.order,
#             'lessons': [{
#                 'id': l.id,
#                 'name': l.title,
#                 'duration': l.duration,
#                 'free': l.is_free,
#                 'order': l.order,
#             } for l in s.lessons.all().order_by('order')]
#         } for s in sections]
#         return Response({'success': True, 'sections': data})
#     except Exception as e:
#         return Response({'success': False, 'sections': [], 'error': str(e)})


# # ======================================================================
# #  REVIEWS — GET + POST
# # ======================================================================
# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def course_reviews_api(request, pk):
#     # ── GET: return all reviews ───────────────────────────────────────
#     if request.method == 'GET':
#         try:
#             reviews = Review.objects.filter(course_id=pk).select_related('student').order_by('-created_at')
#             data = [{
#                 'id':         r.id,
#                 'user_name':  getattr(r.student, 'full_name', None) or r.student.email,
#                 'rating':     r.rating,
#                 'comment':    r.comment,
#                 'created_at': str(r.created_at.date()),
#             } for r in reviews]
#             return Response({'success': True, 'reviews': data})
#         except Exception as e:
#             return Response({'success': False, 'reviews': [], 'error': str(e)})

#     # ── POST: submit a review (must be enrolled + 2 lessons done) ─────
#     if not request.user.is_authenticated:
#         return Response({'success': False, 'error': 'Login required.'}, status=status.HTTP_401_UNAUTHORIZED)

#     try:
#         enrollment = Enrollment.objects.get(student=request.user, course_id=pk)
#     except Enrollment.DoesNotExist:
#         return Response({'success': False, 'error': 'You must be enrolled to review this course.'},
#                         status=status.HTTP_403_FORBIDDEN)

#     if not enrollment.can_review():
#         return Response({'success': False, 'error': 'Complete at least 2 lessons before reviewing.'},
#                         status=status.HTTP_403_FORBIDDEN)

#     rating = request.data.get('rating')
#     comment = request.data.get('comment', '').strip()

#     if not rating or not comment:
#         return Response({'success': False, 'error': 'Rating and comment required.'},
#                         status=status.HTTP_400_BAD_REQUEST)

#     review, created = Review.objects.update_or_create(
#         course_id=pk, student=request.user,
#         defaults={'rating': int(rating), 'comment': comment}
#     )

#     return Response({
#         'success': True,
#         'message': 'Review submitted!' if created else 'Review updated!',
#         'review': {
#             'id':         review.id,
#             'user_name':  getattr(request.user, 'full_name', None) or request.user.email,
#             'rating':     review.rating,
#             'comment':    review.comment,
#             'created_at': str(review.created_at.date()),
#         }
#     }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# # ======================================================================
# #  MY ENROLLMENTS
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def my_enrollments_api(request):
#     enrollments = (
#         Enrollment.objects
#         .filter(student=request.user)
#         .select_related('course__category', 'course__trainer')
#     )
#     data = []
#     for enr in enrollments:
#         course_data = _course_dict(enr.course, request)
#         course_data.update({
#             'enrollment_id':       enr.pk,
#             'payment_status':      enr.payment_status,
#             'progress_percentage': enr.progress_percentage,
#             'completed_lessons':   enr.completed_lessons,
#             'completed':           enr.completed,
#             'can_review':          enr.can_review(),
#         })
#         data.append(course_data)

#     return Response({'success': True, 'enrollments': data})


# # ======================================================================
# #  CATEGORIES
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def categories_api(request):
#     categories = (
#         Course.objects.filter(is_published=True)
#         .values_list('category__name', flat=True)
#         .distinct()
#         .order_by('category__name')
#     )
#     clean_cats = [c for c in categories if c]
#     return Response({'success': True, 'categories': clean_cats})


# # ======================================================================
# #  LESSON MANAGEMENT (Admin/Mentor Only)
# # ======================================================================
# def _check_role(request):
#     return getattr(request.user, 'role', None) in ['MENTOR', 'ADMIN', 'SUPER_ADMIN']

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def upload_lesson_video(request, lesson_id):
#     """Handle video file upload for a lesson"""
#     if not _check_role(request):
#         return Response({'success': False, 'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
#     if 'video' not in request.FILES:
#         return Response({'success': False, 'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     video_file = request.FILES['video']
#     lesson.video_file.save(f'lesson_{lesson_id}_{video_file.name}', video_file)
#     lesson.video_type = Lesson.VideoType.UPLOAD
#     lesson.save()

#     return Response({
#         'success': True,
#         'video_url': request.build_absolute_uri(lesson.video_file.url) if request else lesson.video_file.url,
#         'file_id': lesson.video_file.name,
#     })


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def set_lesson_video_url(request, lesson_id):
#     """Set external video URL for a lesson"""
#     if not _check_role(request):
#         return Response({'success': False, 'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     lesson.video_url = request.data.get('video_url', '')
#     lesson.video_type = request.data.get('video_type', Lesson.VideoType.URL)
#     lesson.save()

#     return Response({'success': True, 'video_url': lesson.video_url})


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_lesson(request, course_id):
#     """Create a new lesson for a course"""
#     if not _check_role(request):
#         return Response({'success': False, 'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

#     # Lesson belongs to a Module, not directly to a Course in merged schema
#     module_id = request.data.get('module_id')
#     if not module_id:
#         module = Module.objects.filter(course_id=course_id).first()
#         if not module:
#             return Response({'success': False, 'error': 'No module found for this course. Create a module first.'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         module_id = module.id

#     data = request.data.copy()
#     data['module'] = module_id

#     serializer = LessonSerializer(data=data)
#     if serializer.is_valid():
#         lesson = serializer.save()
#         return Response({'success': True, 'lesson': LessonSerializer(lesson).data}, status=status.HTTP_201_CREATED)
#     return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
# def update_lesson(request, lesson_id):
#     """Update lesson details"""
#     if not _check_role(request):
#         return Response({'success': False, 'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     serializer = LessonSerializer(lesson, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'success': True, 'lesson': serializer.data})
#     return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

"""
courses/api.py
==============
REST API — Youth K.E.Y Series platform.

Key update: _module_dict() now returns:
  • video_url        — absolute URL of the module video (uploaded or external)
  • video_type       — 'upload' | 'url' | 'none'
  • has_video        — bool shortcut
  • resource_link    — any URL (YouTube, TikTok, PDF …)
  • resource_link_label — button label for the resource link
  • has_resource_link — bool shortcut

Role matrix
-----------
SUPER_ADMIN  full access, including delete
ADMIN        create/edit all courses; assign mentors; cannot delete
MENTOR       create/edit/delete only their own courses & lessons
STUDENT      read-only public endpoints only
"""

import os

from django.shortcuts import get_object_or_404
from django.db        import transaction
from rest_framework.decorators  import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers     import MultiPartParser, FormParser, JSONParser
from rest_framework.response    import Response
from rest_framework             import status

from .models import (
    Course, Module, Lesson, Review, Enrollment,
    Category, LessonProgress, Section,
)
from .serializers import LessonSerializer


# ======================================================================
#  ROLE CONSTANTS & GUARDS
# ======================================================================
SUPER_ADMIN = 'SUPER_ADMIN'
ADMIN       = 'ADMIN'
MENTOR      = 'MENTOR'
STUDENT     = 'STUDENT'
STAFF_ROLES = {SUPER_ADMIN, ADMIN, MENTOR}


def _role(user):
    return getattr(user, 'role', STUDENT)

def _is_staff(user):          return _role(user) in STAFF_ROLES
def _is_admin_or_above(user): return _role(user) in {SUPER_ADMIN, ADMIN}
def _is_super_admin(user):    return _role(user) == SUPER_ADMIN

def _can_edit_course(user, course):
    r = _role(user)
    if r in {SUPER_ADMIN, ADMIN}: return True
    if r == MENTOR:               return course.trainer_id == user.pk
    return False

def _staff_check(request):
    if not request.user.is_authenticated or not _is_staff(request.user):
        return Response({'success': False, 'error': 'Permission denied.'},
                        status=status.HTTP_403_FORBIDDEN)
    return None


# ======================================================================
#  DICT BUILDERS
# ======================================================================

def _course_dict(course, request=None):
    thumbnail_url = None
    if course.thumbnail:
        thumbnail_url = (
            request.build_absolute_uri(course.thumbnail.url)
            if request else course.thumbnail.url
        )
    cat_obj  = course.category
    cat_name = getattr(cat_obj, 'name', 'General') if cat_obj else 'General'
    trainer  = getattr(course, 'trainer', None)
    instructor_name = (
        getattr(trainer, 'full_name', None) or getattr(trainer, 'email', 'Youth K.E.Y')
        if trainer else (course.instructor or 'Youth K.E.Y')
    )
    instructor_bio = course.instructor_bio or (
        f"{instructor_name} is a highly experienced coach helping youth "
        f"across Africa, specialising in {cat_name.lower()}."
    )
    price_val     = float(getattr(course, 'price', course.amount) or 0)
    avg_rating    = course.get_average_rating()
    review_count  = course.reviews.count()
    student_count = course.get_student_count()

    return {
        'id':              course.pk,
        'title':           course.title,
        'description':     course.description,
        'category':        cat_name,
        'instructor':      instructor_name,
        'instructor_bio':  instructor_bio,
        'price':           f'US${price_val:.2f}',
        'amount':          price_val,
        'is_live':         course.is_live,
        'is_published':    course.is_published,
        'start_date':      str(course.start_date) if course.start_date else None,
        'end_date':        str(course.end_date)   if course.end_date   else None,
        'recording_url':   course.recording_url or '',
        'thumbnail':       thumbnail_url,
        'learning_points': course.get_learning_points(),
        'avg_rating':      avg_rating,
        'review_count':    review_count,
        'student_count':   student_count,
        'trainer_id':      course.trainer_id,
    }


def _lesson_dict(lesson, request=None):
    return {
        'id':             lesson.pk,
        'title':          lesson.title,
        'order':          lesson.order,
        'duration':       lesson.duration,
        'is_free':        lesson.is_free,
        'free':           lesson.is_free,   # Flutter alias
        'video_type':     lesson.video_type,
        'video_url':      lesson.video_url,
        'video_file_url': lesson.get_video_url(request),
        'allow_download': lesson.allow_download,
        'module_id':      lesson.module_id,
    }


def _module_dict(module, request=None):
    """
    Returns full module data including:
      - video_url / has_video   — so Flutter can play the module video
      - resource_link           — any external URL the instructor set
      - resource_link_label     — button text for the link
    """
    lessons = module.lessons.all().order_by('order')

    # Build absolute video URL
    video_url = module.get_video_url(request)

    return {
        'id':                   module.pk,
        'title':                module.title,
        'description':          module.description,
        'order':                module.order,
        # ── Video ─────────────────────────────────────────────────
        'video_type':           module.video_type,
        'video_url':            video_url,
        'has_video':            module.has_video,
        # ── Resource link ─────────────────────────────────────────
        'resource_link':        module.resource_link or '',
        'resource_link_label':  module.effective_resource_label or '',
        'has_resource_link':    module.has_resource_link,
        # ── Lessons ───────────────────────────────────────────────
        'lessons':              [_lesson_dict(l, request) for l in lessons],
    }


# ======================================================================
#  PUBLIC — COURSE LIST
# ======================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def courses_list_api(request):
    courses = (
        Course.objects
        .filter(is_published=True)
        .select_related('category', 'trainer')
        .order_by('-created_at')
    )
    grouped = {}
    for course in courses:
        cat = course.category.name if course.category else 'General'
        grouped.setdefault(cat, []).append(_course_dict(course, request))

    return Response({
        'success':    True,
        'categories': [
            {'category': cat, 'courses': items}
            for cat, items in grouped.items()
        ],
    })


# ======================================================================
#  PUBLIC — COURSE DETAIL
# ======================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def course_detail_api(request, pk):
    course = get_object_or_404(
        Course.objects.select_related('category', 'trainer'),
        pk=pk, is_published=True,
    )
    return Response({'success': True, 'course': _course_dict(course, request)})


# ======================================================================
#  PUBLIC — CURRICULUM  (modules + lessons + module video + resource link)
# ======================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def course_curriculum_api(request, pk):
    try:
        modules = (
            Module.objects
            .filter(course_id=pk)
            .prefetch_related('lessons')
            .order_by('order')
        )
        return Response({
            'success':  True,
            'sections': [_module_dict(m, request) for m in modules],
        })
    except Exception as e:
        return Response({'success': False, 'sections': [], 'error': str(e)})


# ======================================================================
#  PUBLIC — REVIEWS  /  STUDENT — POST REVIEW
# ======================================================================
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def course_reviews_api(request, pk):
    if request.method == 'GET':
        try:
            reviews = (
                Review.objects
                .filter(course_id=pk)
                .select_related('student')
                .order_by('-created_at')
            )
            data = [{
                'id':         r.pk,
                'user_name':  getattr(r.student, 'full_name', None) or r.student.email,
                'rating':     r.rating,
                'comment':    r.comment,
                'created_at': str(r.created_at.date()),
            } for r in reviews]
            return Response({'success': True, 'reviews': data})
        except Exception as e:
            return Response({'success': False, 'reviews': [], 'error': str(e)})

    if not request.user.is_authenticated:
        return Response({'success': False, 'error': 'Login required.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    try:
        enrollment = Enrollment.objects.get(student=request.user, course_id=pk)
    except Enrollment.DoesNotExist:
        return Response({'success': False, 'error': 'You must be enrolled to review.'},
                        status=status.HTTP_403_FORBIDDEN)

    if not enrollment.can_review():
        return Response({'success': False,
                         'error': 'Complete at least 2 lessons before reviewing.'},
                        status=status.HTTP_403_FORBIDDEN)

    rating  = request.data.get('rating')
    comment = request.data.get('comment', '').strip()
    if not rating or not comment:
        return Response({'success': False, 'error': 'Rating and comment are required.'},
                        status=status.HTTP_400_BAD_REQUEST)

    review, created = Review.objects.update_or_create(
        course_id=pk, student=request.user,
        defaults={'rating': int(rating), 'comment': comment},
    )
    return Response({
        'success': True,
        'message': 'Review submitted!' if created else 'Review updated!',
        'review': {
            'id':         review.pk,
            'user_name':  getattr(request.user, 'full_name', None) or request.user.email,
            'rating':     review.rating,
            'comment':    review.comment,
            'created_at': str(review.created_at.date()),
        },
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# ======================================================================
#  STUDENT — MY ENROLLMENTS
# ======================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_enrollments_api(request):
    enrollments = (
        Enrollment.objects
        .filter(student=request.user)
        .select_related('course__category', 'course__trainer')
    )
    data = []
    for enr in enrollments:
        cd = _course_dict(enr.course, request)
        cd.update({
            'enrollment_id':       enr.pk,
            'payment_status':      enr.payment_status,
            'progress_percentage': enr.progress_percentage,
            'completed_lessons':   enr.completed_lessons,
            'completed':           enr.completed,
            'can_review':          enr.can_review(),
        })
        data.append(cd)
    return Response({'success': True, 'enrollments': data})


# ======================================================================
#  PUBLIC — CATEGORIES
# ======================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def categories_api(request):
    cats = (
        Course.objects
        .filter(is_published=True)
        .values_list('category__name', flat=True)
        .distinct()
        .order_by('category__name')
    )
    return Response({'success': True, 'categories': [c for c in cats if c]})


# ======================================================================
#  DASHBOARD — COURSE LIST
# ======================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_courses_list(request):
    err = _staff_check(request)
    if err: return err

    qs = Course.objects.select_related('category', 'trainer').order_by('-created_at')
    if _role(request.user) == MENTOR:
        qs = qs.filter(trainer=request.user)

    return Response({'success': True, 'courses': [_course_dict(c, request) for c in qs]})


# ======================================================================
#  DASHBOARD — CREATE COURSE
# ======================================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def dashboard_create_course(request):
    err = _staff_check(request)
    if err: return err

    from django.contrib.auth import get_user_model
    User = get_user_model()

    data        = request.data
    category_id = data.get('category_id') or data.get('category')
    try:
        category = Category.objects.get(pk=category_id)
    except (Category.DoesNotExist, ValueError, TypeError):
        return Response({'success': False, 'error': 'Valid category_id is required.'}, status=400)

    trainer = request.user if _role(request.user) == MENTOR else None
    if _is_admin_or_above(request.user) and data.get('trainer_id'):
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
        amount               = data.get('amount', 0),
        currency             = data.get('currency', 'USD'),
        is_live              = data.get('is_live', False) in [True, 'true', '1'],
        is_published         = (
            data.get('is_published', False) in [True, 'true', '1']
            and _is_admin_or_above(request.user)
        ),
        recording_url        = data.get('recording_url', ''),
        trainer              = trainer,
    )
    if 'thumbnail' in request.FILES:
        course.thumbnail = request.FILES['thumbnail']
        course.save()

    return Response(
        {'success': True, 'message': 'Course created.', 'course': _course_dict(course, request)},
        status=201,
    )


# ======================================================================
#  DASHBOARD — UPDATE COURSE  (thumbnail same pattern as module video)
# ======================================================================
@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def dashboard_update_course(request, pk):
    err = _staff_check(request)
    if err: return err

    course = get_object_or_404(Course, pk=pk)
    if not _can_edit_course(request.user, course):
        return Response({'success': False, 'error': 'You can only edit your own courses.'},
                        status=status.HTTP_403_FORBIDDEN)

    data = request.data
    for field in ['title', 'description', 'instructor', 'instructor_bio',
                  'learning_points_text', 'amount', 'currency', 'recording_url']:
        if field in data:
            setattr(course, field, data[field])

    if 'is_live' in data:
        course.is_live = data['is_live'] in [True, 'true', '1']
    if 'is_published' in data and _is_admin_or_above(request.user):
        course.is_published = data['is_published'] in [True, 'true', '1']
    if 'category_id' in data:
        try:
            course.category = Category.objects.get(pk=data['category_id'])
        except Category.DoesNotExist:
            pass

    if 'thumbnail' in request.FILES:
        if course.thumbnail:
            try:
                old = course.thumbnail.path
                if os.path.isfile(old): os.remove(old)
            except Exception:
                pass
        course.thumbnail = request.FILES['thumbnail']

    course.save()
    return Response({'success': True, 'course': _course_dict(course, request)})


# ======================================================================
#  DASHBOARD — DELETE COURSE  (SUPER_ADMIN only)
# ======================================================================
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def dashboard_delete_course(request, pk):
    if not request.user.is_authenticated or not _is_super_admin(request.user):
        return Response({'success': False, 'error': 'Only Super-Admins can delete courses.'},
                        status=status.HTTP_403_FORBIDDEN)
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return Response({'success': True, 'message': 'Course deleted.'})


# ======================================================================
#  DASHBOARD — FULL CURRICULUM
# ======================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_full_curriculum(request, course_id):
    err = _staff_check(request)
    if err: return err

    course = get_object_or_404(Course, pk=course_id)
    if _role(request.user) == MENTOR and course.trainer_id != request.user.pk:
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    modules = Module.objects.filter(course=course).prefetch_related('lessons').order_by('order')
    return Response({
        'success': True,
        'course':  _course_dict(course, request),
        'modules': [_module_dict(m, request) for m in modules],
    })


# ======================================================================
#  DASHBOARD — MODULE MANAGEMENT
# ======================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_modules_list(request, course_id):
    err = _staff_check(request)
    if err: return err

    course = get_object_or_404(Course, pk=course_id)
    if _role(request.user) == MENTOR and course.trainer_id != request.user.pk:
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    modules = Module.objects.filter(course=course).prefetch_related('lessons').order_by('order')
    return Response({'success': True, 'modules': [_module_dict(m, request) for m in modules]})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def dashboard_create_module(request, course_id):
    err = _staff_check(request)
    if err: return err

    course = get_object_or_404(Course, pk=course_id)
    if not _can_edit_course(request.user, course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    data       = request.data
    last_order = (
        Module.objects.filter(course=course)
        .order_by('-order').values_list('order', flat=True).first()
    ) or 0
    next_order = int(data.get('order', last_order + 1))

    module = Module.objects.create(
        course       = course,
        title        = data.get('title', f'Module {next_order}').strip(),
        description  = data.get('description', '').strip(),
        order        = next_order,
        video_type   = data.get('video_type', Module.VideoType.NONE),
        video_url    = data.get('video_url', '').strip(),
        resource_link       = data.get('resource_link', '').strip(),
        resource_link_label = data.get('resource_link_label', '').strip(),
    )

    # Video file upload — same pattern as thumbnail
    if 'video_file' in request.FILES:
        module.video_file.save(
            request.FILES['video_file'].name,
            request.FILES['video_file'],
            save=False,
        )
        module.video_type = Module.VideoType.UPLOAD
        module.save()

    return Response(
        {'success': True, 'message': 'Module created.', 'module': _module_dict(module, request)},
        status=201,
    )


@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def dashboard_update_module(request, module_id):
    err = _staff_check(request)
    if err: return err

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_course(request.user, module.course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    data = request.data
    if 'title'               in data: module.title               = data['title'].strip()
    if 'description'         in data: module.description         = data['description'].strip()
    if 'order'               in data: module.order               = int(data['order'])
    if 'resource_link'       in data: module.resource_link       = data['resource_link'].strip()
    if 'resource_link_label' in data: module.resource_link_label = data['resource_link_label'].strip()

    # External video URL
    if 'video_url' in data:
        module.video_url  = data['video_url'].strip()
        module.video_type = Module.VideoType.URL
        module.video_file = None   # clear uploaded file reference

    # Video file upload — same pattern as thumbnail replacement
    if 'video_file' in request.FILES:
        if module.video_file:
            try:
                old = module.video_file.path
                if os.path.isfile(old): os.remove(old)
            except Exception:
                pass
        module.video_file.save(
            request.FILES['video_file'].name,
            request.FILES['video_file'],
            save=False,
        )
        module.video_type = Module.VideoType.UPLOAD
        module.video_url  = ''

    module.save()
    return Response({'success': True, 'module': _module_dict(module, request)})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def dashboard_delete_module(request, module_id):
    err = _staff_check(request)
    if err: return err

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_course(request.user, module.course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    module.delete()
    return Response({'success': True, 'message': 'Module deleted.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dashboard_reorder_modules(request, course_id):
    err = _staff_check(request)
    if err: return err

    course = get_object_or_404(Course, pk=course_id)
    if not _can_edit_course(request.user, course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    items = request.data.get('order', [])
    with transaction.atomic():
        for item in items:
            Module.objects.filter(pk=item['id'], course_id=course_id).update(order=item['order'])
    return Response({'success': True, 'message': 'Modules reordered.'})


# ======================================================================
#  DASHBOARD — MODULE VIDEO UPLOAD  (dedicated endpoint)
# ======================================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_module_video(request, module_id):
    """
    Upload a video file from device storage to a module.
    Field name: 'video'
    Same pattern as course thumbnail upload.
    """
    err = _staff_check(request)
    if err: return err

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_course(request.user, module.course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    if 'video' not in request.FILES:
        return Response({'success': False, 'error': 'No video file provided.'}, status=400)

    video_file    = request.FILES['video']
    allowed_types = [
        'video/mp4', 'video/webm', 'video/ogg', 'video/quicktime',
        'video/x-msvideo', 'video/x-matroska', 'video/mpeg',
    ]
    if video_file.content_type not in allowed_types:
        return Response(
            {'success': False, 'error': f'Unsupported video type: {video_file.content_type}'},
            status=400)

    # Delete old uploaded file
    if module.video_file:
        try:
            old = module.video_file.path
            if os.path.isfile(old): os.remove(old)
        except Exception:
            pass

    module.video_file.save(video_file.name, video_file, save=False)
    module.video_type = Module.VideoType.UPLOAD
    module.video_url  = ''
    module.save()

    return Response({
        'success':   True,
        'message':   'Module video uploaded.',
        'video_url': request.build_absolute_uri(module.video_file.url),
        'module':    _module_dict(module, request),
    })


# ======================================================================
#  DASHBOARD — MODULE SET EXTERNAL VIDEO URL
# ======================================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_module_video_url(request, module_id):
    """Set an external video URL for a module (YouTube, Vimeo, CDN …)."""
    err = _staff_check(request)
    if err: return err

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_course(request.user, module.course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    url = (request.data.get('video_url') or '').strip()
    if not url:
        return Response({'success': False, 'error': 'video_url is required.'}, status=400)

    module.video_url  = url
    module.video_type = Module.VideoType.URL
    module.video_file = None
    module.save()

    return Response({'success': True, 'message': 'Module video URL set.', 'module': _module_dict(module, request)})


# ======================================================================
#  DASHBOARD — MODULE SET RESOURCE LINK
# ======================================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_module_resource_link(request, module_id):
    """
    Set or clear the resource link for a module.
    Body: { "resource_link": "https://...", "resource_link_label": "Watch on YouTube" }
    Both fields optional — send empty string to clear.
    """
    err = _staff_check(request)
    if err: return err

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_course(request.user, module.course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    module.resource_link       = (request.data.get('resource_link')       or '').strip()
    module.resource_link_label = (request.data.get('resource_link_label') or '').strip()
    module.save()

    return Response({'success': True, 'message': 'Resource link updated.', 'module': _module_dict(module, request)})


# ======================================================================
#  DASHBOARD — LESSON MANAGEMENT
# ======================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_lessons_list(request, module_id):
    err = _staff_check(request)
    if err: return err

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_course(request.user, module.course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    lessons = Lesson.objects.filter(module=module).order_by('order')
    return Response({'success': True, 'lessons': [_lesson_dict(l, request) for l in lessons]})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dashboard_create_lesson(request, module_id):
    err = _staff_check(request)
    if err: return err

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_course(request.user, module.course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    data       = request.data
    last_order = (
        Lesson.objects.filter(module=module)
        .order_by('-order').values_list('order', flat=True).first()
    ) or 0
    next_order = int(data.get('order', last_order + 1))

    lesson = Lesson.objects.create(
        module         = module,
        title          = data.get('title', f'Lesson {next_order}').strip(),
        order          = next_order,
        duration       = data.get('duration', '00:00'),
        is_free        = data.get('is_free', False) in [True, 'true', '1'],
        allow_download = data.get('allow_download', False) in [True, 'true', '1'],
        video_type     = data.get('video_type', Lesson.VideoType.URL),
        video_url      = data.get('video_url', '').strip(),
    )
    return Response(
        {'success': True, 'message': 'Lesson created.', 'lesson': _lesson_dict(lesson, request)},
        status=201,
    )


@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def dashboard_update_lesson(request, lesson_id):
    err = _staff_check(request)
    if err: return err

    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if not _can_edit_course(request.user, lesson.module.course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    data = request.data
    if 'title'          in data: lesson.title          = data['title'].strip()
    if 'order'          in data: lesson.order          = int(data['order'])
    if 'duration'       in data: lesson.duration       = data['duration']
    if 'is_free'        in data: lesson.is_free        = data['is_free'] in [True, 'true', '1']
    if 'allow_download' in data: lesson.allow_download = data['allow_download'] in [True, 'true', '1']
    if 'video_url'      in data:
        lesson.video_url  = data['video_url'].strip()
        lesson.video_type = Lesson.VideoType.URL
    if 'module_id'      in data: lesson.module_id      = int(data['module_id'])
    lesson.save()
    return Response({'success': True, 'lesson': _lesson_dict(lesson, request)})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def dashboard_delete_lesson(request, lesson_id):
    err = _staff_check(request)
    if err: return err

    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if not _can_edit_course(request.user, lesson.module.course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    if lesson.video_file:
        try:
            if os.path.isfile(lesson.video_file.path):
                os.remove(lesson.video_file.path)
        except Exception:
            pass
    lesson.delete()
    return Response({'success': True, 'message': 'Lesson deleted.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dashboard_reorder_lessons(request, module_id):
    err = _staff_check(request)
    if err: return err

    module = get_object_or_404(Module, pk=module_id)
    if not _can_edit_course(request.user, module.course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    items = request.data.get('order', [])
    with transaction.atomic():
        for item in items:
            Lesson.objects.filter(pk=item['id'], module_id=module_id).update(order=item['order'])
    return Response({'success': True, 'message': 'Lessons reordered.'})


# ======================================================================
#  DASHBOARD — LESSON VIDEO UPLOAD
# ======================================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_lesson_video(request, lesson_id):
    err = _staff_check(request)
    if err: return err

    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if not _can_edit_course(request.user, lesson.module.course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    if 'video' not in request.FILES:
        return Response({'success': False, 'error': 'No video file provided.'}, status=400)

    video_file    = request.FILES['video']
    allowed_types = [
        'video/mp4', 'video/webm', 'video/ogg', 'video/quicktime',
        'video/x-msvideo', 'video/x-matroska', 'video/mpeg',
    ]
    if video_file.content_type not in allowed_types:
        return Response(
            {'success': False, 'error': f'Unsupported video type: {video_file.content_type}'},
            status=400)

    if lesson.video_file:
        try:
            old = lesson.video_file.path
            if os.path.isfile(old): os.remove(old)
        except Exception:
            pass

    lesson.video_file.save(video_file.name, video_file, save=False)
    lesson.video_type = Lesson.VideoType.UPLOAD
    lesson.video_url  = ''
    lesson.save()

    return Response({
        'success':        True,
        'message':        'Lesson video uploaded.',
        'video_file_url': request.build_absolute_uri(lesson.video_file.url),
        'lesson':         _lesson_dict(lesson, request),
    })


# ======================================================================
#  DASHBOARD — LESSON SET EXTERNAL VIDEO URL
# ======================================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_lesson_video_url(request, lesson_id):
    err = _staff_check(request)
    if err: return err

    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if not _can_edit_course(request.user, lesson.module.course):
        return Response({'success': False, 'error': 'Permission denied.'}, status=403)

    url = (request.data.get('video_url') or '').strip()
    if not url:
        return Response({'success': False, 'error': 'video_url is required.'}, status=400)

    lesson.video_url  = url
    lesson.video_type = request.data.get('video_type', Lesson.VideoType.URL)
    lesson.video_file = None
    lesson.save()

    return Response({'success': True, 'message': 'Lesson video URL set.', 'lesson': _lesson_dict(lesson, request)})


# ======================================================================
#  LEGACY ENDPOINTS  (backward-compat)
# ======================================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lesson(request, course_id):
    err = _staff_check(request)
    if err: return err

    module_id = request.data.get('module_id')
    if not module_id:
        module = Module.objects.filter(course_id=course_id).first()
        if not module:
            return Response({'success': False, 'error': 'No module found. Create a module first.'}, status=400)
        module_id = module.pk

    data = request.data.copy()
    data['module'] = module_id
    serializer = LessonSerializer(data=data)
    if serializer.is_valid():
        lesson = serializer.save()
        return Response({'success': True, 'lesson': LessonSerializer(lesson).data}, status=201)
    return Response({'success': False, 'errors': serializer.errors}, status=400)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_lesson(request, lesson_id):
    err = _staff_check(request)
    if err: return err

    lesson     = get_object_or_404(Lesson, pk=lesson_id)
    serializer = LessonSerializer(lesson, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'lesson': serializer.data})
    return Response({'success': False, 'errors': serializer.errors}, status=400)