from django import forms
from django.contrib.auth.models import User
from .models import Profile,Birthday
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile','whatsapp_number','image']
       
class BirthdayAddForm(forms.ModelForm):
    class Meta:
        model = Birthday
        fields = ['fname','mname','lname','dob']

'''
class SkillAddForm(forms.ModelForm):
    class Meta:
        model=Skill
        fields=['skill','u_score']
'''