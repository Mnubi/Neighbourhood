from .models import Business, Neighbourhood, Post, Profile
from django.forms import ModelForm
from django import forms



class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user'] 

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic','email', 'neighbourhood') 

class BusinessForm(forms.ModelForm):
    class Meta:
        model=Business
        fields=['name','email','description','neighbourhood']

class NeighbourhoodForm(forms.ModelForm):
    class Meta:
        model = Neighbourhood
        exclude = ('admin',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=['title','content','neighbourhood']

class NewBusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('user',)

# class PasswordChangeForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields= ['old_password', 'new_password', 'Confirm_new_password']
