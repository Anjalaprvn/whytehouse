import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whytehouse.settings')
django.setup()

from admin_panel.models import TravelPackage, Destination

# Get destinations
kozhikode = Destination.objects.get(id=16)
munnar = Destination.objects.get(id=17)
wayanad = Destination.objects.get(id=18)
ooty = Destination.objects.get(id=19)

packages = [
    # Kozhikode packages
    {
        'name': 'Kozhikode Beach & Heritage Tour',
        'destination': kozhikode,
        'category': 'Domestic',
        'price': 8500,
        'duration': '2 Days 1 Night',
        'location': 'Kozhikode',
        'country': 'India',
        'description': 'Explore the beautiful beaches and rich heritage of Kozhikode. Visit Kappad Beach, Beypore Port, and enjoy authentic Malabar cuisine.',
        'itinerary': 'Day 1: Arrival, Kappad Beach, Beypore Port\nDay 2: Kozhikode Beach, Sweet Street, Departure',
        'inclusions': 'Accommodation\nBreakfast\nSightseeing\nTransportation',
        'exclusions': 'Lunch and Dinner\nPersonal Expenses\nEntry Fees',
        'active': True
    },
    {
        'name': 'Kozhikode Culinary Experience',
        'destination': kozhikode,
        'category': 'Domestic',
        'price': 6500,
        'duration': '1 Day',
        'location': 'Kozhikode',
        'country': 'India',
        'description': 'A food lover\'s paradise! Experience the authentic flavors of Malabar cuisine with guided food tours and cooking sessions.',
        'itinerary': 'Morning: Traditional breakfast tour\nAfternoon: Cooking class\nEvening: Street food exploration',
        'inclusions': 'Food tastings\nCooking class\nGuide\nTransportation',
        'exclusions': 'Accommodation\nPersonal Expenses',
        'active': True
    },
    # Wayanad packages
    {
        'name': 'Wayanad Wildlife & Nature Escape',
        'destination': wayanad,
        'category': 'Domestic',
        'price': 12500,
        'duration': '3 Days 2 Nights',
        'location': 'Wayanad',
        'country': 'India',
        'description': 'Immerse yourself in the lush greenery of Wayanad. Visit wildlife sanctuaries, waterfalls, and ancient caves.',
        'itinerary': 'Day 1: Arrival, Edakkal Caves\nDay 2: Wildlife Safari, Soochipara Falls\nDay 3: Pookode Lake, Departure',
        'inclusions': 'Accommodation\nBreakfast and Dinner\nSafari\nSightseeing\nTransportation',
        'exclusions': 'Lunch\nEntry Fees\nPersonal Expenses',
        'active': True
    },
    {
        'name': 'Wayanad Adventure Package',
        'destination': wayanad,
        'category': 'Domestic',
        'price': 15000,
        'duration': '4 Days 3 Nights',
        'location': 'Wayanad',
        'country': 'India',
        'description': 'Perfect for adventure enthusiasts! Trekking, zip-lining, and camping in the Western Ghats.',
        'itinerary': 'Day 1: Arrival, Chembra Peak trek\nDay 2: Zip-lining, Meenmutty Falls\nDay 3: Camping, Bonfire\nDay 4: Banasura Dam, Departure',
        'inclusions': 'Accommodation\nAll Meals\nAdventure Activities\nGuide\nTransportation',
        'exclusions': 'Personal Expenses\nTravel Insurance',
        'active': True
    },
    # Munnar packages
    {
        'name': 'Munnar Tea Garden Retreat',
        'destination': munnar,
        'category': 'Domestic',
        'price': 11000,
        'duration': '3 Days 2 Nights',
        'location': 'Munnar',
        'country': 'India',
        'description': 'Experience the serene beauty of Munnar\'s tea plantations. Visit tea factories, enjoy scenic views, and relax in nature.',
        'itinerary': 'Day 1: Arrival, Tea Museum, Tea Gardens\nDay 2: Mattupetty Dam, Echo Point, Kundala Lake\nDay 3: Top Station, Departure',
        'inclusions': 'Accommodation\nBreakfast\nTea Factory Tour\nSightseeing\nTransportation',
        'exclusions': 'Lunch and Dinner\nEntry Fees\nPersonal Expenses',
        'active': True
    },
    {
        'name': 'Munnar Honeymoon Special',
        'destination': munnar,
        'category': 'Domestic',
        'price': 18000,
        'duration': '4 Days 3 Nights',
        'location': 'Munnar',
        'country': 'India',
        'description': 'A romantic getaway in the hills of Munnar. Luxury accommodation, candlelight dinners, and scenic spots.',
        'itinerary': 'Day 1: Arrival, Welcome drink, Leisure\nDay 2: Eravikulam National Park, Tea Gardens\nDay 3: Anamudi Peak, Romantic dinner\nDay 4: Attukal Waterfalls, Departure',
        'inclusions': 'Luxury Accommodation\nAll Meals\nCandlelight Dinner\nFlower Decoration\nSightseeing\nTransportation',
        'exclusions': 'Personal Expenses\nAdditional Activities',
        'active': True
    },
    # Ooty packages
    {
        'name': 'Ooty Hill Station Delight',
        'destination': ooty,
        'category': 'Domestic',
        'price': 10500,
        'duration': '3 Days 2 Nights',
        'location': 'Ooty',
        'country': 'India',
        'description': 'Discover the Queen of Hill Stations. Toy train ride, botanical gardens, and scenic viewpoints.',
        'itinerary': 'Day 1: Arrival, Botanical Gardens, Ooty Lake\nDay 2: Toy Train, Doddabetta Peak, Tea Factory\nDay 3: Rose Garden, Shopping, Departure',
        'inclusions': 'Accommodation\nBreakfast\nToy Train Tickets\nSightseeing\nTransportation',
        'exclusions': 'Lunch and Dinner\nEntry Fees\nPersonal Expenses',
        'active': True
    },
    {
        'name': 'Ooty Nature & Wildlife Tour',
        'destination': ooty,
        'category': 'Domestic',
        'price': 13500,
        'duration': '4 Days 3 Nights',
        'location': 'Ooty',
        'country': 'India',
        'description': 'Explore the natural beauty and wildlife of Ooty. Visit Mudumalai Wildlife Sanctuary and pristine waterfalls.',
        'itinerary': 'Day 1: Arrival, Ooty Lake, Boat Ride\nDay 2: Mudumalai Safari, Pykara Falls\nDay 3: Avalanche Lake, Emerald Lake\nDay 4: Needle Rock Viewpoint, Departure',
        'inclusions': 'Accommodation\nBreakfast and Dinner\nWildlife Safari\nSightseeing\nTransportation',
        'exclusions': 'Lunch\nEntry Fees\nPersonal Expenses',
        'active': True
    }
]

# Create packages
created_count = 0
for pkg_data in packages:
    try:
        package = TravelPackage.objects.create(**pkg_data)
        created_count += 1
        print(f"Created: {package.name} - {package.destination.name}")
    except Exception as e:
        print(f"Error creating {pkg_data['name']}: {str(e)}")

print(f"\n{created_count} packages created successfully!")
