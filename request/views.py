from rest_framework import viewsets
from .models import ServiceRequest
from .serializers import CreateRequestSeializer
from .permissions import CreateRequestOnlyCustomer , OwnerToSeeAllRequests , SingleRequestPermisiion , CancelRequestPermission , AvailableRequestPermission , AcceptRequestPermission , ProviderCurrentJobsPermission
from rest_framework.decorators import action
from provider.models import *
from accounts.models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from provider.models import ProviderProfile
from request.models import ServiceRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# from .serializers import ServiceRequestSerializer




class ServiceRequestViewSet(viewsets.ModelViewSet):

    queryset = ServiceRequest.objects.all()
    serializer_class = CreateRequestSeializer
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ["status","service_category"]
    ordering_fields = ["created_at","requested_at"]
    search_fields = ["adress_text"]    
    # def get_permissions(self):
    #     if self.action == "list":
    #         return [OwnerToSeeAllRequests()]
    #     if self.action == "create":
    #         return [CreateRequestOnlyCustomer()]
    #     if self.action == "retrieve":
    #         return [SingleRequestPermisiion()]
    #     # if self.action == "cancelRequest":
    #     #     return [ActionRequestPermission()]
    #     return super().get_permissions()
    def get_permissions(self):

        action = getattr(self, "action", None)

        if action == "list":
            return [OwnerToSeeAllRequests()]

        if action == "create":
            return [CreateRequestOnlyCustomer()]

        if action == "retrieve":
            return [SingleRequestPermisiion()]

        return super().get_permissions()
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=False , methods=['GET'] , url_path='me')
    def myRequests(self , request):
        user=request.user
        print("user belong to request " , user)
        alluserrequest = ServiceRequest.objects.filter(customer=user, status__in=['pending', 'broadcasted', 'accepted', 'arrived', 'in_progress'])
        # for req in alluserrequest:
        #     print(req.status)
        serializer = CreateRequestSeializer(alluserrequest, many=True)

        return Response({
            "Total Requests": alluserrequest.count(),
            "Request Data": serializer.data,
        })
    @action(detail=True , methods=['POST'] , url_path='cancel' , permission_classes=[CancelRequestPermission])
    def cancelRequest(self , request , id=None):
        try:
            request_to_cancelled = ServiceRequest.objects.get(id=id)
        except:
            return Response("Object not fount")  
        self.check_object_permissions(request, request_to_cancelled)
        # request_to_cancelled = self.get_object()   i can also use this built in method of DRF instead of this query it automatically chceck the permisiion and deal with dataase
        if request_to_cancelled.status == "cancelled":
            return Response({"detail": "Request is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)        
        request_to_cancelled.status='cancelled'
        request_to_cancelled.save()
        return Response("object cancelled successfully")
            #  AvailableRequestPermission
    @action(detail=False , methods=['GET'] , url_path='available' , permission_classes=[AvailableRequestPermission])
    def available_request(self , request):
        all_avaible_request=ServiceRequest.objects.filter(status='broadcasted' , provider__isnull=True)
        serializer = CreateRequestSeializer(all_avaible_request, many=True)

        return Response({
            "Total Requests": all_avaible_request.count(),
            "Request Data": serializer.data,
        })
    # AcceptRequestPermission
    @action(detail=True , methods=['POST'] , url_path='accept' , permission_classes=[AcceptRequestPermission])
    def AcceptedRequest(self , request , id=None):
        print("user of this request" , request.user)
        try:
            accepted_request = ServiceRequest.objects.get(id=id)
        except:
            return Response("Object not fount") 
        if accepted_request.status == "accepted":
            return Response({"detail": "Request is already accepted"}, status=status.HTTP_400_BAD_REQUEST) 
        accepted_request.save()
        return Response({
            "Requested Accepted Sussessfully ..."
        })

    @action(detail=True , methods=['POST'] , url_path='reject' , permission_classes=[AcceptRequestPermission])
    def RejectedRequest(self , request , id=None):
        try:
            accepted_request = ServiceRequest.objects.get(id=id)
        except:
            return Response("Object not fount") 
        if accepted_request.status == "cancelled":
            return Response({"detail": "Request is already cancelled"}, status=status.HTTP_400_BAD_REQUEST) 
        accepted_request.save()
        return Response({
            "Requested cancelled Sussessfully ..."
        })
    @action(detail=True , methods=['POST'] , url_path='arrived' , permission_classes=[AcceptRequestPermission])
    def RejectedRequest(self , request , id=None):
        try:
            accepted_request = ServiceRequest.objects.get(id=id)
        except:
            return Response("Object not fount") 
        if accepted_request.status == "accepted":
            accepted_request.status='arrived'
            accepted_request.save()
            return Response({"Requested arrived Sussessfully ..."})
        return Response({"detail": "Only accepted request can arrived"}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=True , methods=['POST'] , url_path='start' , permission_classes=[AcceptRequestPermission])
    def RejectedRequest(self , request , id=None):
        try:
            accepted_request = ServiceRequest.objects.get(id=id)
        except:
            return Response("Object not fount") 
        if accepted_request.status == "accepted":
            accepted_request.status='in_progress'
            accepted_request.save()
            return Response({"work on the request have been started Sussessfully ..."})
        return Response({"detail": "Only accepted request can start"}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=True , methods=['POST'] , url_path='complete' , permission_classes=[AcceptRequestPermission])
    def RejectedRequest(self , request , id=None):
        try:
            accepted_request = ServiceRequest.objects.get(id=id)
        except:
            return Response("Object not fount") 
        if accepted_request.status == "in_progress":
            accepted_request.status='completed'
            accepted_request.save()
            return Response({" request have been started Sussessfully completed ..."})
        return Response({"detail": "Only in_progress request can completed"}, status=status.HTTP_400_BAD_REQUEST) 
    # Current jobs of a provider every provider can see their can jobs that they accepted
    @action(detail=False, methods=['GET'], url_path='providers/current' ,  permission_classes=[ProviderCurrentJobsPermission])
    def provider_current(self, request):
        user = request.user
        try:
            provider_profile = user.ProviderProfile  # check related_name in model
        except ProviderProfile.DoesNotExist:
            return Response({"detail": "Provider profile not found"}, status=404)
        requests = ServiceRequest.objects.filter(provider=provider_profile)
        print(requests.query)
        print(ServiceRequest.objects.filter(provider=provider_profile).count())
        serializer = CreateRequestSeializer(requests, many=True)
        return Response({
        "total_requests": requests.count(),
        "requests": serializer.data
        })

#       python manage.py runserver
















