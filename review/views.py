from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . models import Review
from . serializers import ReviewSerializer
from rest_framework.decorators import action
from django.db import transaction
from provider.models import CustomerProfile , ProviderProfile
from rest_framework.response import Response
from rest_framework import status
from request.models import ServiceRequest
from . permissions import IsCustomerOnly , OnlyCustomerAndOwnAccess , OnlyProviderAndOwnAccess , OnlyCustomerOwnAccessAndOwner
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.


class ReviewViewSet(ModelViewSet):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["provider","rating"]
    ordering_fields = ["created_at","rating"]    
    # permission_classes = [IsAuthenticated, IsCustomerOnly]
    def get_permissions(self):
        if self.action=="retrieve":
            return [IsCustomerOnly()]
        elif self.action == "update" or self.action == "partial_update":
            return [OnlyCustomerOwnAccessAndOwner()]

        elif self.action == "destroy":
            return [OnlyCustomerOwnAccessAndOwner()]
        return super().get_permissions()    
    @action(detail=False, methods=['POST'], url_path="create" , permission_classes = [IsCustomerOnly])
    def CreateReview(self, request):
        user = request.user

        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service_request = serializer.validated_data['service_request']
        rating = serializer.validated_data['rating']
        comment = serializer.validated_data['comment']
        if service_request.customer != user:
            return Response({
            "message": "You can only review your own service request"
        }, status=status.HTTP_403_FORBIDDEN)
        provider = service_request.provider
        if not provider:
            return Response({
            "message": "Provider not assigned yet"
        }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            review = Review.objects.create(
                service_request=service_request,
                Customer=user,
                provider=provider,
                rating=rating,
                comment=comment
        )
        return Response({
        "id": review.id,
        "rating": rating,
        "comment": comment
    })

    @action(detail=True, methods=['GET'], url_path="provider" , permission_classes = [IsCustomerOnly])
    def getReviwofid(self, request , pk=None):
        try:
            provider_related_to_id=ProviderProfile.objects.get(id=pk)
        except ProviderProfile.DoesNotExist:
            return Response({
                "message":"Provider does not exist to given query ...."
            } , status=status.HTTP_400_BAD_REQUEST)  
        # rewiew_related_to_provider=provider_related_to_id.Review.all()  
        rewiew_related_to_provider=Review.objects.filter(provider=provider_related_to_id)
        data=[]
        for i in rewiew_related_to_provider:
            data.append({
                "id":i.id,
                "rating":i.rating,
                "comment":i.comment
            })
            
        return Response({
            "All reviews of this provider":data
        } , status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path="my" , permission_classes = [OnlyCustomerAndOwnAccess] )
    def myallReviewsForCustomer(self, request ):
        user=request.user
        try:
            customer_profile = CustomerProfile.objects.get(user=user)
        except CustomerProfile.DoesNotExist:
            return Response({
        "message": "Provider profile not found"
        }, status=status.HTTP_404_NOT_FOUND)                  
        try:
            # review_related_to_user=Review.objects.filter(Customer=user)
            review_related_to_user=Review.objects.filter(Customer=customer_profile)
        except:
            return Response({
                "message":"User not found ...."
            }, status=status.HTTP_400_BAD_REQUEST) 
        data=[]
        for i in review_related_to_user:
            data.append({
                "id": i.id,
                "rating": i.rating
        })  
        return Response({
            "Your all reviews":data
        }, status=status.HTTP_200_OK)     

    @action(detail=False, methods=['GET'], url_path="provider/my" , permission_classes = [OnlyProviderAndOwnAccess] )
    def myallReviewsForProvider(self, request ): 
        user=request.user
        try:
            provider_profile = ProviderProfile.objects.get(user=user)
        except ProviderProfile.DoesNotExist:
            return Response({
        "message": "Provider profile not found"
        }, status=status.HTTP_404_NOT_FOUND)        
        try:
            review_related_to_user=Review.objects.filter(provider=provider_profile)
        except:    
            return Response({
                "message":"User not found ...."
            }, status=status.HTTP_400_BAD_REQUEST) 
        data=[]
        for i in review_related_to_user:
            data.append({
                "id": i.id,
                "rating": i.rating
        })  
        return Response({
            "Your all reviews":data
        }, status=status.HTTP_200_OK)  
    # @action(detail=True, methods=['PUT'], url_path="update")
    # def myallReviews(self, request pk=id):

 
    # python manage.py runserver