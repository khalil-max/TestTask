from rest_framework import routers

from .api_view import InterviewViewSet, QuestionViewSet, AnswerViewSet, \
    ChoiceViewSet

router = routers.SimpleRouter()
router.register(r'interviews', InterviewViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'choices', ChoiceViewSet)
