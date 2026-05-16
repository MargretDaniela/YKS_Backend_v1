# # C:\Users\Admin\Desktop\TheYKSApp\courses\serializers.py
# from rest_framework import serializers
# from .models import Course, Section, Lesson  # ← Course is HERE, in courses app


# # ======================================================================
# #  CourseSerializer — For course API responses
# # ======================================================================
# class CourseSerializer(serializers.ModelSerializer):
#     instructor = serializers.SerializerMethodField()
#     instructor_bio = serializers.SerializerMethodField()
#     price = serializers.SerializerMethodField()
#     price_raw = serializers.SerializerMethodField()
#     thumbnail = serializers.SerializerMethodField()
#     learning_points = serializers.SerializerMethodField()
#     avg_rating = serializers.SerializerMethodField()
#     review_count = serializers.SerializerMethodField()
#     student_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Course
#         fields = [
#             'id', 'title', 'description', 'category', 'instructor',
#             'instructor_bio', 'price', 'price_raw', 'is_live',
#             'start_date', 'end_date', 'recording_url', 'thumbnail',
#             'learning_points', 'avg_rating', 'review_count', 
#             'student_count', 'created_at', 'updated_at'
#         ]
#         read_only_fields = ['avg_rating', 'review_count', 'student_count']

#     def get_instructor(self, obj):
#         trainer = obj.trainer
#         return getattr(trainer, 'full_name', None) or trainer.email if trainer else 'Youth K.E.Y'

#     def get_instructor_bio(self, obj):
#         if obj.instructor_bio:
#             return obj.instructor_bio
#         trainer = obj.trainer
#         name = getattr(trainer, 'full_name', None) or trainer.email if trainer else 'Youth K.E.Y'
#         return f"{name} is a highly experienced coach helping youth across Africa, specialising in {obj.category.lower()}."

#     def get_price(self, obj):
#         return f'US${float(obj.price):.2f}'

#     def get_price_raw(self, obj):
#         return float(obj.price)

#     def get_thumbnail(self, obj):
#         request = self.context.get('request')
#         if obj.thumbnail and request:
#             return request.build_absolute_uri(obj.thumbnail.url)
#         return obj.thumbnail.url if obj.thumbnail else None

#     def get_learning_points(self, obj):
#         return obj.get_learning_points()

#     def get_avg_rating(self, obj):
#         return obj.get_average_rating()

#     def get_review_count(self, obj):
#         return obj.reviews.count()

#     def get_student_count(self, obj):
#         return obj.get_student_count()

from rest_framework import serializers
from django.utils import timezone
from django.db.models import Avg

from .models import (
    Category, Course, LearningPoint, Module,
    Lesson, Enrollment, LessonProgress, Review, Section
)


# ======================================================================
#  LESSON SERIALIZER
# ======================================================================
class LessonSerializer(serializers.ModelSerializer):
    video_source = serializers.ReadOnlyField()
    file_size_mb = serializers.ReadOnlyField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'order', 'duration',
            'is_free', 'video_type', 'video_url',
            'video_file', 'video_source',
            'allow_download', 'file_size_mb',
            'is_completed',
        ]

    def get_is_completed(self, lesson):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        course = getattr(getattr(lesson, 'module', None), 'course', None)
        if not course:
            return False

        return LessonProgress.objects.filter(
            enrollment__student=request.user,
            enrollment__course=course,
            lesson=lesson,
            is_completed=True,
        ).exists()


# ======================================================================
#  MODULE SERIALIZER
# ======================================================================
class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    total_lessons = serializers.SerializerMethodField()
    free_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = [
            'id', 'title', 'description', 'order',
            'lessons', 'total_lessons', 'free_lessons'
        ]

    def get_total_lessons(self, obj):
        return obj.lessons.count()

    def get_free_lessons(self, obj):
        return obj.lessons.filter(is_free=True).count()


SectionSerializer = ModuleSerializer


# ======================================================================
#  COURSE LIST SERIALIZER
# ======================================================================
class CourseListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    price = serializers.ReadOnlyField()
    avg_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    thumbnail = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'category', 'instructor',
            'price', 'amount', 'currency',
            'avg_rating', 'review_count', 'student_count',
            'start_date', 'end_date', 'is_live',
            'thumbnail', 'is_enrolled', 'is_published',
        ]

    def get_thumbnail(self, course):
        request = self.context.get('request')
        if course.thumbnail and request:
            return request.build_absolute_uri(course.thumbnail.url)
        return None

    def get_is_enrolled(self, course):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        return Enrollment.objects.filter(
            student=request.user,
            course=course,
            is_active=True
        ).exists()


# ======================================================================
#  COURSE DETAIL SERIALIZER
# ======================================================================
class CourseDetailSerializer(CourseListSerializer):
    description = serializers.CharField(read_only=True)
    recording_url = serializers.URLField(read_only=True)

    price_raw = serializers.SerializerMethodField()
    instructor_bio = serializers.SerializerMethodField()
    learning_points = serializers.SerializerMethodField()

    modules = ModuleSerializer(many=True, read_only=True)

    total_lessons = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields + [
            'description', 'recording_url',
            'price_raw', 'instructor_bio',
            'learning_points', 'modules',
            'total_lessons', 'progress',
            'created_at', 'updated_at',
        ]

    # ---------------- SAFE METHODS ----------------

    def get_instructor_bio(self, obj):
        if obj.instructor_bio:
            return obj.instructor_bio
        return f"{obj.instructor or 'Instructor'} teaches this course."

    def get_price_raw(self, obj):
        return float(obj.price or obj.amount or 0)

    def get_learning_points(self, obj):
        structured = list(obj.learning_points.values_list('point', flat=True))
        return structured if structured else obj.get_learning_points()

    def get_total_lessons(self, obj):
        return Lesson.objects.filter(module__course=obj).count()

    def get_progress(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None

        enrollment = Enrollment.objects.filter(
            student=request.user,
            course=obj,
            is_active=True
        ).first()

        if not enrollment:
            return None

        return getattr(
            enrollment,
            'progress_percentage',
            enrollment.computed_progress_percentage if hasattr(enrollment, 'computed_progress_percentage') else 0
        )


CourseSerializer = CourseDetailSerializer


# ======================================================================
#  CATEGORY SERIALIZER
# ======================================================================
class CategoryWithCoursesSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='name')
    courses = CourseListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category', 'icon', 'courses']


# ======================================================================
#  ENROLLMENT SERIALIZER
# ======================================================================
class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id', 'course', 'title',
            'enrolled_at', 'is_active',
            'progress_percentage',
            'payment_status',
            'completed_lessons',
            'completed'
        ]


class EnrollSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()


# ======================================================================
#  LESSON PROGRESS
# ======================================================================
class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = [
            'id', 'lesson',
            'is_completed',
            'completed_at',
            'last_position'
        ]
        read_only_fields = ['completed_at']


class MarkLessonDoneSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()
    is_completed = serializers.BooleanField(default=True)
    last_position = serializers.IntegerField(required=False, default=0)


# ======================================================================
#  REVIEW SERIALIZER
# ======================================================================
class ReviewSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'student_name',
            'rating', 'comment',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ======================================================================
#  LESSON DOWNLOAD SERIALIZER
# ======================================================================
class LessonDownloadSerializer(serializers.ModelSerializer):
    video_source = serializers.ReadOnlyField()
    file_size_mb = serializers.ReadOnlyField()
    can_download = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'video_type',
            'video_source', 'file_size_mb',
            'allow_download', 'can_download'
        ]

    def get_can_download(self, lesson):
        if not lesson.allow_download:
            return False

        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        course = getattr(getattr(lesson, 'module', None), 'course', None)
        if not course:
            return False

        return Enrollment.objects.filter(
            student=request.user,
            course=course,
            is_active=True
        ).exists()