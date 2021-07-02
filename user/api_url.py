from rest_framework import routers

from .api_view import UserViewSet

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)
