from django.contrib import admin
from .models import OrderItem , Order
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin
from courses.admin import export_as_json


class OrderItemInline(StackedInlineJalaliMixin,admin.StackedInline):
    model = OrderItem
    raw_id_fields = ['course']

@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
    list_display = ['id','user','email','paid','get_created_jalali','get_update_jalali']
    list_filter = ('paid','created','update')
    actions = (export_as_json,)
    inlines = [OrderItemInline]

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%Y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'

    def get_update_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%Y/%m/%d _ %H:%M:%S')

    get_update_jalali.short_description = 'تاریخ بروزرسانی'