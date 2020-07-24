from django import forms
from django.forms import ModelForm

from urbazar_app.choices import  Categories
from urbazar_app.models import Product
from urbazar_app.models import Student
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.widgets import Input, TextInput


class UploadProductForm(ModelForm):
   title = forms.CharField(label='Item Name', min_length=5, max_length=100, required=True, help_text='Should be more than 5 characters and less than 100 characters')
   description = forms.CharField(widget=forms.Textarea, min_length=10)
   price = forms.IntegerField(min_value=0, required=True)
   category = forms.ChoiceField(choices=Categories, widget=forms.Select(attrs={'class': 'form-control'}))

   class Meta:
       model = Product
       fields = ['title', 'description', 'price', 'category', 'image']

class EditProfileForm(ModelForm):

    class Meta:
        model = Student
        fields = ['image', 'first_name', 'last_name', 'bio', 'college', 'email']


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Your first name', widget=forms.TextInput
      (attrs={'class' : 'form-control'}))
    last_name = forms.CharField(max_length=100, help_text='last_name', widget=forms.TextInput
      (attrs={'class' : 'form-control'}))
    room_number = forms.IntegerField(max_value=500, help_text='Enter your Room Number', widget=forms.TextInput
      (attrs={'class' : 'form-control'}))
    hostel_name = (
        ('Visvesaraya Hostel', 'Visvesaraya Hostel'),
        ('S.N. Bose Hostel', 'S.N. Bose Hostel'),
        ('Ramanujan Hostel', 'Ramanujan Hostel'),
        ('Aryabhatta Hostel', 'Aryabhatta Hostel'),
        ('Rajputana Hostel', 'Rajputana Hostel'),
    )
    hostel_name = forms.ChoiceField(choices=hostel_name,widget=forms.Select(attrs={'class' : 'form-control'}))
    image = forms.FileField(required=False, widget=forms.FileInput(attrs={'class' : 'form-control', 'accept': 'image/*'}))
    username = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter your email'}))
    password1=forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2=forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-type your password'}))

    class Meta:
        model = DjangoUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'room_number', 'hostel_name', 'image',)#('username', 'password1', 'password2',)
