from rest_framework import viewsets, filters

from .models import (
    Customer,
    Resort,
    Meal,
    Account,
    Invoice,
    Voucher,
    Lead,
    Property,
    Feedback,
    Blog,
    Destination,
    Employee,
    TravelPackage,
)

from .serializers import (
    CustomerSerializer,
    ResortSerializer,
    MealSerializer,
    AccountSerializer,
    InvoiceSerializer,
    VoucherSerializer,
    LeadSerializer,
    PropertySerializer,
    FeedbackSerializer,
    BlogSerializer,
    DestinationSerializer,
    EmployeeSerializer,
    TravelPackageSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-id')
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'display_name', 'contact_number', 'email']
    ordering_fields = ['id', 'created_at', 'updated_at']


class ResortViewSet(viewsets.ModelViewSet):
    queryset = Resort.objects.all().order_by('-id')
    serializer_class = ResortSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['resort_name', 'resort_place', 'city', 'state', 'mobile', 'email']
    ordering_fields = ['id', 'created_at', 'updated_at']


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all().order_by('-id')
    serializer_class = MealSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'created_at', 'updated_at']


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('-id')
    serializer_class = AccountSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['account_name', 'account_number', 'bank_name', 'branch_name', 'ifsc_code']
    ordering_fields = ['id', 'created_at', 'updated_at']


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-id')
    serializer_class = InvoiceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['invoice_no', 'room_type', 'meals_plan', 'notes']
    ordering_fields = ['id', 'invoice_date', 'checkin_date', 'checkout_date', 'created_at', 'updated_at', 'total']


class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all().order_by('-id')
    serializer_class = VoucherSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['voucher_no', 'room_type', 'meals_plan', 'note_for_resort', 'note_for_guest']
    ordering_fields = ['id', 'voucher_date', 'checkin_date', 'checkout_date', 'created_at', 'updated_at', 'total_amount']


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by('-id')
    serializer_class = LeadSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'full_name',
        'mobile_number',
        'alternate_number',
        'place',
        'email',
        'package_name',
        'property_name',
        'source',
        'enquiry_type',
        'status',
        'remarks',
    ]
    ordering_fields = ['id', 'created_at', 'updated_at']


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('-id')
    serializer_class = PropertySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'property_type', 'location', 'owner_name', 'owner_contact', 'summary']
    ordering_fields = ['id', 'created_at']


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all().order_by('-id')
    serializer_class = FeedbackSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'mobile_number', 'feedback_type', 'feedback']
    ordering_fields = ['id', 'created_at', 'rating']


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-id')
    serializer_class = BlogSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'slug', 'excerpt', 'content', 'author_name', 'hashtags', 'tags', 'status']
    ordering_fields = ['id', 'publish_date', 'created_at', 'updated_at', 'reading_time']


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all().order_by('-id')
    serializer_class = DestinationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country', 'category', 'description']
    ordering_fields = ['id', 'created_at', 'packages_start_from']


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('-id')
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'phone', 'role', 'department', 'status']
    ordering_fields = ['id', 'join_date', 'salary', 'created_at', 'updated_at']


class TravelPackageViewSet(viewsets.ModelViewSet):
    queryset = TravelPackage.objects.all().order_by('-id')
    serializer_class = TravelPackageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'package_id',
        'name',
        'category',
        'destination',
        'location',
        'country',
        'description',
        'price_type',
        'meta_title',
        'meta_description',
    ]
    ordering_fields = ['id', 'price', 'adult_price', 'created_at']