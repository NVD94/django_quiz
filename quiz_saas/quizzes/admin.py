from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Quiz
from .models import Question
from .models import Answer
from .models import Participation


class QuizAdmin(admin.ModelAdmin):
    list_display = ("name", "summary", "created", "updated")
    search_fields = ("name", "summary")
    readonly_fields = ("created", "updated")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ("content", "get_quiz_name")
    search_fields = ("content",)

    def get_quiz_name(self, obj):
        return obj.quiz.name

    get_quiz_name.admin_order_field = "quiz"
    get_quiz_name.short_description = "Quiz Name"

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class AnswerAdmin(admin.ModelAdmin):
    model = Question
    list_display = ("content", "is_correct", "get_question_name", "get_quiz_name")
    search_fields = (
        "content",
        "is_correct",
        "question__content",
        "question__quiz__name",
    )

    @admin.display(ordering="question__name", description="Question Name")
    def get_question_name(self, obj):
        return obj.question.content

    @admin.display(ordering="question__quiz__name", description="Quiz Name")
    def get_quiz_name(self, obj):
        return obj.question.quiz.name

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("get_user_email", "get_quiz_name")
    search_fields = ("user__email", "quiz__name")

    @admin.display(ordering="user__email", description="User email")
    def get_user_email(self, obj):
        return obj.user.email

    @admin.display(ordering="quiz__name", description="Quiz Name")
    def get_quiz_name(self, obj):
        return obj.quiz.name

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here.
admin.site.register(Participation, ParticipationAdmin)

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
