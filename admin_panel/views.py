from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import random
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime

# Create your views here.
def home(request):
    return redirect('login')



def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        
        if user is not None and user.email:
            otp = random.randint(100000, 999999)
            request.session['admin_otp'] = otp
            request.session['admin_username'] = username

            send_mail(
                subject="Admin Login OTP for safe and secure login",
                message=f"Your OTP is {otp}",
                from_email="whytehousee@gmail.com",
                recipient_list=[user.email],
            )
            return redirect('verify_otp')
        else:
            context = {'error': 'Invalid credentials or email not configured'}
            return render(request, "admin/login.html", context)

    return render(request, "admin/login.html")

def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST.get("otp", "")
        real_otp = str(request.session.get("admin_otp", ""))

        if user_otp == real_otp:
            request.session['admin_logged_in'] = True
            return redirect('dashboard')
        else:
            context = {'error': 'Invalid OTP. Please try again.'}
            return render(request, "admin/verify_otp.html", context)

    return render(request, "admin/verify_otp.html")

def resend_otp(request):
   
    username = request.session.get('admin_username')
    
    if username:
        try:
            user = User.objects.get(username=username)
            if user.email:
                
                otp = random.randint(100000, 999999)
                request.session['admin_otp'] = otp
                
               
                send_mail(
                    subject="Admin Login OTP for safe and secure login",
                    message=f"Your OTP is {otp}",
                    from_email="whytehousee@gmail.com",
                    recipient_list=[user.email],
                )
        except User.DoesNotExist:
            pass
    
    return redirect('verify_otp')

def forgot_password(request):
    return render(request, 'admin/forgotpassword.html')

def dashboard(request):
    return render(request, 'admin/index.html')
