from rest_framework import serializers
from . models import *
from rest_framework.exceptions import ValidationError

class CustomerSerializer(serializers.ModelSerializer):
    user=serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model=CustomerProfile
        fields=['id','user','profile_image','address','latitude','longitude','created_at','updated_at']
        read_only_fields = ['created_at', 'updated_at']
    def validate(self, attrs):
        # get the current user from the request
        user = self.context['request'].user

        if CustomerProfile.objects.filter(user=user , is_deleted=False).exists():
            raise ValidationError("You already have a profile.")
        return attrs    


class ProviderSerializer(serializers.ModelSerializer):
    user=serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model=ProviderProfile
        fields=['id','user',"profile_image","bio",'service','experience_years','cnic_number','cnic_image','average_rating','total_jobs_completed','is_available','is_verified','city','profile_image','latitude','longitude','created_at','updated_at']
        read_only_fields = ['created_at', 'updated_at' , 'total_jobs_completed','is_verified']    

# serializer for jobs of an entity it will use history active jobs and pending jobs
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id','service','status','scheduled_start','scheduled_end','started_at','completed_at','price']



class ProviderProfileSerializer(serializers.ModelSerializer):
    cnic_image = serializers.ImageField(read_only=True)
    class Meta:
        model = ProviderProfile
        fields = [
            "id", "bio", "service", "experience_years", "cnic_number",
            "cnic_image", "average_rating", "total_jobs_completed",
            "is_available", "is_verified", "city", "latitude", "longitude",
            "created_at"
        ]