from rest_framework import serializers
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
    TravelPackage
)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id',
            'customer_type',
            'salutation',
            'first_name',
            'last_name',
            'display_name',
            'place',
            'contact_number',
            'email',
            'same_as_whatsapp',
            'whatsapp_number',
            'work_number',
            'gst_number',
            'created_at',
            'updated_at',
        ]


class ResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resort
        fields = [
            'id',
            'resort_name',
            'resort_place',
            'mobile',
            'email',
            'cc_emails',
            'location_map_link',
            'created_at',
            'updated_at',
        ]

class MealSerializer(serializers.ModelSerializer):
    included_meals_list = serializers.ReadOnlyField()

    class Meta:
        model = Meal
        fields = [
            'id',
            'name',
            'description',
            'included_meals',
            'included_meals_list',
            'created_at',
            'updated_at',
        ]


class AccountSerializer(serializers.ModelSerializer):
    # Use a CharField so we can accept either choice key or human label,
    # then normalize in `validate_account_type`.
    account_type = serializers.CharField()
    class Meta:
        model = Account
        fields = [
            'id',
            'account_name',
            'account_number',
            'bank_name',
            'branch_name',
            'ifsc_code',
            'account_type',
            'created_at',
            'updated_at',
        ]

    def validate_account_type(self, value):
        """Allow API clients to send either the internal choice key (e.g. 'current')
        or the human label (e.g. 'Current'). Return the internal key for storage.
        """
        if isinstance(value, str):
            v = value.strip()
            # If already a valid key, accept it
            valid_keys = [k for k, _ in Account.ACCOUNT_TYPE_CHOICES]
            if v in valid_keys:
                return v

            # Map human labels (case-insensitive) to keys
            label_map = {label.lower(): key for key, label in Account.ACCOUNT_TYPE_CHOICES}
            low = v.lower()
            if low in label_map:
                return label_map[low]

        return value


class InvoiceSerializer(serializers.ModelSerializer):

    # Optional: show names instead of only IDs (for GET)
    customer_name = serializers.CharField(source='customer.display_name', read_only=True)
    resort_name = serializers.CharField(source='resort.resort_name', read_only=True)
    sales_person_name = serializers.CharField(source='sales_person.name', read_only=True)
    bank_account_name = serializers.CharField(source='bank_account.account_name', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id',

            # Basic Info
            'customer',
            'customer_name',
            'invoice_no',
            'invoice_date',
            'sales_person',
            'sales_person_name',

            # Package Details
            'resort',
            'resort_name',
            'checkin_date',
            'checkout_date',
            'checkin_time',
            'checkout_time',

            # Pax
            'adults',
            'children',
            'pax_total',
            'pax_notes',

            # Room
            'nights',
            'room_type',
            'rooms',
            'meals_plan',

            # Bank
            'bank_account',
            'bank_account_name',

            # Pricing
            'package_price',
            'tax',
            'resort_price',
            'total',
            'received',
            'pending',
            'profit',

            # Notes
            'notes',

            'created_at',
            'updated_at'
        ]

        read_only_fields = [
            'invoice_no',
            'pax_total',
            'total',
            'pending',
            'profit',
            'created_at',
            'updated_at'
        ]

        def _compute_invoice_totals(self, data, instance=None):
            # helper to compute derived fields from supplied data or instance
            adults = data.get('adults') if data.get('adults') is not None else (instance.adults if instance else 0)
            children = data.get('children') if data.get('children') is not None else (instance.children if instance else 0)
            pax_total = (adults or 0) + (children or 0)

            package_price = data.get('package_price') if data.get('package_price') is not None else (getattr(instance, 'package_price', 0) if instance else 0)
            resort_price = data.get('resort_price') if data.get('resort_price') is not None else (getattr(instance, 'resort_price', 0) if instance else 0)
            tax = data.get('tax') if data.get('tax') is not None else (getattr(instance, 'tax', 0) if instance else 0)
            total = (package_price or 0) + (resort_price or 0) + (tax or 0)

            received = data.get('received') if data.get('received') is not None else (getattr(instance, 'received', 0) if instance else 0)
            pending = (total or 0) - (received or 0)

            # profit heuristic: total minus costs (package + resort). Adjust if you have a different definition.
            profit = (total or 0) - ((package_price or 0) + (resort_price or 0))

            return {
                'pax_total': pax_total,
                'total': total,
                'pending': pending,
                'profit': profit,
            }

        def create(self, validated_data):
            totals = self._compute_invoice_totals(validated_data)
            validated_data.update(totals)
            return Invoice.objects.create(**validated_data)

        def update(self, instance, validated_data):
            # perform regular update then recalculate derived fields from instance state
            instance = super().update(instance, validated_data)
            totals = self._compute_invoice_totals({}, instance=instance)
            for k, v in totals.items():
                setattr(instance, k, v)
            instance.save()
            return instance


class VoucherSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.display_name', read_only=True)
    sales_person_name = serializers.CharField(source='sales_person.name', read_only=True)
    resort_name = serializers.CharField(source='resort.resort_name', read_only=True)
    meals_plan_name = serializers.CharField(source='meals_plan.name', read_only=True)
    bank_account_name = serializers.CharField(source='bank_account.account_name', read_only=True)

    class Meta:
        model = Voucher
        fields = [
            'id',

            'customer',
            'customer_name',

            'voucher_no',
            'voucher_date',

            'sales_person',
            'sales_person_name',

            'resort',
            'resort_name',

            'checkin_date',
            'checkout_date',
            'checkin_time',
            'checkout_time',

            'adults',
            'children',
            'pax_total',
            'pax_notes',

            'nights',
            'room_type',
            'no_of_rooms',

            'meals_plan',
            'meals_plan_name',

            'bank_account',
            'bank_account_name',

            'package_price',
            'resort_price',
            'total_amount',
            'received',
            'pending',
            'from_whytehouse',
            'profit',

            'note_for_resort',
            'note_for_guest',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'voucher_no',
            'pax_total',
            'total_amount',
            'pending',
            'from_whytehouse',
            'profit',
            'created_at',
            'updated_at',
        ]

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id',
            'full_name',
            'mobile_number',
            'alternate_number',
            'place',
            'email',
            'message',
            'package',
            'package_name',
            'property_name',
            'source',
            'enquiry_type',
            'status',
            'is_viewed',
            'remarks',
            'employee',
            'created_at',
            'updated_at',
        ]


class PropertySerializer(serializers.ModelSerializer):
    amenity_list = serializers.ReadOnlyField()

    class Meta:
        model = Property
        fields = [
            'id',
            'name',
            'property_type',
            'location',
            'website',
            'address',
            'summary',
            'owner_name',
            'owner_contact',
            'amenities',
            'amenity_list',
            'image',
            'is_active',
            'created_at',
        ]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            'id',
            'name',
            'email',
            'mobile_number',
            'feedback_type',
            'rating',
            'feedback',
            'created_at',
            'featured',
        ]


class BlogSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()

    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'content',
            'status',
            'category',
            'package_id',
            'author_name',
            'author_summary',
            'reading_time',
            'publish_date',
            'featured_image',
            'featured_image_url',
            'image_url',
            'hashtags',
            'tags',
            'created_at',
            'updated_at',
        ]


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = [
            'id',
            'name',
            'country',
            'category',
            'description',
            'packages_start_from',
            'image',
            'map_image',
            'is_popular',
            'is_active',
            'created_at',
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'role',
            'department',
            'join_date',
            'salary',
            'status',
            'profile_picture',
            'created_at',
            'updated_at',
        ]


class TravelPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPackage
        fields = [
            'id',
            'package_id',
            'name',
            'category',
            'destination',
            'location',
            'country',
            'price',
            'adult_price',
            'price_type',
            'duration',
            'description',
            'image',
            'active',
            'itinerary',
            'inclusions',
            'exclusions',
            'meta_title',
            'meta_description',
            'story_main_image',
            'story_side_image1',
            'story_side_image2',
            'created_at',
        ]