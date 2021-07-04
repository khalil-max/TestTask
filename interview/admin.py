from django.contrib import admin
from .models import Interview, Question, Answer, Choice


# Регистрация моделей в панели администратора


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    pass
