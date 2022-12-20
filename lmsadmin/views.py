import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AdminSignupForm, BookForm, IssueBookForm
from lmsapp.forms import ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from lmsapp.models import Student, Book, IssuedBook, Fine
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('admin_login')
    else:
        form = AdminSignupForm()
    return render(request, 'lmsadmin/signup.html', {'form': form})

def admin_login(request):
    return render(request, 'lmsadmin/login.html')


# def home(request):
#     return render(request, 'lmsadmin/home.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        # breakpoint()
        #user1 = user.is_superuser
        if user and user.is_superuser:
            login(request, user)
            return render(request, 'lmsadmin/home.html', {'user':user})         
        elif not user:
            messages.info(request, 'Try again! username or password is incorrect')
    return render(request, 'lmsadmin/login.html')


def logout_page(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='admin_login')
def student_profile(request):   
    student= Student.objects.values( 
            'roll_no', 
            'user_id__username', 
            'user_id__first_name', 
            'user_id__last_name', 
            'user_id__email', 
            'mobile_number', 
            'course_id__name'
            )
    paginator = Paginator(student, 10)
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
                    'course_id__name'
                    )
        paginator = Paginator(student, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'lmsadmin/studentprofile.html', {'page_obj':page_obj})
    return render(request, 'lmsadmin/studentprofile.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
def view_book(request):  
    book= Book.objects.all()
    paginator = Paginator(book, 10)
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
        paginator = Paginator(book, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'lmsadmin/viewbook.html', {'page_obj':page_obj})    
    return render(request, 'lmsadmin/viewbook.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
def view_issued_book(request):
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
    paginator = Paginator(issuedbook, 10)
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
        paginator = Paginator(issuedbook, 10)
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

def book_delete(request, id):
    book = Book.objects.get(pk=id)
    book.delete()
    return HttpResponse("Successfully Deleted")


def book_update(request, id):
    book = Book.objects.get(pk=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponse("successfully update")
    else:
        form = BookForm(initial={
            'author_id':book.author_id,
            'category_id':book.category_id,
            'name':book.name,
            'isbn_number':book.isbn_number,
            'publication':book.publication,
            'price':book.price,
            'quantity':book.quantity
        }
        )
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

