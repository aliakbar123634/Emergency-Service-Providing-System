from django.db import models
from accounts.models import CustomUserModel
from request.models import ServiceRequest
from provider.models import ProviderProfile
# Create your models here.
class Review(models.Model):
    service_request=models.OneToOneField(ServiceRequest , on_delete=models.CASCADE , related_name='Review')
    Customer=models.ForeignKey(CustomUserModel , on_delete=models.CASCADE , related_name='Review')
    provider=models.ForeignKey(ProviderProfile , on_delete=models.CASCADE , related_name='Review')
    rating=models.PositiveIntegerField(default=0)
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.rating}"


#   python manage.py makemigrations review
#   python manage.py migrate