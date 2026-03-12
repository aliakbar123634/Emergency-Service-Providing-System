from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from . import views
router=DefaultRouter()
router.register('registration' , views.RegiatrationViewset)

urlpatterns = [
    path('' , include(router.urls)) , 
    path('login/' , views.loginview , name='login'),
    path('logout/' , views.LogOutView , name='logout'),
    path('user/<uuid:id>' , views.PersonalViewclass.as_view() , name='user'),
    path('wallet/' , views.WalletView.as_view() , name='wallet')
]
