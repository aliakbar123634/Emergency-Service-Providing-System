from . models import *
from rest_framework import serializers


class CreateRequestSeializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceRequest
        fields=['id' , 'customer', 'service_category' , 'latitude' , 'longitude'  , 'adress_text' , 'price_estamited' , 'final_price' , 'requested_at' , 'compeleted_at' , 'created_at' , 'updated_at' ]
        read_only_fields = ['id' ,'created_at' ,'customer', 'updated_at' , 'requested_at']


class ServiceStatusLogSerializer(serializers.ModelSerializer):

    class Meta:
        model=ServiceStatusLog
        fields=['id' , 'service_request', 'changed_by' , 'notes' , 'status' , 'created_at' ]
        # read_only_fields = ['id' ,'created_at' ,'customer', 'updated_at' , 'requested_at']


#    python manage.py runserver       