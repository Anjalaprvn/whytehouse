from . import views
from django.urls import path, include

app_name = "admin_panel"
urlpatterns = [
    # Auth and main dashboard
    path('login/', views.login, name='login'), 
    path('forgot-password/', views.forgot_password, name='forgot_password'), 
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leads/', views.lead_management, name='leads'),
    path('leads/add/', views.add_lead, name='add_lead'),
    path('leads/edit/<int:id>/', views.edit_lead, name='edit_lead'),    
    path('leads/delete/<int:lead_id>/', views.delete_lead, name='delete_lead'),
    path("hospitality-management/", views.hospitality_management, name="admin_hospitality"),
    path("hospitality-management/add/", views.add_property, name="admin_add_property"),
    path("hospitality-management/edit/<int:property_id>/", views.edit_property, name="admin_edit_property"),
    path("hospitality-management/delete/<int:property_id>/", views.delete_property, name="admin_delete_property"),
    path('travel-packages/', views.travel_packages, name='travel_packages'),
    path('travel-packages/add/', views.travel_package_add, name='travel_package_add'),
    path('travel-packages/edit/<int:package_id>/', views.travel_package_edit, name='travel_package_edit'),
    path('travel-packages/delete/<int:package_id>/', views.travel_package_delete, name='travel_package_delete'),
    path('customer-inquiries/', views.customer_inquiries, name='customer_inquiries'),

]