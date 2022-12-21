from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from . serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

class AdminModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer

    def get_permissions(self):
        if self.action in ['update','partial_update','destroy','list']:
            self.permission_classes = [IsAdminUser]
            
        elif self.action in ['create']:
            self.permission_classes = [AllowAny]

        return super(self.__class__, self).get_permissions()



from rest_framework_simplejwt.views import TokenObtainPairView



class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer