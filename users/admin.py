from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from jalali_date import datetime2jalali
from courses.admin import export_as_json , ExportCsvMixin
from .models import User,Profile


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username','first_name','last_name' ,'phone_number', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin,ExportCsvMixin):
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ('register_date',)
    list_display = ('email', 'username','get_register_date_jalali' , 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    actions = (export_as_json,'export_as_csv')
    fieldsets = (
        (None, {'fields': ('email', 'username','password')}),
        ('Personal info', {'fields': ('phone_number', 'first_name','last_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email','username')
    ordering = ('username',)
    filter_horizontal = ()

    def get_register_date_jalali(self, obj):
        return datetime2jalali(obj.register_date).strftime('%Y/%m/%d _ %H:%M:%S')

    get_register_date_jalali.short_description = 'تاریخ ثبت نام'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','show_image_in_admin']
    readonly_fields = ['profile_image']
    def profile_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=obj.image.width,
            height=obj.image.height,
            )
    )
    profile_image.short_description = 'عکس پروفایل'

admin.site.register(Profile,ProfileAdmin)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)