"""LMS URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# router = DefaultRouter()

# router.register('studentapi', views.StudentModelViewSet, basename = 'student')
# router.register('user', views.UserModelViewSet, basename = 'user')
# router.register('issuedbook', views.IssuedBookModelViewSet, basename = 'issuedbook')


#router.register('studentapi', views.StudentReadOnlyModelViewSet, basename = 'student')

urlpatterns = [
    path('index', views.index, name='index'),
    path('currentdatetime', views.currentdatetime, name='currentdatetime'),
    path('student_detail', views.student_detail, name='student_detail'),
    #path('registration', views.registration, name='registration'),
    path('home', views.Home.as_view(), name='Home'),
    #path('signin', views.signin, name='signin'), 
    path('login', views.UserLogin.as_view(), name='UserLogin'), 
    path('', views.UserLogout.as_view(), name='UserLogout'), 
    path('profile', views.Profile.as_view(), name='profile'), 
    path('issuedbook', views.issued_book, name='issued_book'), 
    #path('editprofile', views.profile_edit, name='profile_edit'),
    path('editprofile', views.ProfileEdit.as_view(), name='profile_edit'), 
    

    #path('payfine', views.fine_pay, name='fine_pay'),
    path('handler/', views.handler, name='handler'),
    path('razorpaypayment', views.razorpay_payment, name='razorpay_payment'),
    #path('fine', views.fine, name='fine'),

    # path('', include(router.urls)),
    # path('auth', include('rest_framework.urls', namespace = 'rest_framework')),
    # path('gettoken', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('tokenrefresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('tokenverify', TokenVerifyView.as_view(), name='token_verify'),  
] 