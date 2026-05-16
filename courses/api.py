# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Course, Section, Review, Enrollment


# # ======================================================================
# #  HELPER — build course dict
# # ======================================================================
# def _course_dict(course, request=None):
#     thumbnail_url = None
#     if course.thumbnail:
#         thumbnail_url = (
#             request.build_absolute_uri(course.thumbnail.url)
#             if request else course.thumbnail.url
#         )

#     # ✅ Real rating from reviews
#     avg_rating     = course.get_average_rating()
#     review_count   = course.reviews.count()
#     student_count  = course.get_student_count()
#     learning_points = course.get_learning_points()

#     # ✅ Instructor info from trainer profile
#     trainer = course.trainer
#     instructor_name = getattr(trainer, 'full_name', None) or trainer.email
#     instructor_bio  = course.instructor_bio or (
#         f"{instructor_name} is a highly experienced coach helping youth across Africa, "
#         f"specialising in {course.category.lower()}."
#     )

#     return {
#         'id':               course.pk,
#         'title':            course.title,
#         'description':      course.description,
#         'category':         course.category,
#         'instructor':       instructor_name,
#         'instructor_bio':   instructor_bio,
#         'price':            f'US${float(course.price):.2f}',
#         'price_raw':        float(course.price),
#         'is_live':          course.is_live,
#         'start_date':       str(course.start_date),
#         'end_date':         str(course.end_date),
#         'recording_url':    course.recording_url or '',
#         'thumbnail':        thumbnail_url,
#         'learning_points':  learning_points,   # ✅ real
#         'avg_rating':       avg_rating,         # ✅ real
#         'review_count':     review_count,       # ✅ real
#         'student_count':    student_count,      # ✅ real
#     }


# # ======================================================================
# #  COURSE LIST
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def courses_list_api(request):
#     courses = Course.objects.filter(is_live=True).select_related('trainer')
#     grouped = {}
#     for course in courses:
#         cat = course.category or 'General'
#         if cat not in grouped:
#             grouped[cat] = []
#         grouped[cat].append(_course_dict(course, request))

#     return Response({
#         'success':    True,
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
#     try:
#         course = Course.objects.select_related('trainer').get(pk=pk, is_live=True)
#     except Course.DoesNotExist:
#         return Response({'success': False, 'error': 'Course not found.'},
#                         status=status.HTTP_404_NOT_FOUND)

#     return Response({'success': True, 'course': _course_dict(course, request)})


# # ======================================================================
# #  CURRICULUM
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def course_curriculum_api(request, pk):
#     try:
#         sections = Section.objects.filter(
#             course_id=pk).prefetch_related('lessons')
#         data = [{
#             'title': s.title,
#             'lessons': [{
#                 'name':     l.title,
#                 'duration': l.duration,
#                 'free':     l.is_free,
#             } for l in s.lessons.all()]
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
#             reviews = Review.objects.filter(
#                 course_id=pk).select_related('user')
#             data = [{
#                 'id':         r.id,
#                 'user_name':  getattr(r.user, 'full_name', None) or r.user.email,
#                 'rating':     r.rating,
#                 'comment':    r.comment,
#                 'created_at': str(r.created_at.date()),
#             } for r in reviews]
#             return Response({'success': True, 'reviews': data})
#         except Exception as e:
#             return Response({'success': False, 'reviews': [], 'error': str(e)})

#     # ── POST: submit a review (must be enrolled + 2 lessons done) ─────
#     if request.method == 'POST':
#         if not request.user.is_authenticated:
#             return Response({'success': False, 'error': 'Login required.'},
#                             status=status.HTTP_401_UNAUTHORIZED)
#         try:
#             enrollment = Enrollment.objects.get(
#                 user=request.user, course_id=pk)
#         except Enrollment.DoesNotExist:
#             return Response({
#                 'success': False,
#                 'error':   'You must be enrolled to review this course.'
#             }, status=status.HTTP_403_FORBIDDEN)

#         if not enrollment.can_review():
#             return Response({
#                 'success': False,
#                 'error':   'Complete at least 2 lessons before reviewing.'
#             }, status=status.HTTP_403_FORBIDDEN)

#         rating  = request.data.get('rating')
#         comment = request.data.get('comment', '').strip()

#         if not rating or not comment:
#             return Response({'success': False, 'error': 'Rating and comment required.'},
#                             status=status.HTTP_400_BAD_REQUEST)

#         review, created = Review.objects.update_or_create(
#             course_id=pk,
#             user=request.user,
#             defaults={'rating': int(rating), 'comment': comment},
#         )

#         return Response({
#             'success': True,
#             'message': 'Review submitted!' if created else 'Review updated!',
#             'review': {
#                 'id':         review.id,
#                 'user_name':  getattr(request.user, 'full_name', None) or request.user.email,
#                 'rating':     review.rating,
#                 'comment':    review.comment,
#                 'created_at': str(review.created_at.date()),
#             }
#         })


# # ======================================================================
# #  ENROLLMENTS
# # ======================================================================
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def my_enrollments_api(request):
#     enrollments = (
#         Enrollment.objects
#         .filter(user=request.user)
#         .select_related('course', 'course__trainer')
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
#         Course.objects.filter(is_live=True)
#         .values_list('category', flat=True)
#         .distinct()
#     )
#     return Response({'success': True, 'categories': list(categories)})

# # courses/api.py - Add these endpoints

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def upload_lesson_video(request, lesson_id):
#     """Handle video file upload for a lesson"""
#     if request.user.role not in ['MENTOR', 'ADMIN', 'SUPER_ADMIN']:
#         return Response({'error': 'Permission denied'}, status=403)
    
#     if 'video' not in request.FILES:
#         return Response({'error': 'No video file provided'}, status=400)
    
#     video_file = request.FILES['video']
#     lesson = get_object_or_404(Lesson, id=lesson_id)
    
#     # Save file to media/videos/
#     lesson.video_file.save(f'lesson_{lesson_id}_{video_file.name}', video_file)
#     lesson.video_type = 'uploaded'
#     lesson.save()
    
#     return Response({
#         'success': True,
#         'video_url': request.build_absolute_uri(lesson.video_file.url),
#         'file_id': lesson.video_file.name,
#     })


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def set_lesson_video_url(request, lesson_id):
#     """Set video URL for a lesson"""
#     if request.user.role not in ['MENTOR', 'ADMIN', 'SUPER_ADMIN']:
#         return Response({'error': 'Permission denied'}, status=403)
    
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     video_url = request.data.get('video_url')
#     video_type = request.data.get('video_type', 'direct')
    
#     lesson.video_url = video_url
#     lesson.video_type = video_type
#     lesson.save()
    
#     return Response({'success': True, 'video_url': video_url})


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_lesson(request, course_id):
#     """Create a new lesson for a course"""
#     if request.user.role not in ['MENTOR', 'ADMIN', 'SUPER_ADMIN']:
#         return Response({'error': 'Permission denied'}, status=403)
    
#     serializer = LessonSerializer(data=request.data)
#     if serializer.is_valid():
#         lesson = serializer.save(course_id=course_id)
#         return Response(LessonSerializer(lesson).data, status=201)
#     return Response(serializer.errors, status=400)


# @api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
# def update_lesson(request, lesson_id):
#     """Update lesson details"""
#     if request.user.role not in ['MENTOR', 'ADMIN', 'SUPER_ADMIN']:
#         return Response({'error': 'Permission denied'}, status=403)
    
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     serializer = LessonSerializer(lesson, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=400)

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Course, Module as Section, Lesson, Review, Enrollment
from .serializers import LessonSerializer


# ======================================================================
#  HELPER — Build standardized course dict for API responses
# ======================================================================
def _course_dict(course, request=None):
    # Thumbnail URL
    thumbnail_url = None
    if course.thumbnail:
        thumbnail_url = (
            request.build_absolute_uri(course.thumbnail.url)
            if request else course.thumbnail.url
        )

    # Category (FK safe)
    cat_obj = course.category
    cat_name = getattr(cat_obj, 'name', 'General') if cat_obj else 'General'

    # Instructor & Bio
    trainer = getattr(course, 'trainer', None)
    instructor_name = (
        getattr(trainer, 'full_name', None) or getattr(trainer, 'email', 'Youth K.E.Y')
        if trainer else (course.instructor or 'Youth K.E.Y')
    )
    instructor_bio = course.instructor_bio or (
        f"{instructor_name} is a highly experienced coach helping youth across Africa, "
        f"specialising in {cat_name.lower()}."
    )

    # Pricing & Stats
    price_val = float(getattr(course, 'price', course.amount) or 0)
    avg_rating = course.get_average_rating()
    review_count = course.reviews.count()
    student_count = course.get_student_count()
    learning_points = course.get_learning_points()

    return {
        'id':               course.pk,
        'title':            course.title,
        'description':      course.description,
        'category':         cat_name,
        'instructor':       instructor_name,
        'instructor_bio':   instructor_bio,
        'price':            f'US${price_val:.2f}',
        'price_raw':        price_val,
        'is_live':          course.is_live,
        'is_published':     course.is_published,
        'start_date':       str(course.start_date) if course.start_date else None,
        'end_date':         str(course.end_date) if course.end_date else None,
        'recording_url':    course.recording_url or '',
        'thumbnail':        thumbnail_url,
        'learning_points':  learning_points,
        'avg_rating':       avg_rating,
        'review_count':     review_count,
        'student_count':    student_count,
    }


# ======================================================================
#  COURSE LIST
# ======================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def courses_list_api(request):
    courses = Course.objects.filter(is_published=True).select_related('category', 'trainer').order_by('-created_at')
    grouped = {}
    for course in courses:
        cat = course.category.name if course.category else 'General'
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(_course_dict(course, request))

    return Response({
        'success': True,
        'categories': [
            {'category': cat, 'courses': courses_list}
            for cat, courses_list in grouped.items()
        ],
    })


# ======================================================================
#  COURSE DETAIL
# ======================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def course_detail_api(request, pk):
    course = get_object_or_404(
        Course.objects.select_related('category', 'trainer'),
        pk=pk, is_published=True
    )
    return Response({'success': True, 'course': _course_dict(course, request)})


# ======================================================================
#  CURRICULUM
# ======================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def course_curriculum_api(request, pk):
    try:
        sections = Section.objects.filter(course_id=pk).prefetch_related('lessons').order_by('order')
        data = [{
            'id': s.id,
            'title': s.title,
            'order': s.order,
            'lessons': [{
                'id': l.id,
                'name': l.title,
                'duration': l.duration,
                'free': l.is_free,
                'order': l.order,
            } for l in s.lessons.all().order_by('order')]
        } for s in sections]
        return Response({'success': True, 'sections': data})
    except Exception as e:
        return Response({'success': False, 'sections': [], 'error': str(e)})


# ======================================================================
#  REVIEWS — GET + POST
# ======================================================================
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def course_reviews_api(request, pk):
    # ── GET: return all reviews ───────────────────────────────────────
    if request.method == 'GET':
        try:
            reviews = Review.objects.filter(course_id=pk).select_related('student').order_by('-created_at')
            data = [{
                'id':         r.id,
                'user_name':  getattr(r.student, 'full_name', None) or r.student.email,
                'rating':     r.rating,
                'comment':    r.comment,
                'created_at': str(r.created_at.date()),
            } for r in reviews]
            return Response({'success': True, 'reviews': data})
        except Exception as e:
            return Response({'success': False, 'reviews': [], 'error': str(e)})

    # ── POST: submit a review (must be enrolled + 2 lessons done) ─────
    if not request.user.is_authenticated:
        return Response({'success': False, 'error': 'Login required.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        enrollment = Enrollment.objects.get(student=request.user, course_id=pk)
    except Enrollment.DoesNotExist:
        return Response({'success': False, 'error': 'You must be enrolled to review this course.'},
                        status=status.HTTP_403_FORBIDDEN)

    if not enrollment.can_review():
        return Response({'success': False, 'error': 'Complete at least 2 lessons before reviewing.'},
                        status=status.HTTP_403_FORBIDDEN)

    rating = request.data.get('rating')
    comment = request.data.get('comment', '').strip()

    if not rating or not comment:
        return Response({'success': False, 'error': 'Rating and comment required.'},
                        status=status.HTTP_400_BAD_REQUEST)

    review, created = Review.objects.update_or_create(
        course_id=pk, student=request.user,
        defaults={'rating': int(rating), 'comment': comment}
    )

    return Response({
        'success': True,
        'message': 'Review submitted!' if created else 'Review updated!',
        'review': {
            'id':         review.id,
            'user_name':  getattr(request.user, 'full_name', None) or request.user.email,
            'rating':     review.rating,
            'comment':    review.comment,
            'created_at': str(review.created_at.date()),
        }
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# ======================================================================
#  MY ENROLLMENTS
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
        course_data = _course_dict(enr.course, request)
        course_data.update({
            'enrollment_id':       enr.pk,
            'payment_status':      enr.payment_status,
            'progress_percentage': enr.progress_percentage,
            'completed_lessons':   enr.completed_lessons,
            'completed':           enr.completed,
            'can_review':          enr.can_review(),
        })
        data.append(course_data)

    return Response({'success': True, 'enrollments': data})


# ======================================================================
#  CATEGORIES
# ======================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def categories_api(request):
    categories = (
        Course.objects.filter(is_published=True)
        .values_list('category__name', flat=True)
        .distinct()
        .order_by('category__name')
    )
    clean_cats = [c for c in categories if c]
    return Response({'success': True, 'categories': clean_cats})


# ======================================================================
#  LESSON MANAGEMENT (Admin/Mentor Only)
# ======================================================================
def _check_role(request):
    return getattr(request.user, 'role', None) in ['MENTOR', 'ADMIN', 'SUPER_ADMIN']

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_lesson_video(request, lesson_id):
    """Handle video file upload for a lesson"""
    if not _check_role(request):
        return Response({'success': False, 'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    if 'video' not in request.FILES:
        return Response({'success': False, 'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

    lesson = get_object_or_404(Lesson, id=lesson_id)
    video_file = request.FILES['video']
    lesson.video_file.save(f'lesson_{lesson_id}_{video_file.name}', video_file)
    lesson.video_type = Lesson.VideoType.UPLOAD
    lesson.save()

    return Response({
        'success': True,
        'video_url': request.build_absolute_uri(lesson.video_file.url) if request else lesson.video_file.url,
        'file_id': lesson.video_file.name,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_lesson_video_url(request, lesson_id):
    """Set external video URL for a lesson"""
    if not _check_role(request):
        return Response({'success': False, 'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.video_url = request.data.get('video_url', '')
    lesson.video_type = request.data.get('video_type', Lesson.VideoType.URL)
    lesson.save()

    return Response({'success': True, 'video_url': lesson.video_url})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lesson(request, course_id):
    """Create a new lesson for a course"""
    if not _check_role(request):
        return Response({'success': False, 'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    # Lesson belongs to a Module, not directly to a Course in merged schema
    module_id = request.data.get('module_id')
    if not module_id:
        module = Module.objects.filter(course_id=course_id).first()
        if not module:
            return Response({'success': False, 'error': 'No module found for this course. Create a module first.'},
                            status=status.HTTP_400_BAD_REQUEST)
        module_id = module.id

    data = request.data.copy()
    data['module'] = module_id

    serializer = LessonSerializer(data=data)
    if serializer.is_valid():
        lesson = serializer.save()
        return Response({'success': True, 'lesson': LessonSerializer(lesson).data}, status=status.HTTP_201_CREATED)
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_lesson(request, lesson_id):
    """Update lesson details"""
    if not _check_role(request):
        return Response({'success': False, 'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    lesson = get_object_or_404(Lesson, id=lesson_id)
    serializer = LessonSerializer(lesson, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'lesson': serializer.data})
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)