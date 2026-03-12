from django.shortcuts import render
from . models import *
from . serializers import *
from rest_framework import viewsets
from .permissions import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.db.models import Sum
from decimal import Decimal
# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset=CustomerProfile.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomerProfilePermission]

    # Disable list view
    def list(self, request, *args, **kwargs):
        return Response(
            {"error": "List view is not allowed"},
            status=status.HTTP_403_FORBIDDEN
        )

    # Only allow the user to access their own objects
    def get_queryset(self):
        return CustomerProfile.objects.filter(user=self.request.user)
    # Automatically set user when creating
    def perform_create(self, serializer):
        user=self.request.user
        if CustomerProfile.objects.filter(user=user).exists:
            raise ValidationError("You already have a profile.")
        serializer.save(user=self.request.user)

#  @action is a decorator used inside a ViewSet to create custom API endpoints that are not part of the standard CRUD operations. 
    @action(detail=False, methods=['patch'], url_path='location')
    def update_location(self, request):
        profile=CustomerProfile.objects.filter(user=request.user).first()
        if not profile:
            return Response(    
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        profile.latitude=request.data.get('latitude')
        profile.longitude=request.data.get('longitude')
        profile.save()
        return Response({
            "message": "Location updated successfully",
            "latitude": profile.latitude,
            "longitude": profile.longitude
        })
    


class ProviderViewSet(viewsets.ModelViewSet):
    queryset=ProviderProfile.objects.all()
    serializer_class=ProviderSerializer
    permission_classes = [ProviderProfilePermission]
# No one can see list everyone just can see and CRUD their own profile ....
    def list(self, request, *args, **kwargs):
        return Response(
            {"error": "List view is not allowed"},
            status=status.HTTP_403_FORBIDDEN
        )
# no need to add user id when profile added automatically djnago assign provider his user id     
    def perform_create(self, serializer):
        user = self.request.user

        if ProviderProfile.objects.filter(user=user).exists():
            raise ValidationError("You already have a profile.")

        serializer.save(user=user) 
    @action(detail=False ,methods=['PATCH']  , url_path='location')
    def Update_location(self , request):
        profile=ProviderProfile.objects.filter(user=request.user).first()
        if not profile:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND                
            )
        profile.latitude=request.data.get('latitude')
        profile.longitude=request.data.get('longitude')
        profile.save()
        return Response({
            "message": "Location updated successfully",
            "latitude": profile.latitude,
            "longitude": profile.longitude
        })        

# action for the services and kept in mind one provider profile have many to many relation with services so we cam get multiple servicess to update action will use here is well
    @action(detail=False, methods=['patch'], url_path='services')
    def update_profile_services(self , request):
        profile=ProviderProfile.objects.filter(user=request.user).first()
        if not profile:
            return Response(    
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )   
        pro_ser=request.data.get('service',[]) 
        profile.service.set(pro_ser)
        # profile.save()
        return Response({
            "message": "Services updated successfully",
        })  
    # toglle availibality means ka change avaible or not available 
    @action(detail=False , methods=['PATCH'] , url_path='toggle_availability')
    def toggle_availability(self , request):
        user=self.request.user
        profile=ProviderProfile.objects.filter(user=request.user).first()
        if not profile:
            return Response(    
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            ) 
        profile.is_available=not profile.is_available
        profile.save()
        return Response({
            "message":"Your availibility have been toggeled successfully...",
            "is_available": profile.is_available
        }
        )            

   #  action to show active jobs of an entity      
    @action(detail=False, methods=['GET'], url_path='active_jobs')
    def active_jobs(self, request):
        profile = ProviderProfile.objects.filter(user=request.user).first()
        if not profile:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        jobs = profile.jobs.filter( status__in=['accepted', 'in_progress'],is_deleted=False )
        serializer = JobSerializer(jobs, many=True)
        return Response({
            "total_active_jobs": jobs.count(),
            "jobs": serializer.data
        })

    # action shows history of completed and canceled jobs of an entity
    @action(detail=False, methods=['GET'], url_path='job_history')
    def jobhistory(self , request):
        profile = ProviderProfile.objects.filter(user=request.user).first()
        if not profile:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        job=profile.jobs.filter(status__in=['completed', 'canceled'],is_deleted=False)  
        serializer=JobSerializer(job, many=True, context={'request': request})
        return Response({
            "total_jobs": job.count(),
            "jobs":serializer.data
            })      
    # action shows total pending jobs of an entity
    @action(detail=False, methods=['GET'], url_path='pending_jobs')
    def pending_jobs(self , request):
        user=request.user
        profile=ProviderProfile.objects.filter(user=user).first()
        if not profile:
            return Response(
                {"message":"Objects is not present ..."},
                 status=status.HTTP_404_NOT_FOUND
            )
        job=profile.jobs.filter(status='pending',is_deleted=False)
        serializer=JobSerializer(job, many=True, context={'request': request})
        return Response({
            "total_jobs": job.count(),
            "jobs":serializer.data            
        }
        )
    # action shows total earning of an entity
    @action(detail=False , methods=['GET'] , url_path='earning')
    def earning(self , request):
        user=request.user
        profile=ProviderProfile.objects.filter(user=user).first()
        if not profile:
            return Response(
                {"message" : "this profile is not present ..."},
                status=status.HTTP_404_NOT_FOUND
            )
        Total_jobs=profile.jobs.filter(status='completed',is_deleted=False)
        earning=Total_jobs.aggregate(sum=Sum('price'))['sum'] or Decimal('0.00')
        return Response({
        "total_jobs": Total_jobs.count(),
        "total_earning": earning
        })
    @action(detail=False , methods=['POST'] , url_path='verification')
    def verification_request(self , request):
        user=request.user
        profile=ProviderProfile.objects.filter(user=user).first()
        if not profile:
            return Response(
                {"message" : "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        cnic_image =request.data.get('cnic_image')
        cnic_number=request.data.get('cnic_number')
        if not cnic_image or not cnic_number:
            raise  ValidationError("Cnic Number and Cnic image is required ...")
        profile.cnic_image=cnic_image
        profile.cnic_number=cnic_number
        # profile.is_verified=True
        profile.save()
        return Response({
            "meassage" : "Profile verified successfully ..." ,
            "is_verified": profile.is_verified
        })
#    python manage.py runserver    