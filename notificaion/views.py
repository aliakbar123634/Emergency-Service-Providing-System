from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . serializers import NotificationSerializer
from . models import Notification
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . permissions import AdminOnlyPermission
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.

class NotifilationViewSet(ModelViewSet):
    queryset=Notification.objects.all()
    serializer_class=NotificationSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ["is_read","notification_type"]

    ordering_fields = [ "created_at"]
    def get_permissions(self):
        if self.action=="list":
            return [IsAuthenticated()]  
        if self.action=="retrieve":
            return [AdminOnlyPermission()]  
        if self.action=="destroy":
            return [AdminOnlyPermission()]                
        return super().get_permissions()  
    # actually problem was that here that create function was working here that i get from model view set we just overright that function ...
    def create(self, request, *args, **kwargs):
        return Response(
        {"message": "Use /notification/send/"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )      
      
    @action(detail=False , methods=['POST'] , url_path='send' , permission_classes=[AdminOnlyPermission])
    def sendNotification(self , request):
        user=request.user
        print(request.user.role)
        serializer=NotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data.get('user')
        title=serializer.validated_data.get('title')
        message=serializer.validated_data.get('message')
        notification_type=serializer.validated_data.get('notification_type')
        print(request.user.role)
        noti=Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type
        )
        print(request.user.role)
        return Response({
            "Ntification-id":noti.id,
            "message":"Notification send successfully ..."
        }, status=status.HTTP_200_OK)
    #  here i did the same as i did above i just override the default update method that i got from modelview set because i want to make my own patch method
    def update(self, request, *args, **kwargs):
        return Response(
        {"message": "Use /notification/read/"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )
    @action(detail=True , methods=['PATCH'] , url_path='read' , permission_classes=[AdminOnlyPermission])
    def readNotification(self , request , pk=None):   
        try:
            notification_Related_to_id=Notification.objects.get(id=pk)  
        except Notification.DoesNotExist:
            return Response({
                "message":"notification not related to given query"
            } , status=status.HTTP_400_BAD_REQUEST)
        notification_Related_to_id.is_read=True
        notification_Related_to_id.save()
        return Response({
            "message": "Notification marked as read",
            "is_read": notification_Related_to_id.is_read
        } , status=status.HTTP_200_OK)
    @action(detail=False, methods=['PATCH'], url_path='read-all', permission_classes=[IsAuthenticated])
    def read_all(self, request):
        user = request.user
        unread_qs = Notification.objects.filter(user=user ,is_read=False)
        unread_count = unread_qs.count()
        for obj in unread_qs:
            obj.is_read = True
            obj.save()
        # unread_qs.update(is_read=True)
        return Response({
            "message": "All notifications marked as read",
            "updated_count": unread_count,
            "unread_before": unread_count,
            "unread_after": 0
        })

#   python manage.py runserver