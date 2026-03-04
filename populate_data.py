import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whytehouse.settings')
django.setup()

from admin_panel.models import Destination, TravelPackage

# Clear existing data (optional)
print("Clearing existing destinations and packages...")
TravelPackage.objects.all().delete()
Destination.objects.all().delete()

# Domestic Destinations
domestic_destinations = [
    {"name": "Goa", "country": "India", "description": "Beautiful beaches and vibrant nightlife"},
    {"name": "Kerala", "country": "India", "description": "God's own country with backwaters and hill stations"},
    {"name": "Rajasthan", "country": "India", "description": "Land of kings with majestic forts and palaces"},
    {"name": "Himachal Pradesh", "country": "India", "description": "Scenic mountains and adventure activities"},
    {"name": "Andaman", "country": "India", "description": "Pristine beaches and crystal clear waters"},
]

# International Destinations
international_destinations = [
    {"name": "Dubai", "country": "UAE", "description": "Luxury shopping and modern architecture"},
    {"name": "Bali", "country": "Indonesia", "description": "Tropical paradise with temples and beaches"},
    {"name": "Maldives", "country": "Maldives", "description": "Luxury resorts and underwater beauty"},
    {"name": "Thailand", "country": "Thailand", "description": "Exotic temples and vibrant street life"},
    {"name": "Singapore", "country": "Singapore", "description": "Modern city-state with diverse attractions"},
]

print("\nAdding Domestic Destinations and Packages...")
for idx, dest_data in enumerate(domestic_destinations, 1):
    dest = Destination.objects.create(
        name=dest_data["name"],
        country=dest_data["country"],
        category="Domestic",
        description=dest_data["description"],
        is_popular=idx <= 3
    )
    print(f"[+] Added destination: {dest.name}")
    
    # Package 1
    TravelPackage.objects.create(
        name=f"{dest.name} Beach Paradise",
        category="Domestic",
        destination=dest,
        location=dest.name,
        country=dest.country,
        price=15000 + (idx * 2000),
        duration="3 Days 2 Nights",
        description=f"Explore the best of {dest.name} with comfortable stays and guided tours",
        itinerary=f"Day 1: Arrival and local sightseeing\nDay 2: Full day tour\nDay 3: Departure",
        inclusions="Hotel accommodation\nBreakfast\nSightseeing\nTransfers",
        exclusions="Lunch and Dinner\nPersonal expenses\nTravel insurance",
        active=True
    )
    print(f"  [+] Added package: {dest.name} Beach Paradise")
    
    # Package 2
    TravelPackage.objects.create(
        name=f"{dest.name} Adventure Tour",
        category="Domestic",
        destination=dest,
        location=dest.name,
        country=dest.country,
        price=20000 + (idx * 2500),
        duration="5 Days 4 Nights",
        description=f"Experience adventure and culture in {dest.name} with premium amenities",
        itinerary=f"Day 1: Arrival\nDay 2-4: Adventure activities and sightseeing\nDay 5: Departure",
        inclusions="Hotel accommodation\nAll meals\nAdventure activities\nTransfers",
        exclusions="Personal expenses\nTravel insurance\nExtra activities",
        active=True
    )
    print(f"  [+] Added package: {dest.name} Adventure Tour")

print("\nAdding International Destinations and Packages...")
for idx, dest_data in enumerate(international_destinations, 1):
    dest = Destination.objects.create(
        name=dest_data["name"],
        country=dest_data["country"],
        category="International",
        description=dest_data["description"],
        is_popular=idx <= 3
    )
    print(f"[+] Added destination: {dest.name}")
    
    # Package 1
    TravelPackage.objects.create(
        name=f"{dest.name} Luxury Escape",
        category="International",
        destination=dest,
        location=dest.name,
        country=dest.country,
        price=45000 + (idx * 5000),
        duration="4 Days 3 Nights",
        description=f"Luxury experience in {dest.name} with premium hotels and exclusive tours",
        itinerary=f"Day 1: Arrival and welcome dinner\nDay 2-3: City tours and activities\nDay 4: Departure",
        inclusions="Flight tickets\n5-star hotel\nAll meals\nSightseeing\nVisa assistance",
        exclusions="Personal expenses\nTravel insurance\nOptional activities",
        active=True
    )
    print(f"  [+] Added package: {dest.name} Luxury Escape")
    
    # Package 2
    TravelPackage.objects.create(
        name=f"{dest.name} Family Package",
        category="International",
        destination=dest,
        location=dest.name,
        country=dest.country,
        price=65000 + (idx * 7000),
        duration="6 Days 5 Nights",
        description=f"Perfect family vacation in {dest.name} with kid-friendly activities",
        itinerary=f"Day 1: Arrival\nDay 2-5: Family activities and sightseeing\nDay 6: Departure",
        inclusions="Flight tickets\nFamily suite accommodation\nAll meals\nFamily activities\nVisa assistance\nAirport transfers",
        exclusions="Personal expenses\nTravel insurance\nExtra excursions",
        active=True
    )
    print(f"  [+] Added package: {dest.name} Family Package")

print("\n" + "="*50)
print("DATA POPULATION COMPLETE!")
print("="*50)
print(f"Total Destinations: {Destination.objects.count()}")
print(f"  - Domestic: {Destination.objects.filter(category='Domestic').count()}")
print(f"  - International: {Destination.objects.filter(category='International').count()}")
print(f"Total Packages: {TravelPackage.objects.count()}")
print(f"  - Domestic: {TravelPackage.objects.filter(category='Domestic').count()}")
print(f"  - International: {TravelPackage.objects.filter(category='International').count()}")
print("="*50)
