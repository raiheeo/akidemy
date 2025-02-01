from django.contrib import admin
from .models import (
    UserProfile, Teacher, Student, Network, Category, Course, Lesson,
    Assignment, Exam, Question, Option, Certificate, CourseReview,
    TeacherRating, History, Cart, CartItem, Favorite, FavoriteItem
)
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin
import nested_admin


class GlobalAdminConfig:
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class OptionInline(nested_admin.NestedStackedInline, TranslationInlineModelAdmin):
    model = Option
    extra = 1
    fk_name = 'question'


class QuestionInline(nested_admin.NestedStackedInline, TranslationInlineModelAdmin):
    model = Question
    extra = 1
    inlines = [OptionInline]


@admin.register(Exam)
class ExamAdmin(TranslationAdmin, nested_admin.NestedModelAdmin,  GlobalAdminConfig):
    inlines = [QuestionInline]


@admin.register(Category)
class CategoryAdmin(TranslationAdmin, nested_admin.NestedModelAdmin, GlobalAdminConfig):
    pass


class LessonInline(nested_admin.NestedStackedInline, TranslationInlineModelAdmin):
    model = Lesson
    extra = 1
    fk_name = 'course'


class AssignmentInline(nested_admin.NestedStackedInline, TranslationInlineModelAdmin):
    model = Assignment
    extra = 1


@admin.register(Course)
class CourseAdmin(TranslationAdmin, nested_admin.NestedModelAdmin, GlobalAdminConfig):
    inlines = [LessonInline, AssignmentInline]


@admin.register(Lesson)
class LessonAdmin(TranslationAdmin, nested_admin.NestedModelAdmin,  GlobalAdminConfig):
    pass


@admin.register(Assignment)
class AssignmentAdmin(TranslationAdmin, nested_admin.NestedModelAdmin,  GlobalAdminConfig):
    pass


@admin.register(Question)
class QuestionAdmin(TranslationAdmin, nested_admin.NestedModelAdmin,  GlobalAdminConfig):
    pass


@admin.register(Option)
class OptionAdmin(TranslationAdmin, nested_admin.NestedModelAdmin, GlobalAdminConfig):
    pass


admin.site.register(UserProfile)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Network)
admin.site.register(Certificate)
admin.site.register(TeacherRating)
admin.site.register(History)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)
admin.site.register(CourseReview)
