from rest_framework import serializers
from interview.models import Interview, Question, Answer, Choice
from user.serializer import UserSerializer


# Внимание ! Я ставлю так serializers для того чтобы на стороне клиента было меньше запросов. Советую всем делать также

# Сериализатор модели варианта ответа
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = 'id', 'question', 'text'


# Сериализатор модели вопроса
class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(
        many=True,
        read_only=True,
        source='choice'
    )

    class Meta:
        model = Question
        fields = 'id', 'interview', \
                 'text', 'question_type', 'choices'


# Сериализатор модели опроса
class InterviewSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(
        many=True,
        read_only=True,
        source='question'
    )

    class Meta:
        model = Interview
        fields = 'id', 'title', 'start_time', \
                 'end_time', 'description', 'questions', 'surveyed'


# Сериализатор модели ответа
class AnswerSerializer(serializers.ModelSerializer):
    user_item = UserSerializer(
        many=False,
        read_only=True,
        source='user',
    )
    choices_items = ChoiceSerializer(
        many=True,
        read_only=True,
        source='choices'
    )

    class Meta:
        model = Answer
        fields = 'id', 'user', 'user_item', 'question', \
                 'anonymously', 'value', \
                 'choices', 'choices_items'


# Фильтрация ответов по пользователю
class FilterUserCompletedAnswerSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        # Помните context={} который я передал в user completed polls в CompletedInterviewsSerializer
        # Теперь я беру его здесь для фильтрации по user_id
        # Это нужно для того чтобы пользователь видел только его ответы на вопросы
        data = data.filter(user_id=self.context['pk'])
        return super(FilterUserCompletedAnswerSerializer, self).to_representation(data)


# Сериализатор модели ответов пройденных опросов
# list_serializer_class  как фильтр данных в данном случае
class CompletedAnswerSerializer(serializers.ModelSerializer):
    user_item = UserSerializer(
        many=False,
        read_only=True,
        source='user',
    )
    choices_items = ChoiceSerializer(
        many=True,
        read_only=True,
        source='choices'
    )

    class Meta:
        model = Answer
        fields = 'id', 'user', 'user_item', 'question', \
                 'anonymously', 'value', \
                 'choices', 'choices_items'
        list_serializer_class = FilterUserCompletedAnswerSerializer


# Сериализатор модели вопроса
class CompletedQuestionsSerializer(serializers.ModelSerializer):
    answers = CompletedAnswerSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Question
        fields = 'id', 'interview', \
                 'text', 'question_type', 'answers'


# Сериализатор модели пройденных опросов
class CompletedInterviewsSerializer(serializers.ModelSerializer):
    questions = CompletedQuestionsSerializer(
        many=True,
        read_only=True,
        source='question'
    )

    class Meta:
        model = Interview
        fields = 'id', 'title', 'start_time', \
                 'end_time', 'description', 'questions', 'surveyed'
