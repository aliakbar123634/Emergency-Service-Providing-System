from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    # admin can see all the services and normal user can see only active services 
    path('service/' , views.ServiceCategoryView.as_view() , name="service"),
    # only admin can post patch or delete a single service normal user can see single service
    path('service/<int:id>' , views.SingleServiceCategoryView.as_view() , name="service"),
    # only admin can activate or deactivate a service
    path('service/<int:id>/activate/' , views.Activate_Service.as_view(), name="service"),
    path('service/<int:id>/deactivate/' , views.Deactivate_Service.as_view(), name="deactivate"),
]
