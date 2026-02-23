from . import views
from django.urls import path, include


urlpatterns = [
    # Auth and main dashboard
    path('login/', views.login, name='login'), 
    path('forgot-password/', views.forgot_password, name='forgot_password'), 
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('dashboard/', views.dashboard, name='dashboard'),
]