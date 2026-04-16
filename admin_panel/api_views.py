from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
import random

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


@extend_schema_view(
    list=extend_schema(tags=['Customers'], description='List all customers with pagination, search, and ordering'),
    create=extend_schema(tags=['Customers'], description='Create a new customer'),
    retrieve=extend_schema(tags=['Customers'], description='Get customer details by ID'),
    update=extend_schema(tags=['Customers'], description='Update customer (full update)'),
    partial_update=extend_schema(tags=['Customers'], description='Update customer (partial update)'),
    destroy=extend_schema(tags=['Customers'], description='Delete a customer'),
)
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-id')
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'display_name', 'contact_number', 'email']
    ordering_fields = ['id', 'created_at', 'updated_at']


@extend_schema_view(
    list=extend_schema(tags=['Resorts']),
    create=extend_schema(tags=['Resorts']),
    retrieve=extend_schema(tags=['Resorts']),
    update=extend_schema(tags=['Resorts']),
    partial_update=extend_schema(tags=['Resorts']),
    destroy=extend_schema(tags=['Resorts']),
)
class ResortViewSet(viewsets.ModelViewSet):
    queryset = Resort.objects.all().order_by('-id')
    serializer_class = ResortSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['resort_name', 'resort_place', 'city', 'state', 'mobile', 'email']
    ordering_fields = ['id', 'created_at', 'updated_at']


@extend_schema_view(
    list=extend_schema(tags=['Meals']),
    create=extend_schema(tags=['Meals']),
    retrieve=extend_schema(tags=['Meals']),
    update=extend_schema(tags=['Meals']),
    partial_update=extend_schema(tags=['Meals']),
    destroy=extend_schema(tags=['Meals']),
)
class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all().order_by('-id')
    serializer_class = MealSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'created_at', 'updated_at']


@extend_schema_view(
    list=extend_schema(tags=['Accounts']),
    create=extend_schema(tags=['Accounts']),
    retrieve=extend_schema(tags=['Accounts']),
    update=extend_schema(tags=['Accounts']),
    partial_update=extend_schema(tags=['Accounts']),
    destroy=extend_schema(tags=['Accounts']),
)
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('-id')
    serializer_class = AccountSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['account_name', 'account_number', 'bank_name', 'branch_name', 'ifsc_code']
    ordering_fields = ['id', 'created_at', 'updated_at']


@extend_schema_view(
    list=extend_schema(tags=['Invoices']),
    create=extend_schema(tags=['Invoices']),
    retrieve=extend_schema(tags=['Invoices']),
    update=extend_schema(tags=['Invoices']),
    partial_update=extend_schema(tags=['Invoices']),
    destroy=extend_schema(tags=['Invoices']),
)
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-id')
    serializer_class = InvoiceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['invoice_no', 'room_type', 'meals_plan', 'notes']
    ordering_fields = ['id', 'invoice_date', 'checkin_date', 'checkout_date', 'created_at', 'updated_at', 'total']


@extend_schema_view(
    list=extend_schema(tags=['Vouchers']),
    create=extend_schema(tags=['Vouchers']),
    retrieve=extend_schema(tags=['Vouchers']),
    update=extend_schema(tags=['Vouchers']),
    partial_update=extend_schema(tags=['Vouchers']),
    destroy=extend_schema(tags=['Vouchers']),
)
class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all().order_by('-id')
    serializer_class = VoucherSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['voucher_no', 'room_type', 'meals_plan', 'note_for_resort', 'note_for_guest']
    ordering_fields = ['id', 'voucher_date', 'checkin_date', 'checkout_date', 'created_at', 'updated_at', 'total_amount']


@extend_schema_view(
    list=extend_schema(tags=['Leads'], description='List all leads/enquiries with filtering and search'),
    create=extend_schema(tags=['Leads'], description='Create a new lead/enquiry'),
    retrieve=extend_schema(tags=['Leads'], description='Get lead details by ID'),
    update=extend_schema(tags=['Leads'], description='Update lead (full update)'),
    partial_update=extend_schema(tags=['Leads'], description='Update lead (partial update)'),
    destroy=extend_schema(tags=['Leads'], description='Delete a lead'),
)
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


@extend_schema_view(
    list=extend_schema(tags=['Properties']),
    create=extend_schema(tags=['Properties']),
    retrieve=extend_schema(tags=['Properties']),
    update=extend_schema(tags=['Properties']),
    partial_update=extend_schema(tags=['Properties']),
    destroy=extend_schema(tags=['Properties']),
)
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('-id')
    serializer_class = PropertySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'property_type', 'location', 'owner_name', 'owner_contact', 'summary']
    ordering_fields = ['id', 'created_at']


@extend_schema_view(
    list=extend_schema(tags=['Feedbacks']),
    create=extend_schema(tags=['Feedbacks']),
    retrieve=extend_schema(tags=['Feedbacks']),
    update=extend_schema(tags=['Feedbacks']),
    partial_update=extend_schema(tags=['Feedbacks']),
    destroy=extend_schema(tags=['Feedbacks']),
)
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all().order_by('-id')
    serializer_class = FeedbackSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'mobile_number', 'feedback_type', 'feedback']
    ordering_fields = ['id', 'created_at', 'rating']


@extend_schema_view(
    list=extend_schema(tags=['Blogs']),
    create=extend_schema(tags=['Blogs']),
    retrieve=extend_schema(tags=['Blogs']),
    update=extend_schema(tags=['Blogs']),
    partial_update=extend_schema(tags=['Blogs']),
    destroy=extend_schema(tags=['Blogs']),
)
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-id')
    serializer_class = BlogSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'slug', 'excerpt', 'content', 'author_name', 'hashtags', 'tags', 'status']
    ordering_fields = ['id', 'publish_date', 'created_at', 'updated_at', 'reading_time']


@extend_schema_view(
    list=extend_schema(tags=['Destinations']),
    create=extend_schema(tags=['Destinations']),
    retrieve=extend_schema(tags=['Destinations']),
    update=extend_schema(tags=['Destinations']),
    partial_update=extend_schema(tags=['Destinations']),
    destroy=extend_schema(tags=['Destinations']),
)
class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all().order_by('-id')
    serializer_class = DestinationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country', 'category', 'description']
    ordering_fields = ['id', 'created_at', 'packages_start_from']


@extend_schema_view(
    list=extend_schema(tags=['Employees']),
    create=extend_schema(tags=['Employees']),
    retrieve=extend_schema(tags=['Employees']),
    update=extend_schema(tags=['Employees']),
    partial_update=extend_schema(tags=['Employees']),
    destroy=extend_schema(tags=['Employees']),
)
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('-id')
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'phone', 'role', 'department', 'status']
    ordering_fields = ['id', 'join_date', 'salary', 'created_at', 'updated_at']


@extend_schema_view(
    list=extend_schema(tags=['Packages']),
    create=extend_schema(tags=['Packages']),
    retrieve=extend_schema(tags=['Packages']),
    update=extend_schema(tags=['Packages']),
    partial_update=extend_schema(tags=['Packages']),
    destroy=extend_schema(tags=['Packages']),
)
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



# ============================================
# OTP-Based JWT Authentication Views
# ============================================

@extend_schema(
    tags=['Authentication'],
    summary='Request OTP for login',
    description='Step 1: Send email and password to receive OTP via email. OTP is valid for 5 minutes.',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'email': {'type': 'string', 'format': 'email', 'example': 'admin@example.com'},
                'password': {'type': 'string', 'format': 'password', 'example': 'admin123'}
            },
            'required': ['email', 'password']
        }
    },
    responses={
        200: {
            'description': 'OTP sent successfully',
            'content': {
                'application/json': {
                    'example': {
                        'message': 'OTP sent to your registered email',
                        'email': 'admin@example.com',
                        'user_id': 1
                    }
                }
            }
        },
        400: {'description': 'Bad request - missing fields or email not configured'},
        401: {'description': 'Invalid credentials'},
        500: {'description': 'Failed to send OTP email'}
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def request_otp(request):
    """
    Step 1: Request OTP for login
    Send email and password, receive OTP via email
    """
    email = request.data.get('email', '').strip().lower()
    password = request.data.get('password', '')

    if not email or not password:
        return Response(
            {'error': 'Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Find user by email
    user = User.objects.filter(email__iexact=email).first()

    if not user:
        return Response(
            {'error': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Verify password
    if not user.check_password(password):
        return Response(
            {'error': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Check if user has email configured
    if not user.email:
        return Response(
            {'error': 'Email not configured for this account'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Generate OTP
    otp = random.randint(100000, 999999)

    # Store OTP in cache or database (using cache for security)
    from django.core.cache import cache
    cache_key = f'api_otp_{user.id}'
    cache.set(cache_key, str(otp), timeout=300)  # 5 minutes expiry

    # Send OTP email
    try:
        send_mail(
            subject='WhyteHouse API Login OTP',
            message=f'Your OTP for API login is: {otp}\n\nThis OTP will expire in 5 minutes.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to send OTP: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response({
        'message': 'OTP sent to your registered email',
        'email': user.email,
        'user_id': user.id
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Authentication'],
    summary='Verify OTP and get JWT tokens',
    description='Step 2: Verify the OTP received via email and get access & refresh tokens.',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'user_id': {'type': 'integer', 'example': 1},
                'otp': {'type': 'string', 'example': '123456'}
            },
            'required': ['user_id', 'otp']
        }
    },
    responses={
        200: {
            'description': 'Login successful - returns JWT tokens',
            'content': {
                'application/json': {
                    'example': {
                        'message': 'Login successful',
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                        'user': {
                            'id': 1,
                            'username': 'admin',
                            'email': 'admin@example.com',
                            'first_name': 'Admin',
                            'last_name': 'User'
                        }
                    }
                }
            }
        },
        400: {'description': 'Bad request - missing fields or OTP expired'},
        401: {'description': 'Invalid OTP'},
        404: {'description': 'User not found'}
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp_and_login(request):
    """
    Step 2: Verify OTP and get JWT tokens
    Send user_id and OTP, receive access and refresh tokens
    """
    user_id = request.data.get('user_id')
    otp = request.data.get('otp')
    
    # Convert OTP to string and strip whitespace
    if otp is not None:
        otp = str(otp).strip()
    
    if not user_id or not otp:
        return Response(
            {'error': 'user_id and otp are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get stored OTP from cache
    from django.core.cache import cache
    cache_key = f'api_otp_{user_id}'
    stored_otp = cache.get(cache_key)

    if not stored_otp:
        return Response(
            {'error': 'OTP expired or not found. Please request a new OTP'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Verify OTP
    if otp != stored_otp:
        return Response(
            {'error': 'Invalid OTP'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Get user
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Delete OTP from cache after successful verification
    cache.delete(cache_key)

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response({
        'message': 'Login successful',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Authentication'],
    summary='Resend OTP',
    description='Resend OTP to user email if the previous one expired or was not received.',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'user_id': {'type': 'integer', 'example': 1}
            },
            'required': ['user_id']
        }
    },
    responses={
        200: {
            'description': 'OTP resent successfully',
            'content': {
                'application/json': {
                    'example': {
                        'message': 'OTP resent to your registered email',
                        'email': 'admin@example.com'
                    }
                }
            }
        },
        400: {'description': 'Bad request - missing user_id or email not configured'},
        404: {'description': 'User not found'},
        500: {'description': 'Failed to send OTP email'}
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def resend_otp(request):
    """
    Resend OTP to user's email
    """
    user_id = request.data.get('user_id')

    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get user
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if not user.email:
        return Response(
            {'error': 'Email not configured for this account'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Generate new OTP
    otp = random.randint(100000, 999999)

    # Store OTP in cache
    from django.core.cache import cache
    cache_key = f'api_otp_{user.id}'
    cache.set(cache_key, str(otp), timeout=300)  # 5 minutes expiry

    # Send OTP email
    try:
        send_mail(
            subject='WhyteHouse API Login OTP - Resent',
            message=f'Your new OTP for API login is: {otp}\n\nThis OTP will expire in 5 minutes.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to send OTP: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response({
        'message': 'OTP resent to your registered email',
        'email': user.email
    }, status=status.HTTP_200_OK)
