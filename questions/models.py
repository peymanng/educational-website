from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from courses.models import Course

User = get_user_model()

class Question(models.Model):
    title = models.CharField(max_length=200 , verbose_name='عنوان')
    slug = models.SlugField(unique=True , allow_unicode=True)
    body = models.TextField(verbose_name='بدنه')
    course = models.ForeignKey(Course , on_delete=models.CASCADE , related_name='questions',verbose_name='دوره')
    user = models.ForeignKey(User , on_delete=models.CASCADE , verbose_name='کاربر')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, verbose_name='فعال/غیر فعال')
    is_solved = models.BooleanField(default=False,verbose_name='حل شده است؟')

    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'

    def get_absolute_url(self):
        return reverse('question_detail' , kwargs={'slug' : self.slug})

    def __str__(self):
        return self.title

class Answer(models.Model):
    body = models.TextField(verbose_name='بدنه')
    user = models.ForeignKey(User , on_delete=models.CASCADE , verbose_name='کاربر')
    question = models.ForeignKey(Question , on_delete=models.CASCADE , related_name='answers' , verbose_name="سوال")
    created = models.DateTimeField(auto_now_add=True)
    correct_answer = models.BooleanField(default=False,verbose_name='ایا پاسخ درست است؟')
    active = models.BooleanField(default=True, verbose_name='فعال/غیر فعال')

    class Meta:
        verbose_name = 'پاسخ'
        verbose_name_plural = 'پاسخ ها'

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if self.correct_answer:
            self.question.is_solved = True
            self.question.save()
        else:
            self.question.is_solved=False
            self.question.save()
        super(Answer, self).save(*args, **kwargs)