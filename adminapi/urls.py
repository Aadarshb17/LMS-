from django.urls import path, include
from .import views

from rest_framework.routers import DefaultRouter
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

router = DefaultRouter()

router.register('adminapi', views.AdminModelViewSet, basename = 'admin')
router.register('issuebookadminapi', views.IssuedBookAdminModelViewSet, basename = 'admin')

urlpatterns = [

    path('', include(router.urls)),
    path('auth', include('rest_framework.urls', namespace = 'rest_framework')),
   
]
   