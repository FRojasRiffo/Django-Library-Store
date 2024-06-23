from django import forms
from django.forms import ModelForm
from .models import Book
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        labels = {
            'title': 'Título del libro',
            'price': 'Precio',
            'cover_image': 'Imagen de portada',
            'description': 'Descripción',
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username','email','password1','password2')