from rest_framework import pagination, status
from rest_framework.permissions import SAFE_METHODS, \
    BasePermission, IsAdminUser
from rest_framework.response import Response

from interview.models import Interview


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        limit = self.request.GET.get('limit', self.page_size)
        next_page = None
        previous_page = None
        if self.page.has_next():
            next_page = self.page.next_page_number()
        if self.page.has_previous():
            previous_page = self.page.previous_page_number()
        return Response({
            'next': self.get_next_link(),
            'next_page': next_page,
            'previous': self.get_previous_link(),
            'previous_page': previous_page,
            'count': self.page.paginator.count,
            'limit': int(limit),
            'results': data,
        })


# Проверяю create/update на start_time
def check_interview_start_time(self, request):
    interview = Interview.objects.get(
        id=request.data.get('interview')
    )

    if not interview.start_time:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
    else:
        return Response({
            "error": True,
            "msg": "Дата старта была добавлена в опрос процесс необратим"
        })


# Класс для post/put/delete только администратору
class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            print(request.user.is_staff, request.method)
            return request.user.is_staff
