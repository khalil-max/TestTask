from django.db import models

from interview.choices import QUESTION_TYPES


# Модель опроса
class Interview(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    start_time = models.DateField(
        verbose_name='Дата начала',
        null=True,
        blank=True,
    )
    end_time = models.DateField(
        verbose_name='Дата конца',
    )
    description = models.TextField(
        verbose_name='Описание',
    )


# Модель вопроса
class Question(models.Model):
    interview = models.ForeignKey(
        Interview,
        verbose_name='Опрос',
        on_delete=models.CASCADE,
        related_name='question',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    question_type = models.SmallIntegerField(
        verbose_name='Тип вопроса',
        default=0,
        choices=QUESTION_TYPES
    )


# Модель варианта ответа
class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст'
    )


# Модель ответа
class Answer(models.Model):
    user = models.ForeignKey(
        'user.User',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        verbose_name='Опрос',
        on_delete=models.CASCADE,
    )
    anonymously = models.BooleanField(
        verbose_name='Анонимно',
        default=False,
    )
    value = models.TextField(
        verbose_name='Значение',
    )
