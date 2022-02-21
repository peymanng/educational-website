from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from PIL import Image


class UserManager(BaseUserManager):
    def create_user(self, email, username,first_name=None , last_name=None ,  phone_number=None,  password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have an username')


        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,username , first_name=None , last_name=None , phone_number=None, password=None):
        user = self.create_user(
            email,
            username= username,
            phone_number=phone_number,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=100 , unique=True , verbose_name = 'نام کاربری')
    phone_number = models.CharField(max_length=11 , null=True , blank=True,verbose_name = 'شماره تلفن')
    register_date = models.DateTimeField(auto_now_add=True ,)
    first_name = models.CharField(max_length=50, null=True , blank=True, verbose_name = 'نام')
    last_name = models.CharField(max_length=100, null=True , blank=True, verbose_name = 'نام خانوادگی')
    is_active = models.BooleanField(default=True, verbose_name = 'فعال/غیر فعال')
    is_admin = models.BooleanField(default=False, verbose_name = 'ادمین')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name='کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return None


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name = 'کاربر')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', verbose_name = 'عکس')

    class Meta:
        verbose_name='پروفایل'
        verbose_name_plural = 'پروفایل ها'

    def __str__(self):
        return f'{self.user.username} Profile'

    def show_image_in_admin(self):
        if self.image:
            return format_html(
                "<img style='border-radius: 5px;' width=100px height=75px  src='{}' >".format(self.image.url))
        else:
            return ''

    show_image_in_admin.allow_tags = True
    show_image_in_admin.short_description = 'تصویر'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)  # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)