from allauth.account.forms import SignupForm
from django import forms
from django.forms import ModelForm
from .models import Student 
from django.contrib.auth.models import User


class StudentForm(forms.Form):
    first_name = forms.CharField(label='first name', max_length=100)
    last_name = forms.CharField(label='last name', max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    age = forms.IntegerField()


class MyCustomSignupForm(SignupForm, ModelForm):
    first_name = forms.CharField(max_length=25, label='First Name',  widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=25, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    class Meta:
         model = Student
         fields = [
            "mobile_number", 
            "course_id",
            ]
         widgets = {
             'mobile_number': forms.TextInput(attrs={'placeholder': 'Mobile Number'})
         }
         
    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        mobile_number = self.cleaned_data.get('mobile_number')
        course_id = self.cleaned_data.get('course_id')
        
        student = Student.objects.create(
            mobile_number=mobile_number, 
            course_id=course_id, 
            user_id=user
            )
        return user

class ProfileUpdateForm(ModelForm):
    username =  forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    # mobile_number = forms.CharField(max_length=10, required=True)
    # course_id = forms.CharField(max_length=10, required=True)
    class Meta:
         model = Student
         fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'mobile_number',
            'course_id'
            ]


    def save(self):
        #breakpoint()
        user = super(ProfileUpdateForm, self).save()
        mobile_number = self.cleaned_data.get('mobile_number')
        course_id = self.cleaned_data.get('course_id')
        student = Student.objects.filter(user_id=user)
        student.update(
            mobile_number=mobile_number, 
            course_id=course_id
            )
      













        # user = super(MyCustomSignupForm, self).save(request)
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        # user.save()
        # username = request.POST.get('username')
        # email = request.POST.get('email')
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        # mobile_number = request.POST.get('mobile_number')
        # course_id = request.POST.get('course_id')
        # password1 = request.POST.get('password1')
        # password2 = request.POST.get('password2')




        
        # return user
    


    
        


    
        
        



