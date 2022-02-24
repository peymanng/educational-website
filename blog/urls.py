from django.urls import path , re_path
from . import views

urlpatterns = [
    path("", views.posts, name="post_list"),
    re_path(r'category/(?P<slug>[-\w]+)/', views.posts_by_category, name='posts_by_category'),
    re_path(r"post/(?P<slug>[-\w]+)", views.post, name="post_detail"),
    re_path(r'tag/r"(?P<tag_slug>[-\w]*)/', views.posts , name='posts_by_tag')
]