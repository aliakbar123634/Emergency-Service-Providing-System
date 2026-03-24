from . models import Review
from rest_framework import serializers



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=[ 'id' , 'service_request' , 'Customer' , 'provider' , 'rating' , 'comment' ,'created_at' ]
        read_only_fields = ['id' ,'Customer' ,'provider', 'created_at']





        #   python manage.py runserver