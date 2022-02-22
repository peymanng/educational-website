from django.contrib import admin
from .models import PostCategory , Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title' , 'get_categories', 'slug' , 'get_visits' , 'tag_list' , 'pub_date')
    prepopulated_fields = {'slug' : ('title' ,)}

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    tag_list.short_description = 'برچسب ها'

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('title' , 'slug')
    prepopulated_fields = {"slug": ("title",)}