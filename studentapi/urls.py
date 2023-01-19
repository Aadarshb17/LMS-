from django.urls import path, include
from .import views

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView

router = DefaultRouter()
# router.register('userapi', views.UserViewSet, basename = 'user')
# router.register('registerapi', views.UserRegister, basename = 'student')
router.register('studentapi', views.UserModelViewSet, basename='user')
router.register('issuedbookapi', views.IssuedBookModelViewSet, basename='issuedbook')

urlpatterns = [
    path('', include(router.urls)),
  # path('auth', include('rest_framework.urls', namespace = 'rest_framework')),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tokenrefresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('tokenverify', TokenVerifyView.as_view(), name='token_verify'),
    path('logouttoken', TokenBlacklistView.as_view(), name='token_blacklist'),
]
   