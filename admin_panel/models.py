from django.db import models
from datetime import time
from django.utils import timezone

# LEAD MODEL
class Lead(models.Model):
    SOURCE_CHOICES = (
        ('Direct', 'Direct Contact'),
        ('Website', 'Website'),
        ('Manual', 'Manual Entry'),
        ('Referral', 'Referral'),
    )
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    place = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='Manual')
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.full_name

# AMENITY MODEL
class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name_plural = "Amenities"
        ordering = ['name']
    def __str__(self):
        return self.name

# PROPERTY MODEL
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
    amenities = models.ManyToManyField(Amenity, blank=True)
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

# TRAVEL PACKAGE MODEL
class TravelPackage(models.Model):
    CATEGORY_CHOICES = (
        ('Domestic', 'Domestic'),
        ('International', 'International'),
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='travel_packages/', blank=True, null=True)
    active = models.BooleanField(default=True)
    itinerary = models.TextField(blank=True, null=True)
    inclusions = models.TextField(blank=True, null=True)
    exclusions = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

# INQUIRY MODEL
class Inquiry(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Converted', 'Converted'),
        ('Junk', 'Junk'),
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

        
# Create your models here.
class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('savings', 'Savings'),
        ('current', 'Current'),
        ('checking', 'Checking'),
    ]
    
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50, unique=True)
    bank_name = models.CharField(max_length=255)
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
        ('Corporate', 'Corporate'),
        ('Government', 'Government'),
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
    
    resort_name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=RESORT_STATUS_CHOICES,
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.resort_name
    
    class Meta:
        ordering = ['-created_at']


class Meal(models.Model):
    MEAL_STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    included_meals = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=MEAL_STATUS_CHOICES,
        default='Available'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']


class Voucher(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)

    voucher_no = models.CharField(max_length=50, unique=True)
    voucher_date = models.DateField(null=True, blank=True)

    sales_person = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    resort = models.ForeignKey(Resort, on_delete=models.SET_NULL, null=True, blank=True)

    checkin_date = models.DateField(null=True, blank=True)
    checkout_date = models.DateField(null=True, blank=True)

    # ✅ stop migration prompts
    checkin_time = models.TimeField(default=time(0, 0))
    checkout_time = models.TimeField(default=time(0, 0))

    adults = models.IntegerField(default=0)
    children = models.IntegerField(default=0)
    nights = models.IntegerField(default=1)

    # ✅ safer (avoid non-null issues)
    pax_notes = models.TextField(blank=True, default="")

    room_type = models.CharField(max_length=100, blank=True, default="")
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

    note_for_resort = models.TextField(max_length=130, blank=True, default="")
    note_for_guest = models.TextField(max_length=130, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.voucher_no} - {self.customer.display_name if self.customer else 'N/A'}"

    class Meta:
        ordering = ['-created_at']


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=50, unique=True)
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
    
    class Meta:
        ordering = ['-created_at']