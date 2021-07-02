from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from interview.helpers import CustomPagination, check_interview_start_time, \
    IsAdminUserOrReadOnly
from interview.models import Interview, Question, Choice, Answer
from interview.serializer import InterviewSerializer, ChoiceSerializer, \
    QuestionSerializer, AnswerSerializer


class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSerializer
    queryset = Interview.objects.all()
    permission_classes = [
        IsAdminUserOrReadOnly
    ]
    pagination_class = CustomPagination
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )


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
