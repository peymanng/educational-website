from django.contrib import admin
from .models import Question , Answer

@admin.register(Question)
class QusetionAdmin(admin.ModelAdmin):
    list_display = ('title' , 'course' , 'user'  , 'is_solved' , 'active')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_solved' , 'active')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'correct_answer', 'active')
    list_editable = ('correct_answer', 'active')