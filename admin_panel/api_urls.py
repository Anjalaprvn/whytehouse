from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .api_views import (
    CustomerViewSet,
    ResortViewSet,
    MealViewSet,
    AccountViewSet,
    InvoiceViewSet,
    VoucherViewSet,
    LeadViewSet,
    PropertyViewSet,
    FeedbackViewSet,
    BlogViewSet,
    DestinationViewSet,
    EmployeeViewSet,
    TravelPackageViewSet,
    request_otp,
    verify_otp_and_login,
    resend_otp,
)

router = DefaultRouter()

router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'resorts', ResortViewSet, basename='resort')
router.register(r'meals', MealViewSet, basename='meal')
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'vouchers', VoucherViewSet, basename='voucher')
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'destinations', DestinationViewSet, basename='destination')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'packages', TravelPackageViewSet, basename='package')

urlpatterns = [
    # OTP-based JWT Authentication endpoints
    path('auth/request-otp/', request_otp, name='request_otp'),
    path('auth/verify-otp/', verify_otp_and_login, name='verify_otp'),
    path('auth/resend-otp/', resend_otp, name='resend_otp'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('', include(router.urls)),
]