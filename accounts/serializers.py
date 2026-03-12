from rest_framework import serializers
from . models import *

class RegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=CustomUserModel
        fields=['email' ,'phone' , 'password', 'password2','full_name','role']
    def validate(self, attrs):
        pass1=attrs.get('password')
        pass2 = attrs.pop('password2')
        if pass1 != pass2 :
            raise serializers.ValidationError("password and confirm password are not similar....")
        return attrs 
    def create(self, validated_data):
        password = validated_data.pop('password')
        # User create
        user = CustomUserModel.objects.create_user(password=password, **validated_data)
        
        # Send verification email after user creation

        return user

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)


class PersonalSerializer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(read_only=True)
    updated_at=serializers.DateTimeField(read_only=True)
    class Meta:
        model=CustomUserModel
        fields=['id' , 'email'  , 'phone' , 'full_name' , 'role' , 'created_at' , 'updated_at']
class PersonalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUserModel
        fields=[ 'phone' , 'full_name']            


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wallet
        fields=['id' , 'user'  , 'balance' , 'currency' , 'is_active' , 'created_at' , 'updated_at']
