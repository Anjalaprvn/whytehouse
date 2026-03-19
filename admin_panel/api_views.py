from django.db.models import Q, Sum
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer


class CustomerBrowsableAPIRenderer(BrowsableAPIRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        ret = super().render(data, accepted_media_type, renderer_context)
        if isinstance(ret, bytes):
            ret = ret.decode('utf-8')
        script = """
        <script>
        document.addEventListener('DOMContentLoaded', function () {
            var contact = document.querySelector('input[name="contact_number"]');
            var whatsapp = document.querySelector('input[name="whatsapp_number"]');
            var checkbox = document.querySelector('input[name="same_as_whatsapp"]');
            if (!contact || !whatsapp || !checkbox) return;
            function sync() {
                if (checkbox.checked) {
                    whatsapp.value = contact.value;
                    whatsapp.setAttribute('readonly', 'readonly');
                    whatsapp.style.opacity = '0.6';
                } else {
                    whatsapp.removeAttribute('readonly');
                    whatsapp.style.opacity = '1';
                }
            }
            checkbox.addEventListener('change', sync);
            contact.addEventListener('input', function () {
                if (checkbox.checked) whatsapp.value = contact.value;
            });
        });
        </script>
        """
        return (ret + script).encode('utf-8')

from .models import (
    Blog,
    BlogCategory,
    BlogImage,
    Lead,
    Property,
    TravelPackage,
    Destination,
    Customer,
    Meal,
    Account,
    Inquiry,
    Employee,
    Resort,
    Voucher,
    Invoice,
    Feedback,
    FeedbackImage,
)

from .serializers import (
    BlogSerializer,
    BlogListSerializer,
    BlogCategorySerializer,
    BlogImageSerializer,
    LeadSerializer,
    PropertySerializer,
    TravelPackageSerializer,
    TravelPackageListSerializer,
    DestinationSerializer,
    CustomerSerializer,
    MealSerializer,
    AccountSerializer,
    InquirySerializer,
    EmployeeSerializer,
    ResortSerializer,
    VoucherSerializer,
    InvoiceSerializer,
    FeedbackSerializer,
    FeedbackImageSerializer,
)


# ==================== BLOG CATEGORY VIEWSET ====================
class BlogCategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    serializer_class = BlogCategorySerializer
    queryset = BlogCategory.objects.all().order_by("order", "name")

    def get_queryset(self):
        qs = super().get_queryset()

        is_active = (self.request.query_params.get("is_active") or "").strip().lower()
        if is_active == "true":
            qs = qs.filter(is_active=True)
        elif is_active == "false":
            qs = qs.filter(is_active=False)

        search_query = (self.request.query_params.get("search") or "").strip()
        if search_query:
            qs = qs.filter(
                Q(name__icontains=search_query) |
                Q(slug__icontains=search_query)
            )

        return qs

    @action(detail=False, methods=["get"])
    def active(self, request):
        categories = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def blogs(self, request, pk=None):
        category = self.get_object()
        blogs = Blog.objects.filter(
            status="published",
            category=category
        ).order_by("-publish_date")
        serializer = BlogListSerializer(blogs, many=True, context={"request": request})
        return Response(serializer.data)


# ==================== BLOG VIEWSET ====================
class BlogViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Blog.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "list":
            return BlogListSerializer
        return BlogSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        search_query = (self.request.query_params.get("search") or "").strip()
        if search_query:
            qs = qs.filter(
                Q(title__icontains=search_query) |
                Q(author_name__icontains=search_query) |
                Q(slug__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query)
            )

        status_filter = (self.request.query_params.get("status") or "").strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        category_filter = (self.request.query_params.get("category") or "").strip()
        if category_filter:
            qs = qs.filter(category_id=category_filter)

        package_id = (self.request.query_params.get("package_id") or "").strip()
        if package_id:
            qs = qs.filter(package_id=package_id)

        return qs

    def perform_create(self, serializer):
        hashtags_value = (self.request.data.get("hashtags") or "").strip()
        tags_value = (self.request.data.get("tags") or "").strip()
        serializer.save(
            hashtags=hashtags_value,
            tags=tags_value or hashtags_value
        )

    def perform_update(self, serializer):
        hashtags_value = (self.request.data.get("hashtags") or "").strip()
        tags_value = (self.request.data.get("tags") or "").strip()
        serializer.save(
            hashtags=hashtags_value,
            tags=tags_value or hashtags_value
        )

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "published_count": qs.filter(status="published").count(),
            "draft_count": qs.filter(status="draft").count(),
            "scheduled_count": qs.filter(status="scheduled").count(),
            "total": qs.count(),
        })

    @action(detail=False, methods=["get"])
    def published(self, request):
        blogs = self.get_queryset().filter(status="published").order_by("-publish_date")
        serializer = self.get_serializer(blogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        categories = BlogCategory.objects.filter(is_active=True).order_by("order", "name")
        result = {}

        for cat in categories:
            blogs = Blog.objects.filter(
                status="published",
                category=cat
            ).order_by("-publish_date")[:6]

            result[cat.slug] = BlogListSerializer(
                blogs,
                many=True,
                context={"request": request}
            ).data

        return Response(result)


# ==================== LEAD VIEWSET ====================
class LeadViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = LeadSerializer
    queryset = Lead.objects.all().order_by("-created_at")

    def get_queryset(self):
        qs = super().get_queryset()

        enquiry_type = (self.request.query_params.get("enquiry_type") or "").strip()
        source = (self.request.query_params.get("source") or "").strip()
        employee = (self.request.query_params.get("employee") or "").strip()
        search = (self.request.query_params.get("search") or "").strip()
       

        if enquiry_type:
            qs = qs.filter(enquiry_type=enquiry_type)

        if source:
            qs = qs.filter(source=source)

        if employee:
            qs = qs.filter(employee_id=employee)

        if search:
            qs = qs.filter(
                Q(full_name__icontains=search) |
                Q(mobile_number__icontains=search) |
                Q(place__icontains=search) |
                Q(remarks__icontains=search)
            )

        return qs

# ==================== PROPERTY VIEWSET ====================
class PropertyViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Property.objects.all().order_by("-created_at")
    serializer_class = PropertySerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        ptype = (self.request.query_params.get("property_type") or "").strip()
        location = (self.request.query_params.get("location") or "").strip()
        is_active = (self.request.query_params.get("is_active") or "").strip().lower()
        search = (self.request.query_params.get("search") or "").strip()

        if ptype:
            qs = qs.filter(property_type=ptype)

        if location:
            qs = qs.filter(location__icontains=location)

        if is_active == "true":
            qs = qs.filter(is_active=True)
        elif is_active == "false":
            qs = qs.filter(is_active=False)

        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(location__icontains=search) |
                Q(address__icontains=search) |
                Q(summary__icontains=search) |
                Q(owner_name__icontains=search) |
                Q(owner_contact__icontains=search) |
                Q(amenities__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def active(self, request):
        properties = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)


# ==================== DESTINATION VIEWSET ====================
class DestinationViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Destination.objects.all().order_by("-created_at")
    serializer_class = DestinationSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        category = (self.request.query_params.get("category") or "").strip()
        if category:
            qs = qs.filter(category=category)

        is_popular = (self.request.query_params.get("is_popular") or "").strip().lower()
        if is_popular == "true":
            qs = qs.filter(is_popular=True)
        elif is_popular == "false":
            qs = qs.filter(is_popular=False)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(country__icontains=search) |
                Q(description__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "domestic_count": qs.filter(category="Domestic").count(),
            "international_count": qs.filter(category="International").count(),
            "popular_count": qs.filter(is_popular=True).count(),
        })

    @action(detail=True, methods=["get"])
    def packages(self, request, pk=None):
        destination = self.get_object()
        packages = destination.packages.filter(active=True)
        serializer = TravelPackageListSerializer(
            packages, many=True, context={"request": request}
        )
        return Response(serializer.data)


# ==================== TRAVEL PACKAGE VIEWSET ====================
class TravelPackageViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = TravelPackage.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "list":
            return TravelPackageListSerializer
        return TravelPackageSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        category = (self.request.query_params.get("category") or "").strip()
        if category:
            qs = qs.filter(category=category)

        active = (self.request.query_params.get("active") or "").strip().lower()
        if active == "true":
            qs = qs.filter(active=True)
        elif active == "false":
            qs = qs.filter(active=False)

        destination_id = (self.request.query_params.get("destination") or "").strip()
        if destination_id:
            qs = qs.filter(destination_id=destination_id)

        country = (self.request.query_params.get("country") or "").strip()
        if country:
            qs = qs.filter(country__icontains=country)

        package_id = (self.request.query_params.get("package_id") or "").strip()
        if package_id:
            qs = qs.filter(package_id=package_id)

        min_price = (self.request.query_params.get("min_price") or "").strip()
        max_price = (self.request.query_params.get("max_price") or "").strip()

        if min_price:
            try:
                qs = qs.filter(price__gte=float(min_price))
            except ValueError:
                pass

        if max_price:
            try:
                qs = qs.filter(price__lte=float(max_price))
            except ValueError:
                pass

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(package_id__icontains=search) |
                Q(location__icontains=search) |
                Q(country__icontains=search) |
                Q(description__icontains=search) |
                Q(itinerary__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "active_count": qs.filter(active=True).count(),
            "inactive_count": qs.filter(active=False).count(),
            "domestic_count": qs.filter(category="Domestic").count(),
            "international_count": qs.filter(category="International").count(),
        })

    @action(detail=False, methods=["get"])
    def featured(self, request):
        packages = self.get_queryset().filter(active=True)[:6]
        serializer = self.get_serializer(packages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        domestic = self.get_queryset().filter(category="Domestic", active=True)[:6]
        international = self.get_queryset().filter(category="International", active=True)[:6]

        return Response({
            "domestic": TravelPackageListSerializer(
                domestic, many=True, context={"request": request}
            ).data,
            "international": TravelPackageListSerializer(
                international, many=True, context={"request": request}
            ).data,
        })


# ==================== CUSTOMER VIEWSET ====================
class CustomerViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Customer.objects.all().order_by("-created_at")
    serializer_class = CustomerSerializer
    renderer_classes = [JSONRenderer, CustomerBrowsableAPIRenderer]

    def get_queryset(self):
        qs = super().get_queryset()

        customer_type = (self.request.query_params.get("customer_type") or "").strip()
        if customer_type:
            qs = qs.filter(customer_type=customer_type)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(display_name__icontains=search) |
                Q(contact_number__icontains=search) |
                Q(email__icontains=search) |
                Q(place__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "individual_count": qs.filter(customer_type="Individual").count(),
            "corporate_count": qs.filter(customer_type="Corporate").count(),
            "government_count": qs.filter(customer_type="Government").count(),
        })


class MealBrowsableAPIRenderer(BrowsableAPIRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        ret = super().render(data, accepted_media_type, renderer_context)
        if isinstance(ret, bytes):
            ret = ret.decode('utf-8')
        script = """
        <script>
        document.addEventListener('DOMContentLoaded', function () {
            document.querySelectorAll('form input:not([type=hidden]):not([type=submit]):not([type=button]), form textarea, form select').forEach(function(el) {
                if (el.tagName === 'SELECT') {
                    el.selectedIndex = 0;
                } else {
                    el.value = '';
                }
            });
            document.querySelectorAll('.alert').forEach(function(el) {
                el.style.display = 'none';
            });
        });
        </script>
        """
        return (ret + script).encode('utf-8')


# ==================== MEAL VIEWSET ====================
class MealViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Meal.objects.all().order_by("-created_at")
    serializer_class = MealSerializer
    renderer_classes = [JSONRenderer, MealBrowsableAPIRenderer]

    def get_queryset(self):
        qs = super().get_queryset()

        status_filter = (self.request.query_params.get("status") or "").strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(included_meals__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "available_count": qs.filter(status="Available").count(),
            "unavailable_count": qs.filter(status="Unavailable").count(),
        })


# ==================== ACCOUNT VIEWSET ====================
class AccountViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Account.objects.all().order_by("-created_at")
    serializer_class = AccountSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        account_type = (self.request.query_params.get("account_type") or "").strip()
        if account_type:
            qs = qs.filter(account_type=account_type)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(account_name__icontains=search) |
                Q(bank_name__icontains=search) |
                Q(account_number__icontains=search) |
                Q(ifsc_code__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
        })


# ==================== INQUIRY VIEWSET ====================
class InquiryViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Inquiry.objects.all().order_by("-created_at")
    serializer_class = InquirySerializer

    def get_queryset(self):
        qs = super().get_queryset()

        status_filter = (self.request.query_params.get("status") or "").strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search) |
                Q(package__icontains=search) |
                Q(message__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "new_count": qs.filter(status="New").count(),
            "contacted_count": qs.filter(status="Contacted").count(),
            "converted_count": qs.filter(status="Converted").count(),
            "junk_count": qs.filter(status="Junk").count(),
        })


# ==================== EMPLOYEE VIEWSET ====================
class EmployeeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Employee.objects.all().order_by("-created_at")
    serializer_class = EmployeeSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        status_filter = (self.request.query_params.get("status") or "").strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        role = (self.request.query_params.get("role") or "").strip()
        if role:
            qs = qs.filter(role__icontains=role)

        department = (self.request.query_params.get("department") or "").strip()
        if department:
            qs = qs.filter(department__icontains=department)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search) |
                Q(role__icontains=search) |
                Q(department__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "active_count": qs.filter(status="Active").count(),
            "inactive_count": qs.filter(status="Inactive").count(),
            "on_leave_count": qs.filter(status="On Leave").count(),
        })


# ==================== RESORT VIEWSET ====================
class ResortViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Resort.objects.all().order_by("-created_at")
    serializer_class = ResortSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        status_filter = (self.request.query_params.get("status") or "").strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        location = (self.request.query_params.get("location") or "").strip()
        if location:
            qs = qs.filter(location__icontains=location)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(resort_name__icontains=search) |
                Q(location__icontains=search) |
                Q(contact_person__icontains=search) |
                Q(email__icontains=search) |
                Q(address__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "active_count": qs.filter(status="Active").count(),
            "inactive_count": qs.filter(status="Inactive").count(),
        })


# ==================== VOUCHER VIEWSET ====================
class VoucherViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Voucher.objects.all().order_by("-created_at")
    serializer_class = VoucherSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        customer_id = (self.request.query_params.get("customer") or "").strip()
        if customer_id:
            qs = qs.filter(customer_id=customer_id)

        resort_id = (self.request.query_params.get("resort") or "").strip()
        if resort_id:
            qs = qs.filter(resort_id=resort_id)

        sales_person_id = (self.request.query_params.get("sales_person") or "").strip()
        if sales_person_id:
            qs = qs.filter(sales_person_id=sales_person_id)

        check_in = (self.request.query_params.get("checkin_date") or "").strip()
        if check_in:
            qs = qs.filter(checkin_date__gte=check_in)

        check_out = (self.request.query_params.get("checkout_date") or "").strip()
        if check_out:
            qs = qs.filter(checkout_date__lte=check_out)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(voucher_no__icontains=search) |
                Q(customer__display_name__icontains=search) |
                Q(resort__resort_name__icontains=search) |
                Q(sales_person__name__icontains=search) |
                Q(room_type__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        total_amount = qs.aggregate(total=Sum("total_amount"))["total"] or 0
        received_amount = qs.aggregate(total=Sum("received"))["total"] or 0
        pending_amount = qs.aggregate(total=Sum("pending"))["total"] or 0
        profit_amount = qs.aggregate(total=Sum("profit"))["total"] or 0

        return Response({
            "total": qs.count(),
            "total_amount": float(total_amount),
            "received_amount": float(received_amount),
            "pending_amount": float(pending_amount),
            "profit_amount": float(profit_amount),
        })


# ==================== INVOICE VIEWSET ====================
class InvoiceViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Invoice.objects.all().order_by("-created_at")
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        customer_id = (self.request.query_params.get("customer") or "").strip()
        if customer_id:
            qs = qs.filter(customer_id=customer_id)

        resort_id = (self.request.query_params.get("resort") or "").strip()
        if resort_id:
            qs = qs.filter(resort_id=resort_id)

        sales_person_id = (self.request.query_params.get("sales_person") or "").strip()
        if sales_person_id:
            qs = qs.filter(sales_person_id=sales_person_id)

        date_from = (self.request.query_params.get("date_from") or "").strip()
        if date_from:
            qs = qs.filter(invoice_date__gte=date_from)

        date_to = (self.request.query_params.get("date_to") or "").strip()
        if date_to:
            qs = qs.filter(invoice_date__lte=date_to)

        search = (self.request.query_params.get("search") or "").strip()
        if search:
            qs = qs.filter(
                Q(invoice_no__icontains=search) |
                Q(customer__display_name__icontains=search) |
                Q(resort__resort_name__icontains=search) |
                Q(sales_person__name__icontains=search) |
                Q(room_type__icontains=search)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        total_val = qs.aggregate(total=Sum("total"))["total"] or 0
        paid_val = qs.aggregate(total=Sum("received"))["total"] or 0
        pending_val = qs.aggregate(total=Sum("pending"))["total"] or 0
        profit_val = qs.aggregate(total=Sum("profit"))["total"] or 0

        return Response({
            "total": qs.count(),
            "total_amount": float(total_val),
            "received_amount": float(paid_val),
            "pending_amount": float(pending_val),
            "profit_amount": float(profit_val),
        })

    @action(detail=False, methods=["get"])
    def pending(self, request):
        invoices = self.get_queryset().filter(pending__gt=0)
        serializer = self.get_serializer(invoices, many=True)
        return Response(serializer.data)


# ==================== FEEDBACK VIEWSET ====================
class FeedbackViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all().prefetch_related("images").order_by("-created_at")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve", "featured"]:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        qs = super().get_queryset()

        feedback_type = (self.request.query_params.get("feedback_type") or "").strip()
        if feedback_type:
            qs = qs.filter(feedback_type=feedback_type)

        featured = (self.request.query_params.get("featured") or "").strip().lower()
        if featured == "true":
            qs = qs.filter(featured=True)
        elif featured == "false":
            qs = qs.filter(featured=False)

        rating = (self.request.query_params.get("rating") or "").strip()
        if rating:
            try:
                qs = qs.filter(rating=int(rating))
            except ValueError:
                pass

        return qs

    @action(detail=False, methods=["get"], url_path="featured", permission_classes=[permissions.AllowAny])
    def featured(self, request):
        qs = Feedback.objects.filter(featured=True).prefetch_related("images").order_by("-created_at")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "total": qs.count(),
            "featured_count": qs.filter(featured=True).count(),
            "five_star_count": qs.filter(rating=5).count(),
        })


# ==================== BLOG IMAGE VIEWSET ====================
class BlogImageViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = BlogImage.objects.all().order_by("order")
    serializer_class = BlogImageSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        blog_id = (self.request.query_params.get("blog") or "").strip()
        if blog_id:
            qs = qs.filter(blog_id=blog_id)
        return qs


# ==================== FEEDBACK IMAGE VIEWSET ====================
class FeedbackImageViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = FeedbackImage.objects.all().order_by("-uploaded_at")
    serializer_class = FeedbackImageSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        feedback_id = (self.request.query_params.get("feedback") or "").strip()
        if feedback_id:
            qs = qs.filter(feedback_id=feedback_id)
        return qs


# ==================== BLOG TITLE/SLUG VALIDATION ENDPOINTS ====================
@api_view(["GET"])
def validate_blog_title(request):
    title = (request.query_params.get("title") or "").strip()
    exists = Blog.objects.filter(title__iexact=title).exists() if title else False
    return Response({"exists": exists})


@api_view(["GET"])
def validate_blog_slug(request):
    slug = (request.query_params.get("slug") or "").strip()
    exists = Blog.objects.filter(slug=slug).exists() if slug else False
    return Response({"exists": exists})


# ==================== PACKAGE ID VALIDATION ENDPOINT ====================
@api_view(["GET"])
def validate_package_id(request, package_id):
    package_id = package_id.strip().upper()
    exists = TravelPackage.objects.filter(package_id=package_id).exists()

    return Response({
        "package_id": package_id,
        "exists": exists
    })


# ==================== INVOICE ID GENERATION ENDPOINT ====================
@api_view(["GET"])
def get_next_invoice_id(request):
    last_invoice = Invoice.objects.filter(invoice_no__startswith="INV").order_by("-invoice_no").first()

    if last_invoice and last_invoice.invoice_no:
        try:
            last_num = int(last_invoice.invoice_no[3:])
            next_id = f"INV{str(last_num + 1).zfill(3)}"
        except (ValueError, IndexError):
            next_id = "INV001"
    else:
        next_id = "INV001"

    return Response({"next_id": next_id})


# ==================== VOUCHER ID GENERATION ENDPOINT ====================
@api_view(["GET"])
def get_next_voucher_id(request):
    last_voucher = Voucher.objects.filter(voucher_no__startswith="VCH").order_by("-voucher_no").first()

    if last_voucher and last_voucher.voucher_no:
        try:
            last_num = int(last_voucher.voucher_no[3:])
            next_id = f"VCH{str(last_num + 1).zfill(3)}"
        except (ValueError, IndexError):
            next_id = "VCH001"
    else:
        next_id = "VCH001"

    return Response({"next_id": next_id})
