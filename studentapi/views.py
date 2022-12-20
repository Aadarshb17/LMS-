from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from . serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class UserModelViewSet(viewsets.ModelViewSet):
    #queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    def get_permissions(self):
        # breakpoint()
        if self.action in ['update','partial_update','destroy','list']:
            self.permission_classes = [IsAuthenticated]
            
        elif self.action in ['create']:
            self.permission_classes = [AllowAny]

        return super(self.__class__, self).get_permissions()

    # def create(self):
    #     serializer = UserSerializer(request.data)
    #     if serializer.is_valid():
    #         perform_create(serializer)
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

class StudentModelViewSet(viewsets.ModelViewSet):
    #queryset = Student.objects.all()

    def get_queryset(self):
        return Student.objects.filter(user_id=self.request.user)
    serializer_class = StudentSerializer

    def get_permissions(self):
    
        if self.action in ['update','partial_update','destroy','create']:
            self.permission_classes = [IsAdminUser]
            
        elif self.action in ['list']:
            self.permission_classes = [IsAuthenticated]

        return super(self.__class__, self).get_permissions() 