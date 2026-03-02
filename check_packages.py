import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whytehouse.settings')
django.setup()

from admin_panel.models import TravelPackage

packages = TravelPackage.objects.filter(active=True, category='International')[:4]
print(f'Total International packages: {TravelPackage.objects.filter(active=True, category="International").count()}')
print(f'\nFirst 4 packages:')
for i, pkg in enumerate(packages, 1):
    print(f'{i}. ID: {pkg.id}, Name: {pkg.name}, Has Image: {bool(pkg.image)}')
