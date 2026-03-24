from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path , include
from . import views
router=DefaultRouter()
router.register('payments', views.PaymentViewSet, basename='payments')
router.register('wallet', views.WallteandTransactionModelViewset, basename='wallet')

urlpatterns = [
    path('' , include(router.urls) )
]


#    python manage.py runserver