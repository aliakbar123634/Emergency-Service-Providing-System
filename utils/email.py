from django.core.mail import send_mail
from django.conf import settings


#  send emial to verify   ...
def send_verification_email(email, token):
    link = f"http://127.0.0.1:8000/auth/verify-email/?token={token}"

    send_mail(
        "Verify Email",
        f"Click to verify: {link}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )


#   utilts for reset password ...
def send_reset_email(email, token):

    link = f"http://127.0.0.1:8000/auth/reset-password/?token={token}"

    send_mail(
        "Reset Password",
        f"Click to reset password: {link}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )    