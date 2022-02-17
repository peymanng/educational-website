from django.urls import path , re_path
from . import views

urlpatterns = [
    path('', views.course_list , name='course_list'),
    re_path(r'category/(?P<slug>[-\w]+)/', views.category_courses , name='category_courses'),
    re_path(r'tags/(?P<slug>[-\w]*)/', views.tag_courses , name='tag_courses'),
    path('filter/',views.course_filter , name='course_filter'),
    re_path(r'(?P<slug>[-\w]+)/' , views.course_detail, name="course_detail"),
]