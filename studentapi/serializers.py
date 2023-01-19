from rest_framework import serializers
from lmsapp.models import *
from django.contrib.auth.models import User


class FineBookSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Fine
        fields = [        
            'fine_date',
            'fine_amount',
            ] 

        
class IssuedBookSerializer(serializers.ModelSerializer): 
    fine_set =  FineBookSerializer(many=True, read_only= True)
    class Meta:
        model = IssuedBook
        fields = [        
            'book_id',
            'issue_date',
            'expiry_date',
            'fine_set',
            ] 

class UserSerializer(serializers.ModelSerializer):
    
    class StudentSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Student
            fields = [
                'course_id',
                'mobile_number',
                ]

    student = StudentSerializer(read_only=False)   
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

        # def create(self, validated_data):
        #     mobile = validated_data.get('mobile')
        #     course = validated_data.get('course')
        #     user = User.objects.create(**validated_data)
        #     Student.objects.create(user_id=user, mobile_number=mobile, course_id=course)
        #     return user

    def create(self, validated_data):
        # breakpoint()
        student_data = validated_data.pop('student')
        password = validated_data.pop('password')  
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Student.objects.create(user_id=user, **student_data)
        return user
        
    def update(self, instance, validated_data):
        students_data = validated_data.pop('student')        
        instance = super(UserSerializer, self).update(instance, validated_data)
        student = instance.student
        student.course_id = students_data.get('course_id')
        student.mobile_number = students_data.get('mobile_number')
        student.save()
        return instance


 