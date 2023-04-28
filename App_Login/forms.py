from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateNewUser(UserCreationForm):
    email = forms.EmailField(required=True) #as not included in User auth class
    class Meta:
        model = User
        fields = ('email','username','password1','password2')