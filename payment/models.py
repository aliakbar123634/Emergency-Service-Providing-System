from django.db import models
from request.models import ServiceRequest
from accounts.models import Wallet
# Create your models here.
class WalletTransaction(models.Model):
    transaction_status=(
        ('credit' , 'credit'),
        ('debit' , 'debit'),
    )
    wallet=models.ForeignKey(Wallet , on_delete=models.CASCADE , related_name="WalletTransaction")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type=models.CharField(max_length=15 , choices=transaction_status , default="credit")
    refrence_type=models.CharField(max_length=50)
    refrence_id=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.transaction_type} {self.amount}"

class Payment(models.Model):
    payment_status=(
        ('pending' , 'pending'),
        ('success' , 'success'),
        ('failed' , 'failed'),
        ('refund' , 'refund'),
    )
    servicerequest=models.OneToOneField(ServiceRequest , on_delete=models.CASCADE , related_name="Payment")
    transaction = models.OneToOneField(WalletTransaction , on_delete=models.CASCADE , related_name="Payment")
    plate_form_fee=models.DecimalField(max_digits=8 , decimal_places=3)
    provider_amount=models.DecimalField(max_digits=10 , decimal_places=3)
    status=models.CharField(max_length=15 , choices=payment_status , default="pending")
    paid_at=models.DateTimeField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Payment for {self.servicerequest.id}"
    


#   python manage.py makemigrations payment
#   python manage.py migrate