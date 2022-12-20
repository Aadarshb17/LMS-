from django.db import models
from django.contrib.auth.models import User 
import datetime
 

# Create your models here.
class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    isbn_number = models.IntegerField(blank=False, unique=True)
    publication = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Student(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    mobile_number = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return f'Roll No-{self.roll_no} User- {self.user_id.pk}'

class IssuedBook(models.Model):
    issue_id = models.AutoField(primary_key=True)
    roll_no = models.ForeignKey(Student, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=datetime.datetime.now())
    expiry_date = models.DateField(default=datetime.datetime.now()+datetime.timedelta(days=30))

    def __str__(self):
        return f'{self.roll_no}------{self.book_id}'

    # def save(self):
    #     issued_book.expiry_date = 
    #     issued_book.issue_date = 
    #     issued_book.save()

    
class Fine(models.Model):
    fine_id = models.AutoField(primary_key=True)
    issue_id = models.ForeignKey(IssuedBook, on_delete=models.CASCADE )
    fine_date = models.DateField()
    fine_amount = models.IntegerField()

    def __str__(self):
        return f'{self.fine_id}------{self.issue_id}'
    
