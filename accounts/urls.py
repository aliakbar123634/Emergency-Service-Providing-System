from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from . import views
# from .views import test_email
from .views import SendVerificationEmail , VerifyEmail , ForgotPasswordView , ResetPasswordView , ChangePasswordView
router=DefaultRouter()
router.register('registration' , views.RegiatrationViewset)
router.register('admin-user' , views.AdminViewSet , basename='admin/users')

urlpatterns = [
    path('' , include(router.urls)) , 
    path('login/' , views.loginview , name='login'),
    path('logout/' , views.LogOutView , name='logout'),
    path('user/<uuid:id>' , views.PersonalViewclass.as_view() , name='user'),
    path('wallet/' , views.WalletView.as_view() , name='wallet'), 
    path('send-verification-email/', SendVerificationEmail.as_view()),
    path('verify-email/', VerifyEmail.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
]     
   #    python manage.py runserver
