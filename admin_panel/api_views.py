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
        serializer.save(hashtags=hashtags_value)

    def perform_update(self, serializer):
        hashtags_value = (self.request.data.get("hashtags") or "").strip()
        serializer.save(hashtags=hashtags_value)

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


# ==================== ACCOUNT BROWSABLE API RENDERER ====================
class AccountBrowsableAPIRenderer(BrowsableAPIRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        ret = super().render(data, accepted_media_type, renderer_context)
        if isinstance(ret, bytes):
            ret = ret.decode('utf-8')
        script = """
        <style>.acct-err{color:#d13b3b;font-size:12px;margin-top:4px;}</style>
        <script>
        document.addEventListener('DOMContentLoaded', function () {
            var nameInput   = document.querySelector('input[name="account_name"]');
            var numInput    = document.querySelector('input[name="account_number"]');
            var bankInput   = document.querySelector('input[name="bank_name"]');
            var branchInput = document.querySelector('input[name="branch_name"]');
            var ifscInput   = document.querySelector('input[name="ifsc_code"]');
            var typeSelect  = document.querySelector('select[name="account_type"]');
            if (!nameInput) return;

            function getOrCreateErr(input) {
                var err = input.parentElement.querySelector('.acct-err');
                if (!err) {
                    err = document.createElement('div');
                    err.className = 'acct-err';
                    input.parentElement.appendChild(err);
                }
                return err;
            }
            function showErr(input, msg) {
                getOrCreateErr(input).textContent = msg;
                input.style.borderColor = msg ? '#d13b3b' : '';
            }
            function clearErr(input) { showErr(input, ''); }

            // letters + spaces only
            function liveLetters(input, label) {
                var v = input.value.trim();
                if (!v) { clearErr(input); return; }
                if (!/^[A-Za-z\s]+$/.test(v)) showErr(input, label + ' must contain letters only.');
                else clearErr(input);
            }

            // digits only
            function liveDigits(input, label) {
                var v = input.value.trim();
                if (!v) { clearErr(input); return; }
                if (!/^\d+$/.test(v)) showErr(input, label + ' must contain digits only.');
                else clearErr(input);
            }

            // IFSC: alphanumeric, auto-uppercase
            function liveIFSC(input) {
                input.value = input.value.toUpperCase();
                var v = input.value.trim();
                if (!v) { clearErr(input); return; }
                if (!/^[A-Z0-9]+$/.test(v)) showErr(input, 'IFSC Code must be alphanumeric only.');
                else clearErr(input);
            }

            // AJAX duplicate check on account number
            var dupTimer, isDuplicate = false;
            numInput.addEventListener('input', function() {
                liveDigits(this, 'Account Number');
                isDuplicate = false;
                clearTimeout(dupTimer);
                var v = this.value.trim();
                if (!v || !/^\d+$/.test(v)) return;
                dupTimer = setTimeout(function() {
                    fetch('/sales/accounts/check-number/?number=' + encodeURIComponent(v))
                        .then(function(r){ return r.json(); })
                        .then(function(d){
                            isDuplicate = d.exists;
                            if (d.exists) showErr(numInput, 'This account number already exists.');
                            else clearErr(numInput);
                        });
                }, 400);
            });

            nameInput.addEventListener('input',   function(){ liveLetters(this, 'Account Name'); });
            bankInput.addEventListener('input',   function(){ liveLetters(this, 'Bank Name'); });
            if (branchInput) branchInput.addEventListener('input', function(){ liveLetters(this, 'Branch Name'); });
            if (ifscInput)   ifscInput.addEventListener('input',   function(){ liveIFSC(this); });

            var form = document.querySelector('form');
            if (form) {
                form.addEventListener('submit', function(e) {
                    var ok = true;

                    var name = nameInput.value.trim();
                    if (!name) { showErr(nameInput, 'Account Name is required.'); ok = false; }
                    else if (!/^[A-Za-z\s]+$/.test(name)) { showErr(nameInput, 'Account Name must contain letters only.'); ok = false; }
                    else clearErr(nameInput);

                    var num = numInput.value.trim();
                    if (!num) { showErr(numInput, 'Account Number is required.'); ok = false; }
                    else if (!/^\d+$/.test(num)) { showErr(numInput, 'Account Number must contain digits only.'); ok = false; }
                    else if (isDuplicate) { showErr(numInput, 'This account number already exists.'); ok = false; }
                    else clearErr(numInput);

                    var bank = bankInput.value.trim();
                    if (!bank) { showErr(bankInput, 'Bank Name is required.'); ok = false; }
                    else if (!/^[A-Za-z\s]+$/.test(bank)) { showErr(bankInput, 'Bank Name must contain letters only.'); ok = false; }
                    else clearErr(bankInput);

                    if (branchInput && branchInput.value.trim() && !/^[A-Za-z\s]+$/.test(branchInput.value.trim())) {
                        showErr(branchInput, 'Branch Name must contain letters only.'); ok = false;
                    }
                    if (ifscInput && ifscInput.value.trim() && !/^[A-Z0-9]+$/.test(ifscInput.value.trim())) {
                        showErr(ifscInput, 'IFSC Code must be alphanumeric only.'); ok = false;
                    }
                    if (typeSelect && !typeSelect.value) {
                        getOrCreateErr(typeSelect).textContent = 'Please select an Account Type.';
                        typeSelect.style.borderColor = '#d13b3b'; ok = false;
                    }
                    if (!ok) e.preventDefault();
                });
            }
        });
        </script>
        """
        return (ret + script).encode('utf-8')


# ==================== ACCOUNT VIEWSET ====================
class AccountViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Account.objects.all().order_by("-created_at")
    serializer_class = AccountSerializer
    renderer_classes = [JSONRenderer, AccountBrowsableAPIRenderer]

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



# ==================== EMPLOYEE BROWSABLE API RENDERER ====================
class EmployeeBrowsableAPIRenderer(BrowsableAPIRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        ret = super().render(data, accepted_media_type, renderer_context)
        if isinstance(ret, bytes):
            ret = ret.decode('utf-8')
        script = (
            '<style>'
            '.emp-err{color:#d13b3b;font-size:12px;margin-top:4px;}'
            '.emp-ok{color:#16a34a;font-size:12px;margin-top:4px;}'
            '</style>'
            '<script>'
            'document.addEventListener("DOMContentLoaded",function(){'
            '  var n=document.querySelector("input[name=\\"name\\"]");'
            '  var em=document.querySelector("input[name=\\"email\\"]");'
            '  var ph=document.querySelector("input[name=\\"phone\\"]");'
            '  var sal=document.querySelector("input[name=\\"salary\\"]");'
            '  var dept=document.querySelector("input[name=\\"department\\"]");'
            '  if(!n)return;'
            '  function mkErr(inp){'
            '    var e=inp.parentElement.querySelector(".emp-err");'
            '    if(!e){e=document.createElement("div");e.className="emp-err";inp.parentElement.appendChild(e);}'
            '    return e;'
            '  }'
            '  function se(inp,msg){mkErr(inp).textContent=msg;inp.style.borderColor=msg?"#d13b3b":""}'
            '  function ce(inp){se(inp,"")}'
            '  n.addEventListener("input",function(){'
            '    this.value=this.value.replace(/[^A-Za-z\\s]/g,"");'
            '    var v=this.value.trim();'
            '    if(!v){ce(this);return;}'
            '    se(this,!/^[A-Za-z\\s]+$/.test(v)?"Name should contain letters only.":"");'
            '  });'
            '  em.addEventListener("input",function(){'
            '    var v=this.value.trim();'
            '    if(!v){ce(this);return;}'
            '    se(this,!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(v)?"Enter a valid email address.":"");'
            '  });'
            '  ph.addEventListener("input",function(){'
            '    this.value=this.value.replace(/\\D/g,"").slice(0,10);'
            '    var v=this.value.trim();'
            '    if(!v){ce(this);return;}'
            '    se(this,!/^\\d{10}$/.test(v)?"Phone must be exactly 10 digits.":"");'
            '  });'
            '  if(dept){'
            '    dept.addEventListener("input",function(){'
            '      this.value=this.value.replace(/[^A-Za-z\\s]/g,"");'
            '      var v=this.value.trim();'
            '      if(!v){ce(this);return;}'
            '      se(this,!/^[A-Za-z\\s]+$/.test(v)?"Department should contain letters only.":"");'
            '    });'
            '  }'
            '  if(sal){'
            '    sal.addEventListener("input",function(){'
            '      var v=this.value.trim();'
            '      if(!v){ce(this);return;}'
            '      se(this,isNaN(v)||parseFloat(v)<0?"Salary must be a positive number.":"");'
            '    });'
            '  }'
            '  var et,pt;'
            '  em.addEventListener("blur",function(){'
            '    var v=this.value.trim();'
            '    if(!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(v))return;'
            '    clearTimeout(et);'
            '    et=setTimeout(function(){'
            '      fetch("/employee/check-duplicate/?field=email&value="+encodeURIComponent(v))'
            '        .then(function(r){return r.json();})'
            '        .then(function(d){se(em,d.exists?"This email is already registered to another employee.":"");});'
            '    },300);'
            '  });'
            '  em.addEventListener("input",function(){ce(em);clearTimeout(et);});'
            '  ph.addEventListener("blur",function(){'
            '    var v=this.value.trim();'
            '    if(!/^\\d{10}$/.test(v))return;'
            '    clearTimeout(pt);'
            '    pt=setTimeout(function(){'
            '      fetch("/employee/check-duplicate/?field=phone&value="+encodeURIComponent(v))'
            '        .then(function(r){return r.json();})'
            '        .then(function(d){se(ph,d.exists?"This phone number is already registered to another employee.":"");});'
            '    },300);'
            '  });'
            '  ph.addEventListener("input",function(){ce(ph);clearTimeout(pt);});'
            '  var form=document.querySelector("form");'
            '  if(form){'
            '    form.addEventListener("submit",function(e){'
            '      var ok=true;'
            '      var nv=n.value.trim();'
            '      if(!nv){se(n,"Name is required.");ok=false;}'
            '      else if(!/^[A-Za-z\\s]+$/.test(nv)){se(n,"Name should contain letters only.");ok=false;}'
            '      else ce(n);'
            '      var ev=em.value.trim();'
            '      if(!ev){se(em,"Email is required.");ok=false;}'
            '      else if(!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(ev)){se(em,"Enter a valid email address.");ok=false;}'
            '      else ce(em);'
            '      var pv=ph.value.trim();'
            '      if(!pv){se(ph,"Phone is required.");ok=false;}'
            '      else if(!/^\\d{10}$/.test(pv)){se(ph,"Phone must be exactly 10 digits.");ok=false;}'
            '      else ce(ph);'
            '      if(dept&&dept.value.trim()&&!/^[A-Za-z\\s]+$/.test(dept.value.trim())){se(dept,"Department should contain letters only.");ok=false;}'
            '      if(sal&&sal.value.trim()){var sv=sal.value.trim();if(isNaN(sv)||parseFloat(sv)<0){se(sal,"Salary must be a positive number.");ok=false;}else ce(sal);}'
            '      if(!ok)e.preventDefault();'
            '    });'
            '  }'
            '});'
            '<\/script>'
        )
        return (ret + script).encode('utf-8')

# ==================== EMPLOYEE VIEWSET ====================
class EmployeeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Employee.objects.all().order_by("-created_at")
    serializer_class = EmployeeSerializer
    renderer_classes = [JSONRenderer, EmployeeBrowsableAPIRenderer]

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


# ==================== RESORT BROWSABLE API RENDERER ====================
class ResortBrowsableAPIRenderer(BrowsableAPIRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        ret = super().render(data, accepted_media_type, renderer_context)
        if isinstance(ret, bytes):
            ret = ret.decode('utf-8')
        script = """
        <style>.resort-api-err{color:#d13b3b;font-size:12px;margin-top:4px;}</style>
        <script>
        document.addEventListener('DOMContentLoaded', function () {
            var nameInput   = document.querySelector('input[name="resort_name"]');
            var placeInput  = document.querySelector('input[name="resort_place"]');
            var mobileInput = document.querySelector('input[name="mobile"]');
            var emailInput  = document.querySelector('input[name="email"]');
            var ccInput     = document.querySelector('input[name="cc_emails"]');
            if (!nameInput) return;

            var nameRegex  = /^[A-Za-z ,]+$/;
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            function getOrCreateError(input) {
                var err = input.parentElement.querySelector('.resort-api-err');
                if (!err) {
                    err = document.createElement('div');
                    err.className = 'resort-api-err';
                    input.parentElement.appendChild(err);
                }
                return err;
            }
            function showErr(input, msg) {
                getOrCreateError(input).textContent = msg;
                input.style.borderColor = msg ? '#d13b3b' : '';
            }
            function clearErr(input) { showErr(input, ''); }

            var dupTimer;
            function checkDuplicate() {
                var name  = nameInput.value.trim();
                var place = placeInput ? placeInput.value.trim() : '';
                if (!name || !place) return;
                clearTimeout(dupTimer);
                dupTimer = setTimeout(function() {
                    fetch('/sales/resorts/check-duplicate/?name=' + encodeURIComponent(name) + '&place=' + encodeURIComponent(place))
                        .then(function(r){ return r.json(); })
                        .then(function(d){
                            if (d.exists) {
                                showErr(nameInput, 'A resort with this name and place already exists.');
                                if (placeInput) showErr(placeInput, 'A resort with this name and place already exists.');
                            } else {
                                clearErr(nameInput);
                                if (placeInput) clearErr(placeInput);
                            }
                        });
                }, 400);
            }

            nameInput.addEventListener('input', function() {
                this.value = this.value.replace(/[^A-Za-z ,]/g, '');
                showErr(this, this.value && !nameRegex.test(this.value) ? 'Only letters, spaces, and commas are allowed.' : '');
                checkDuplicate();
            });
            if (placeInput) {
                placeInput.addEventListener('input', function() {
                    this.value = this.value.replace(/[^A-Za-z ,]/g, '');
                    showErr(this, this.value && !nameRegex.test(this.value) ? 'Only letters, spaces, and commas are allowed.' : '');
                    checkDuplicate();
                });
            }
            if (mobileInput) {
                mobileInput.addEventListener('input', function() {
                    this.value = this.value.replace(/\D/g, '').slice(0, 10);
                    showErr(this, this.value && this.value.length !== 10 ? 'Mobile number must be exactly 10 digits.' : '');
                });
            }
            if (emailInput) {
                emailInput.addEventListener('input', function() {
                    showErr(this, this.value && !emailRegex.test(this.value) ? 'Enter a valid email address.' : '');
                });
            }
            if (ccInput) {
                ccInput.addEventListener('input', function() {
                    var parts = this.value.split(',').map(function(s){ return s.trim(); }).filter(Boolean);
                    var invalid = parts.filter(function(e){ return !emailRegex.test(e); });
                    showErr(this, invalid.length ? 'Invalid email(s): ' + invalid.join(', ') : '');
                });
            }

            var form = document.querySelector('form');
            if (form) {
                form.addEventListener('submit', function(e) {
                    var ok = true;
                    var name = nameInput.value.trim();
                    if (!name) { showErr(nameInput, 'Resort name is required.'); ok = false; }
                    else if (!nameRegex.test(name)) { showErr(nameInput, 'Only letters, spaces, and commas are allowed.'); ok = false; }
                    else clearErr(nameInput);
                    if (placeInput) {
                        var place = placeInput.value.trim();
                        if (!place) { showErr(placeInput, 'Resort place is required.'); ok = false; }
                        else if (!nameRegex.test(place)) { showErr(placeInput, 'Only letters, spaces, and commas are allowed.'); ok = false; }
                        else clearErr(placeInput);
                    }
                    if (mobileInput && mobileInput.value && mobileInput.value.replace(/\D/g,'').length !== 10) {
                        showErr(mobileInput, 'Mobile number must be exactly 10 digits.'); ok = false;
                    }
                    if (emailInput && emailInput.value && !emailRegex.test(emailInput.value)) {
                        showErr(emailInput, 'Enter a valid email address.'); ok = false;
                    }
                    if (ccInput && ccInput.value) {
                        var parts = ccInput.value.split(',').map(function(s){ return s.trim(); }).filter(Boolean);
                        var invalid = parts.filter(function(e){ return !emailRegex.test(e); });
                        if (invalid.length) { showErr(ccInput, 'Invalid email(s): ' + invalid.join(', ')); ok = false; }
                        else clearErr(ccInput);
                    }
                    if (!ok) e.preventDefault();
                });
            }
        });
        </script>
        """
        return (ret + script).encode('utf-8')


# ==================== RESORT VIEWSET ====================
class ResortViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
    queryset = Resort.objects.all().order_by("-created_at")
    serializer_class = ResortSerializer
    renderer_classes = [JSONRenderer, ResortBrowsableAPIRenderer]

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
    exclude_id = (request.query_params.get("exclude_id") or "").strip()
    if not title:
        return Response({"exists": False})
    qs = Blog.objects.filter(title__iexact=title)
    if exclude_id:
        qs = qs.exclude(id=exclude_id)
    return Response({"exists": qs.exists()})


@api_view(["GET"])
def validate_blog_slug(request):
    slug = (request.query_params.get("slug") or "").strip()
    exclude_id = (request.query_params.get("exclude_id") or "").strip()
    if not slug:
        return Response({"exists": False})
    qs = Blog.objects.filter(slug=slug)
    if exclude_id:
        qs = qs.exclude(id=exclude_id)
    return Response({"exists": qs.exists()})


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
