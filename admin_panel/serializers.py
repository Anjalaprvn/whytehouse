import re
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
        return Blog.objects.filter(status="published", category=obj).count()


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


class BlogSerializer(serializers.ModelSerializer):
    STATUS_CHOICES_LIMITED = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    status = serializers.ChoiceField(choices=STATUS_CHOICES_LIMITED)
    image_url = serializers.SerializerMethodField(read_only=True)
    content_images = BlogImageSerializer(source="images", many=True, read_only=True)
    upload_content_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        help_text="Upload one or more content images (multipart/form-data, key: upload_content_images)",
    )
    content = serializers.CharField(
        style={"base_template": "textarea.html", "rows": 10},
        help_text="Write your blog content here. Reference uploaded images using {{image1}}, {{image2}}, etc.",
    )
    category_name = serializers.CharField(source="category.name", read_only=True)

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
            "content_images",
            "upload_content_images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "image_url",
            "category_name",
            "content_images",
        ]
        extra_kwargs = {
            "content": {
                "style": {"base_template": "textarea.html", "rows": 10},
                "help_text": "Write your blog content here. Reference uploaded images using {{image1}}, {{image2}}, etc.",
            },
            "hashtags": {
                "help_text": "Comma-separated hashtags (e.g. #travel, #beach)",
                "style": {"base_template": "textarea.html", "placeholder": "#travel, #beach", "rows": 2},
            },
            "category": {"required": True},
            "publish_date": {"required": True},
            "featured_image": {"required": False},
            "featured_image_url": {"required": False, "allow_blank": True, "allow_null": True},
        }

    _RICH_TEXT_RE = r'^[A-Za-z0-9\s&,.]+$'

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Blog title is required.")
        if re.search(r'\d', value):
            raise serializers.ValidationError("Blog title should not contain numbers.")
        instance = getattr(self, 'instance', None)
        qs = Blog.objects.filter(title__iexact=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A blog with this title already exists.")
        return value

    def validate_slug(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("URL slug is required.")
        if not re.match(r'^[a-z0-9-]+$', value):
            raise serializers.ValidationError("Slug must contain only lowercase letters, numbers, and hyphens.")
        instance = getattr(self, 'instance', None)
        qs = Blog.objects.filter(slug=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A blog with this slug already exists.")
        return value

    def validate_excerpt(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Excerpt is required.")
        if not re.match(self._RICH_TEXT_RE, value):
            raise serializers.ValidationError("Excerpt can only contain letters, numbers, spaces, &, comma, and fullstop.")
        if not (50 <= len(value) <= 300):
            raise serializers.ValidationError("Excerpt must be between 50 and 300 characters.")
        return value

    def validate_author_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Author name is required.")
        if not re.match(r'^[A-Za-z\s]+$', value):
            raise serializers.ValidationError("Author name should contain letters and spaces only (no numbers or special characters).")
        return value

    def validate_author_summary(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Author summary is required.")
        if not re.match(self._RICH_TEXT_RE, value):
            raise serializers.ValidationError("Author summary can only contain letters, numbers, spaces, &, comma, and fullstop.")
        return value

    def validate_reading_time(self, value):
        if value is None:
            raise serializers.ValidationError("Reading time is required.")
        if not (1 <= value <= 120):
            raise serializers.ValidationError("Reading time must be between 1 and 120 minutes.")
        return value

    def validate_content(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Content is required.")
        if not re.match(self._RICH_TEXT_RE, value):
            raise serializers.ValidationError("Content can only contain letters, numbers, spaces, &, comma, and fullstop.")
        return value

    def validate_package_id(self, value):
        if not value:
            return value
        value = value.strip().upper()
        if not re.match(r'^PKG\d{3}$', value):
            raise serializers.ValidationError("Package ID must be in format PKG followed by 3 digits (e.g., PKG001).")
        if not TravelPackage.objects.filter(package_id=value).exists():
            raise serializers.ValidationError("No package found with this ID.")
        return value

    def validate_hashtags(self, value):
        if not value:
            return ""

        if isinstance(value, (list, tuple)):
            parts = [str(tag).strip() for tag in value if str(tag).strip()]
        else:
            parts = [tag.strip() for tag in str(value).split(",") if tag.strip()]

        cleaned = []
        for tag in parts:
            tag = tag.lstrip('#').strip()
            if not re.match(r'^[A-Za-z\s]+$', tag):
                raise serializers.ValidationError("Hashtags should contain letters only.")
            cleaned.append(f"#{tag}")
        return ", ".join(cleaned)

    def create(self, validated_data):
        upload_content_images = validated_data.pop("upload_content_images", [])
        instance = super().create(validated_data)
        for i, image in enumerate(upload_content_images):
            BlogImage.objects.create(blog=instance, image=image, order=i)
        return instance

    def update(self, instance, validated_data):
        upload_content_images = validated_data.pop("upload_content_images", [])
        instance = super().update(instance, validated_data)
        for i, image in enumerate(upload_content_images):
            BlogImage.objects.create(blog=instance, image=image, order=i)
        return instance

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.featured_image and request:
            return request.build_absolute_uri(obj.featured_image.url)
        if obj.featured_image_url:
            return obj.featured_image_url
        return None



class BlogListSerializer(serializers.ModelSerializer):
    STATUS_CHOICES_LIMITED = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    status = serializers.ChoiceField(choices=STATUS_CHOICES_LIMITED, read_only=True)
    image_url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True)

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

    def validate_full_name(self, value):
        if any(c.isdigit() for c in value):
            raise serializers.ValidationError("Full name must not contain numbers.")
        return value

    def validate_mobile_number(self, value):
        if not value.strip().lstrip('+').isdigit():
            raise serializers.ValidationError("Mobile number must contain digits only.")
        return value
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
    customer_type = serializers.ChoiceField(
        choices=['Individual', 'Business'],
        required=True,
        error_messages={
            'required': 'This field is required.',
            'invalid_choice': 'Invalid customer type.'
        }
    )
    first_name = serializers.CharField(
        required=True,
        error_messages={
            'required': 'This field is required.',
            'blank': 'This field may not be blank.'
        }
    )
    display_name = serializers.CharField(
        required=True,
        error_messages={
            'required': 'This field is required.',
            'blank': 'This field may not be blank.'
        }
    )
    contact_number = serializers.CharField(
        required=True,
        error_messages={
            'required': 'This field is required.',
            'blank': 'This field may not be blank.'
        }
    )
    salutation = serializers.ChoiceField(
        choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.'), ('Dr.', 'Dr.')],
        required=False,
        allow_blank=True,
    )

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
        extra_kwargs = {
            'last_name': {'required': False, 'allow_blank': True},
            'email': {'required': False, 'allow_blank': True},
            'place': {'required': False, 'allow_blank': True},
            'work_number': {'required': False, 'allow_blank': True},
            'gst_number': {'required': False, 'allow_blank': True},
            'whatsapp_number': {'required': False, 'allow_blank': True},
            'same_as_whatsapp': {'required': False},
        }

    def _no_digits(self, value, field):
        if value and any(c.isdigit() for c in value):
            raise serializers.ValidationError(f"{field} must not contain numbers.")
        return value

    def _phone(self, value, field):
        if not value:
            return value
        digits = value.strip().lstrip('+')
        if not digits.isdigit():
            raise serializers.ValidationError(f"{field} must contain digits only.")
        if not (10 <= len(digits) <= 15):
            raise serializers.ValidationError(f"{field} must be 10–15 digits.")
        return value

    def validate_first_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("First name is required.")
        return self._no_digits(value, "First name")

    def validate_last_name(self, value):
        return self._no_digits(value, "Last name")

    def validate_display_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Display name is required.")
        return self._no_digits(value, "Display name")

    def validate_place(self, value):
        return self._no_digits(value, "Customer Place")

    def validate_contact_number(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Contact number is required.")
        self._phone(value, "Contact number")
        instance = getattr(self, 'instance', None)
        qs = Customer.objects.filter(contact_number=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A customer with this contact number already exists.")
        return value

    def validate_email(self, value):
        if not value or not value.strip():
            return value
        instance = getattr(self, 'instance', None)
        qs = Customer.objects.filter(email=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A customer with this email already exists.")
        return value

    def validate_whatsapp_number(self, value):
        return self._phone(value, "WhatsApp number")

    def validate_work_number(self, value):
        return self._phone(value, "Work number")

    def validate(self, data):
        if data.get('same_as_whatsapp'):
            contact = data.get('contact_number') or (self.instance.contact_number if self.instance else '')
            data['whatsapp_number'] = contact
        return data

    def validate_gst_number(self, value):
        if not value:
            return value
        if not re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$', value.strip().upper()):
            raise serializers.ValidationError("Invalid GST number format (e.g. 22AAAAA0000A1Z5).")
        return value.strip().upper()


# ==================== MEAL SERIALIZER ====================
class MealSerializer(serializers.ModelSerializer):
    included_meals_list = serializers.SerializerMethodField(read_only=True)
    included_meals = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Comma-separated meal items (e.g. Breakfast, Lunch, Dinner)",
        style={"base_template": "textarea.html", "rows": 2,
               "placeholder": "Breakfast, Lunch, Dinner"},
    )

    class Meta:
        model = Meal
        fields = [
            "id",
            "name",
            "description",
            "included_meals",
            "included_meals_list",
            "meal_type",
            "price_per_person",
            "children_pricing",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "included_meals_list", "created_at", "updated_at"]

    def get_included_meals_list(self, obj):
        if obj.included_meals:
            return [m.strip() for m in obj.included_meals.split(',') if m.strip()]
        return []

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Meal plan name is required.")
        if len(value.strip()) < 2 or len(value.strip()) > 50:
            raise serializers.ValidationError("Meal plan name must be between 2 and 50 characters.")
        instance = getattr(self, 'instance', None)
        qs = Meal.objects.filter(name=value.strip())
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A meal plan with this name already exists.")
        return value.strip()

    def validate_included_meals(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Please provide at least one meal item.")
        items = [m.strip() for m in value.split(',') if m.strip()]
        if not items:
            raise serializers.ValidationError("Please provide at least one meal item.")
        # Normalise back to clean comma-separated string
        return ', '.join(items)


# ==================== ACCOUNT SERIALIZER ====================
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "account_name",
            "account_number",
            "bank_name",
            "branch_name",
            "ifsc_code",
            "account_type",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_account_name(self, value):
        if any(c.isdigit() for c in value):
            raise serializers.ValidationError("Account name must not contain numbers.")
        return value

    def validate_account_number(self, value):
        if not value.strip().isdigit():
            raise serializers.ValidationError("Account number must contain digits only.")
        return value

    def validate_bank_name(self, value):
        if any(c.isdigit() for c in value):
            raise serializers.ValidationError("Bank name must not contain numbers.")
        return value

    def validate_branch_name(self, value):
        if value and any(c.isdigit() for c in value):
            raise serializers.ValidationError("Branch name must not contain numbers.")
        return value

    def validate_ifsc_code(self, value):
        if value and not value.strip().isalnum():
            raise serializers.ValidationError("IFSC code must be alphanumeric only.")
        return value.upper() if value else value


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

    def validate_name(self, value):
        if any(c.isdigit() for c in value):
            raise serializers.ValidationError("Name must not contain numbers.")
        return value

    def validate_phone(self, value):
        if not value.strip().lstrip('+').isdigit():
            raise serializers.ValidationError("Phone must contain digits only.")
        return value


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
        extra_kwargs = {
            "role": {"required": False, "allow_blank": True},
            "department": {"required": False, "allow_blank": True},
            "join_date": {"required": False, "allow_null": True},
            "salary": {"required": False, "allow_null": True},
            "profile_picture": {"required": False},
        }

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name is required.")
        if not re.match(r'^[A-Za-z\s]+$', value):
            raise serializers.ValidationError("Name should contain letters only (no numbers or special characters).")
        return value

    def validate_email(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Email is required.")
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', value):
            raise serializers.ValidationError("Enter a valid email address.")
        instance = getattr(self, 'instance', None)
        qs = Employee.objects.filter(email=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This email is already registered to another employee.")
        return value

    def validate_phone(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Phone is required.")
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("Phone must be exactly 10 digits.")
        instance = getattr(self, 'instance', None)
        qs = Employee.objects.filter(phone=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This phone number is already registered to another employee.")
        return value

    def validate_salary(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Salary must be a positive number.")
        return value


# ==================== RESORT SERIALIZER ====================
class ResortSerializer(serializers.ModelSerializer):
    resort_place = serializers.CharField(source='location', required=True)
    mobile       = serializers.CharField(source='contact_number', required=False, allow_blank=True, default='')
    cc_emails    = serializers.CharField(required=False, allow_blank=True, default='',
                       help_text='Enter multiple CC emails separated by commas. e.g. a@b.com, c@d.com')

    class Meta:
        model = Resort
        fields = [
            'id',
            'resort_name',
            'resort_place',
            'mobile',
            'email',
            'cc_emails',
            'location',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'location', 'created_at', 'updated_at']

    def validate_resort_name(self, value):
        if any(c.isdigit() for c in value):
            raise serializers.ValidationError('Resort name must not contain numbers.')
        return value

    def validate_mobile(self, value):
        if value and not value.strip().lstrip('+').isdigit():
            raise serializers.ValidationError('Mobile must contain digits only.')
        if value and len(value.strip()) != 10:
            raise serializers.ValidationError('Mobile number must be exactly 10 digits.')
        return value

    def validate_cc_emails(self, value):
        if not value:
            return value
        import re
        email_re = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
        for email in [e.strip() for e in value.split(',') if e.strip()]:
            if not email_re.match(email):
                raise serializers.ValidationError(f'Invalid email address: {email}')
        return value

    def create(self, validated_data):
        validated_data.pop('cc_emails', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('cc_emails', None)
        return super().update(instance, validated_data)


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

    def validate_name(self, value):
        if any(c.isdigit() for c in value):
            raise serializers.ValidationError("Name must not contain numbers.")
        return value

    def validate_mobile_number(self, value):
        if value and not value.strip().isdigit():
            raise serializers.ValidationError("Mobile number must contain digits only.")
        return value

    def validate_rating(self, value):
        if value not in range(1, 6):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value