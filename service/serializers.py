from rest_framework import serializers
from . models import *

class ServiceCategorySerializer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(read_only=True)
    updated_at=serializers.DateTimeField(read_only=True)
    class Meta:
        model=ServiceCategory
        fields=['id','name','description','base_price','is_active','created_at','updated_at']