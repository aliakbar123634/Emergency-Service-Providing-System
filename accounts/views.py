# from django.shortcuts import render
from rest_framework import viewsets
from . serializers import *
from . models import *
from . permissions import onlyUserpermission , AdminOnlyPermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from  rest_framework.decorators import action
User = get_user_model()




# Create your views here.

class RegiatrationViewset(viewsets.ModelViewSet):
    queryset=CustomUserModel.objects.all()
    serializer_class=RegistrationSerializer

@api_view(['POST'])
def loginview(request):
    ser=LoginSerializer(data=request.data)
    if ser.is_valid():
        email=ser.validated_data['email']
        password=ser.validated_data['password']
        user = CustomUserModel.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=200)
        return Response({"error": "Invalid email or password"}, status=401)
    return Response(ser.errors , status=status.HTTP_400_BAD_REQUEST ) 
           

          
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def LogOutView(request):
    try:
        refresh_token = request.data.get("refresh")
        token=RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {"message": "User logged out successfully"},
            status=status.HTTP_205_RESET_CONTENT
        )    
    except:
        return Response(
        {"error": "Invalid token"},
            status=status.HTTP_400_BAD_REQUEST
        )

class PersonalViewclass(APIView):
    permission_classes=[onlyUserpermission]
    def get(self , request , id):  
        try:
            person = User.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )          
        self.check_object_permissions(request, person)
        ser = PersonalSerializer(person)
        return Response(ser.data, status=status.HTTP_200_OK)        
    def put(self , request , id):
        try:
            person = User.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            ) 
        self.check_object_permissions(request, person)
        profileUpdateSerializer=PersonalUpdateSerializer(instance=person , data=request.data ,  partial=True)
        if profileUpdateSerializer.is_valid():
            profileUpdateSerializer.save()
            response_serializer=PersonalSerializer(person)
            return Response(
                response_serializer.data,
                status=status.HTTP_202_ACCEPTED
            )
        return Response(profileUpdateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self , request , id):
        try:
            person = User.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            ) 
        self.check_object_permissions(request, person)
        person.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class WalletView(APIView):
    def get(self , request):
        wallet=Wallet.objects.all()
        ser=WalletSerializer(wallet , many=True)
        return Response(ser.data , status=status.HTTP_200_OK)     
    

class AdminViewSet(viewsets.ModelViewSet):
    queryset=CustomUserModel.objects.all()
    serializer_class=PersonalSerializer
    permission_classes=[AdminOnlyPermission] 
    #   action to verify any user
    @action(detail=True , methods=['PATCH'] , url_path='verify')  
    def verify_any_user(self , request , pk=None):
        try:
            user_related_to_query=CustomUserModel.objects.get(id=pk)
        except CustomUserModel.DoesNotExist:
            return Response({
                "Message": "User not found to the given query ...."
            } , status=status.HTTP_400_BAD_REQUEST)
        if user_related_to_query.is_verified:
            return Response({
                "message"  : "this user already verified ..."
            })
        user_related_to_query.is_verified=True
        user_related_to_query.save()
        return Response({
                "message"  : "User Verified successfully    .........."
        })        
        

      