from django.urls import path , re_path
from . import views

urlpatterns = [
    path("", views.posts, name="post_list"),
    re_path(r"post/(?P<slug>[-\w]+)", views.post, name="post_detail"),
]