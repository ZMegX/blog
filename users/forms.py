from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm #Inheritance Relationship

from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
        
class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
  image = forms.FileField(required=False)

  class Meta:
    model = Profile 
    fields = ['image']    