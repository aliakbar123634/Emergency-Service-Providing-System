from django.db import models
from accounts.models import CustomUserModel
# Create your models here.
class Notification(models.Model):
    NOTIFICATION_TYPES = (
    ("request", "Emergency Request"),
    ("accepted", "Request Accepted"),
    ("completed", "Service Completed"),
    ("payment", "Payment"),
    ("system", "System Notification"),
    )
    user=models.ForeignKey(CustomUserModel , on_delete=models.CASCADE , related_name='notifications')
    title=models.CharField(max_length=50)
    message=models.TextField()
    notification_type=models.CharField(max_length=20 , choices=NOTIFICATION_TYPES)
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)



#   python manage.py makemigrations notificaion
#   python manage.py migrate
#   python manage.py runserver