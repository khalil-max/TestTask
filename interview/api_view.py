from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from interview.helpers import CustomPagination, check_interview_start_time, \
    IsAdminUserOrReadOnly
from interview.models import Interview, Question, Choice, Answer
from interview.serializer import InterviewSerializer, ChoiceSerializer, \
    QuestionSerializer, AnswerSerializer


class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSerializer
    queryset = Interview.objects.prefetch_related('question', 'surveyed')
    pagination_class = CustomPagination
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )

    @action(detail=True, methods=['get', 'post'])
    def interview(self, request, pk):
        query = Interview.objects.prefetch_related('question').get(pk=pk)
        serializer = InterviewSerializer(query, many=False)
        if query.start_time:
            if request.method == 'POST':
                user = request.data.get('user', None)
                answers = request.data.get('answers', None)
                anonymously = request.data.get('anonymously', None)
                if user and answers:
                    answers_list = []
                    for answer in answers:
                        creating_answer = Answer(
                            user_id=user,
                            question_id=answer["question"]["id"],
                            anonymously=anonymously,
                        )
                        creating_answer.save()
                        if answer["question"]["question_type"] == 0:
                            creating_answer.value = answer["value"]
                        elif answer["question"]["question_type"] == 1 and len(
                                answer["choices"]) == 1:
                            creating_answer.choices.add(
                                Choice.objects.get(pk=answer["choices"][0]))
                        elif answer["question"]["question_type"] == 2:
                            for choice in answer['choices']:
                                creating_answer.choices.add(choice)
                        else:
                            return Response({
                                "error": True,
                                "msg": "Данные указаны неправильно"
                            })
                        creating_answer.save()
                        answers_list.append(creating_answer)
                    query.surveyed.add(user)
                    serializer = AnswerSerializer(answers_list, many=True)
                    return Response(serializer.data)
                else:
                    return Response({
                        "error": True,
                        "msg": "Не добалено поле user или answers"
                    })
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.select_related('interview')
    permission_classes = [
        IsAdminUserOrReadOnly
    ]
    pagination_class = CustomPagination
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )

    def create(self, request, *args, **kwargs):
        return check_interview_start_time(self, request)

    def update(self, request, *args, **kwargs):
        return check_interview_start_time(self, request)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        interview = Interview.objects.get(
            pk=request.data.get('interview')
        )
        if not interview.start_time:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "error": True,
                "msg": "Дата старта была добавлена в опрос процесс необратим"
            })


class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.select_related('question')
    permission_classes = [
        IsAdminUserOrReadOnly
    ]
    pagination_class = CustomPagination
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.select_related('user', 'question')
    permission_classes = [
        IsAuthenticated
    ]
    pagination_class = CustomPagination
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )
