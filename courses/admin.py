import csv
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Course , Video , Category , Comment , IP
from jalali_date import datetime2jalali
from django.http import HttpResponse
from django.core import serializers
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin

# ----------actions-----------
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields if field.name not in ('description','image')]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response,delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL, dialect='excel')

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "خروجی اکسل"


@admin.action(description="غیر فعال کردن دوره ها")
def inactive_items(modeladmin , request , queryset):
    result = queryset.update(active=False)
    modeladmin.message_user(request , f'{result} مورد غیر فعال گردید.')

@admin.action(description="فعال کردن دوره ها")
def active_items(modeladmin , request , queryset):
    result = queryset.update(active=True)
    modeladmin.message_user(request , f'{result} مورد فعال گردید.')

@admin.action(description='گرفتن خروجی json')
def export_as_json(modeladmin , request , queryset):
    response = HttpResponse(content_type = 'application/json')
    serializers.serialize('json',queryset,stream=response)
    return response

#----------inlines-------------
class VideoCourseInlines(StackedInlineJalaliMixin,admin.StackedInline):
    model = Video
    extra = 0

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['title','show_image_in_admin','get_teacher_name','price' ,'get_visits','discount' ,'category_to_str' ,'tag_to_str','total_time' , 'is_finish','level' , 'active']
    prepopulated_fields = {'slug':('title',)}
    list_filter = ['active','is_finish']
    search_fields = ['title','categories__title','teacher__username','teacher__first_name','teacher__last_name']
    list_editable = ['active' , 'is_finish']
    raw_id_fields = ['teacher']
    actions = [inactive_items,active_items , export_as_json,"export_as_csv"]
    inlines = [VideoCourseInlines]
    readonly_fields = ['course_image']
    def course_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=obj.image.width,
            height=obj.image.height,
            )
    )
    course_image.short_description = 'عکس دوره'

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

admin.site.register(IP)