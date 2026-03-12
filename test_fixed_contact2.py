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

def test_fixed_contact_form():
    print("=== TESTING FIXED CONTACT FORM ===")
    
    # Test data (simulating form submission)
    form_data = {
        'name': 'John Doe Fixed',
        'email': 'johndoe@gmail.com',
        'phone': '9876543210',
        'country': '+91',
        'package': 'Kerala Tour Package',
        'message': 'I am interested in your Kerala tour package. Please provide more details.',
        'subject': 'Package related'
    }
    
    # Process the data (same as in contact view)
    name = form_data['name'].strip()
    email = form_data['email'].strip()
    phone = form_data['phone'].strip()
    country_code = form_data['country'].strip()
    package = form_data['package'].strip()
    message = form_data['message'].strip()
    subject = form_data['subject'].strip()
    
    # Combine country code with phone number
    full_phone = f"{country_code}{phone}" if phone else ''
    
    # Map subject to enquiry type
    subject_mapping = {
        'Package related': 'General',
        'Holiday Package': 'General', 
        'Property Management': 'Hospitality',
        'General Enquiry': 'General',
    }
    enquiry_type = subject_mapping.get(subject, 'General')
    
    print("Processing submission:")
    print(f"  Name: {name}")
    print(f"  Email: {email}")
    print(f"  Phone: {phone} -> Full Phone: {full_phone}")
    print(f"  Package: {package}")
    print(f"  Subject: {subject} -> Enquiry Type: {enquiry_type}")
    print(f"  Message: {message}")
    
    try:
        # Create Customer record
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        customer, created = Customer.objects.get_or_create(
            contact_number=full_phone,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'display_name': name,
                'email': email,
                'whatsapp_number': full_phone,
                'same_as_whatsapp': True,
                'customer_type': 'Individual',
                'place': ''
            }
        )
        print(f"Customer: {'Created' if created else 'Updated'} - ID: {customer.id}")
        
        # Create Lead record
        lead = Lead.objects.create(
            full_name=name,
            mobile_number=full_phone,
            email=email,
            place=None,
            source='Website',
            enquiry_type=enquiry_type,
            message=message,
            package=package,
            remarks=f'Subject: {subject}\\nPackage: {package}\\nMessage: {message}'
        )
        print(f"Lead: Created - ID: {lead.id}")
        
        # Create Inquiry record
        inquiry = Inquiry.objects.create(
            lead=lead,
            name=name,
            email=email,
            phone=full_phone,
            package=package or 'General Inquiry',
            message=message,
            status='New'
        )
        print(f"Inquiry: Created - ID: {inquiry.id}")
        
        print("SUCCESS: Fixed contact form submission created successfully!")
        print("Now check your admin panel:")
        print("  - Lead Management: Should show 'John Doe Fixed' with phone +919876543210")
        print("  - Customer Inquiries: Should show the same inquiry")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fixed_contact_form()