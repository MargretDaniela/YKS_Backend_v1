# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Course, Section, Review, Enrollment

# def _course_dict(course, request=None):
#     thumbnail_url = None
#     if course.thumbnail:
#         thumbnail_url = (
#             request.build_absolute_uri(course.thumbnail.url)
#             if request else course.thumbnail.url
#         )
#     avg_rating = course.get_average_rating()
#     review_count = course.reviews.count()
#     student_count = course.get_student_count()
#     learning_points = course.get_learning_points()
#     trainer = course.trainer
#     instructor_name = getattr(trainer, 'full_name', None) or trainer.email
#     instructor_bio = course.instructor_bio or (
#         f"{instructor_name} is a highly experienced coach helping youth across Africa, "
#         f"specialising in {course.category.lower()}."
#     )
#     return {
#         'id': course.pk,
#         'title': course.title,
#         'description': course.description,
#         'category': course.category,
#         'instructor': instructor_name,
#         'instructor_bio': instructor_bio,
#         'price': f'US${float(course.price):.2f}',
#         'price_raw': float(course.price),
#         'is_live': course.is_live,
#         'start_date': str(course.start_date),
#         'end_date': str(course.end_date),
#         'recording_url': course.recording_url or '',
#         'thumbnail': thumbnail_url,
#         'learning_points': learning_points,
#         'avg_rating': avg_rating,
#         'review_count': review_count,
#         'student_count': student_count,
#     }

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def courses_list_api(request):
#     # courses = Course.objects.all().select_related('trainer').order_by('-created_at')
#     courses = Course.objects.all().select_related('trainer').order_by('-id')
#     grouped = {}
#     for course in courses:
#         cat = course.category or 'General'
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

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def course_detail_api(request, pk):
#     try:
#         course = Course.objects.select_related('trainer').get(pk=pk)
#     except Course.DoesNotExist:
#         return Response({'success': False, 'error': 'Course not found.'},
#                         status=status.HTTP_404_NOT_FOUND)
#     return Response({'success': True, 'course': _course_dict(course, request)})

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def course_curriculum_api(request, pk):
#     try:
#         sections = Section.objects.filter(course_id=pk).prefetch_related('lessons')
#         data = [{
#             'title': s.title,
#             'lessons': [{
#                 'name': l.title,
#                 'duration': l.duration,
#                 'free': l.is_free,
#             } for l in s.lessons.all()]
#         } for s in sections]
#         return Response({'success': True, 'sections': data})
#     except Exception as e:
#         return Response({'success': False, 'sections': [], 'error': str(e)})

# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def course_reviews_api(request, pk):
#     if request.method == 'GET':
#         try:
#             reviews = Review.objects.filter(course_id=pk).select_related('user')
#             data = [{
#                 'id': r.id,
#                 'user_name': getattr(r.user, 'full_name', None) or r.user.email,
#                 'rating': r.rating,
#                 'comment': r.comment,
#                 'created_at': str(r.created_at.date()),
#             } for r in reviews]
#             return Response({'success': True, 'reviews': data})
#         except Exception as e:
#             return Response({'success': False, 'reviews': [], 'error': str(e)})
#     if request.method == 'POST':
#         if not request.user.is_authenticated:
#             return Response({'success': False, 'error': 'Login required.'},
#                             status=status.HTTP_401_UNAUTHORIZED)
#         try:
#             enrollment = Enrollment.objects.get(user=request.user, course_id=pk)
#         except Enrollment.DoesNotExist:
#             return Response({
#                 'success': False,
#                 'error': 'You must be enrolled to review this course.'
#             }, status=status.HTTP_403_FORBIDDEN)
#         if not enrollment.can_review():
#             return Response({
#                 'success': False,
#                 'error': 'Complete at least 2 lessons before reviewing.'
#             }, status=status.HTTP_403_FORBIDDEN)
#         rating = request.data.get('rating')
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
#                 'id': review.id,
#                 'user_name': getattr(request.user, 'full_name', None) or request.user.email,
#                 'rating': review.rating,
#                 'comment': review.comment,
#                 'created_at': str(review.created_at.date()),
#             }
#         })

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
#             'enrollment_id': enr.pk,
#             'payment_status': enr.payment_status,
#             'progress_percentage': enr.progress_percentage,
#             'completed_lessons': enr.completed_lessons,
#             'completed': enr.completed,
#             'can_review': enr.can_review(),
#         })
#         data.append(course_data)
#     return Response({'success': True, 'enrollments': data})

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def categories_api(request):
#     categories = Course.objects.values_list('category', flat=True).distinct()
#     return Response({'success': True, 'categories': list(categories)})

from django.http import FileResponse, Http404
from django.utils import timezone
from django.shortcuts import get_object_or_404
import os   # ✅ FIX ADDED (VERY IMPORTANT)

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .api import _course_dict  

from .models import (
    Category, Course, Module, Lesson,
    Enrollment, LessonProgress, Review, Section,
)

from .serializers import (
    CategoryWithCoursesSerializer,
    CourseDetailSerializer,
    EnrollmentSerializer,
    EnrollSerializer,
    MarkLessonDoneSerializer,
    LessonProgressSerializer,
    ReviewSerializer,
    LessonDownloadSerializer,
)

# ======================================================================
#  COURSES & CATEGORIES
# ======================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def courses_list(request):
    categories = Category.objects.prefetch_related(
        'courses__learning_points',
        'courses__modules__lessons',
        'courses__reviews',
        'courses__enrollments',
    ).filter(courses__is_published=True).distinct()

    serializer = CategoryWithCoursesSerializer(
        categories, many=True, context={'request': request}
    )
    return Response({'success': True, 'categories': serializer.data})


# ======================================================================
#  COURSE DETAIL
# ======================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def course_detail(request, course_id):
    course = get_object_or_404(
        Course.objects.prefetch_related(
            'learning_points',
            'modules__lessons',
            'reviews__student',
            'enrollments',
        ),
        id=course_id, is_published=True
    )
    serializer = CourseDetailSerializer(course, context={'request': request})
    return Response({'success': True, 'course': serializer.data})


# ======================================================================
#  CATEGORIES
# ======================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def categories_api(request):
    categories = Course.objects.filter(
        is_published=True
    ).values_list('category__name', flat=True).distinct().order_by('category__name')

    clean_cats = [c for c in categories if c]
    return Response({'success': True, 'categories': clean_cats})


# ======================================================================
#  CURRICULUM
# ======================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def course_curriculum_api(request, pk):
    course = get_object_or_404(Course, id=pk, is_published=True)

    sections = Module.objects.filter(course=course).prefetch_related(
        'lessons'
    ).order_by('order')

    data = []
    for s in sections:
        data.append({
            'id': s.id,
            'title': s.title,
            'description': s.description,
            'order': s.order,
            'lessons': [
                {
                    'id': l.id,
                    'name': l.title,
                    'duration': l.duration,
                    'free': l.is_free,
                    'order': l.order,
                }
                for l in s.lessons.all()
            ]
        })

    return Response({'success': True, 'course_id': pk, 'sections': data})


# ======================================================================
#  ENROLLMENTS
# ======================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_enrollments(request):
    enrollments = Enrollment.objects.filter(
        student=request.user, is_active=True
    ).select_related(
        'course__category', 'course__trainer'
    ).prefetch_related(
        'lesson_progress', 'course__modules__lessons'
    )

    serializer = EnrollmentSerializer(
        enrollments, many=True, context={'request': request}
    )
    return Response({'success': True, 'enrollments': serializer.data})


# ======================================================================
#  ENROLL
# ======================================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll(request):
    ser = EnrollSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    course = get_object_or_404(
        Course,
        id=ser.validated_data['course_id'],
        is_published=True
    )

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course,
        defaults={'is_active': True}
    )

    if not created and not enrollment.is_active:
        enrollment.is_active = True
        enrollment.save()

    if created:
        lessons = Lesson.objects.filter(module__course=course)

        LessonProgress.objects.bulk_create([
            LessonProgress(enrollment=enrollment, lesson=lesson)
            for lesson in lessons
        ], ignore_conflicts=True)

        Course.objects.filter(id=course.id).update(
            student_count=course.student_count + 1
        )

    return Response({
        'success': True,
        'message': 'Enrolled successfully' if created else 'Already enrolled',
        'enrollment_id': enrollment.id,
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# ======================================================================
#  PROGRESS
# ======================================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_lesson_progress(request):
    ser = MarkLessonDoneSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    lesson = get_object_or_404(Lesson, id=ser.validated_data['lesson_id'])

    # SAFE FIX (prevents crash if module is missing)
    course = lesson.module.course if lesson.module else None

    enrollment = get_object_or_404(
        Enrollment,
        student=request.user,
        course=course,
        is_active=True,
    )

    progress, _ = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )

    progress.is_completed = ser.validated_data['is_completed']
    progress.last_position = ser.validated_data.get('last_position', 0)

    if progress.is_completed and not progress.completed_at:
        progress.completed_at = timezone.now()

    progress.save()

    return Response({
        'success': True,
        'lesson_id': lesson.id,
        'is_completed': progress.is_completed,
        'last_position': progress.last_position,
        'course_progress': enrollment.progress_percentage,
    })


# ======================================================================
#  COURSE PROGRESS
# ======================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_progress(request, course_id):
    enrollment = get_object_or_404(
        Enrollment,
        student=request.user,
        course_id=course_id,
        is_active=True,
    )

    progress_records = LessonProgress.objects.filter(
        enrollment=enrollment
    ).select_related('lesson').order_by('lesson__order')

    return Response({
        'success': True,
        'course_id': course_id,
        'progress_percentage': enrollment.progress_percentage,
        'lessons': [
            {
                'lesson_id': p.lesson_id,
                'title': p.lesson.title,
                'is_completed': p.is_completed,
                'last_position': p.last_position,
                'completed_at': p.completed_at,
            }
            for p in progress_records
        ],
    })


# ======================================================================
#  REVIEWS
# ======================================================================
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def course_reviews(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)

    if request.method == 'GET':
        reviews = course.reviews.select_related('student').order_by('-created_at')
        ser = ReviewSerializer(reviews, many=True, context={'request': request})

        return Response({
            'success': True,
            'avg_rating': course.avg_rating,
            'review_count': course.review_count,
            'reviews': ser.data,
        })

    if not request.user.is_authenticated:
        return Response(
            {'success': False, 'error': 'Authentication required'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course,
        is_active=True
    ).first()

    if not enrollment:
        return Response(
            {'success': False, 'error': 'You must be enrolled to review'},
            status=status.HTTP_403_FORBIDDEN
        )

    if not enrollment.can_review():
        return Response(
            {'success': False, 'error': 'Complete at least 2 lessons before reviewing.'},
            status=status.HTTP_403_FORBIDDEN
        )

    ser = ReviewSerializer(data=request.data, context={'request': request})
    ser.is_valid(raise_exception=True)

    review, created = Review.objects.update_or_create(
        course=course,
        student=request.user,
        defaults={
            'rating': ser.validated_data['rating'],
            'comment': ser.validated_data.get('comment', ''),
        }
    )

    return Response({
        'success': True,
        'message': 'Review submitted!' if created else 'Review updated!',
        'review': ReviewSerializer(review).data,
    })


# ======================================================================
#  LESSON DOWNLOAD INFO (FIXED MISSING VIEW)
# ======================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lesson_download_info(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    course = lesson.module.course if lesson.module else None

    # Check enrollment
    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=course,
        is_active=True
    ).exists()

    if not is_enrolled:
        return Response({
            'success': False,
            'error': 'Enrollment required'
        }, status=status.HTTP_403_FORBIDDEN)

    return Response({
        'success': True,
        'lesson_id': lesson.id,
        'title': lesson.title,
        'allow_download': lesson.allow_download,
        'video_type': lesson.video_type,
        'download_available': lesson.allow_download and lesson.video_file is not None,
    })