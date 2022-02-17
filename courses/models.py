from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator , MaxValueValidator
from django.utils import timezone
from django.utils.html import format_html
from ckeditor.fields import RichTextField
from django.db.models import Q
from taggit.managers import TaggableManager
from django.urls import reverse
from PIL import Image
# Create your models here.

User = get_user_model()

class CourseCategoryManager(models.Manager):
    def get_active_category(self):
        return self.get_queryset().filter(active=True)


class CourseManager(models.Manager):
    def get_publish_course(self):
        return self.get_queryset().filter(active=True)

    def get_course_by_category(self, category_name):
        return self.get_queryset().filter(categories__title__iexact=category_name, active=True).distinct()

    def search(self, query):
        lookup = (
                Q(title__icontains=query) | Q(description__icontains=query) #| Q(tags__title__icontains=query)
        )
        return self.get_queryset().filter(lookup, active=True).distinct()

    def get_popular_course(self):
        return self.get_queryset().annotate(q_count=models.Count('student')).filter(active=True).order_by('-q_count',
                                                                                      '-created').distinct()

class VideoManager(models.Manager):
    def get_active_video(self):
        return self.get_queryset().filter(active=True)

class CommentManager(models.Manager):
    def get_active_comments(self):
        return self.get_queryset().filter(active=True)

class Category(models.Model):
    title = models.CharField(max_length=50 , verbose_name="عنوان")
    slug = models.SlugField(unique=True, allow_unicode=True)
    active = models.BooleanField(default=True,verbose_name='فعال/غیر فعال')
    parent = models.ForeignKey('self',on_delete=models.PROTECT , blank=True , null=True , related_name='children')

    objects = CourseCategoryManager()

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title

class Course(models.Model):
    LEVEL_CHOICES = (
        ('b', 'مقدماتی'),
        ('m', 'متوسط'),
        ('a', 'پیشرفته'),
        ('bm', 'مقدماتی تا متوسط'),
        ('ma', 'متوسط تا پیشرفته'),
        ('ba', 'مقدماتی تا پیشرفته'),
    )

    title = models.CharField(max_length=130,verbose_name="عنوان")
    description = RichTextField(verbose_name='توضیحات')
    slug = models.SlugField(unique=True, allow_unicode=True)
    active = models.BooleanField(default=True, verbose_name='فعال/غیر فعال')
    categories = models.ManyToManyField(Category , verbose_name='دسته بندی ها')
    price = models.PositiveIntegerField(verbose_name="قیمت")
    discount = models.PositiveIntegerField(blank=True, null=True,validators=[MinValueValidator(1), MaxValueValidator(100)] , verbose_name="تخفیف")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='teacher_courses',verbose_name='مدرس')
    image = models.ImageField(upload_to='courses/course-img/',verbose_name='عکس')
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='b', verbose_name='سطح دوره')
    student = models.ManyToManyField(User, blank=True, related_name='student_courses', verbose_name='دانشجو')
    is_finish = models.BooleanField(default=False, verbose_name='آیا دوره تمام شده؟')
    tags = TaggableManager(verbose_name='برچسب ها')

    objects = CourseManager()

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره ها'
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)  # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('course_detail', args=[str(self.slug)])

    def total_price(self):
        if self.discount:
            total = (self.price * self.discount) / 100
            return int(self.price - total)
        else:
            return self.price

    total_price.short_description = 'جمع مبلغ کل'

    def total_discount(self):
        if self.discount:
            total = (self.price * self.discount) / 100
            return int(total)
        else:
            return 0


    def category_to_str(self):
        return " - ".join([category.title for category in self.categories.get_active_category()])

    category_to_str.short_description = 'دسته بندی'

    def tag_to_str(self):
        return " - ".join([tag.name for tag in self.tags.all()])

    tag_to_str.short_description = 'برچسب ها'

    def show_image_in_admin(self):
        if self.image:
            return format_html(
                "<img style='border-radius: 5px;' width=100px height=75px  src='{}' >".format(self.image.url))
        else:
            return ''
    show_image_in_admin.allow_tags =True
    show_image_in_admin.short_description = 'تصویر'

    def get_sec(self):
        total = 0
        for video in self.video.get_active_video():
            secs = video.time.hour * 3600 + video.time.minute * 60 + video.time.second
            total += secs
        return total

    def total_time(self):
        total = 0
        for video in self.video.get_active_video():
            secs = video.time.hour * 3600 + video.time.minute * 60 + video.time.second
            total += secs

        # return datetime.time(total // 3600, (total % 3600) // 60, total % 60)
        def hour_return():
            if len(str(total // 3600)) == 1:
                return f"0{total // 3600}"
            else:
                return total // 3600

        def minute_return():
            if len(str((total % 3600) // 60)) == 1:
                return f"0{(total % 3600) // 60}"
            else:
                return (total % 3600) // 60

        def second_return():
            if len(str(total % 60)) == 1:
                return f"0{total % 60}"
            else:
                return total % 60

        return f"{hour_return()}:{minute_return()}:{second_return()}"

    total_time.short_description = 'مدت زمان'

    def get_level(self):
        if self.level == 'b':
            return 'مقدماتی'
        elif self.level == 'm':
            return 'متوسط'
        elif self.level == 'a':
            return 'پیشرفته'
        elif self.level == 'bm':
            return 'مقدماتی تا متوسط'
        elif self.level == 'ma':
            return 'متوسط تا پیشرفته'
        elif self.level == 'ba':
            return 'مقدماتی تا پیشرفته'

    def count_of_student(self):
        count = len(self.student.all())
        return count

    count_of_student.short_description = 'تعداد دانشجو ها'

    def get_teacher_name(self):
            return self.teacher
    get_teacher_name.short_description = 'مدرس'

    def finish(self):
        if self.is_finish:
            return 'به پایان رسیده'
        else:
            return 'در حال برگزاری'


class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان جلسه")
    video = models.FileField(upload_to='course/course-videos/', verbose_name='ویدیو')
    position = models.PositiveIntegerField(default=0, verbose_name='شماره جلسه')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='video',
                               verbose_name='دوره')
    description = models.TextField(verbose_name="توضیحات")
    time = models.TimeField(verbose_name='زمان ویدیو', help_text='مثال:00:00:30')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")

    objects = VideoManager()

    class Meta:
        verbose_name = 'ویدیو'
        verbose_name_plural = 'ویدیوها'
        ordering = ['position']

    def __str__(self):
        return self.title

class Comment(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='comment',verbose_name='دوره')
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='comment',verbose_name='کاربر')
    body = models.TextField(default=" ",verbose_name='بدنه')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies' , on_delete=models.CASCADE ,verbose_name='والد')

    objects = CommentManager()

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.user)
