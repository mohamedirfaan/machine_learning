from django import forms
from django.forms import ModelForm
from .models import Member
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput
from .models import post_photos_and_videos
class CustomClearableFileInput(ClearableFileInput):
    template_name = 'custom_clearable_file_input.html'
class regform(ModelForm):
    class Meta:
        model=Member
        fields=['username','email','password','gender','profile_pic']
        labels={
            'name':'',
            'email':'',
            'password':'',
            'gender':'',
            'profile_pic':'',
        }
        widgets={
            'username':forms.TextInput(),
            'email':forms.TextInput(),
            'password':forms.PasswordInput(),
            'gender':forms.Select(attrs={'class':'float-right landingRightField'},choices=[('Male','Male'),('Female','Female')]),
            #'profile_pic':forms.ImageField({'class':'form-control','place-holder':'picture'})
        }

class postform(ModelForm):
    class Meta:
        model = post_photos_and_videos
        fields = ['post_or_video','tags']
        labels={
            'post_or_video':'',
            'tags':'',
        }
        widgets = {
            'tags':forms.TextInput()
        }