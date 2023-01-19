from django.contrib.auth.models import User
from rest_framework import serializers

from lmsadmin.models import *
from lmsapp.models import *

# class AdminSerializer(serializers.ModelSerializer):
     
#     class Meta:
#         model = Admin
#         fields = [ 
#             'mobile', 
#             ] 
#     admin = AdminSerializer(read_only=False)  


class AdminUserSerializer(serializers.ModelSerializer):

    class StudentAdminSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Student
            fields = [
                'course_id',
                'mobile_number',
                ]

    student = StudentAdminSerializer(read_only=False)   
    
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'first_name', 
            'last_name',
            'password',
            'student',
        ]        
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        admin_data = validated_data.pop('student')
        password = validated_data.pop('password')  
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Student.objects.create(user_id=user, **admin_data)
        return user
        
    def update(self, instance, validated_data):
        students_data = validated_data.pop('student')        
        instance = super(AdminUserSerializer, self).update(instance, validated_data)
        student = instance.student
        student.course_id = students_data.get('course_id')
        student.mobile_number = students_data.get('mobile_number')
        student.save()
        return instance


class FineBookAdminSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Fine
        fields = [        
            'fine_date',
            'fine_amount',
            ] 

        
class IssueBookAdminSerializer(serializers.ModelSerializer): 
    fine_set =  FineBookAdminSerializer(many=True, read_only= True)
    class Meta:
        model = IssuedBook
        fields = [ 
            'issue_id',       
            'book_id',
            'roll_no',
            'issue_date',
            'expiry_date',
            'fine_set',
            ] 
        extra_kwargs = {
            'issue_date': {"required": False, "allow_null": True},
            'expiry_date': {"required": False, "allow_null": True},
            'fine_set': {"required": False, "allow_null": True},        
        }

class BookAdminSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Book
        fields = [ 
            'author_id',
            'category_id',
            'name',
            'isbn_number',
            'publication',
            'price',
            'quantity',
            ] 
    

    # def create(self, validated_data):
    #     admin_data = validated_data.pop('student')
    #     password = validated_data.pop('password')  
    #     user = User.objects.create(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     Admin.objects.create(user_id=user, **admin_data)
    #     return user
        
    # def update(self, instance, validated_data):
    #     admin_data = validated_data.pop('student')        
    #     instance = super(AdminSerializer, self).update(instance, validated_data)
    #     admin = instance.admin
    #     admin.mobile = admin_data.get('mobile')
    #     admin.save()
    #     return instance


# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         return token