from rest_framework import serializers
from . models import *
from service.models import *
from accounts.models import Wallet



class PaymentCreateSerializer(serializers.Serializer):
    # service_request = serializers.UUIDField()
    service_request = serializers.UUIDField(source='servicerequest.id')
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class PostPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields=['id' , 'servicerequest' , 'plate_form_fee' , 'provider_amount' , 'status']
        read_only_fields = ['id' ,'plate_form_fee' ,'provider_amount', 'status']
        

#   wallet model that i took from accounts model
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wallet
        fields=['id' , 'user'  , 'balance' , 'currency' , 'is_active' , 'created_at' , 'updated_at']



        #   python manage.py runserver