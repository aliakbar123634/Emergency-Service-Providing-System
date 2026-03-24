from django.shortcuts import render
from . models import *
from . serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .permissions import AdminAllowOnly
from provider.models import ProviderProfile
# # from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.

class ServiceCategoryView(APIView):
    permission_classes=[AdminAllowOnly]
    def get(self , request):
        if request.user.role=="admin":
            category=ServiceCategory.objects.all()
        else:    
            category=ServiceCategory.objects.filter(is_active=True)
        ser=ServiceCategorySerializer(category, many=True)
        return Response(ser.data , status=status.HTTP_200_OK)
    def post(self, request):
        ser=ServiceCategorySerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data , status=status.HTTP_201_CREATED)
        return Response(ser.errors , status=status.HTTP_400_BAD_REQUEST)


class SingleServiceCategoryView(APIView):
    permission_classes=[AdminAllowOnly]
    def get(self , request , id):
        try:
            singleservice=ServiceCategory.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        ser=ServiceCategorySerializer(singleservice)                
        return Response(ser.data, status=status.HTTP_200_OK)
    
    def patch(self , request , id):
        try:
            singleservice=ServiceCategory.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        ser=ServiceCategorySerializer(instance=singleservice , data=request.data , partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data , status=status.HTTP_202_ACCEPTED)  
        return Response(ser.errors , status=status.HTTP_400_BAD_REQUEST) 
      
    def delete(self , request , id):
        try:
            singleservice=ServiceCategory.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
        )  
        singleservice.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)



class Activate_Service(APIView):
    permission_classes=[AdminAllowOnly]
    def patch(self , request , id):    
        try:
            singleservice=ServiceCategory.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
        ) 
        singleservice.is_active=True
        singleservice.save()
        return Response("Activated successfully .....")
class Deactivate_Service(APIView):
    permission_classes=[AdminAllowOnly]
    def patch(self , request , id):    
        try:
            singleservice=ServiceCategory.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
        ) 
        singleservice.is_active=False
        singleservice.save()
        return Response("Deactivated successfully .....")        

class Deactivate_Service(APIView):
    permission_classes=[AdminAllowOnly]
    def get(self , request , id):
        try:
            singleservice=ServiceCategory.objects.get(id=id)
        except ServiceCategory.DoesNotExist:
            return Response({
                "message":"No query related to this id ..."
            },
                status=status.HTTP_400_BAD_REQUEST
        ) 
        providersOfTheService=singleservice.ProviderProfile.all()
        data=[]
        total_providers=0
        for i in providersOfTheService:
            total_providers+=1
            data.append({
                "id":i.id,
                "experience_years":i.experience_years,
                "average_rating":i.average_rating,
                "city":i.city
            })
        return Response({
            "Total providers":total_providers,
            "All Providers Data":data
        } , status=status.HTTP_200_OK)    








    #   python manage.py runserver    