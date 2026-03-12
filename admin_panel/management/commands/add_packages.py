from django.core.management.base import BaseCommand
from admin_panel.models import TravelPackage, Destination
from decimal import Decimal

class Command(BaseCommand):
    help = 'Add 2 sample packages under each destination'

    def handle(self, *args, **options):
        destinations = Destination.objects.all()
        
        if not destinations.exists():
            self.stdout.write(self.style.ERROR('No destinations found. Please create destinations first.'))
            return
        
        for destination in destinations:
            # Check if packages already exist for this destination
            existing_count = TravelPackage.objects.filter(destination=destination).count()
            
            if existing_count >= 2:
                self.stdout.write(self.style.WARNING(f'Destination "{destination.name}" already has {existing_count} packages. Skipping...'))
                continue
            
            # Create first package
            package1_name = f"{destination.name} Adventure Package"
            package1, created1 = TravelPackage.objects.get_or_create(
                name=package1_name,
                destination=destination,
                defaults={
                    'category': destination.category,
                    'location': destination.name,
                    'country': destination.country,
                    'price': Decimal('15999.00'),
                    'duration': '3 Days 2 Nights',
                    'description': f'Experience the best of {destination.name} with our exclusive adventure package. Includes accommodation, meals, and guided tours.',
                    'active': True,
                    'itinerary': f'Day 1: Arrival and city tour\nDay 2: Adventure activities\nDay 3: Departure',
                    'inclusions': 'Accommodation, Breakfast, Lunch, Dinner, Guided tours, Transportation',
                    'exclusions': 'Flights, Travel insurance, Personal expenses',
                }
            )
            
            if created1:
                self.stdout.write(self.style.SUCCESS(f'✓ Created package: {package1_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Package already exists: {package1_name}'))
            
            # Create second package
            package2_name = f"{destination.name} Luxury Escape"
            package2, created2 = TravelPackage.objects.get_or_create(
                name=package2_name,
                destination=destination,
                defaults={
                    'category': destination.category,
                    'location': destination.name,
                    'country': destination.country,
                    'price': Decimal('24999.00'),
                    'duration': '4 Days 3 Nights',
                    'description': f'Indulge in luxury at {destination.name}. Premium accommodations, fine dining, and exclusive experiences await.',
                    'active': True,
                    'itinerary': f'Day 1: Arrival and welcome dinner\nDay 2: Spa and relaxation\nDay 3: Cultural tour\nDay 4: Departure',
                    'inclusions': 'Luxury accommodation, All meals, Spa treatments, Guided tours, Airport transfers',
                    'exclusions': 'Flights, Travel insurance, Personal expenses',
                }
            )
            
            if created2:
                self.stdout.write(self.style.SUCCESS(f'✓ Created package: {package2_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Package already exists: {package2_name}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Package creation completed!'))
