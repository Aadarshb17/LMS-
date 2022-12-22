from django.shortcuts import render
from rest_framework import viewsets
from . serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class UserModelViewSet(viewsets.ModelViewSet):
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


class IssuedBookModelViewSet(viewsets.ModelViewSet):
    serializer_class = IssuedBookSerializer

    def get_queryset(self):
        return IssuedBook.objects.filter(roll_no__user_id=self.request.user)

    def get_permissions(self):
            
        if self.action in ['list']:
            self.permission_classes = [IsAuthenticated]

        return super(self.__class__, self).get_permissions() 