from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse

from .models import *
from unittest.mock import patch
from lmsapp.views import razorpay_payment


# class SimpleTest(TestCase):
#     def setUp(self):   
#         self.username = 'aadarsh17'
#         self.password = 'Am170106'
#         self.user = get_user_model().objects.create_user(username=self.username, password=self.password)

#     def test_login(self):
#         self.client = Client()
#         self.client.login(
#             username='aadarsh17',
#             password='Am170106'
#             )
#         response = self.client.post('/accounts/login')
#         self.assertEqual(response.status_code, 200)


# class TestForm(TestCase):
#     def setUp(self):
#         self.credentials = {
#             'username': 'aadarshb06',
#             'password': 'Aj06081701'
#             }
#         User.objects.create(**self.credentials)

#     def test_login(self):
#         breakpoint()
#         self.client = Client()
#         response = self.client.post('/lmsadmin/loginpage/', self.credentials)
#         #breakpoint()
#         print(response.context['user'])
#         self.assertTrue(response.context['user'].is_active)

# login test

class SimpleLoginTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='aadarsh17', 
            email='aadarshb@gmail.com', 
            password='Am170106'
            )
        self.client = Client()


    def test_valid_login(self):
        self.client.login(username='aadarsh17', password='Am170106')
        response = self.client.post('/accounts/login', follow=True)
        user = User.objects.get(email='aadarshb@gmail.com')
        self.assertEqual(response.context['user'].email, user.email)

    def test_invalid_username(self):
        self.client.login(username='aadarshb17k', password='Am170106')
        response = self.client.post('/lmsadmin/loginpage')
        self.assertTrue(response.context['user'].is_anonymous)

    def test_invalid_password(self):    
        self.client.login(username='aadarsh17', password='Am1701055608')
        response = self.client.get('/lmsadmin/adminlogin')
        self.assertTrue(response.context['user'].is_anonymous)

    def test_blank_username(self):
        self.client.login(username='', password='')
        response =self.client.get('/lmsadmin/adminlogin')
        #breakpoint()
        self.assertTrue(response.context['user'].is_anonymous)

class SignUpPageTests(TestCase):
    def setUp(self):
        self.username = 'test12user'
        self.email = 'test12user@email.com'
        self.password = 'adgsaswefdhg143213'
        self.first_name = 'anuj'
        self.last_name = 'verma'
        self.mobile_number = '6545646488'
        # self.course_id = "B.tech(CS)"
        # user = User.objects.create_user(
        #     username= self.username, 
        #     email=self.email, 
        #     password=self.password, 
        #     first_name=self.first_name, 
        #     last_name=self.last_name,      
        #     )
        # breakpoint()
        self.course_id = Course.objects.create(name='btech').course_id

        # student = Student.objects.create(
        #     mobile_number=self.mobile_number,
        #     course_id=course,
        #     user_id=user
        #     )
  
    def test_signup_page_url(self):
        response = self.client.get('/accounts/signup', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_page_name(self):
        response = self.client.post(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='account/signup.html')

    def test_signup_form(self):  
        response = self.client.post(reverse('account_signup'), data={
            'username': self.username,
            'email': self.email,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'mobile_number':self.mobile_number,
            'course_id':self.course_id,
            'password1': self.password,
            'password2': self.password
           
        })
        self.assertEqual(response.status_code, 302)    
        user = get_user_model().objects.all() 
        student = Student.objects.all() 
        self.assertEqual(user.count(), 1)
        self.assertEqual(student.count(), 1)

    def test_signup_page_invalid_url(self):
        response = self.client.get('/accountdgf/signupwe', follow=True)
        self.assertEqual(response.status_code, 404)
        #self.assertTemplateUsed(response, template_name='accounts/signup.html')

    def test_signup_invalid_form(self):
        response = self.client.post(reverse('account_signup'), data={
            'username': 'username',
            'email': 'awxgsgr@gmail.com',
            'password1': 'self.password',
            'password2': 'self.password',
            'first_name': 'self.first_name',
            'last_name': 'self.last_name',
            'mobile_number': 'self.mobile_number',
           
        }
        )

        self.assertEqual(response.status_code, 302)    
        user = get_user_model().objects.all() 
        student = Student.objects.all() 
        self.assertEqual(user.count(), 1)
        self.assertEqual(student.count(), 1)

    def test_signup_page_invalid_url(self):
        response = self.client.get('/accountdgf/signupwe', follow=True)
        self.assertEqual(response.status_code, 404)
        #self.assertTemplateUsed(response, template_name='accounts/signup.html')

    def test_signup_invalid_form(self):
        response = self.client.post(reverse('account_signup'), data={
            'username': 'username',
            'email': 'awxgsgr@gmail.com',
            'password1': 'self.password',
            'password2': 'self.password',
            'first_name': 'self.first_name',
            'last_name': 'self.last_name',
            'mobile_number': '5775575737',
            
        }
        )
       
        self.assertEqual(response.status_code, 200)    
        user = get_user_model().objects.all() 
        self.assertEqual(user.count(), 0)


class UpdateProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='user@example.com', password='amj17010608')
        course = Course.objects.create(name='btech')
        Student.objects.create(user_id=self.user, course_id=course)
        self.client = Client()

    def test_update_profile(self):
        course = Course.objects.create(name='mtech').course_id
        self.client.login(username='testuser', password='amj17010608')     
        response = self.client.post(reverse('profile_edit'), data = {
            'username': 'username',
            'first_name': 'self.first_name',
            'last_name': 'self.last_name',
            'email': 'updated@example.com',
            'mobile_number': '7878654488',
            'course_id': course
            })
        #breakpoint()
        is_user = User.objects.filter(email='updated@example.com')
        self.assertTrue(is_user)
        self.assertEqual(response.content, b'<h1>Successfully Update</h1>')


from faker import Faker
from django.contrib.auth.hashers import make_password
import json
import factory
import random
import datetime

passw = Faker().password()
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
         
    username = factory.Faker('user_name') 
    email = factory.Faker('email')
    password = factory.LazyFunction(lambda: make_password(passw))


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course
    
    name = factory.Faker('name') 


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
    
    name = factory.Faker('name') 


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    
    category = factory.Faker('name')


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
    name = factory.Faker('name')
    price = factory.LazyAttribute(lambda x: random.randrange(0, 10000))
    quantity = factory.LazyAttribute(lambda x: random.randrange(0, 10000))
    author_id = factory.SubFactory(AuthorFactory)
    category_id = factory.SubFactory(CategoryFactory)
    isbn_number = factory.LazyAttribute(lambda x: random.randrange(0, 10000))


class IsssuedBookTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.course = CourseFactory()
        self.book = BookFactory()
        #breakpoint()
        student = Student.objects.create(user_id=self.user, course_id=self.course)
        self.issue_book = IssuedBook.objects.create(roll_no=student, book_id=self.book)
        fine = Fine.objects.create(issue_id= self.issue_book, fine_amount=100, fine_date=datetime.datetime.now())
        self.client = Client()
    
    @patch('lmsapp.views.razorpay_payment')
    def test_issued_book(self, mock_razorpay_payment):  
        self.client.login(username=self.user.username, password=passw)
        #breakpoint()    
        mock_razorpay_payment.return_value = 100
        response = self.client.get(reverse('issued_book'))

        self.assertEqual(response.status_code, 200)
        mock_razorpay_payment.assert_called_once()
        
        
 
# class TestRazorpayPayment(TestCase):
#     @patch("views.razorpay_payment")
#     def test_razorpay_pay(mock_razorpay_payment):
#         payment_order = client.order.create(
#                     dict(
#                         amount=50000,
#                         currency="INR",
#                         payment_capture=1
#                         )
#                     )
#         payment_order_id = payment_order['id']



