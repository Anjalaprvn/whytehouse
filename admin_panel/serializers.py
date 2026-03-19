from rest_framework import serializers

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


# ==================== BLOG CATEGORY SERIALIZER ====================
class BlogCategorySerializer(serializers.ModelSerializer):
    blog_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogCategory
        fields = [
            "id",
            "name",
            "slug",
            "order",
            "is_active",
            "created_at",
            "blog_count",
        ]
        read_only_fields = ["id", "created_at", "blog_count"]

    def get_blog_count(self, obj):
        return Blog.objects.filter(status="published", category=obj.slug).count()


# ==================== BLOG IMAGE SERIALIZER ====================
class BlogImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogImage
        fields = ["id", "image", "image_url", "order"]
        read_only_fields = ["id", "image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ==================== BLOG SERIALIZER ====================
class BlogSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    content_images = BlogImageSerializer(source="images", many=True, read_only=True)
    category_name = serializers.SerializerMethodField()
    tag_list = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "content",
            "status",
            "category",
            "category_name",
            "package_id",
            "author_name",
            "author_summary",
            "reading_time",
            "publish_date",
            "featured_image",
            "featured_image_url",
            "image_url",
            "hashtags",
            "tags",
            "tag_list",
            "content_images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "image_url",
            "category_name",
            "tag_list",
            "content_images",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.featured_image and request:
            return request.build_absolute_uri(obj.featured_image.url)
        if obj.featured_image_url:
            return obj.featured_image_url
        return None

    def get_category_name(self, obj):
        if obj.category:
            cat = BlogCategory.objects.filter(slug=obj.category).first()
            return cat.name if cat else obj.category
        return None

    def get_tag_list(self, obj):
        raw = obj.tags or obj.hashtags or ""
        return [t.strip() for t in str(raw).split(",") if t.strip()]


class BlogListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "status",
            "category",
            "category_name",
            "author_name",
            "reading_time",
            "publish_date",
            "image_url",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "image_url", "category_name"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.featured_image and request:
            return request.build_absolute_uri(obj.featured_image.url)
        if obj.featured_image_url:
            return obj.featured_image_url
        return None

    def get_category_name(self, obj):
        if obj.category:
            cat = BlogCategory.objects.filter(slug=obj.category).first()
            return cat.name if cat else obj.category
        return None


# ==================== LEAD SERIALIZER ====================
class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id',
            'full_name',
            'mobile_number',
            'place',
            'enquiry_type',
            'source',
            'employee',
            'remarks',
            'created_at',
            'updated_at',
        ]
# ==================== PROPERTY SERIALIZER ====================
class PropertySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    amenity_list = serializers.ReadOnlyField()

    class Meta:
        model = Property
        fields = [
            "id",
            "name",
            "property_type",
            "location",
            "website",
            "address",
            "summary",
            "owner_name",
            "owner_contact",
            "amenities",
            "amenity_list",
            "image",
            "image_url",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "image_url", "amenity_list", "created_at"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ==================== DESTINATION SERIALIZER ====================
class DestinationSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    map_image_url = serializers.SerializerMethodField()
    package_count = serializers.SerializerMethodField()

    class Meta:
        model = Destination
        fields = [
            "id",
            "name",
            "country",
            "category",
            "description",
            "packages_start_from",
            "image",
            "image_url",
            "map_image",
            "map_image_url",
            "is_popular",
            "created_at",
            "package_count",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "image_url",
            "map_image_url",
            "package_count",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_map_image_url(self, obj):
        request = self.context.get("request")
        if obj.map_image and request:
            return request.build_absolute_uri(obj.map_image.url)
        return None

    def get_package_count(self, obj):
        return obj.packages.filter(active=True).count()


# ==================== TRAVEL PACKAGE SERIALIZERS ====================
class TravelPackageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    story_main_image_url = serializers.SerializerMethodField()
    story_side_image1_url = serializers.SerializerMethodField()
    story_side_image2_url = serializers.SerializerMethodField()
    destination_details = DestinationSerializer(source="destination", read_only=True)

    class Meta:
        model = TravelPackage
        fields = [
            "id",
            "package_id",
            "name",
            "category",
            "destination",
            "destination_details",
            "location",
            "country",
            "price",
            "duration",
            "description",
            "image",
            "image_url",
            "active",
            "itinerary",
            "inclusions",
            "exclusions",
            "meta_title",
            "meta_description",
            "story_main_image",
            "story_main_image_url",
            "story_side_image1",
            "story_side_image1_url",
            "story_side_image2",
            "story_side_image2_url",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "package_id",
            "created_at",
            "image_url",
            "story_main_image_url",
            "story_side_image1_url",
            "story_side_image2_url",
            "destination_details",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_story_main_image_url(self, obj):
        request = self.context.get("request")
        if obj.story_main_image and request:
            return request.build_absolute_uri(obj.story_main_image.url)
        return None

    def get_story_side_image1_url(self, obj):
        request = self.context.get("request")
        if obj.story_side_image1 and request:
            return request.build_absolute_uri(obj.story_side_image1.url)
        return None

    def get_story_side_image2_url(self, obj):
        request = self.context.get("request")
        if obj.story_side_image2 and request:
            return request.build_absolute_uri(obj.story_side_image2.url)
        return None


class TravelPackageListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    destination_name = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = TravelPackage
        fields = [
            "id",
            "package_id",
            "name",
            "category",
            "destination",
            "destination_name",
            "location",
            "country",
            "price",
            "duration",
            "image",
            "image_url",
            "active",
            "created_at",
        ]
        read_only_fields = ["id", "package_id", "created_at", "image_url", "destination_name"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ==================== CUSTOMER SERIALIZER ====================
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "customer_type",
            "salutation",
            "first_name",
            "last_name",
            "display_name",
            "place",
            "contact_number",
            "email",
            "same_as_whatsapp",
            "whatsapp_number",
            "work_number",
            "gst_number",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ==================== MEAL SERIALIZER ====================
class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = [
            "id",
            "name",
            "description",
            "included_meals",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ==================== ACCOUNT SERIALIZER ====================
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "account_name",
            "account_number",
            "bank_name",
            "ifsc_code",
            "account_type",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ==================== INQUIRY SERIALIZER ====================
class InquirySerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source="lead.full_name", read_only=True)

    class Meta:
        model = Inquiry
        fields = [
            "id",
            "lead",
            "lead_name",
            "name",
            "email",
            "phone",
            "package",
            "message",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "lead_name"]


# ==================== EMPLOYEE SERIALIZER ====================
class EmployeeSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "role",
            "department",
            "join_date",
            "salary",
            "status",
            "profile_picture",
            "image_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None


# ==================== RESORT SERIALIZER ====================
class ResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resort
        fields = [
            "id",
            "resort_name",
            "location",
            "contact_person",
            "contact_number",
            "email",
            "address",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ==================== VOUCHER SERIALIZER ====================
class VoucherSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.display_name", read_only=True)
    sales_person_name = serializers.CharField(source="sales_person.name", read_only=True)
    resort_name = serializers.CharField(source="resort.resort_name", read_only=True)
    meals_plan_name = serializers.CharField(source="meals_plan.name", read_only=True)
    bank_account_name = serializers.CharField(source="bank_account.account_name", read_only=True)

    class Meta:
        model = Voucher
        fields = [
            "id",
            "customer",
            "customer_name",
            "voucher_no",
            "voucher_date",
            "sales_person",
            "sales_person_name",
            "resort",
            "resort_name",
            "checkin_date",
            "checkout_date",
            "checkin_time",
            "checkout_time",
            "adults",
            "children",
            "nights",
            "pax_notes",
            "room_type",
            "no_of_rooms",
            "meals_plan",
            "meals_plan_name",
            "bank_account",
            "bank_account_name",
            "package_price",
            "resort_price",
            "total_amount",
            "received",
            "pending",
            "from_whytehouse",
            "profit",
            "note_for_resort",
            "note_for_guest",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "voucher_no",
            "created_at",
            "updated_at",
            "customer_name",
            "sales_person_name",
            "resort_name",
            "meals_plan_name",
            "bank_account_name",
        ]


# ==================== INVOICE SERIALIZER ====================
class InvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.display_name", read_only=True)
    resort_name = serializers.CharField(source="resort.resort_name", read_only=True)
    sales_person_name = serializers.CharField(source="sales_person.name", read_only=True)
    account_name = serializers.CharField(source="bank_account.account_name", read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "customer",
            "customer_name",
            "invoice_no",
            "invoice_date",
            "sales_person",
            "sales_person_name",
            "resort",
            "resort_name",
            "checkin_date",
            "checkout_date",
            "checkin_time",
            "checkout_time",
            "adults",
            "children",
            "pax_total",
            "pax_notes",
            "nights",
            "room_type",
            "rooms",
            "meals_plan",
            "bank_account",
            "account_name",
            "package_price",
            "tax",
            "resort_price",
            "total",
            "received",
            "pending",
            "profit",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "invoice_no",
            "created_at",
            "updated_at",
            "customer_name",
            "resort_name",
            "sales_person_name",
            "account_name",
        ]


# ==================== FEEDBACK IMAGE SERIALIZER ====================
class FeedbackImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = FeedbackImage
        fields = ["id", "image", "image_url", "uploaded_at"]
        read_only_fields = ["id", "image_url", "uploaded_at"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ==================== FEEDBACK SERIALIZER ====================
class FeedbackSerializer(serializers.ModelSerializer):
    images = FeedbackImageSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = [
            "id",
            "name",
            "email",
            "mobile_number",
            "feedback_type",
            "rating",
            "feedback",
            "featured",
            "created_at",
            "images",
        ]
        read_only_fields = ["id", "created_at", "images"]