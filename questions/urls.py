from django.urls import path , re_path
from . import views

urlpatterns = [
    path('' , views.questions , name="question_list"),
    re_path(r'question/(?P<slug>[-\w]+)/' , views.question , name="question_detail"),
    path('ask/' , views.ask_question , name ='ask_question'),
    re_path(r'(?P<slug>[-\w]+)/' , views.questions , name='course_questions'),
]