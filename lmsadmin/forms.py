import datetime
from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from .models import Admin 
from django.contrib.auth.models import User 
from django.forms import ModelForm
from lmsapp.models import Student, Book, IssuedBook, Fine



class AdminSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True, help_text='Enter a valid email address.')
    mobile = forms.CharField(max_length=10, required=True)
    # is_superuser = forms.BooleanField(default=True)
    class Meta:
         model = User
         fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'mobile',
            'is_superuser',
            
            ]
         widgets = {
             'username': forms.TextInput(attrs={'placeholder': 'Username'}),
         }

            # 'first_name': forms.TextInput(attrs={'placeholder': 'first_name'}),            
            #  'last_name': forms.TextInput(attrs={'placeholder': 'last_name'}),
            #  'email': forms.TextInput(attrs={'placeholder': 'email'}),
            # 'password1': forms.TextInput(attrs={'placeholder': 'password'}),
            #  'password2': forms.TextInput(attrs={'placeholder': 'confirm password'}),
            #   'mobile': forms.TextInput(attrs={'placeholder': 'Mobile Number'}),
         
    def save(self, request):
        user = super(AdminSignupForm, self).save(request)
        mobile = self.cleaned_data.get('mobile')
        admin = Admin.objects.create(
            mobile = mobile, 
            user_id=user,
           
            )
        return user
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address is already in use ')

    
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'author_id',
            'category_id',
            'name',
            'isbn_number',
            'publication',
            'price',
            'quantity'
        ]

class IssueBookForm(ModelForm):
    class Meta:
        model = IssuedBook
        exclude = [
            'issue_date',
            'expiry_date',         
        ]
    
        

   