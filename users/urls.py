from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name='login'),
    path("signup/", views.signup_view, name='signup'),
    path("logout/", views.logout_view, name='logout'),
    path('profile/',views.profile,name='profile'),
    path('change-info/',views.update_user , name='update_user'),
    path('change-pass/',views.update_pass , name='update_pass'),
    path('change-profpic', views.update_prof_pic , name='update_profpic'),
    path('user-courses/',views.user_courses,name='user_courses'),
]