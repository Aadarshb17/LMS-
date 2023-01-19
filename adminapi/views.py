from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from lmsapp.models import *

from .serializers import *


class AdminModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer

    def get_permissions(self):
        if self.action in ['update','partial_update','destroy','list']:
            self.permission_classes = [IsAdminUser]
            
        elif self.action in ['create']:
            self.permission_classes = [AllowAny]

        return super(self.__class__, self).get_permissions()


class IssuedBookAdminModelViewSet(viewsets.ModelViewSet):
    queryset = IssuedBook.objects.all()
    serializer_class = IssueBookAdminSerializer
    permission_classes = [IsAdminUser]


class BookAdminModelViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookAdminSerializer
    permission_classes = [IsAdminUser]

# from rest_framework_simplejwt.views import TokenObtainPairView



# class AdminTokenObtainPairView(TokenObtainPairView):
#     serializer_class = AdminTokenObtainPairSerializer