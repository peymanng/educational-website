from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit.serializers import TaggitSerializer , TagListSerializerField
from users.models import Profile
from courses.models import Category, Course, Comment, Video
from orders.models import Order , OrderItem
from blog.models import Post , PostCategory
from questions.models import Question , Answer

User = get_user_model()

# users

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password'
        )

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user' , 'image')

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'title',
            'video',
            'position',
            'description',
            'time',
            'active'
        )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id' , 'title' , 'parent' , 'active')

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), required=False, allow_null=True, default=None)
    class Meta:
        model = Comment
        fields = (
            'course',
            'user',
            'body',
            'parent',
        )

class CourseSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField()
    video = VideoSerializer(many=True)
    categories = CategorySerializer(many=True)
    comment = CommentSerializer(many=True)
    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'description',
            'categories',
            'price',
            'discount',
            'created',
            'updated',
            'teacher',
            'image',
            'level',
            'student',
            'is_finish',
            'tags',
            'visits',
            'video',
            'comment'
        )

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'course',
            'price',
        )

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = (
            'user',
            'email',
            'paid',
            'items'
        )

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for order_item in items:
            OrderItem.objects.create(order=order , **order_item)
        return order

class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ('id' , 'title')

class PostSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Post
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Question
        fields = (
            'id',
            'title',
            'slug',
            'body',
            'course',
            'user',
            'created',
            'active',
            'is_solved',
            'answers'
        )
