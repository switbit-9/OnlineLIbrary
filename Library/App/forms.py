from django import forms
from django.db.models.expressions import WindowFrame
from django.forms import fields
from django.forms.formsets import DELETION_FIELD_NAME
from django.forms.models import ModelForm
from django.forms.widgets import PasswordInput, TextInput
from django.http.response import FileResponse
from .models import *


class RegisterForm(forms.ModelForm):
    
    email = forms.CharField(
        widget=forms.EmailInput(
        attrs={
            'placeholder' : 'Enter Email...'
            }   
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder' : 'Email Username...'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs= {
                'placeholder': 'Enter Password...'
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password...'
            }
        )
    )

    


    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    


class LoginForm(forms.Form):
    username = forms.CharField(
    widget=TextInput(
        attrs={
            'placeholder' : 'Email or Username',
            'class' : 'username'
            }
        ), max_length=20
    )
    password = forms.CharField(
        widget=PasswordInput(
            attrs={
            'placeholder': 'Password...',
            'class' : 'password'
            }
        ), max_length=20
    )

class BooksForm(ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'price', 'quantity', 'availability', 'books_img', 'publisher', 'category']

class BorrowForm(ModelForm):
    class Meta:
        model = Borrow
        fields= ['date']

class MessageFrom(ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your name...',
                'label' : 'Surname'
                }
            )
        )
    
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
            'placeholder': 'Enter your email...',    
            'label' : 'Email'      
            }
        )
    )

    content = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder' : 'Write your message ...',
                'class': 'content',
                'label' : 'Subject'
            }
        )
    )

    class Meta:
        model = Message
        fields = ['name', 'email', 'content']

