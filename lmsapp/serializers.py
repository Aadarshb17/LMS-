# from rest_framework import serializers
# from .models import *
# from django.contrib.auth.models import User



    




# class StudentSerializer(serializers.ModelSerializer): 
#     # username =  serializers.CharField(max_length=30, required=True)
#     # first_name = serializers.CharField(label='first name', max_length=100)
#     # last_name = serializers.CharField(label='last name', max_length=100)
#     # email = serializers.EmailField()
#     class Meta:
#         model = Student
#         fields = [
#             'user_id',
#             'roll_no', 
#             'course_id',
#             'mobile_number',
       
#             ] 

# class UserSerializer(serializers.ModelSerializer):
#     student = StudentSerializer()
#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'first_name', 
#             'last_name',
#             'email',
#             'student'          
#             ] 
    
#     def create(self, validated_data):
#         student_data = validated_data.pop('student')
#         user = User.objects.create(**validated_data)
#         Student.objects.create(user_id=user, **student_data)
#         return user

# class IssuedbookSerializer(serializers.ModelSerializer): 
#     class Meta:
#         model = IssuedBook
#         fields = [
#             'issue_id',
#             'roll_no', 
#             'book_id',
#             'issue_date',
#             'expiry_date'
           
#             ] 

    