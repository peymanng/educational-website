# Generated by Django 4.0.1 on 2022-02-23 20:40

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('courses', '0002_alter_ip_options'),
        ('blog', '0003_alter_postcategory_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to=settings.AUTH_USER_MODEL, verbose_name='نویسنده'),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='متن'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(to='blog.PostCategory', verbose_name='دسته بندی'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=100, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='posts/', verbose_name='عکس'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='برچسب ها'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='post',
            name='visits',
            field=models.ManyToManyField(blank=True, related_name='views', to='courses.IP', verbose_name='بازدید ها'),
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='description',
            field=models.CharField(max_length=130, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='عنوان'),
        ),
    ]
