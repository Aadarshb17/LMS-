from django.urls import path
from .import views



urlpatterns = [
   path('adminsignup', views.admin_signup, name='admin_signup'),
   path('adminlogin', views.admin_login, name='admin_login'),
   path('home', views.home, name='home'),
   path('loginpage', views.login_page, name='login_page'),
   path('logoutpage', views.logout_page, name='logout_page'),
   path('studentprofile', views.student_profile, name='student_profile'),
   path('viewbook', views.view_book, name='view_book'),
   path('viewissuedbook', views.view_issued_book, name='view_issued_book'),
   path('bookform', views.book_form, name='book_form'),
   path('issuebookform/<int:id>/', views.issue_book_form, name='issue_book_form'),
   path('bookhistory/<int:id>/', views.book_history, name='book_history'),
   path('bookdelete/<int:id>/', views.book_delete, name='book_delete'),
   path('bookupdate/<int:id>/', views.book_update, name='book_update'),
   path('editstudentprofile/<int:id>/', views.student_profile_edit, name='student_profile_edit'),
   
   #path('booksearch', views.book_search, name='book_search'),
   # path('adminlogin', views.admin_login, name='admin_login'),
]
   