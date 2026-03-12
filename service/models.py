from django.db import models

# Create your models here.
class ServiceCategory(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    base_price=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)    
    updated_at=models.DateTimeField(auto_now=True)    


#   python manage.py makemigrations service
#   python manage.py migrate