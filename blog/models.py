from django.db import models
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from taggit.managers import TaggableManager
from courses.models import IP

User = get_user_model()

class PostCategory(models.Model):
    title = models.CharField(max_length=100, unique=True,verbose_name="عنوان")
    slug = models.SlugField(allow_unicode=True)
    description = models.CharField(max_length=130, null=True,verbose_name="توضیحات")

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title

    def get_absolut_url(self):
        return reverse('posts_by_category' , kwargs={'slug' : self.slug})

class Post(models.Model):
    title = models.CharField(max_length=50,verbose_name="عنوان")
    slug = models.SlugField(unique=True, allow_unicode=True)
    category = models.ManyToManyField(PostCategory,verbose_name="دسته بندی")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post',verbose_name="نویسنده")
    description = models.CharField(max_length=100,verbose_name="توضیحات")
    body = RichTextUploadingField(verbose_name="متن")
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    image = models.ImageField(upload_to='posts/',verbose_name="عکس")
    tags = TaggableManager(verbose_name="برچسب ها")
    visits = models.ManyToManyField(IP, blank=True, related_name='views' ,verbose_name="بازدید ها")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail' , kwargs={'slug' : self.slug})

    def get_categories(self):
        return ' , '.join([category.title for category in self.category.all()])

    get_categories.short_description = "دسته بندی ها"

    def get_visits(self):
        return self.visits.count()

    get_visits.short_description = 'بازدید'
