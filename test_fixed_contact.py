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
    
    print(f\"Processing submission:\")\n    print(f\"  Name: {name}\")\n    print(f\"  Email: {email}\")\n    print(f\"  Phone: {phone} -> Full Phone: {full_phone}\")\n    print(f\"  Package: {package}\")\n    print(f\"  Subject: {subject} -> Enquiry Type: {enquiry_type}\")\n    print(f\"  Message: {message}\")\n    \n    try:\n        # Create Customer record\n        name_parts = name.split(' ', 1)\n        first_name = name_parts[0]\n        last_name = name_parts[1] if len(name_parts) > 1 else ''\n        \n        customer, created = Customer.objects.get_or_create(\n            contact_number=full_phone,\n            defaults={\n                'first_name': first_name,\n                'last_name': last_name,\n                'display_name': name,\n                'email': email,\n                'whatsapp_number': full_phone,\n                'same_as_whatsapp': True,\n                'customer_type': 'Individual',\n                'place': ''\n            }\n        )\n        print(f\"\\nCustomer: {'Created' if created else 'Updated'} - ID: {customer.id}\")\n        \n        # Create Lead record\n        lead = Lead.objects.create(\n            full_name=name,\n            mobile_number=full_phone,\n            email=email,\n            place=None,\n            source='Website',\n            enquiry_type=enquiry_type,\n            message=message,\n            package=package,\n            remarks=f'Subject: {subject}\\nPackage: {package}\\nMessage: {message}'\n        )\n        print(f\"Lead: Created - ID: {lead.id}\")\n        \n        # Create Inquiry record\n        inquiry = Inquiry.objects.create(\n            lead=lead,\n            name=name,\n            email=email,\n            phone=full_phone,\n            package=package or 'General Inquiry',\n            message=message,\n            status='New'\n        )\n        print(f\"Inquiry: Created - ID: {inquiry.id}\")\n        \n        print(\"\\nSUCCESS: Fixed contact form submission created successfully!\")\n        print(\"\\nNow check your admin panel:\")\n        print(\"  - Lead Management: Should show 'John Doe Fixed' with phone +919876543210\")\n        print(\"  - Customer Inquiries: Should show the same inquiry\")\n        \n    except Exception as e:\n        print(f\"ERROR: {str(e)}\")\n        import traceback\n        traceback.print_exc()\n\nif __name__ == \"__main__\":\n    test_fixed_contact_form()