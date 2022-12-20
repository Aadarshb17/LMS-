from rest_framework import serializers
from lmsadmin.models import *
from django.contrib.auth.models import User


class AdminSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Admin
        fields = [ 
            'mobile', 
            ] 


class AdminUserSerializer(serializers.ModelSerializer):

    admin = AdminSerializer(read_only=False)  
    
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'first_name', 
            'last_name',
            'password',
            'admin',
        ]        
        extra_kwargs = {'password': {'write_only': True}}

    

    def create(self, validated_data):
        admin_data = validated_data.pop('student')
        password = validated_data.pop('password')  
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Admin.objects.create(user_id=user, **admin_data)
        return user
        
    def update(self, instance, validated_data):
        admin_data = validated_data.pop('student')        
        instance = super(AdminSerializer, self).update(instance, validated_data)
        admin = instance.admin
        admin.mobile = admin_data.get('mobile')
        admin.save()
        return instance