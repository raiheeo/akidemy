from rest_framework import serializers
from .models import (
    UserProfile, Teacher, Student, Network, Category, Course, Lesson,
    Assignment, Exam, Question, Option, Certificate, CourseReview,
    TeacherRating, History, Cart, CartItem, Favorite, FavoriteItem
)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'profile_picture', 'phone_number', 'email', 'age',
            'first_name', 'last_name', 'date_joined', 'last_login'
        ]

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class TeacherListSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role_display')
    class Meta:
        model = Teacher
        fields = [
            'profile_picture',
            'first_name', 'last_name', 'subjects',
            'experience'
        ]

class TeacherDetailSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role_display')
    class Meta:
        model = Teacher
        fields = [
            'id', 'username', 'profile_picture', 'phone_number', 'email', 'age',
            'first_name', 'last_name', 'bio', 'work_days', 'subjects',
            'experience', 'role'
        ]

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Student
        fields = ['id', 'user', 'role']

class StudentDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'profile_picture', 'phone_number', 'email', 'age',
            'first_name', 'last_name', 'date_joined', 'last_login'
        ]

class CourseDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    author = serializers.StringRelatedField(many=True)
    teacher = TeacherDetailSerializer(many=True)
    class Meta:
        model = Course
        fields = [
            'id', 'category', 'course_name', 'course_description', 'author',
            'level', 'price', 'course_type', 'created_at', 'updated_at'
        ]

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'course_name',
            'level', 'price',
            'course_type',
        ]

class CategoryDetailSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'course_name']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name', ]


class LessonListSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = ['title',  'course']


class LessonDetailSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url', 'video', 'content', 'course']


class AssignmentSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    students = serializers.StringRelatedField()

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'due_date', 'course', 'students']


class ExamSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = Exam
        fields = ['id', 'title', 'course', 'end_time']


class QuestionsSerializer(serializers.ModelSerializer):
    exam = serializers.StringRelatedField()

    class Meta:
        model = Question
        fields = ['id', 'exam', 'title', 'score']


class OptionSerializer(serializers.ModelSerializer):
    questions = serializers.StringRelatedField()

    class Meta:
        model = Option
        fields = ['id', 'questions', 'variant', 'check']


class CertificateSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    class Meta:
        model = Certificate
        fields = ['id', 'student', 'course', 'issued_at', 'certificate_url']


class CourseReviewSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = CourseReview
        fields = ['id', 'course', 'user', 'text', 'stats']


class TeacherRatingSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = TeacherRating
        fields = ['id', 'teacher', 'user', 'stars']


class HistorySerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    class Meta:
        model = History
        fields = ['id', 'student', 'course', 'date']


class CartSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()

    class Meta:
        model = Cart
        fields = ['id', 'student']


class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'course']


class FavoriteSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()

    class Meta:
        model = Favorite
        fields = ['id', 'student']


class FavoriteItemSerializer(serializers.ModelSerializer):
    cart = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    class Meta:
        model = FavoriteItem
        fields = ['id', 'cart', 'course']


class NetworkSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Network
        fields = ['id', 'network_name', 'network_link', 'title', 'user']