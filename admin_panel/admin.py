from django.contrib import admin
from .models import (
    Lead, Inquiry, TravelPackage, Destination, Property,
    BlogCategory, Blog, BlogImage, Feedback, FeedbackImage,
    Customer, Employee, Account, Resort, Meal, Invoice
)

# Inquiry Admin Inline
class InquiryInline(admin.TabularInline):
    model = Inquiry
    extra = 0
    fields = ('name', 'email', 'phone', 'package', 'message', 'status')
    readonly_fields = ('name', 'email', 'phone', 'package', 'message', 'created_at')
    can_delete = False

# Lead Admin
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'mobile_number', 'source', 'enquiry_type', 'status', 'employee', 'created_at')
    list_filter = ('source', 'enquiry_type', 'status', 'employee', 'created_at')
    search_fields = ('full_name', 'mobile_number', 'place', 'employee__name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [InquiryInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'mobile_number', 'place')
        }),
        ('Enquiry Details', {
            'fields': ('source', 'enquiry_type', 'status', 'employee')
        }),
        ('Additional Info', {
            'fields': ('remarks',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# Inquiry Admin
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'package', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'package')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('lead', 'package', 'message', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

# Travel Package Admin
@admin.register(TravelPackage)
class TravelPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'price', 'active')
    list_filter = ('category', 'active')
    search_fields = ('name', 'location', 'country')

# Destination Admin
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'category', 'is_popular')
    list_filter = ('category', 'is_popular')
    search_fields = ('name', 'country')

# Property Admin
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_type', 'location', 'is_active')
    list_filter = ('property_type', 'is_active')
    search_fields = ('name', 'location')

# Blog Category Admin
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

# Blog Admin
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category', 'publish_date', 'author_name')
    list_filter = ('status', 'category', 'publish_date')
    search_fields = ('title', 'author_name')
    prepopulated_fields = {'slug': ('title',)}

# Blog Image Admin
@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ('blog', 'order', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('blog__title',)

# Feedback Admin
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'rating', 'feedback_type', 'featured', 'created_at')
    list_filter = ('rating', 'feedback_type', 'featured', 'created_at')
    search_fields = ('name', 'email')

# Feedback Image Admin
@admin.register(FeedbackImage)
class FeedbackImageAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'uploaded_at')
    list_filter = ('uploaded_at',)

# Customer Admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'contact_number', 'customer_type', 'created_at')
    list_filter = ('customer_type', 'created_at')
    search_fields = ('display_name', 'contact_number', 'email')

# Employee Admin
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role', 'department', 'status')
    list_filter = ('status', 'department')
    search_fields = ('name', 'email')

# Account Admin
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_number', 'bank_name', 'account_type')
    list_filter = ('account_type', 'bank_name')
    search_fields = ('account_name', 'account_number')

# Resort Admin
@admin.register(Resort)
class ResortAdmin(admin.ModelAdmin):
    list_display = ('resort_name', 'resort_place', 'mobile', 'status')
    list_filter = ('status',)
    search_fields = ('resort_name', 'resort_place', 'mobile', 'email')


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'included_meals', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'included_meals']

# Invoice Admin
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'customer', 'invoice_date', 'total', 'pending')
    list_filter = ('invoice_date',)
    search_fields = ('invoice_no', 'customer__display_name')
