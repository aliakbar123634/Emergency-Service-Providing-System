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
from  rest_framework.decorators import action
User = get_user_model()
from django.utils import timezone  
from django.core.mail import send_mail
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.email import send_verification_email
from utils.email import send_reset_email

#  this is my firstend point which will send ka verification token on the email of the authenticated user 
class SendVerificationEmail(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        token = str(uuid.uuid4())
        user.verification_token = token
        user.save()
        send_verification_email(user.email, token)
        return Response({
            "message": "Verification email sent"
        })

#   this is the second endpoint which will verify the gmail through the token we send by using send verification email we will take that token and pass in the body of this endpoint ....
class VerifyEmail(APIView):
    def post(self, request):
        token = request.data.get("token")
        user = CustomUserModel.objects.filter(
            verification_token=token
        ).first()
        if not user:
            return Response(
                {"error": "Invalid token"},
                status=400
            )
        user.is_verified = True
        user.verification_token = None
        user.save()
        return Response({
            "message": "Email verified"
        })



#  this end point work same as work verification send email endpoints work we will simply send a gmail and new email with the token
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = CustomUserModel.objects.filter(
            email=email
        ).first()
        if not user:
            return Response(
                {"error": "User not found"},
                status=404
            )
        token = str(uuid.uuid4())
        user.reset_token = token
        user.reset_token_created_at = timezone.now()
        user.save()
        send_reset_email(user.email, token)
        return Response({
            "message": "Reset email sent"
        })


#  in this end point we will take the token from emial we will receive and then pass new password and token to chane the password .....
class ResetPasswordView(APIView):
    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        if not token or not new_password:
            return Response(
                {"error": "token and new_password required"},
                status=400,
            )
        user = CustomUserModel.objects.filter(
            reset_token=token
        ).first()
        if not user:
            return Response(
                {"error": "Invalid token"},
                status=400,
            )
        #expire check (30 min)
        if user.reset_token_created_at:
            diff = timezone.now() - user.reset_token_created_at
            if diff.total_seconds() > 1800:
                return Response(
                    {"error": "Token expired"},
                    status=400,
                )
        user.set_password(new_password)
        user.reset_token = None
        user.reset_token_created_at = None
        user.save()
        return Response(
            {"message": "Password reset successful"}
        )

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            return Response(
                {"error": "old_password and new_password required"},
                status=400,
            )
        if not user.check_password(old_password):
            return Response(
                {"error": "Old password incorrect"},
                status=400,
            )
        user.set_password(new_password)
        user.save()
        return Response(
            {"message": "Password changed successfully"}
        )





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
        

      


      #    python manage.py runserver