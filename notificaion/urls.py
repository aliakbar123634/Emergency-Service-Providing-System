from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path , include
from . import views
router=DefaultRouter()
router.register('notification', views.NotifilationViewSet, basename='notification')


urlpatterns = [
    path('' , include(router.urls) )
]