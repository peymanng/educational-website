# Generated by Django 4.0.1 on 2022-02-24 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_alter_ip_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('body', models.TextField(verbose_name='بدنه')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True, verbose_name='فعال/غیر فعال')),
                ('is_solved', models.BooleanField(default=False, verbose_name='حل شده است؟')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='courses.course', verbose_name='دوره')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='بدنه')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('correct_answer', models.BooleanField(default=False, verbose_name='ایا پاسخ درست است؟')),
                ('active', models.BooleanField(default=True, verbose_name='فعال/غیر فعال')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='questions.question', verbose_name='سوال')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
    ]
