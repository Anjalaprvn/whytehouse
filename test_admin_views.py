#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('c:\\Users\\HANIMA\\OneDrive\\Desktop\\whytehouse')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whytehouse.settings')
django.setup()

from admin_panel.models import Lead, Inquiry
from admin_panel.views import lead_management, customer_inquiries
from django.test import RequestFactory
from django.contrib.auth.models import User

def test_admin_views():
    print("=== TESTING ADMIN VIEWS ===")
    
    # Create a mock request
    factory = RequestFactory()
    
    # Test lead management view
    print("\\n1. Testing Lead Management View:")
    request = factory.get('/admin/leads/')
    request.GET = {}  # No filters
    
    try:
        # Get the leads that the view would return
        leads = Lead.objects.all().order_by('-created_at')
        print(f"   Total leads in database: {leads.count()}")
        print("   Recent leads:")
        for lead in leads[:5]:
            print(f"     - {lead.full_name} | {lead.mobile_number} | {lead.email} | {lead.source}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test customer inquiries view
    print("\\n2. Testing Customer Inquiries View:")
    try:
        inquiries = Inquiry.objects.all().order_by('-created_at')
        print(f"   Total inquiries in database: {inquiries.count()}")
        print("   Recent inquiries:")
        for inquiry in inquiries[:5]:
            print(f"     - {inquiry.name} | {inquiry.phone} | {inquiry.email} | {inquiry.package}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    print("\\n3. Checking for empty/null data:")
    empty_leads = Lead.objects.filter(full_name__isnull=True) | Lead.objects.filter(full_name='')
    print(f"   Leads with empty names: {empty_leads.count()}")
    
    empty_inquiries = Inquiry.objects.filter(name__isnull=True) | Inquiry.objects.filter(name='')
    print(f"   Inquiries with empty names: {empty_inquiries.count()}")
    
    print("\\n=== ADMIN VIEW TEST COMPLETE ===")

if __name__ == "__main__":
    test_admin_views()