from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
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



# ============================================
# OTP-Based JWT Authentication Views
# ============================================

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


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp_and_login(request):
    """
    Step 2: Verify OTP and get JWT tokens
    Send user_id and OTP, receive access and refresh tokens
    """
    user_id = request.data.get('user_id')
    otp = request.data.get('otp', '').strip()

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
