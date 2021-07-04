from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from interview.helpers import CustomPagination
from interview.models import Interview
from interview.serializer import InterviewSerializer, CompletedInterviewsSerializer
from user.models import User
from user.serializer import UserSerializer


# ViewSet пользователей
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated
    ]
    pagination_class = CustomPagination
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )

    @action(detail=True, methods=['get'])
    def completed_polls(self, request, pk):
        '''
        1) Беру pk и фильтрую есть ли такой user прошедших опрос, функция детальная потому что надо брать пройденные опросы одного пользователя.
        2) Сериализую передаю в контест pk пользователя для того чтобы потом профильтровать его в serializers.
        '''
        interview = Interview.objects.prefetch_related('question', 'question__answers').filter(
            surveyed__in=[pk]
        )
        serializer = CompletedInterviewsSerializer(interview, many=True, context={'pk': pk})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active_interview(self, request, pk=None):
        '''
            Активные опросы, беру те у которых есть start_time
        '''
        interview = Interview.objects.prefetch_related('question').filter(
            start_time__isnull=False
        )
        serializer = InterviewSerializer(interview, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        '''
            Возможность регистраци в api
        '''
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user.set_password(request.data.get('password', None))
            user.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        except Exception as ex:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.errors,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        '''
            Также возможность update
        '''

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data,
                                             partial=True)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.set_password(request.data.get('password', None))
                user.save()
            return Response(serializer.data)

        except Exception as ex:
            print(ex)
