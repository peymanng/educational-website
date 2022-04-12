from django.urls import path
from . import views

urlpatterns = [
    path('account/resgister/' , views.UserRegisterAPIView.as_view()),
    path('account/<int:pk>/' , views.UserDetailAPIView.as_view()),
    path('account/profile/<int:pk>/' , views.ProfileAPIView.as_view()),
    path('courses/' , views.CourseListAPIView.as_view()),
    path('courses/<int:pk>' , views.CourseRetrieveAPIView.as_view()),
    path('categories' , views.CategoryListAPIView.as_view()),
    path('categories/<int:id>' , views.CategoryFilterCourseAPIView.as_view()),
    path('comments/' , views.CommentCreateAPIView.as_view()),
    path('orders/', views.OrderView.as_view()),
    path('blog/posts/' , views.PostListAPIView.as_view()),
    path('blog/posts/<int:pk>' , views.PostListAPIView.as_view()),
    path('blog/categories/' , views.PostCategoryListAPIView.as_view()),
    path('blog/categories/<int:id>', views.PostCategoryFilterPostAPIView.as_view()),
    path('questions/' , views.QuestionListCreateAPIView.as_view()),
    path('questions/<int:pk>' , views.QuestionRetrieveAPIView.as_view()),
    path('answers/' , views.AnswerAPIView.as_view()),
]