import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import (DeleteView, DetailView, RedirectView,
                                  TemplateView, View)

from lmsapp.forms import ProfileUpdateForm
from lmsapp.models import Book, Fine, IssuedBook, Student

from .forms import AdminSignupForm, BookForm, IssueBookForm


def admin_signup(request):
    if request.method == 'POST':
       # breakpoint()
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('admin_login')
    else:
        form = AdminSignupForm()
    return render(request, 'lmsadmin/signup.html', {'form': form})

def admin_login(request):
    return render(request, 'lmsadmin/login.html')


@login_required(login_url='admin_login')
def home(request):
    return render(request, 'lmsadmin/home.html', {'user': request.user})


def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        # breakpoint()
        #user1 = user.is_superuser
        if user and user.is_superuser:
            user_login(request, user)
            return redirect('home')         
        elif not user:
            messages.info(request, 'Try again! username or password is incorrect')
    return render(request, 'lmsadmin/login.html')


def logout_page(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='admin_login')
def student_profile(request):   
    page_no = 10
    student= Student.objects.values( 
            'roll_no', 
            'user_id__username', 
            'user_id__first_name', 
            'user_id__last_name', 
            'user_id__email', 
            'mobile_number', 
            'course_id__name',
            'user_id__id'
            )
    paginator = Paginator(student, page_no)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if 'search' in request.GET:
        search_term = request.GET['search']
        student = Student.objects.filter(
                  Q(user_id__first_name__icontains=search_term)| 
                  Q(course_id__name__icontains=search_term)|
                  Q(roll_no__icontains=search_term)
                  ).values(
                    'roll_no', 
                    'user_id__username', 
                    'user_id__first_name', 
                    'user_id__last_name', 
                    'user_id__email', 
                    'mobile_number', 
                    'course_id__name',
                    'user_id__id'
                    )
        paginator = Paginator(student, page_no)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'lmsadmin/studentprofile.html', {'page_obj':page_obj})
    return render(request, 'lmsadmin/studentprofile.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
def view_book(request): 
    page_no = 10 
    book= Book.objects.all()
    paginator = Paginator(book, page_no)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if 'search' in request.GET:
        search_term = request.GET['search']
        book = Book.objects.filter(
                  Q(author_id__name__icontains=search_term)| 
                  Q(name__icontains=search_term)|
                  Q(isbn_number__icontains=search_term)|
                  Q(category_id__category__icontains=search_term)|
                  Q(publication__icontains=search_term)
                  )
        paginator = Paginator(book, page_no)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'lmsadmin/viewbook.html', {'page_obj':page_obj})    
    return render(request, 'lmsadmin/viewbook.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
def view_issued_book(request):
    page_no = 10
    issuedbook= IssuedBook.objects.all().values(
            'issue_id', 
            'fine__fine_id', 
            'fine__fine_date', 
            'fine__fine_amount', 
            'issue_date', 
            'expiry_date', 
            'book_id__name', 
            'roll_no__course_id__name', 
            'roll_no__user_id__first_name'
            )
    paginator = Paginator(issuedbook, page_no)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if 'search' in request.GET:
        search_term = request.GET['search']
        issuedbook = IssuedBook.objects.filter(
                  Q(roll_no__user_id__first_name__icontains=search_term)| 
                  Q(roll_no__course_id__name__icontains=search_term)|
                  Q(book_id__name__icontains=search_term)
                  ).values(
                    'issue_id', 
                    'fine__fine_id', 
                    'fine__fine_date', 
                    'fine__fine_amount', 
                    'issue_date', 
                    'expiry_date', 
                    'book_id__name', 
                    'roll_no__course_id__name', 
                    'roll_no__user_id__first_name'
                    )
        paginator = Paginator(issuedbook, page_no)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'lmsadmin/viewissuedbook.html', {'page_obj':page_obj})
    return render(request, 'lmsadmin/viewissuedbook.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
def book_form(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'lmsadmin/home.html')
    else:
        form = BookForm()
    return render(request, 'lmsadmin/bookform.html', {'form': form})


def issue_book_form(request, id):
    book = Book.objects.get(pk=id)
    #fine = Fine.objects.get(pk=id)
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            form.save()        
            # issued_book = form.save(commit=False)
            # issued_book.issue_date = datetime.datetime.now()
            # issued_book.expiry_date = datetime.datetime.now() + datetime.timedelta(days=30) 
            # issued_book.save()
            book.quantity = book.quantity - 1
            book.save()   
            # fine.fine_date =  datetime.datetime.now() 
            # amount =  fine.fine_date - form.expiry_date
            # fine.fine_amount = amount.days*5
            # fine.save()

            return HttpResponse("Successfully Issued")
        
    else:
        form = IssueBookForm(initial={
                  'book_id':book.pk,
                #   'issue_date': datetime.datetime.now(),
                #   'expiry_date':datetime.datetime.now() + datetime.timedelta(days=30)
                  }
                  )
    return render(request, 'lmsadmin/issuebookform.html', {'form': form})


def book_history(request, id):
    issued_book = IssuedBook.objects.filter(book_id=id).values(
        'roll_no__user_id__first_name', 
        'roll_no__roll_no', 
        'fine__fine_amount', 
        'fine__fine_date', 
        'book_id', 
        'roll_no__course_id__name', 
        'issue_date', 
        'expiry_date'
        )
    # book =  Book.objects.filter(pk=id).values('issuedbook__roll_no')
    return render(request, 'lmsadmin/bookhistory.html', {'issued_book':issued_book})

# def book_search(request):
#     if 'search' in request.GET:
#         search_term = request.GET['search']
#         book = Book.objects.filter(Q(author_id__name__icontains=search_term) | Q(name__icontains=search_term)) 
#         # book = Book.objects.filter(author_id__name__icontains=search_term) 
#         # book = book.filter(name__icontains=search_term)

#     return render(request, 'lmsadmin/viewbook.html', {'page_obj':book})    

# def book_delete(request, id):
#     book = Book.objects.get(pk=id)
#     book.delete()
#     return HttpResponse("Successfully Deleted")

class DeleteBook(DeleteView):

    model = Book
    success_url = '/lmsadmin/home'
    template_name = "lmsadmin/Book_confirm_delete.html"



def book_update(request, id):
    book = Book.objects.get(pk=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponse("successfully update")
    else:
        form = BookForm(instance=book)
    return render(request, 'lmsadmin/bookform.html', {'form': form})


def student_profile_edit(request, id):  
    student = Student.objects.get(pk=id)
    user = student.user_id
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponse('<h1>Successfully Update</h1>')

    else:
        form = ProfileUpdateForm(instance=user, initial={
                  'mobile_number' : student.mobile_number,
                  'course_id' : student.course_id             
                  }
                  ) 
    return render(request, "account/studprofileupdate.html", {'form':form})


# def delete_profile(request, id):
#     student = Student.objects.get(pk=id)
#     student.user_id.delete()
#     return HttpResponse("Successfully Deleted")
 

class DeleteProfile(DeleteView):

    model = User
    success_url = '/lmsadmin/home'
    template_name = "lmsadmin/student_confirm_delete.html"

    