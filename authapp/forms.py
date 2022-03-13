from django.contrib.auth.models import User
from django import forms
# from .models import Profile
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from django.db.models.fields import CommaSeparatedIntegerField
from .models import UserRegistrationModel
from django.contrib.auth.forms import PasswordResetForm


class TestUserForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    password = forms.CharField()
    confirm_password = forms.CharField()
    code = forms.CharField()

class UserRegistration(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match.')
            return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


# class CreatePostForm(forms.ModelForm):
#     class Meta:
#         model = UserPost
#         fields = ('post_text',)