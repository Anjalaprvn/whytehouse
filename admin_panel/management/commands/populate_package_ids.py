from django.core.management.base import BaseCommand
from admin_panel.models import TravelPackage

class Command(BaseCommand):
    help = 'Populate package_id for existing packages'

    def handle(self, *args, **options):
        packages = TravelPackage.objects.filter(package_id__isnull=True).order_by('id')
        
        if not packages.exists():
            self.stdout.write(self.style.SUCCESS('No packages without IDs found'))
            return
        
        # Get the highest existing package ID
        last_package = TravelPackage.objects.filter(package_id__startswith='PKG').order_by('-package_id').first()
        if last_package and last_package.package_id:
            try:
                last_num = int(last_package.package_id[3:])
            except (ValueError, IndexError):
                last_num = 0
        else:
            last_num = 0
        
        count = 0
        for package in packages:
            last_num += 1
            package.package_id = f'PKG{str(last_num).zfill(3)}'
            package.save()
            count += 1
            self.stdout.write(f'Updated {package.name} with ID {package.package_id}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully populated {count} package IDs'))
