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

def create_test_contact_submission():
    print("=== CREATING TEST CONTACT FORM SUBMISSION ===")
    
    # Test data
    name = "Test User"
    email = "testuser@gmail.com"
    phone = "9999999999"
    package = "Test Package"
    message = "This is a test message from contact form"
    subject = "General Enquiry"
    
    # Map subject to enquiry type (same as in contact view)
    subject_mapping = {
        'Package related': 'General',
        'Holiday Package': 'General', 
        'Property Management': 'Hospitality',
        'General Enquiry': 'General',
    }
    enquiry_type = subject_mapping.get(subject, 'General')
    
    print(f"Creating submission with:")
    print(f"  Name: {name}")
    print(f"  Email: {email}")
    print(f"  Phone: {phone}")
    print(f"  Package: {package}")
    print(f"  Subject: {subject} -> Enquiry Type: {enquiry_type}")
    print(f"  Message: {message}")
    
    try:
        # Create Customer record (same as in contact view)
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        customer, created = Customer.objects.get_or_create(
            contact_number=phone,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'display_name': name,
                'email': email,
                'whatsapp_number': phone,
                'same_as_whatsapp': True,
                'customer_type': 'Individual',
                'place': ''
            }
        )
        print(f"Customer: {'Created' if created else 'Updated'} - ID: {customer.id}")
        
        # Create Lead record (same as in contact view)
        lead = Lead.objects.create(
            full_name=name,
            mobile_number=phone,
            email=email,
            place=None,
            source='Website',
            enquiry_type=enquiry_type,
            message=message,
            package=package,
            remarks=f'Subject: {subject}\\nPackage: {package}\\nMessage: {message}'
        )
        print(f"Lead: Created - ID: {lead.id}")
        
        # Create Inquiry record (same as in contact view)
        inquiry = Inquiry.objects.create(
            lead=lead,
            name=name,
            email=email,
            phone=phone,
            package=package or 'General Inquiry',
            message=message,
            status='New'
        )
        print(f"Inquiry: Created - ID: {inquiry.id}")
        
        print("\\n✅ SUCCESS: Test contact form submission created successfully!")
        print("\\nNow check your admin panel:")
        print("  - Lead Management: Should show the new lead")
        print("  - Customer Inquiries: Should show the new inquiry")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_test_contact_submission()