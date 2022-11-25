from django.contrib import admin
from .models import (
    Course,
    Quiz,
    QuizAnswer,
    QuizOption,
    QuizOptionAnswer,
    Subscription,
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'max_capacity',
        'is_active',
        'modified',
        'created',
    )
    search_fields = (
        'name',
    )


class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 0


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = (
        QuizOptionInline,
    )
    list_display = (
        'id',
        'course',
        'name',
        'question',
        'is_active',
        'modified',
        'created',
    )
    search_fields = (
        'course__name',
        'name',
        'question',
    )
    raw_id_fields = (
        'course',
    )


@admin.register(QuizOption)
class QuizOptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'quiz',
        'name',
        'is_a_right_answer',
        'is_active',
        'order',
        'modified',
        'created',
    )
    list_editable = (
        'name',
        'is_a_right_answer',
        'order',
    )
    raw_id_fields = (
        'quiz',
    )
    search_fields = (
        'quiz__course__name',
        'quiz__name',
        'name',
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'student',
        'course',
        'is_active',
        'modified',
        'created',
    )
    search_fields = (
        'course__name',
        'student__first_name',
        'student__last_name',
    )
    raw_id_fields = (
        'student',
    )


class QuizOptionAnswerInline(admin.TabularInline):
    model = QuizOptionAnswer
    extra = 0


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    inlines = (
        QuizOptionAnswerInline,
    )
    list_display = (
        'id',
        'subscription',
        'quiz',
        'succeeded',
        'modified',
        'created',
    )
    readonly_fields = (
        'succeeded',
    )


@admin.register(QuizOptionAnswer)
class QuizOptionAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'quiz_answer',
        'quiz_option',
        'modified',
        'created',
    )