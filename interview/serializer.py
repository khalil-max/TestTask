from rest_framework import serializers
from interview.models import Interview, Question, Answer, Choice
from user.serializer import UserSerializer


# Сериализатор модели опроса
class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = 'id', 'title', 'start_time', 'end_time', 'description'


# Сериализатор модели вопроса
class QuestionSerializer(serializers.ModelSerializer):
    interview_item = InterviewSerializer(
        many=False,
        source='interview',
        read_only=True
    )

    class Meta:
        model = Question
        fields = 'id', 'interview', 'interview_item', \
                 'text', 'question_type'


# Сериализатор модели ответа
class AnswerSerializer(serializers.ModelSerializer):
    user_item = UserSerializer(
        many=False,
        read_only=True,
        source='user',
    )

    question_item = QuestionSerializer(
        many=False,
        source='question',
        read_only=True
    )

    class Meta:
        model = Answer
        fields = 'id', 'user', 'user_item', 'question', \
                 'question_item', 'anonymously', 'value'


# Сериализатор модели варианта ответа
class ChoiceSerializer(serializers.ModelSerializer):
    question_item = QuestionSerializer(
        many=False,
        source='question',
        read_only=True
    )

    class Meta:
        model = Choice
        fields = 'id', 'question', 'question_item', 'text'
