from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.exceptions import ValidationError

# Global choices
ROLE_CHOICES = (
    ('teacher', 'Teacher'),
    ('student', 'Student'),
)

STATUS_CHOICES = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
)

class UserProfile(AbstractUser):
    username = models.CharField(max_length=128, null=True, blank=True, unique=True)
    profile_picture = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(unique=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16), MaxValueValidator(75)], null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Teacher(UserProfile):
    bio = models.TextField()
    DAYS_CHOICES = (
        ('MN', 'Monday'),
        ('TS', 'Tuesday'),
        ('TH', 'Thursday'),
        ('TD', 'Wednesday'),
        ('FR', 'Friday'),
        ('SD', 'Saturday'),
    )
    work_days = MultiSelectField(choices=DAYS_CHOICES, max_choices=6)
    subjects = models.TextField()
    experience = models.PositiveSmallIntegerField(validators=[MaxValueValidator(30)])
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='teacher')

    def __str__(self):
        return f'{self.first_name}, {self.role}'

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = 'Teachers'


class Student(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}, {self.role}'


class Network(models.Model):
    network_name = models.CharField(max_length=32)
    network_link = models.URLField()
    title = models.CharField(max_length=32, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.network_name} - {self.network_link}'


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.category_name


class Course(models.Model):
    category = models.ManyToManyField(Category)
    course_name = models.CharField(max_length=128)
    course_description = models.TextField()
    author = models.ManyToManyField(Teacher)
    level = models.CharField(max_length=32, choices=STATUS_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    TYPE_CHOICES = (
        ('free', 'Free'),
        ('paid', 'Paid'),
    )
    course_type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    certificate = models.BooleanField()
    course_assignment = models.ManyToManyField('Assignment', related_name='assignment_in_courses')


    def __str__(self):
        return self.course_name


class Lesson(models.Model):
    title = models.CharField(max_length=64, null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    video = models.FileField(upload_to='lesson_video', null=True, blank=True)
    content = models.FileField(upload_to='lesson_content', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title or 'No Title'


class Assignment(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField()
    due_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.title or 'No Title'


class Exam(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    end_time = models.DurationField()

    def __str__(self):
        return self.title or 'No Title'


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=True, blank=True)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.title or 'No Title'


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    another_fk = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='another_options')
    variant = models.CharField(max_length=64)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.variant


class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="certificates")
    issued_at = models.DateField(auto_now_add=True)
    certificate_url = models.FileField(upload_to='certificates')

    def __str__(self):
        return f'Certificate for {self.student.user.first_name} in {self.course.course_name}'


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)

    def __str__(self):
        return f'Review by {self.user.user.first_name} for {self.course.course_name}'

    def clean(self):
        super().clean()
        if not self.text and not self.rating:
            raise ValidationError('Choose minimum one of (text, stars)!')

class TeacherRating(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)

    def __str__(self):
        return f'Rating {self.rating} for {self.teacher.first_name}'


class History(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.user.first_name} - {self.course.course_name}'
    

class Cart(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='student_cart')

    def __str__(self):
        return f'{self.student}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cart} - {self.course}'

    def get_total_price(self):
        return self.course.price


class Favorite(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student}'

    def get_favorite_item(self):
        return (item.get_favorite_item() for item in self.favorite_items.all())


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='favorite_items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.favorite}, {self.course}'

    def get_favorite_item(self):
        return self.course.course_name
