from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError


User = get_user_model()

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email' , 'first_name' , 'last_name' , 'phone_number')

