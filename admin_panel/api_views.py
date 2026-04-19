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



# ============================================
# Dashboard Statistics API
# ============================================

@extend_schema(
    tags=['Dashboard'],
    summary='Get dashboard statistics',
    description='Returns comprehensive dashboard statistics including counts, recent items, and upcoming bookings. Supports pagination for lists.',
    parameters=[
        OpenApiParameter(
            name='upcoming_limit',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Number of upcoming bookings to return (default: 10, max: 50)',
            required=False,
        ),
        OpenApiParameter(
            name='invoices_limit',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Number of recent invoices to return (default: 10, max: 50)',
            required=False,
        ),
        OpenApiParameter(
            name='leads_limit',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Number of recent leads to return (default: 10, max: 50)',
            required=False,
        ),
    ],
    responses={
        200: {
            'description': 'Dashboard statistics retrieved successfully',
            'content': {
                'application/json': {
                    'example': {
                        'statistics': {
                            'total_bookings': 0,
                            'total_vouchers': 0,
                            'total_invoices': 15,
                            'total_profit': 50000,
                            'new_leads': 6,
                            'total_customers': 6,
                            'avg_feedback_rating': 3.9,
                            'total_blogs': 3,
                            'international_packages': 10,
                            'domestic_packages': 8,
                            'hospitality_properties': 8
                        },
                        'upcoming_bookings': {
                            'count': 2,
                            'results': [
                                {
                                    'id': 1,
                                    'invoice_no': 'INV001',
                                    'customer_name': 'John Doe',
                                    'resort_name': 'Paradise Resort',
                                    'checkin_date': '2026-05-01',
                                    'checkout_date': '2026-05-05',
                                    'total': 47500
                                }
                            ]
                        },
                        'recent_invoices': {
                            'count': 5,
                            'results': []
                        },
                        'recent_leads': {
                            'count': 5,
                            'results': []
                        }
                    }
                }
            }
        }
    }
)
@api_view(['GET'])
def dashboard_statistics(request):
    """
    Get comprehensive dashboard statistics with pagination support
    """
    from django.db.models import Sum, Avg
    from django.utils import timezone
    from datetime import timedelta
    
    # Get pagination limits from query parameters (default: 10, max: 50)
    upcoming_limit = min(int(request.GET.get('upcoming_limit', 10)), 50)
    invoices_limit = min(int(request.GET.get('invoices_limit', 10)), 50)
    leads_limit = min(int(request.GET.get('leads_limit', 10)), 50)
    
    # Calculate statistics
    total_invoices = Invoice.objects.count()
    total_vouchers = Voucher.objects.count()
    total_profit = Invoice.objects.aggregate(Sum('profit'))['profit__sum'] or 0
    new_leads_count = Lead.objects.filter(created_at__gte=timezone.now() - timedelta(days=30)).count()
    total_customers = Customer.objects.count()
    
    # Feedback statistics
    avg_feedback_raw = Feedback.objects.aggregate(Avg('rating'))['rating__avg']
    avg_feedback = round(avg_feedback_raw, 1) if avg_feedback_raw else 0
    
    # Content statistics
    total_blogs = Blog.objects.count()
    international_packages = TravelPackage.objects.filter(category='International').count()
    domestic_packages = TravelPackage.objects.filter(category='Domestic').count()
    total_properties = Property.objects.count()
    
    # Upcoming bookings (invoices with future check-in dates)
    upcoming_bookings_queryset = Invoice.objects.filter(
        checkin_date__gte=timezone.now().date()
    ).select_related('customer', 'resort').order_by('checkin_date')
    
    upcoming_bookings_count = upcoming_bookings_queryset.count()
    upcoming_bookings = upcoming_bookings_queryset[:upcoming_limit]
    
    upcoming_bookings_data = [
        {
            'id': booking.id,
            'invoice_no': booking.invoice_no,
            'customer_name': booking.customer.display_name if booking.customer else 'N/A',
            'resort_name': booking.resort.resort_name if booking.resort else 'N/A',
            'checkin_date': booking.checkin_date,
            'checkout_date': booking.checkout_date,
            'checkin_time': booking.checkin_time,
            'checkout_time': booking.checkout_time,
            'total': float(booking.total) if booking.total else 0,
            'nights': booking.nights,
            'rooms': booking.rooms,
            'adults': booking.adults,
            'children': booking.children,
        }
        for booking in upcoming_bookings
    ]
    
    # Recent invoices
    recent_invoices_queryset = Invoice.objects.select_related('customer').order_by('-created_at')
    recent_invoices_count = recent_invoices_queryset.count()
    recent_invoices = recent_invoices_queryset[:invoices_limit]
    
    recent_invoices_data = [
        {
            'id': invoice.id,
            'invoice_no': invoice.invoice_no,
            'customer_name': invoice.customer.display_name if invoice.customer else 'N/A',
            'invoice_date': invoice.invoice_date,
            'created_at': invoice.created_at,
            'total': float(invoice.total) if invoice.total else 0,
            'received': float(invoice.received) if invoice.received else 0,
            'pending': float(invoice.pending) if invoice.pending else 0,
            'profit': float(invoice.profit) if invoice.profit else 0,
        }
        for invoice in recent_invoices
    ]
    
    # Recent leads
    recent_leads_queryset = Lead.objects.order_by('-created_at')
    recent_leads_count = recent_leads_queryset.count()
    recent_leads = recent_leads_queryset[:leads_limit]
    
    recent_leads_data = [
        {
            'id': lead.id,
            'full_name': lead.full_name,
            'mobile_number': lead.mobile_number,
            'alternate_number': lead.alternate_number,
            'place': lead.place,
            'email': lead.email,
            'enquiry_type': lead.enquiry_type,
            'status': lead.status,
            'is_viewed': lead.is_viewed,
            'source': lead.source,
            'created_at': lead.created_at,
        }
        for lead in recent_leads
    ]
    
    return Response({
        'statistics': {
            'total_bookings': 0,  # You can add booking model count if you have it
            'total_vouchers': total_vouchers,
            'total_invoices': total_invoices,
            'total_profit': float(total_profit),
            'new_leads': new_leads_count,
            'total_customers': total_customers,
            'avg_feedback_rating': avg_feedback,
            'total_blogs': total_blogs,
            'international_packages': international_packages,
            'domestic_packages': domestic_packages,
            'hospitality_properties': total_properties,
        },
        'upcoming_bookings': {
            'count': upcoming_bookings_count,
            'limit': upcoming_limit,
            'results': upcoming_bookings_data,
        },
        'recent_invoices': {
            'count': recent_invoices_count,
            'limit': invoices_limit,
            'results': recent_invoices_data,
        },
        'recent_leads': {
            'count': recent_leads_count,
            'limit': leads_limit,
            'results': recent_leads_data,
        },
    }, status=status.HTTP_200_OK)
