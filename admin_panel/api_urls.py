from django.urls import path, include
from rest_framework.routers import DefaultRouter

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
    path('', include(router.urls)),
]