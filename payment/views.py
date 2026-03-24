from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db import transaction
from decimal import Decimal
from provider.models import ProviderProfile
from request.models import ServiceRequest
from accounts.models import Wallet
from .models import Payment, WalletTransaction
from .serializers import PaymentCreateSerializer , PostPaymentSerializer
from .permissions import IsCustomerAndOwner , IsProviderOnly , IsAdminRole
from accounts.models import Wallet
from django.db.models import Sum
from decimal import Decimal, InvalidOperation
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class PaymentViewSet(ModelViewSet):

    queryset = Payment.objects.all()
    serializer_class = PostPaymentSerializer
    permission_classes = [IsCustomerAndOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status"]
    ordering_fields = ["created_at", "paid_at"]    
    def get_permissions(self):
        if self.action=="list":
            return [IsAdminRole()]
        return super().get_permissions()
    @action(detail=False, methods=["post"], url_path="pay")
    def pay(self, request):

        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service_request_id = serializer.validated_data["service_request"]
        amount = serializer.validated_data["amount"]

        service_request = ServiceRequest.objects.filter(id=service_request_id).first()

        if not service_request:
            return Response({"message": "Service request not found"}, status=404)

        wallet = Wallet.objects.filter(user=request.user).first()

        if not wallet:
            return Response({"message": "Wallet not found"}, status=404)

        with transaction.atomic():

            if wallet.balance < amount:
                return Response({"message": "Insufficient balance"}, status=400)

            wallet.balance -= amount
            wallet.save()

            transaction_obj = WalletTransaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type="debit",
                refrence_type="service_payment",
                refrence_id=str(service_request.id),
            )

            platform_fee = amount * Decimal("0.15")
            provider_amount = amount - platform_fee

            payment = Payment.objects.create(
                servicerequest=service_request,
                transaction=transaction_obj,
                plate_form_fee=platform_fee,
                provider_amount=provider_amount,
                status="pending",
            )

        return Response({"id": payment.id})
    @action(detail=True, methods=["get"], url_path="detail" )
    def payment_detail(self, request, pk=None):
        payment = self.get_object()
        return Response({
            "id": payment.id,
            "status": payment.status,
            "platform_fee": payment.plate_form_fee,
            "provider_amount": payment.provider_amount,
        })    

    @action(detail=False, methods=["GET"], url_path="history")
    def history_detail(self, request):
        user = request.user
    # get all service requests of this user
        service_requests = ServiceRequest.objects.filter(customer=user)
        if not service_requests.exists():
            return Response(
                {"message": "No service requests found"},
                status=status.HTTP_404_NOT_FOUND
            )
    # get all payments of those requests
        payments = Payment.objects.filter(servicerequest__in=service_requests)
        if not payments.exists():
            return Response(
                {"message": "No payments found"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = []
        for payment in payments:
            data.append({
            "id": payment.id,
            "status": payment.status,
            "platform_fee": payment.plate_form_fee,
            "provider_amount": payment.provider_amount,
        })

        return Response(data, status=status.HTTP_200_OK)
    
  
  
  
    @action(detail=False, methods=["GET"], url_path="earning" , permission_classes = [IsProviderOnly] )    #
    def provider_earning(self , request):
        user = request.user
        try:
            provider_profile = ProviderProfile.objects.get(user=request.user)
        except ProviderProfile.DoesNotExist:
            return Response(
        {"message": "Provider profile not found"},
        status=status.HTTP_404_NOT_FOUND
    )        
        service_requests = ServiceRequest.objects.filter(provider=provider_profile)
        if not service_requests.exists():
            
            return Response(
                {"message": "No service requests found"},
                status=status.HTTP_404_NOT_FOUND
            )   
        payments = Payment.objects.filter(servicerequest__in=service_requests)
        if not payments.exists():
            return Response(
                {"message": "No payments found"},
                status=status.HTTP_404_NOT_FOUND
            )
        data = []
        total_earning=0
        total_completed_jobs=0
        pending_amount=0
        for payment in payments:
            total_earning+=payment.provider_amount
            total_completed_jobs+=1    
            if payment.status=="pending":
                pending_amount+=payment.provider_amount
            data.append({
            "id": payment.id,
            "status": payment.status,
            "platform_fee": payment.plate_form_fee,
            "provider_amount": payment.provider_amount,
        }) 
        return Response({
            "total_earning":total_earning,
            "total_completed_jobs":total_completed_jobs,
            "pending_amount":pending_amount,
            "one by one query" :data,
        },
            status=status.HTTP_200_OK)                       
    # action to refunf money from payments for any reason
    @action(detail=True, methods=["POST"], url_path="refund" , permission_classes=[IsCustomerAndOwner]  ) 
    def RefundMoney(self , request , pk=None):
        payment_belong_to_id = self.get_object()
        if payment_belong_to_id.servicerequest.customer != request.user:
            return Response({"message": "Not allowed"}, status=403) 
        if payment_belong_to_id.status == "refunded":
            return Response({"message": "Payment already refunded"}, status=400)       
        try:
            wallet_belong_to_customer=Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            return Response({
                "message": "wallet does not found ..."
            } , status=status.HTTP_400_BAD_REQUEST) 
        with transaction.atomic():   

        # 💰 refund amount
        # refund_amount = payment.provider_amount

        # wallet.balance += refund_amount
        # wallet.save() 
            wallet_belong_to_customer.balance+=payment_belong_to_id.provider_amount
            wallet_belong_to_customer.save()
            WalletTransaction.objects.create(
                wallet=wallet_belong_to_customer,
                amount=payment_belong_to_id.provider_amount,
                transaction_type="credit",
                refrence_type="refund",
                refrence_id=str(payment_belong_to_id.id)
            )
            payment_belong_to_id.status = "refunded"
            payment_belong_to_id.save()            
        return Response({
            "message":"Amount refund successfully ...",
            'payment_id':payment_belong_to_id.id,
            "refund_amount":payment_belong_to_id.provider_amount,
            "wallet_balance": wallet_belong_to_customer.balance,
            'status':payment_belong_to_id.status            
        })             


# wallet model view that i make from wallet and different kind of transaction
class WallteandTransactionModelViewset(ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsCustomerAndOwner]    
    #   show balance in the walet 
    @action(detail=False, methods=["GET"], url_path="balance", permission_classes=[IsProviderOnly])
    def wallet_balance(self, request):
        try:
            wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            return Response(
            {"message": "Wallet not found"},
            status=status.HTTP_404_NOT_FOUND
        )

        return Response({
            "user": request.user.email,
            "wallet_id": wallet.id,
            "balance": wallet.balance
        }, status=status.HTTP_200_OK)

    # action to show transactions of a wallet
    @action(detail=False, methods=["GET"], url_path="transaction", permission_classes=[IsProviderOnly])
    def WalletTransaction(self , request):
        user=request.user
        try:
            wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            return Response(
            {"message": "Wallet not found"},
            status=status.HTTP_404_NOT_FOUND
        )
        wallet_transactions=wallet.WalletTransaction.all()
        # wallet_transactions = WalletTransaction.objects.filter(wallet=wallet).order_by("-id")
        deta=[]
        total_balance=0
        for i in wallet_transactions:
            if i.transaction_type == "credit":
                total_balance += i.amount
            else:
                total_balance -= i.amount  
            total_balance = 0
            total_balance+=i.amount
            deta.append({
            "id": i.id,
            "amount": i.amount,
            "transaction_type": i.transaction_type,
            "refrence_type": i.refrence_type,
            "refrence_id": i.refrence_id,
            "created_at": i.created_at,
        })             
        return Response({
            "wallet_id":wallet.id,   
            "total_balance":total_balance,
            "Transactions":deta
        } ,
            status=status.HTTP_200_OK)

    # action to add money in the wallet 
    @action(detail=False, methods=["POST"], url_path="deposite", permission_classes=[IsProviderOnly])
    def AddMoney(self , request ):
        deposited_amount = request.data.get("amount")
        if not deposited_amount:
            return Response(
            {"message": "Amount is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
        try:
             deposited_amount = Decimal(deposited_amount)
        except (InvalidOperation, TypeError):
              return Response(
        {"message": "Invalid amount"},
        status=status.HTTP_400_BAD_REQUEST
    )

        if deposited_amount <= 0:
             return Response(
            {"message": "Amount must be greater than 0"},
            status=status.HTTP_400_BAD_REQUEST
        )        
        user=request.user
        try:
            userwallet=Wallet.objects.get(user=user)
        except Wallet.DoesNotExist :   
            return Response(
            {"message": "Wallet not found"},
            status=status.HTTP_404_NOT_FOUND
        )
        userwallet.balance += deposited_amount
        userwallet.save()
        WalletTransaction.objects.create(
            wallet=userwallet,
            amount=deposited_amount,
            transaction_type="credit",
            refrence_type="deposit",
        refrence_id=str(userwallet.id)
    )
        return Response({
            "message":"amount deposted successfully",
            "wallet_id":userwallet.id,
            "deposited_amount":deposited_amount,
            "new_balance":userwallet.balance
        })

    # action to withdraw  money in the wallet 
    @action(detail=False, methods=["POST"], url_path="withdraw", permission_classes=[IsProviderOnly])
    def WithdrawMoney(self , request ):
        withdraw_amount = request.data.get("amount")
        if not withdraw_amount:
            return Response(
            {"message": "Amount is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
        try:
            withdraw_amount = Decimal(withdraw_amount)
        except (InvalidOperation, TypeError):
              return Response(
        {"message": "Invalid amount"},
        status=status.HTTP_400_BAD_REQUEST
    )

        if withdraw_amount <= 0:
             return Response(
            {"message": "Amount must be greater than 0"},
            status=status.HTTP_400_BAD_REQUEST
        )        
        user=request.user
        try:
            userwallet=Wallet.objects.get(user=user)
        except Wallet.DoesNotExist :   
            return Response(
            {"message": "Wallet not found"},
            status=status.HTTP_404_NOT_FOUND
        )
        userwallet.balance -= withdraw_amount
        userwallet.save()
        WalletTransaction.objects.create(
            wallet=userwallet,
            amount=withdraw_amount,
            transaction_type="credit",
            refrence_type="deposit",
        refrence_id=str(userwallet.id)
    )
        return Response({
            "message":"amount deposted successfully",
            "wallet_id":userwallet.id,
            "withdraw_amount":withdraw_amount,
            "new_balance":userwallet.balance
        })



#   python manage.py runserver