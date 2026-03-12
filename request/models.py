from django.db import models
import uuid
from accounts.models import CustomUserModel
from provider.models import ProviderProfile
from service.models import ServiceCategory
# Create your models here.
class ServiceRequest(models.Model):
    status_choice=(
        ('pending' , 'pending'),
        ('broadcasted' , 'broadcasted'),
        ('accepted' , 'accepted'),
        ('arrived' , 'arrived'),
        ('in_progress' , 'in_progress'),
        ('completed' , 'completed'),
        ('cancelled' , 'cancelled'),
    )
    id=models.UUIDField(primary_key=True ,  default=uuid.uuid4 , editable=False)
    customer=models.ForeignKey(CustomUserModel , on_delete=models.CASCADE , related_name="ServiceRequest")
    provider=models.ForeignKey(ProviderProfile , on_delete=models.SET_NULL , related_name="ServiceRequest" , null=True , blank=True)
    service_category=models.ForeignKey(ServiceCategory , on_delete=models.CASCADE , related_name="ServiceRequest")
    latitude = models.FloatField()
    longitude = models.FloatField()
    adress_text=models.TextField()
    status=models.CharField(max_length=30 , choices=status_choice, default='pending')
    price_estamited=models.DecimalField(max_digits=10 , decimal_places=3 , default=0)
    final_price=models.DecimalField(max_digits=10 , decimal_places=3 , default=0)
    requested_at=models.DateTimeField(auto_now_add=True) 
    accepted_at=models.DateTimeField(null=True, blank=True) 
    compeleted_at=models.DateTimeField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)    
    updated_at=models.DateTimeField(auto_now=True)  
    def __str__(self):
        return f"{self.service_category.name} request"
    

class ServiceStatusLog(models.Model):
    service_request=models.ForeignKey(ServiceRequest , on_delete=models.CASCADE , related_name="ServiceStatusLog")  
    changed_by=models.ForeignKey(CustomUserModel , on_delete=models.CASCADE , related_name="ServiceStatusLog")  
    notes=models.TextField()
    status=models.CharField(max_length=30)
    created_at=models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.notes
    
#   python manage.py makemigrations request
#   python manage.py migrate
#   python manage.py runserver