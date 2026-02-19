from django.core.cache import cache
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect , render
from django.contrib.auth import login

def send_otp(email):
    otp = random.randint(100000, 999999)
    cache.set(email,otp,timeout=300)

    message = f"""
                    Hi there,

                    You recently requested an OTP for your account. Please use the following code to proceed:

                    OTP: {otp}

                    This OTP is valid for the next 5 minutes. For security reasons, do not share this code with anyone.

                    If you did not request this OTP, please ignore this email.

                    Thank you,
                    YourStore Team
                    """

    send_mail(
        subject="Your OTP",
        message=message,
        from_email="noreply@RadhaPiya.com",
        recipient_list=[email],
        fail_silently=False,
    )
    return True



