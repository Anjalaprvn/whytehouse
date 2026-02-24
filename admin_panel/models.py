from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
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
    source = models.CharField(
    max_length=50,
    choices=SOURCE_CHOICES,
    default='Manual'
)    
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
from django.db import models

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name_plural = "Amenities"
        ordering = ['name']

    def __str__(self):
        return self.name

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