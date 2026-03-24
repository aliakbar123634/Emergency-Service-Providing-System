
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceRequestViewSet


router = DefaultRouter()

router.register("requests", ServiceRequestViewSet, basename="requests")

urlpatterns = [
    path('', include(router.urls)),
]

# python manage.py runserver 