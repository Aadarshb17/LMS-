import datetime

import razorpay
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (DeleteView, DetailView, RedirectView,
                                  TemplateView, View)

from LMS.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY

from .forms import ProfileUpdateForm, StudentForm
from .models import Fine, IssuedBook, Student


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


# def home(request):
#     return render(request, 'home.html')

class Home(TemplateView):
    template_name = 'home.html'


# def user_login(request):
#     # import pdb;pdb.set_trace()
#     return render(request, 'login.html')


class UserLogin(TemplateView):
    template_name = 'login.html'


# def user_logout(request):
#     return redirect('accounts/login')


class UserLogout(RedirectView):
    url = 'accounts/login'


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
    student = Student.objects.get(user_id=user)
    issued_books = IssuedBook.objects.filter(roll_no__user_id=user)
    issued_book_data= issued_books.values(
        'issue_id', 
        'fine__fine_id', 
        'fine__fine_date', 
        'fine__fine_amount', 
        'issue_date', 
        'expiry_date', 
        'book_id__name',
        )
    # breakpoint()
    if issued_books.filter(fine__fine_amount__isnull=False):  
        #breakpoint()
        fine_amount = issued_books.filter(fine__fine_amount__isnull=False).aggregate(amount=Sum(
            'fine__fine_amount'
            ) * 100
            )
        #breakpoint()
        book_fine_amount = fine_amount.get('amount')                                                                                                            ,                             
        #  comment
        payment_order_id = razorpay_payment(book_fine_amount)

        #fine_data = issued_books.values('fine__fine_id')

        context = {
            'mobile':student.mobile_number,
            # 'fine_id' : fine_data[0]['fine__fine_id'],
            'amount': book_fine_amount,
            'api_key': RAZORPAY_API_KEY,
            'order_id': payment_order_id
        }       
    
        return render(request, 'issuedbook.html', {'issued_book_data':issued_book_data, 'context':context})
    return render(request, 'issuedbook.html', {'issued_book_data':issued_book_data})


def razorpay_payment(book_fine_amount):
    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
    currency = 'INR'
    payment_order = client.order.create(
                dict(
                    amount=book_fine_amount[0],
                    currency=currency,
                    payment_capture=1
                    )
                )
    payment_order_id = payment_order['id']
    return payment_order_id


# def fine(request):
#     user = request.user
#     fine= Fine.objects.filter(issue_id__roll_no__user_id=user)
#     return render(request, 'fine.html', {'fine':fine})


# def profile_edit(request):
#     user = request.user
#     student = Student.objects.get(user_id=user)
#     if request.method == 'POST':
#         form = ProfileUpdateForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponse('<h1>Successfully Update</h1>')
#     else:
#         form = ProfileUpdateForm(initial={
#                   'username': user.username,
#                   'first_name' : user.first_name,
#                   'last_name' : user.last_name,
#                   'email' : user.email,
#                   'mobile_number' : student.mobile_number,
#                   'course_id' : student.course_id             
#                   }
#                   ) 
#     return render(request, "account/studprofileupdate.html", {'form':form})


class ProfileEdit(View):

    template_name = "account/studprofileupdate.html"

    def post(self, request):
        form = ProfileUpdateForm(request.POST, instance=self.request.user)
        if form.is_valid():
            form.save()
            return HttpResponse('<h1>Successfully Update</h1>')

    def get(self, request):
        user = request.user
        student = Student.objects.get(user_id=self.request.user)
        form = ProfileUpdateForm(instance=user, initial={
                  'mobile_number' : student.mobile_number,
                  'course_id' : student.course_id             
                  }
                  ) 
        return render(request, self.template_name, {'form':form})


# def delete_profile(request, id):
#     student = Student.objects.get(pk=id)
#     student.user_id.delete()
#     return HttpResponse("Successfully Deleted")
 


@csrf_exempt
def handler(request):
    # breakpoint()
    if request.POST.get('error[code]') is not None:
        return HttpResponse("payment failed")
    payment_id = request.POST.get("razorpay_payment_id", "")
    order_id = request.POST.get("razorpay_order_id", "")
    signature = request.POST.get("razorpay_signature", "")
    print(payment_id, order_id, signature)
    # fine = Fine.objects.get(pk=id)
    # fine.delete()
    return HttpResponse('<h1>Payment Successfull</h1>')