from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from . import views
# from .views import test_email
from .views import SendVerificationEmail , VerifyEmail
router=DefaultRouter()
router.register('registration' , views.RegiatrationViewset)
router.register('admin-user' , views.AdminViewSet , basename='admin/users')

urlpatterns = [
    path('' , include(router.urls)) , 
    path('login/' , views.loginview , name='login'),
    path('logout/' , views.LogOutView , name='logout'),
    path('user/<uuid:id>' , views.PersonalViewclass.as_view() , name='user'),
    path('wallet/' , views.WalletView.as_view() , name='wallet'),
    # path('test-email/', test_email), 
    path('send-verification-email/', SendVerificationEmail.as_view()),
    path('verify-email/', VerifyEmail.as_view()),
    
]     
   #    python manage.py runserver
