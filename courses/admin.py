from django.contrib import admin
from .models import Course , Video , Category , Comment
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin

# ----------actions-----------
@admin.action(description="غیر فعال کردن دوره ها")
def inactive_items(modeladmin , request , queryset):
    result = queryset.update(active=False)
    modeladmin.message_user(request , f'{result} مورد غیر فعال گردید.')

@admin.action(description="فعال کردن دوره ها")
def active_items(modeladmin , request , queryset):
    result = queryset.update(active=True)
    modeladmin.message_user(request , f'{result} مورد فعال گردید.')

#----------inlines-------------
class VideoCourseInlines(StackedInlineJalaliMixin,admin.StackedInline):
    model = Video
    extra = 0

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title','show_image_in_admin','get_teacher_name','price' ,'discount' ,'category_to_str' ,'tag_to_str','total_time' , 'is_finish','level' , 'active']
    prepopulated_fields = {'slug':('title',)}
    list_filter = ['active','is_finish']
    search_fields = ['title','categories__title','teacher__username','teacher__first_name','teacher__last_name']
    list_editable = ['active' , 'is_finish']
    raw_id_fields = ['teacher']
    actions = [inactive_items,active_items]
    inlines = [VideoCourseInlines]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    prepopulated_fields = {'slug':('title',)}
    list_editable = ['active']
    list_filter = ['active']
    search_fields = ['title']
    actions = [inactive_items,active_items]


@admin.register(Video)
class VideoAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
    list_display = ['title','position','video','course','time','get_publish_time_jalali','active']
    list_filter = ['active','publish_time']
    search_fields = ['active','course__title']
    raw_id_fields = ['course']
    actions = [inactive_items,active_items]


    def get_publish_time_jalali(self, obj):
        return datetime2jalali(obj.publish_time).strftime('%Y/%m/%d _ %H:%M:%S')

    get_publish_time_jalali.short_description = 'تاریخ انتشار'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'active' , 'parent','get_created_jalali')
    list_editable = ('active',)
    list_filter = ('user','active','parent')
    actions = [inactive_items,active_items]

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%Y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'