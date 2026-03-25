from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager , UserManager
import uuid
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required ...")
        email=self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user    

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
class CustomUserModel(AbstractUser):
    role=(
        ('customer' , 'customer'),
        ('provider' , 'provider'),
        ('admin' , 'admin')
    )
    id=models.UUIDField(primary_key=True ,  default=uuid.uuid4 , editable=False)
    username=None
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15 , unique=True)
    full_name=models.CharField(max_length=100)
    role=models.CharField(max_length=30 , choices=role, default='customer')
    verification_token = models.CharField(max_length=100,null=True,blank=True)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)    
    updated_at=models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects=CustomUserManager()
    def __str__(self):
        return self.email
     

class Wallet(models.Model):
    user=models.OneToOneField(CustomUserModel , on_delete=models.CASCADE , related_name='Wallet')
    balance=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency=models.CharField(max_length=10, default="PKR")
    is_active=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)    
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} wallet"


#   python manage.py makemigrations accounts
#   python manage.py migrate
#   python manage.py runserver
#   python manage.py createsuperuser   