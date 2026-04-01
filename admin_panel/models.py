from django.db import models
from datetime import time
from django.utils import timezone
from django.utils.text import slugify

# BLOG CATEGORY MODEL
class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Blog Categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# LEAD MODEL
class Lead(models.Model):
    SOURCE_CHOICES = (
        ('Direct', 'Direct Contact'),
        ('Website', 'Website'),
        ('Manual', 'Manual Entry'),
        ('Referral', 'Referral'),
        ('Enquire Now', 'Enquire Now'),
    )
    ENQUIRY_TYPE_CHOICES = (
        ('General', 'General Enquiry'),
        ('International', 'International'),
        ('Domestic', 'Domestic'),
        ('Hospitality', 'Hospitality'),
    )
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Converted', 'Converted'),
        ('Junk', 'Junk'),
    )
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    alternate_number = models.CharField(max_length=15, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    package = models.CharField(max_length=200, blank=True, null=True)
    package_name = models.CharField(max_length=200, blank=True, null=True)
    property_name = models.CharField(max_length=200, blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='Manual')
    enquiry_type = models.CharField(max_length=50, choices=ENQUIRY_TYPE_CHOICES, default='General')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    is_viewed = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.full_name


class Property(models.Model):
    PROPERTY_TYPES = [
        ('hotel', 'Luxury Hotel'),
        ('resort', 'Mountain Resort'),
        ('beach', 'Beach Resort'),
        ('villa', 'Villa'),
        ('apartment', 'Apartment'),
    ]

    name = models.CharField(max_length=200)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    location = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    address = models.TextField()
    summary = models.TextField()
    owner_name = models.CharField(max_length=150, blank=True, null=True)
    owner_contact = models.CharField(max_length=20, blank=True, null=True)

    # comma separated amenities (TEXT)
    amenities = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def amenity_list(self):
        if self.amenities:
            return [a.strip() for a in self.amenities.split(",") if a.strip()]
        return []

class Destination(models.Model):
    CATEGORY_CHOICES = (
        ('Domestic', 'Domestic'),
        ('International', 'International'),
    )
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Domestic')
    description = models.TextField(blank=True, null=True)
    packages_start_from = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    map_image = models.ImageField(upload_to='destinations/maps/', blank=True, null=True)
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name}, {self.country}"

    class Meta:
        ordering = ['-created_at']

# TRAVEL PACKAGE MODEL
class TravelPackage(models.Model):
    CATEGORY_CHOICES = (
        ('Domestic', 'Domestic'),
        ('International', 'International'),
    )
    
    package_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    destination = models.ForeignKey(
        Destination,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="packages"
    )

    location = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    adult_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    child_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    child_pricing = models.TextField(blank=True, null=True, default='[]', help_text="JSON age brackets: [{min_age, max_age, price}]")
    price_type = models.CharField(max_length=20, blank=True, null=True, default='Per Person')
    base_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='travel_packages/', blank=True, null=True)
    active = models.BooleanField(default=True)
    itinerary = models.TextField(blank=True, null=True)
    inclusions = models.TextField(blank=True, null=True)
    exclusions = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    resort = models.ForeignKey(
        'Resort',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='packages'
    )
    meal_plans = models.ManyToManyField(
        'Meal',
        blank=True,
        related_name='packages'
    )

    story_main_image = models.ImageField(upload_to='package_stories/', blank=True, null=True)
    story_side_image1 = models.ImageField(upload_to='package_stories/', blank=True, null=True)
    story_side_image2 = models.ImageField(upload_to='package_stories/', blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.package_id:
            last_package = TravelPackage.objects.filter(package_id__startswith='PKG').order_by('-package_id').first()
            if last_package and last_package.package_id:
                try:
                    last_num = int(last_package.package_id[3:])
                    self.package_id = f'PKG{str(last_num + 1).zfill(3)}'
                except (ValueError, IndexError):
                    self.package_id = 'PKG001'
            else:
                self.package_id = 'PKG001'
        super().save(*args, **kwargs)

    def get_child_pricing(self):
        import json
        if not self.child_pricing or self.child_pricing == '[]':
            return []
        try:
            return json.loads(self.child_pricing)
        except (json.JSONDecodeError, TypeError):
            return []

    def __str__(self):
        return self.name

class Inquiry(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Converted', 'Converted'),
        ('Junk', 'Junk'),
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inquiries"
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    package = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


#EMPLOYEE MODEL OF ADMINAPP

class Employee(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('On Leave', 'On Leave'),
    )
    
    # Basic Information
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    join_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    profile_picture = models.ImageField(upload_to='employee/', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    class Meta:
        ordering = ['-created_at']

        
class EmployeeRole(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# Create your models here.
class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('savings', 'Savings'),
        ('current', 'Current'),
        ('business', 'Business'),
    ]
    
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50, unique=True)
    bank_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    ifsc_code = models.CharField(max_length=11)
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default='current'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.account_name} - {self.account_number}"
    
    class Meta:
        ordering = ['-created_at']


class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('Individual', 'Individual'),
        ('Business', 'Business'),
    ]
    
    SALUTATION_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        ('Dr', 'Dr'),
    ]
    
    customer_type = models.CharField(
        max_length=50,
        choices=CUSTOMER_TYPE_CHOICES,
        default='Individual'
    )
    salutation = models.CharField(max_length=10, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    display_name = models.CharField(max_length=255)
    place = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    same_as_whatsapp = models.BooleanField(default=False)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    work_number = models.CharField(max_length=20, blank=True, null=True)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.display_name} - {self.contact_number}"
    
    class Meta:
        ordering = ['-created_at']


class Resort(models.Model):
    RESORT_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    # Basic Information
    resort_name = models.CharField(max_length=255, unique=True)
    resort_place = models.CharField(max_length=255)
    full_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    location_map_link = models.URLField(blank=True, null=True, help_text="Google Map Link")

    # Contact Details
    mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cc_emails = models.TextField(blank=True, null=True, help_text="Comma-separated CC email addresses")

    # Owner / Legal Details
    owner_manager_name = models.CharField(max_length=200, blank=True, null=True)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    business_registration_number = models.CharField(max_length=50, blank=True, null=True)
    registration_certificate = models.FileField(upload_to='resorts/certificates/', blank=True, null=True)
    id_proof = models.FileField(upload_to='resorts/id_proofs/', blank=True, null=True, help_text="Aadhaar/PAN Upload")

    # Property Details
    description = models.TextField(blank=True, null=True)
    number_of_rooms = models.PositiveIntegerField(blank=True, null=True)
    amenities = models.TextField(blank=True, null=True, help_text="Comma-separated amenities")
    resort_images = models.FileField(upload_to='resorts/images/', blank=True, null=True, help_text="Multiple images can be uploaded separately")
    resort_video = models.FileField(upload_to='resorts/videos/', blank=True, null=True)

    # Online Presence (Optional)
    website_url = models.URLField(blank=True, null=True)
    social_media_links = models.TextField(blank=True, null=True, help_text="Comma-separated social media links")
    google_listing_link = models.URLField(blank=True, null=True)

    # Status and timestamps
    status = models.CharField(
        max_length=20,
        choices=RESORT_STATUS_CHOICES,
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.resort_name

    @property
    def amenity_list(self):
        if self.amenities:
            return [a.strip() for a in self.amenities.split(",") if a.strip()]
        return []

    @property
    def cc_emails_list(self):
        if self.cc_emails:
            return [email.strip() for email in self.cc_emails.split(",") if email.strip()]
        return []

    @property
    def social_media_list(self):
        if self.social_media_links:
            return [link.strip() for link in self.social_media_links.split(",") if link.strip()]
        return []

    class Meta:
        ordering = ['-created_at']


class ResortRoomType(models.Model):
    resort = models.ForeignKey('Resort', on_delete=models.CASCADE, related_name='room_types')
    room_type_name = models.CharField(max_length=150)
    total_rooms = models.PositiveIntegerField(default=0)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_guests = models.PositiveIntegerField(default=1)
    room_size = models.CharField(max_length=100, blank=True, null=True)
    amenities = models.TextField(blank=True, null=True, help_text='Comma-separated amenity values (AC, WiFi, Balcony, etc.)')
    room_images = models.FileField(upload_to='resorts/room_types/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.room_type_name} ({self.resort.resort_name})"

    @property
    def amenities_list(self):
        if self.amenities:
            return [x.strip() for x in self.amenities.split(',') if x.strip()]
        return []

    @property
    def room_type_image_list(self):
        # Support both new multiple room type image records and legacy single room_images field
        if self.room_type_images.exists():
            return self.room_type_images.all()
        if self.room_images:
            class LegacyImageObject:
                def __init__(self, image):
                    self.image = image
            return [LegacyImageObject(self.room_images)]
        return []

    class Meta:
        ordering = ['-created_at']


class ResortRoomTypeImage(models.Model):
    room_type = models.ForeignKey('ResortRoomType', on_delete=models.CASCADE, related_name='room_type_images')
    image = models.ImageField(upload_to='resorts/room_type_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_type.room_type_name} - {self.image.name}"

    class Meta:
        ordering = ['-uploaded_at']


class ResortImage(models.Model):
    resort = models.ForeignKey('Resort', on_delete=models.CASCADE, related_name='resort_images_list')
    image = models.ImageField(upload_to='resorts/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resort.resort_name} - {self.image.name}"

    class Meta:
        ordering = ['-uploaded_at']


class Meal(models.Model):
    MEAL_STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
    ]
    
    MEAL_TYPE_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
        ('both', 'Both'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    included_meals = models.CharField(max_length=500, blank=True, null=True)
    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_TYPE_CHOICES,
        default='both'
    )
    price_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Price per person in INR"
    )
    children_pricing = models.TextField(
        blank=True,
        null=True,
        default='[]',
        help_text="JSON list of age ranges with prices: [{'min_age': 0, 'max_age': 5, 'price': 0}, {'min_age': 6, 'max_age': 12, 'price': 250}]"
    )
    status = models.CharField(
        max_length=20,
        choices=MEAL_STATUS_CHOICES,
        default='Available'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def included_meals_list(self):
        if self.included_meals:
            return [m.strip() for m in self.included_meals.split(',') if m.strip()]
        return []
    
    def get_children_pricing(self):
        """Get children's pricing as a list of dictionaries"""
        import json
        if not self.children_pricing or self.children_pricing == '[]':
            return []
        try:
            return json.loads(self.children_pricing)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def set_children_pricing(self, pricing_list):
        """Set children's pricing from a list of dictionaries"""
        import json
        if not pricing_list:
            self.children_pricing = '[]'
        else:
            self.children_pricing = json.dumps(pricing_list)
    
    class Meta:
        ordering = ['-created_at']


class PackageTransportOption(models.Model):
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE, related_name='transport_options')
    name = models.CharField(max_length=150)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_persons = models.PositiveIntegerField(default=1, help_text='Maximum number of persons this transport can accommodate')

    def __str__(self):
        return f"{self.name} - ₹{self.price_per_person}/person ({self.package.name})"

    class Meta:
        ordering = ['price_per_person']


class Voucher(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    voucher_no = models.CharField(max_length=50, unique=True, blank=True)
    voucher_date = models.DateField(null=True, blank=True)
    sales_person = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    resort = models.ForeignKey(Resort, on_delete=models.SET_NULL, null=True, blank=True)
    checkin_date = models.DateField(null=True, blank=True)
    checkout_date = models.DateField(null=True, blank=True)
    checkin_time = models.TimeField(null=True, blank=True)
    checkout_time = models.TimeField(null=True, blank=True)
    adults = models.IntegerField(default=0)
    children = models.IntegerField(default=0)
    pax_total = models.IntegerField(default=0)
    pax_notes = models.TextField(blank=True, null=True)
    nights = models.IntegerField(default=1)
    room_type = models.CharField(max_length=100, blank=True)
    no_of_rooms = models.IntegerField(default=1)
    meals_plan = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True, blank=True)
    bank_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    package_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    resort_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    from_whytehouse = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note_for_resort = models.TextField(blank=True, null=True)
    note_for_guest = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Voucher {self.voucher_no} - {self.customer.display_name if self.customer else 'N/A'}"
    
    class Meta:
        ordering = ['-voucher_date', '-id']


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=50, unique=True, blank=True)
    invoice_date = models.DateField()
    sales_person = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    resort = models.ForeignKey(Resort, on_delete=models.SET_NULL, null=True)
    checkin_date = models.DateField(null=True, blank=True)
    checkout_date = models.DateField(null=True, blank=True)
    checkin_time = models.TimeField(null=True, blank=True)
    checkout_time = models.TimeField(null=True, blank=True)
    adults = models.IntegerField(default=0)
    children = models.IntegerField(default=0)
    pax_total = models.IntegerField(default=0)
    pax_notes = models.TextField(blank=True, null=True)
    nights = models.IntegerField(default=1)
    room_type = models.CharField(max_length=100, blank=True)
    rooms = models.IntegerField(default=1)
    meals_plan = models.CharField(max_length=50, blank=True)
    bank_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    package_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    resort_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Invoice #{self.invoice_no} - {self.customer.display_name}"
    
    def save(self, *args, **kwargs):
        # Auto-generate invoice number if not provided
        if not self.invoice_no:
            last_invoice = Invoice.objects.filter(invoice_no__startswith='INV').order_by('-invoice_no').first()
            if last_invoice and last_invoice.invoice_no:
                try:
                    last_num = int(last_invoice.invoice_no[3:])
                    self.invoice_no = f'INV{str(last_num + 1).zfill(3)}'
                except (ValueError, IndexError):
                    self.invoice_no = 'INV001'
            else:
                self.invoice_no = 'INV001'
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']

class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('scheduled', 'Scheduled'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blogs"
    )
    package_id = models.CharField(max_length=50, blank=True, null=True)
    
    author_name = models.CharField(max_length=100)
    author_summary = models.TextField(max_length=500)
    reading_time = models.PositiveIntegerField(default=1)
    publish_date = models.DateField()
    
    # Main images
    featured_image = models.ImageField(upload_to='blog_images/featured/', blank=True, null=True)
    featured_image_url = models.URLField(blank=True, null=True)
    
    hashtags = models.CharField(max_length=500, blank=True)
    tags = models.CharField(max_length=255, blank=True, null=True, help_text="Comma separated tags")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def image_url(self):
        return self.featured_image.url if self.featured_image else self.featured_image_url


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog_images/content/')
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image {self.order + 1} for {self.blog.title}"


from django.db import models

class Feedback(models.Model):

    RATING_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    FEEDBACK_TYPE_CHOICES = [
        ('Travel Package', 'Travel Package'),
        ('Customer Service', 'Customer Service'),
        ('Booking Experience', 'Booking Experience'),
        ('Property Management', 'Property Management'),
        ('Website Experience', 'Website Experience'),
        ('Trip Management', 'Trip Management'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=10, blank=True)

    feedback_type = models.CharField(
        max_length=50,
        choices=FEEDBACK_TYPE_CHOICES,
        default='Other'
    )

    rating = models.IntegerField(choices=RATING_CHOICES)
    feedback = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.rating}⭐"


class FeedbackImage(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='feedback_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.feedback.name}"