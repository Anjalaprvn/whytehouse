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

def check_recent_submissions():
    print("=== CHECKING RECENT CONTACT FORM SUBMISSIONS ===")
    
    # Check recent leads
    recent_leads = Lead.objects.all().order_by('-created_at')[:10]
    print(f"\nRecent Leads ({recent_leads.count()}):")
    for lead in recent_leads:
        print(f"  - ID: {lead.id} | Name: {lead.full_name} | Phone: {lead.mobile_number} | Email: {lead.email} | Source: {lead.source} | Created: {lead.created_at}")
    
    # Check recent inquiries
    recent_inquiries = Inquiry.objects.all().order_by('-created_at')[:10]
    print(f"\nRecent Inquiries ({recent_inquiries.count()}):")
    for inquiry in recent_inquiries:
        print(f"  - ID: {inquiry.id} | Name: {inquiry.name} | Phone: {inquiry.phone} | Email: {inquiry.email} | Package: {inquiry.package} | Created: {inquiry.created_at}")
    
    # Check recent customers
    recent_customers = Customer.objects.all().order_by('-created_at')[:10]
    print(f"\nRecent Customers ({recent_customers.count()}):")
    for customer in recent_customers:
        print(f"  - ID: {customer.id} | Name: {customer.display_name} | Phone: {customer.contact_number} | Email: {customer.email} | Created: {customer.created_at}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    check_recent_submissions()