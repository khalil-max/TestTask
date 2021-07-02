from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from interview.helpers import CustomPagination
from user.models import User
from user.serializer import UserSerializer


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

    def create(self, request, *args, **kwargs):
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
