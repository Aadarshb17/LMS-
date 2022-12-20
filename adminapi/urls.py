from django.urls import path, include
from .import views

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

router = DefaultRouter()

router.register('adminapi', views.AdminModelViewSet, basename = 'admin')

urlpatterns = [

    path('', include(router.urls)),
    path('auth', include('rest_framework.urls', namespace = 'rest_framework')),
    path('admin/gettoken', views.AdminTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tokenrefresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', TokenBlacklistView.as_view(), name='token_blacklist'),
   
]
   