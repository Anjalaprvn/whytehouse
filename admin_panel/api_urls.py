from django.urls import path
from .api_views import (
    BlogViewSet,
    BlogCategoryViewSet,
    LeadViewSet,
    PropertyViewSet,
    TravelPackageViewSet,
    DestinationViewSet,
    CustomerViewSet,
    MealViewSet,
    AccountViewSet,
    InquiryViewSet,
    EmployeeViewSet,
    ResortViewSet,
    VoucherViewSet,
    InvoiceViewSet,
    FeedbackViewSet,
    validate_package_id,
    get_next_invoice_id,
    get_next_voucher_id,
)

def list_view(viewset):
    return viewset.as_view({'get': 'list'})

def add_view(viewset):
    return viewset.as_view({'post': 'create'})

def detail_view(viewset):
    return viewset.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [
    # Blogs
    path('blogs/', list_view(BlogViewSet), name='blogs-list'),
    path('blogs/add/', add_view(BlogViewSet), name='blogs-add'),
    path('blogs/<pk>/', detail_view(BlogViewSet), name='blogs-detail'),

    # Blog Categories
    path('blog-categories/', list_view(BlogCategoryViewSet), name='blog-categories-list'),
    path('blog-categories/add/', add_view(BlogCategoryViewSet), name='blog-categories-add'),
    path('blog-categories/<pk>/', detail_view(BlogCategoryViewSet), name='blog-categories-detail'),

    # Leads
    path('leads/', list_view(LeadViewSet), name='leads-list'),
    path('leads/add/', add_view(LeadViewSet), name='leads-add'),
    path('leads/<pk>/', detail_view(LeadViewSet), name='leads-detail'),

    # Properties
    path('properties/', list_view(PropertyViewSet), name='properties-list'),
    path('properties/add/', add_view(PropertyViewSet), name='properties-add'),
    path('properties/<pk>/', detail_view(PropertyViewSet), name='properties-detail'),

    # Inquiries
    path('inquiries/', list_view(InquiryViewSet), name='inquiries-list'),
    path('inquiries/add/', add_view(InquiryViewSet), name='inquiries-add'),
    path('inquiries/<pk>/', detail_view(InquiryViewSet), name='inquiries-detail'),

    # Packages
    path('packages/', list_view(TravelPackageViewSet), name='packages-list'),
    path('packages/add/', add_view(TravelPackageViewSet), name='packages-add'),
    path('packages/<pk>/', detail_view(TravelPackageViewSet), name='packages-detail'),

    # Destinations
    path('destinations/', list_view(DestinationViewSet), name='destinations-list'),
    path('destinations/add/', add_view(DestinationViewSet), name='destinations-add'),
    path('destinations/<pk>/', detail_view(DestinationViewSet), name='destinations-detail'),

    # Customers
    path('customers/', list_view(CustomerViewSet), name='customers-list'),
    path('customers/add/', add_view(CustomerViewSet), name='customers-add'),
    path('customers/<pk>/', detail_view(CustomerViewSet), name='customers-detail'),

    # Invoices
    path('invoices/', list_view(InvoiceViewSet), name='invoices-list'),
    path('invoices/add/', add_view(InvoiceViewSet), name='invoices-add'),
    path('invoices/<pk>/', detail_view(InvoiceViewSet), name='invoices-detail'),

    # Vouchers
    path('vouchers/', list_view(VoucherViewSet), name='vouchers-list'),
    path('vouchers/add/', add_view(VoucherViewSet), name='vouchers-add'),
    path('vouchers/<pk>/', detail_view(VoucherViewSet), name='vouchers-detail'),

    # Resorts
    path('resorts/', list_view(ResortViewSet), name='resorts-list'),
    path('resorts/add/', add_view(ResortViewSet), name='resorts-add'),
    path('resorts/<pk>/', detail_view(ResortViewSet), name='resorts-detail'),

    # Meals
    path('meals/', list_view(MealViewSet), name='meals-list'),
    path('meals/add/', add_view(MealViewSet), name='meals-add'),
    path('meals/<pk>/', detail_view(MealViewSet), name='meals-detail'),

    # Accounts
    path('accounts/', list_view(AccountViewSet), name='accounts-list'),
    path('accounts/add/', add_view(AccountViewSet), name='accounts-add'),
    path('accounts/<pk>/', detail_view(AccountViewSet), name='accounts-detail'),

    # Employees
    path('employees/', list_view(EmployeeViewSet), name='employees-list'),
    path('employees/add/', add_view(EmployeeViewSet), name='employees-add'),
    path('employees/<pk>/', detail_view(EmployeeViewSet), name='employees-detail'),

    # Feedback
    path('feedback/', list_view(FeedbackViewSet), name='feedback-list'),
    path('feedback/add/', add_view(FeedbackViewSet), name='feedback-add'),
    path('feedback/<pk>/', detail_view(FeedbackViewSet), name='feedback-detail'),

    # Utilities
    path('validate-package-id/<str:package_id>/', validate_package_id, name='validate-package-id'),
    path('get-next-invoice-id/', get_next_invoice_id, name='get-next-invoice-id'),
    path('get-next-voucher-id/', get_next_voucher_id, name='get-next-voucher-id'),
]
