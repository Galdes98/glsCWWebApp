from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from.models import Post
from crispy_forms.helper import FormHelper

MOD = [
    ('','Personal'),
    ('','Jefe de personal'),
]

class RegisterForm(UserCreationForm):
    
    email = forms.EmailField(required=True)
    #mod = forms.ChoiceField(choices=MOD)
    class Meta:
        model = User
        fields = ["username","email","password1", "password2"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]
