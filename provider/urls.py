from django.contrib import admin
from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('customer/profile' , views.CustomerViewSet)
router.register('provider/profile' , views.ProviderViewSet),
router.register('admin-providers', views.AdminEndpoints, basename='adminproviders')
urlpatterns = [
    path('' , include(router.urls) )
]
