import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import DetailView
from .forms import StudentForm, ProfileUpdateForm
from .models import Student, IssuedBook, Fine
from django.contrib.auth.models import User 

# Create your views here.
def index(request):
    return HttpResponse("Welcome to Bestpeers")


def currentdatetime(request):
    now = datetime.datetime.now()
    html = "<h1>It is now %s</h1>" % now
    return HttpResponse(html)


def student_detail(request): 
    if request.method == 'POST':    
        form = StudentForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = StudentForm()
    return render(request, 'form.html', {'form': form})


def home(request):
    return render(request, 'home.html')

# def registration(request):
#     return render(request, 'registration.html')

# def signin(request):
#     return render(request, 'signin.html')

def user_login(request):
    # import pdb;pdb.set_trace()
    return render(request, 'login.html')


def user_logout(request):
    return redirect('accounts/login')


# def profile(request):
#     # mobile_number = request.POST.get('mobile_number')
#     # course_id = request.POST.get('course_id') 
#     # student = Student.objects.values(mobile_number = mobile_number, course_id = course_id)
#     user = request.user
#     student= Student.objects.get(user_id=user)
#     return render(request, 'profile.html', {'student': student})



class Profile(DetailView):
    template_name = 'profile.html'
    
    def get_object(self, queryset=None):
        return Student.objects.get(user_id=self.request.user)


def issued_book(request):
    user = request.user
    #issued_book= IssuedBook.objects.filter(roll_no__user_id=user)
    fine= IssuedBook.objects.filter(roll_no__user_id=user).values(
        'issue_id', 
        'fine__fine_id', 
        'fine__fine_date', 
        'fine__fine_amount', 
        'issue_date', 
        'expiry_date', 
        'book_id__name'
        )
    return render(request, 'issuedbook.html', {'fine':fine})


# def fine(request):
#     user = request.user
#     fine= Fine.objects.filter(issue_id__roll_no__user_id=user)
#     return render(request, 'fine.html', {'fine':fine})


def profile_edit(request):
    user = request.user
    student = Student.objects.get(user_id=user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponse('<h1>Successfully Update</h1>')

    else:
        form = ProfileUpdateForm(initial={
                  'username': user.username,
                  'first_name' : user.first_name,
                  'last_name' : user.last_name,
                  'email' : user.email,
                  'mobile_number' : student.mobile_number,
                  'course_id' : student.course_id             
                  }
                  ) 
    return render(request, "account/studprofileupdate.html", {'form':form})


def delete_profile(request, id):
    student = Student.objects.get(pk=id)
    student.user_id.delete()
    return HttpResponse("Successfully Deleted")


# from rest_framework import viewsets
# from . serializers import *
# from rest_framework.authentication import BasicAuthentication, SessionAuthentication
# from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
# from rest_framework_simplejwt.authentication import JWTAuthentication
# # Authentication and Permission

# class StudentModelViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     # #authentication_classes = [JWTAuthentication]
#     # authentication_classes = [SessionAuthentication]
#     # # authentication_classes = [BasicAuthentication]
#     # permission_classes = [IsAuthenticated]
#     # #permission_classes = [AllowAny]
#     # #permission_classes = [IsAdminUser]

# class UserModelViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

# class IssuedBookModelViewSet(viewsets.ModelViewSet):
#     queryset = IssuedBook.objects.all()
#     serializer_class = IssuedbookSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
