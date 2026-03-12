#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('c:\\Users\\HANIMA\\OneDrive\\Desktop\\whytehouse')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whytehouse.settings')
django.setup()

from admin_panel.models import Lead, Inquiry, Customer

def test_customer_inquiries_view():
    print("=== TESTING CUSTOMER INQUIRIES VIEW ===")
    
    # Get all inquiries (same as customer_inquiries view)
    inquiries = Inquiry.objects.all().order_by('-created_at')
    
    print(f"Total inquiries found: {inquiries.count()}")
    print("Recent inquiries:")
    for inquiry in inquiries[:10]:
        print(f"  - ID: {inquiry.id}")
        print(f"    Name: {inquiry.name}")
        print(f"    Email: {inquiry.email}")
        print(f"    Phone: {inquiry.phone}")
        print(f"    Package: {inquiry.package}")
        print(f"    Message: {inquiry.message}")
        print(f"    Status: {inquiry.status}")
        print(f"    Created: {inquiry.created_at}")
        print(f"    Lead: {inquiry.lead}")
        print()
    
    # Count by status
    all_inquiries = Inquiry.objects.all()
    new_count = all_inquiries.filter(status='New').count()
    contacted_count = all_inquiries.filter(status='Contacted').count()
    converted_count = all_inquiries.filter(status='Converted').count()
    junk_count = all_inquiries.filter(status='Junk').count()
    
    print(f"Status counts:")
    print(f"  Total: {all_inquiries.count()}")
    print(f"  New: {new_count}")
    print(f"  Contacted: {contacted_count}")
    print(f"  Converted: {converted_count}")
    print(f"  Junk: {junk_count}")
    
    print("\\n=== THESE SHOULD APPEAR IN CUSTOMER INQUIRIES PAGE ===")

if __name__ == "__main__":
    test_customer_inquiries_view()