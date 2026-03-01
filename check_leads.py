import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whytehouse.settings')
django.setup()

from admin_panel.models import Lead

leads = Lead.objects.filter(enquiry_type='General')
print(f'Total General leads: {leads.count()}')
print(f'New: {leads.filter(status="New").count()}')
print(f'Contacted: {leads.filter(status="Contacted").count()}')
print(f'Converted: {leads.filter(status="Converted").count()}')
print(f'Junk: {leads.filter(status="Junk").count()}')

print("\nAll leads with their status:")
for lead in leads:
    print(f"ID: {lead.id}, Name: {lead.full_name}, Status: {lead.status}")
