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

def create_test_inquiry():
    print("=== CREATING TEST INQUIRY FOR CUSTOMER INQUIRIES ===")
    
    # Create a test inquiry that should appear in Customer Inquiries
    inquiry = Inquiry.objects.create(
        name="TEST CUSTOMER INQUIRY",
        email="testinquiry@gmail.com",
        phone="+919999888777",
        package="General Enquiry Test Package",
        message="This is a test inquiry that should appear in Customer Inquiries page immediately!",
        status="New"
    )
    
    print(f"Created test inquiry:")
    print(f"  ID: {inquiry.id}")
    print(f"  Name: {inquiry.name}")
    print(f"  Email: {inquiry.email}")
    print(f"  Phone: {inquiry.phone}")
    print(f"  Package: {inquiry.package}")
    print(f"  Message: {inquiry.message}")
    print(f"  Status: {inquiry.status}")
    print(f"  Created: {inquiry.created_at}")
    
    print("\\nNow check your Customer Inquiries page - this should appear at the top!")
    print("URL: http://127.0.0.1:8000/admin/customer-inquiries/")

if __name__ == "__main__":
    create_test_inquiry()