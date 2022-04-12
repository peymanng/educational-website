from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from blog.models import Post, PostCategory
from orders.models import Order
from questions.models import Question, Answer
from users.models import Profile
from courses.models import Course, Category, Comment
from .permissions import IsSuperUserOrUserOrReadOnly, IsProfileOwnerOrSuperUserOrReadOnly
from . import serializers


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [AllowAny]

class UserDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [IsSuperUserOrUserOrReadOnly]

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsProfileOwnerOrSuperUserOrReadOnly]

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.get_publish_course()
    serializer_class = serializers.CourseSerializer
    filter_backends = [DjangoFilterBackend , filters.SearchFilter , filters.OrderingFilter]
    filterset_fields = [
        'categories',
        'price',
        'is_finish',
    ]
    search_fields = ['title', 'description' , 'tags__name' , 'teacher__username']
    ordering_fields = ['price' ,'created' , 'updated']

class CourseRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.get_publish_course()
    serializer_class = serializers.CourseSerializer

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

class CategoryFilterCourseAPIView(generics.ListAPIView):
    serializer_class = serializers.CourseSerializer

    def get_queryset(self):
        category_id = self.kwargs['id']
        return Course.objects.filter(categories__in=[category_id]).distinct()

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderView(generics.ListCreateAPIView):
    serializer_class = serializers.OrderCreateSerializer
    queryset = Order.objects.all()

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.CourseSerializer

class PostCategoryListAPIView(generics.ListAPIView):
    queryset = PostCategory.objects.all()
    serializer_class = serializers.PostCategorySerializer

class PostCategoryFilterPostAPIView(generics.ListAPIView):
    serializer_class = serializers.CourseSerializer

    def get_queryset(self):
        category_id = self.kwargs['id']
        return Course.objects.filter(categories__in=[category_id]).distinct()

class QuestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class QuestionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer

class AnswerAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAuthenticated]