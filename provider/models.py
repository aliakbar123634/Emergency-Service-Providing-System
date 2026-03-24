from django.db import models
from accounts.models import CustomUserModel
from service.models import ServiceCategory
from datetime import datetime



class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
# Create your models here.
class CustomerProfile(models.Model):
    user=models.OneToOneField(CustomUserModel ,on_delete=models.CASCADE , related_name='CustomerProfile')
    profile_image = models.ImageField(upload_to='profile_images/',null=True, blank=True)
    address = models.TextField() 
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)    
    updated_at=models.DateTimeField(auto_now=True) 
    is_deleted = models.BooleanField(default=False)  # New field
    objects = ActiveManager()
    all_objects = models.Manager()
    def delete(self, using =None, keep_parents = False):
        self.is_deleted = True
        self.save()
 
    def __str__(self):
        return self.user.email    
class ProviderProfile(models.Model):
    user=models.OneToOneField(CustomUserModel ,on_delete=models.CASCADE , related_name='ProviderProfile')
    profile_image = models.ImageField(upload_to='provider_profiles/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    service=models.ManyToManyField(ServiceCategory  , related_name="ProviderProfile")
    experience_years=models.PositiveIntegerField(default=0)
    cnic_number=models.CharField(max_length=30)
    cnic_image = models.ImageField(upload_to='provider_documents/', null=True, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_jobs_completed=models.PositiveIntegerField(default=0)
    is_available=models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    city = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True) 
    created_at=models.DateTimeField(auto_now_add=True)    
    updated_at=models.DateTimeField(auto_now=True) 
    is_deleted = models.BooleanField(default=False)
    objects = ActiveManager()
    all_objects = models.Manager()    
    def delete(self, using = None, keep_parents = False):
        self.is_deleted=True
        self.save()
    def __str__(self):     
        return self.user.email


class Job(models.Model):
    customer = models.ForeignKey('CustomerProfile', on_delete=models.CASCADE, related_name="jobs")
    provider = models.ForeignKey('ProviderProfile', on_delete=models.CASCADE, related_name="jobs")
    service = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True)
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    scheduled_start = models.DateTimeField(default=datetime.now)
    scheduled_end = models.DateTimeField(null=True, blank=True)
    
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.provider.user.email} - {self.service.name}"

#   python manage.py makemigrations provider
#   python manage.py migrate
#   python manage.py runserver