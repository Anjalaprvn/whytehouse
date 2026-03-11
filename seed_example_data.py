import os
import django
from decimal import Decimal
from datetime import date, timedelta, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "whytehouse.settings")
django.setup()

from django.utils import timezone
from django.utils.text import slugify

from admin_panel.models import (
    BlogCategory,
    Lead,
    Property,
    Destination,
    TravelPackage,
    Inquiry,
    Employee,
    Account,
    Customer,
    Resort,
    Meal,
    Voucher,
    Invoice,
    Blog,
    Feedback,
)


def seed_blog_categories():
    data = [
        {"name": "Travel Tips", "order": 1},
        {"name": "Adventure", "order": 2},
        {"name": "Culture", "order": 3},
        {"name": "Food", "order": 4},
        {"name": "Beach Escapes", "order": 5},
        {"name": "Hill Stations", "order": 6},
        {"name": "Luxury Travel", "order": 7},
        {"name": "Budget Travel", "order": 8},
        {"name": "Family Trips", "order": 9},
        {"name": "Honeymoon", "order": 10},
    ]

    for item in data:
        BlogCategory.objects.get_or_create(
            name=item["name"],
            defaults={
                "slug": slugify(item["name"]),
                "order": item["order"],
                "is_active": True,
            },
        )
    print("✅ BlogCategory - 10 examples added")


def seed_leads():
    data = [
        ("Rahul Nair", "9876543210", "Kochi", "Website", "Domestic", "New"),
        ("Anjali Menon", "9847123456", "Trivandrum", "Direct", "International", "Contacted"),
        ("Arun Kumar", "9895012345", "Calicut", "Manual", "General", "Converted"),
        ("Lakshmi Pillai", "9567012345", "Kollam", "Referral", "Domestic", "New"),
        ("Faisal Rahman", "9745011122", "Malappuram", "Enquire Now", "International", "New"),
        ("Neha Joseph", "9633123456", "Kottayam", "Website", "General", "Contacted"),
        ("Vishnu Prasad", "9847019988", "Kannur", "Direct", "Domestic", "Converted"),
        ("Ajith Das", "9876123456", "Alappuzha", "Manual", "International", "Junk"),
        ("Sandeep Varma", "9447012345", "Thrissur", "Referral", "Domestic", "New"),
        ("Priya Nambiar", "9656012345", "Kasaragod", "Website", "General", "Contacted"),
    ]

    for full_name, mobile, place, source, enquiry_type, status in data:
        Lead.objects.get_or_create(
            mobile_number=mobile,
            defaults={
                "full_name": full_name,
                "place": place,
                "source": source,
                "enquiry_type": enquiry_type,
                "status": status,
                "remarks": f"Sample remark for {full_name}",
                "is_viewed": False,
            },
        )
    print("✅ Lead - 10 examples added")


def seed_properties():
    data = [
        ("Blue Mountain Resort", "resort", "Munnar"),
        ("Sea Breeze Beach Stay", "beach", "Goa"),
        ("Royal Orchid Hotel", "hotel", "Bangalore"),
        ("Palm Grove Villa", "villa", "Wayanad"),
        ("City View Apartment", "apartment", "Dubai"),
        ("Snow Valley Resort", "resort", "Manali"),
        ("Golden Sands Beach Resort", "beach", "Maldives"),
        ("Lake Palace Hotel", "hotel", "Udaipur"),
        ("Sunset Villa", "villa", "Bali"),
        ("Skyline Apartment", "apartment", "Singapore"),
    ]

    for i, (name, prop_type, location) in enumerate(data, start=1):
        Property.objects.get_or_create(
            name=name,
            defaults={
                "property_type": prop_type,
                "location": location,
                "website": f"https://example{i}.com",
                "address": f"{location} Main Road, Sample Address {i}",
                "summary": f"{name} is a beautiful property located in {location}.",
                "owner_name": f"Owner {i}",
                "owner_contact": f"99999000{i:02d}",
                "amenities": "WiFi, Pool, Parking, Restaurant",
                "is_active": True,
                "created_at": timezone.now(),
            },
        )
    print("✅ Property - 10 examples added")


def seed_destinations():
    data = [
        ("Munnar", "India", "Domestic"),
        ("Ooty", "India", "Domestic"),
        ("Goa", "India", "Domestic"),
        ("Kashmir", "India", "Domestic"),
        ("Dubai", "UAE", "International"),
        ("Bali", "Indonesia", "International"),
        ("Singapore", "Singapore", "International"),
        ("Maldives", "Maldives", "International"),
        ("Thailand", "Thailand", "International"),
        ("Vietnam", "Vietnam", "International"),
    ]

    for i, (name, country, category) in enumerate(data, start=1):
        Destination.objects.get_or_create(
            name=name,
            country=country,
            defaults={
                "category": category,
                "description": f"Explore the beauty of {name}, {country}.",
                "packages_start_from": Decimal(str(12000 + i * 3500)),
                "is_popular": i % 2 == 0,
                "created_at": timezone.now(),
            },
        )
    print("✅ Destination - 10 examples added")


def seed_travel_packages():
    destinations = list(Destination.objects.all()[:10])
    data = [
        ("Munnar Nature Escape", "Domestic", "Munnar", "India", Decimal("15999.00")),
        ("Ooty Hill Station Delight", "Domestic", "Ooty", "India", Decimal("14999.00")),
        ("Goa Beach Paradise", "Domestic", "Goa", "India", Decimal("18999.00")),
        ("Kashmir Snow Retreat", "Domestic", "Kashmir", "India", Decimal("25999.00")),
        ("Dubai Luxury Escape", "International", "Dubai", "UAE", Decimal("45999.00")),
        ("Bali Honeymoon Special", "International", "Bali", "Indonesia", Decimal("49999.00")),
        ("Singapore City Explorer", "International", "Singapore", "Singapore", Decimal("42999.00")),
        ("Maldives Romantic Getaway", "International", "Maldives", "Maldives", Decimal("69999.00")),
        ("Thailand Adventure Tour", "International", "Bangkok", "Thailand", Decimal("38999.00")),
        ("Vietnam Culture Trail", "International", "Hanoi", "Vietnam", Decimal("40999.00")),
    ]

    for i, item in enumerate(data):
        name, category, location, country, price = item
        destination = destinations[i] if i < len(destinations) else None

        TravelPackage.objects.get_or_create(
            name=name,
            defaults={
                "category": category,
                "destination": destination,
                "location": location,
                "country": country,
                "price": price,
                "duration": f"{3 + i} Days / {2 + i} Nights",
                "description": f"{name} package for an unforgettable trip.",
                "active": True,
                "itinerary": f"Day wise itinerary for {name}",
                "inclusions": "Hotel, Breakfast, Sightseeing, Transfers",
                "exclusions": "Flights, Personal expenses",
                "meta_title": name,
                "meta_description": f"Book {name} at the best price.",
                "created_at": timezone.now(),
            },
        )
    print("✅ TravelPackage - 10 examples added")


def seed_employees():
    data = [
        ("Akhil Raj", "akhil@example.com", "9876500001", "Manager", "Sales"),
        ("Meera Joseph", "meera@example.com", "9876500002", "Executive", "Sales"),
        ("Nithin Das", "nithin@example.com", "9876500003", "Coordinator", "Operations"),
        ("Anu Mary", "anu@example.com", "9876500004", "Consultant", "Support"),
        ("Fida Rahman", "fida@example.com", "9876500005", "Executive", "Marketing"),
        ("Vivek S", "vivek@example.com", "9876500006", "Manager", "Finance"),
        ("Riya Thomas", "riya@example.com", "9876500007", "Designer", "Creative"),
        ("Sreejith P", "sreejith@example.com", "9876500008", "HR", "Human Resources"),
        ("Athira Nair", "athira@example.com", "9876500009", "Executive", "Sales"),
        ("Jishnu K", "jishnu@example.com", "9876500010", "Support", "Customer Care"),
    ]

    for i, (name, email, phone, role, department) in enumerate(data, start=1):
        Employee.objects.get_or_create(
            email=email,
            defaults={
                "name": name,
                "phone": phone,
                "role": role,
                "department": department,
                "join_date": date.today() - timedelta(days=30 * i),
                "salary": Decimal(str(18000 + i * 2500)),
                "status": "Active" if i % 3 != 0 else "On Leave",
            },
        )
    print("✅ Employee - 10 examples added")


def seed_accounts():
    data = [
        ("Whytehouse Main Account", "1000000001", "SBI", "SBIN0000001", "current"),
        ("Whytehouse Reserve Account", "1000000002", "HDFC", "HDFC0000002", "current"),
        ("Operations Account", "1000000003", "ICICI", "ICIC0000003", "savings"),
        ("Travel Desk Account", "1000000004", "Axis Bank", "UTIB0000004", "current"),
        ("Package Sales Account", "1000000005", "Canara Bank", "CNRB0000005", "checking"),
        ("Vendor Settlement Account", "1000000006", "Federal Bank", "FDRL0000006", "current"),
        ("Corporate Booking Account", "1000000007", "South Indian Bank", "SIBL0000007", "savings"),
        ("Customer Advance Account", "1000000008", "Punjab National Bank", "PUNB0000008", "current"),
        ("Holiday Collections", "1000000009", "Bank of Baroda", "BARB0000009", "checking"),
        ("Resort Payment Account", "1000000010", "Union Bank", "UBIN0000010", "current"),
    ]

    for account_name, account_number, bank_name, ifsc_code, account_type in data:
        Account.objects.get_or_create(
            account_number=account_number,
            defaults={
                "account_name": account_name,
                "bank_name": bank_name,
                "ifsc_code": ifsc_code,
                "account_type": account_type,
            },
        )
    print("✅ Account - 10 examples added")


def seed_customers():
    data = [
        ("Individual", "Mr", "Rahul", "Nair", "Rahul Nair", "Kochi", "9876543210", True, "9876543210", "", ""),
        ("Individual", "Ms", "Anjali", "Menon", "Anjali Menon", "Trivandrum", "9847123456", True, "9847123456", "", ""),
        ("Individual", "Mr", "Arun", "Kumar", "Arun Kumar", "Calicut", "9895012345", True, "9895012345", "0495223344", ""),
        ("Individual", "Mrs", "Lakshmi", "Pillai", "Lakshmi Pillai", "Kollam", "9567012345", True, "9567012345", "", ""),
        ("Individual", "Mr", "Faisal", "Rahman", "Faisal Rahman", "Malappuram", "9745011122", True, "9745011122", "", ""),
        ("Corporate", "Mr", "Sandeep", "Varma", "Varma Travels Pvt Ltd", "Thrissur", "9847012345", False, "9847099999", "0487220011", "32ABCDE1234F1Z5"),
        ("Corporate", "Mr", "Ajith", "Das", "Das Holidays", "Alappuzha", "9876123456", False, "9876000000", "0477223344", "32PQRSX1234L1Z9"),
        ("Government", "Mr", "Rajesh", "Kumar", "Kerala Tourism Dept", "Trivandrum", "9447012345", True, "9447012345", "0471234567", "32AAAGK1234A1Z2"),
        ("Individual", "Dr", "Neha", "Joseph", "Dr Neha Joseph", "Kottayam", "9633123456", True, "9633123456", "", ""),
        ("Corporate", "Mr", "Vishnu", "Prasad", "Prasad Tours", "Kannur", "9847019988", False, "9847000001", "0497221122", "32LMNOP5678G1Z4"),
    ]

    for row in data:
        (
            customer_type, salutation, first_name, last_name, display_name,
            place, contact_number, same_as_whatsapp, whatsapp_number,
            work_number, gst_number
        ) = row

        Customer.objects.get_or_create(
            contact_number=contact_number,
            defaults={
                "customer_type": customer_type,
                "salutation": salutation,
                "first_name": first_name,
                "last_name": last_name,
                "display_name": display_name,
                "place": place,
                "same_as_whatsapp": same_as_whatsapp,
                "whatsapp_number": whatsapp_number,
                "work_number": work_number,
                "gst_number": gst_number,
            },
        )
    print("✅ Customer - 10 examples added")


def seed_resorts():
    data = [
        ("Green Valley Resort", "Munnar"),
        ("Blue Ocean Resort", "Goa"),
        ("Hilltop Residency", "Ooty"),
        ("Snow View Resort", "Kashmir"),
        ("Palm Breeze Stay", "Bali"),
        ("Marina Beach Resort", "Maldives"),
        ("Royal Orchid Resort", "Dubai"),
        ("Sunrise Eco Resort", "Wayanad"),
        ("Lake Side Resort", "Kodaikanal"),
        ("City Lights Resort", "Singapore"),
    ]

    for i, (resort_name, location) in enumerate(data, start=1):
        Resort.objects.get_or_create(
            resort_name=resort_name,
            defaults={
                "location": location,
                "contact_person": f"Manager {i}",
                "contact_number": f"90000000{i:02d}",
                "email": f"resort{i}@example.com",
                "address": f"{location}, Sample address line {i}",
                "status": "Active",
            },
        )
    print("✅ Resort - 10 examples added")


def seed_meals():
    data = [
        ("Breakfast Only", "Morning breakfast included", "Breakfast"),
        ("Half Board", "Breakfast and Dinner included", "Breakfast, Dinner"),
        ("Full Board", "All three meals included", "Breakfast, Lunch, Dinner"),
        ("All Inclusive", "Meals and refreshments included", "Breakfast, Lunch, Dinner, Snacks"),
        ("Veg Plan", "Vegetarian meal plan", "Veg Breakfast, Veg Lunch, Veg Dinner"),
        ("Non-Veg Plan", "Non vegetarian meal plan", "Breakfast, Lunch, Dinner"),
        ("Kids Meal Plan", "Special meals for kids", "Kids Breakfast, Kids Lunch"),
        ("Honeymoon Meal Plan", "Romantic dinner specials", "Breakfast, Candle Light Dinner"),
        ("Corporate Plan", "Business travel meal plan", "Breakfast, Lunch"),
        ("Custom Meal Plan", "Customizable meal package", "As per request"),
    ]

    for name, description, included_meals in data:
        Meal.objects.get_or_create(
            name=name,
            defaults={
                "description": description,
                "included_meals": included_meals,
                "status": "Available",
            },
        )
    print("✅ Meal - 10 examples added")


def seed_inquiries():
    leads = list(Lead.objects.all()[:10])

    data = [
        ("Rahul Nair", "rahul@example.com", "9876543210", "Munnar Nature Escape"),
        ("Anjali Menon", "anjali@example.com", "9847123456", "Dubai Luxury Escape"),
        ("Arun Kumar", "arun@example.com", "9895012345", "Goa Beach Paradise"),
        ("Lakshmi Pillai", "lakshmi@example.com", "9567012345", "Bali Honeymoon Special"),
        ("Faisal Rahman", "faisal@example.com", "9745011122", "Singapore City Explorer"),
        ("Neha Joseph", "neha@example.com", "9633123456", "Kashmir Snow Retreat"),
        ("Vishnu Prasad", "vishnu@example.com", "9847019988", "Thailand Adventure Tour"),
        ("Ajith Das", "ajith@example.com", "9876123456", "Maldives Romantic Getaway"),
        ("Sandeep Varma", "sandeep@example.com", "9447012345", "Ooty Hill Station Delight"),
        ("Priya Nambiar", "priya@example.com", "9656012345", "Vietnam Culture Trail"),
    ]

    for i, (name, email, phone, package) in enumerate(data):
        Inquiry.objects.get_or_create(
            email=email,
            package=package,
            defaults={
                "lead": leads[i] if i < len(leads) else None,
                "name": name,
                "phone": phone,
                "message": f"I would like more details about {package}.",
                "status": "New" if i % 2 == 0 else "Contacted",
                "created_at": timezone.now(),
            },
        )
    print("✅ Inquiry - 10 examples added")


def seed_vouchers():
    customers = list(Customer.objects.all()[:10])
    employees = list(Employee.objects.all()[:10])
    resorts = list(Resort.objects.all()[:10])
    meals = list(Meal.objects.all()[:10])
    accounts = list(Account.objects.all()[:10])

    for i in range(10):
        voucher_no = f"VCH{1001 + i}"
        package_price = Decimal(str(18000 + i * 4000))
        resort_price = Decimal(str(14000 + i * 3000))
        total_amount = package_price
        received = Decimal(str(10000 + i * 2000))
        pending = total_amount - received
        profit = package_price - resort_price

        Voucher.objects.get_or_create(
            voucher_no=voucher_no,
            defaults={
                "customer": customers[i],
                "voucher_date": date.today() - timedelta(days=i),
                "sales_person": employees[i],
                "resort": resorts[i],
                "checkin_date": date.today() + timedelta(days=i + 5),
                "checkout_date": date.today() + timedelta(days=i + 7),
                "checkin_time": time(12, 0),
                "checkout_time": time(11, 0),
                "adults": 2,
                "children": i % 3,
                "nights": 2,
                "pax_notes": "Sample pax notes",
                "room_type": "Deluxe",
                "no_of_rooms": 1,
                "meals_plan": meals[i],
                "bank_account": accounts[i],
                "package_price": package_price,
                "resort_price": resort_price,
                "total_amount": total_amount,
                "received": received,
                "pending": pending,
                "from_whytehouse": Decimal("1000.00"),
                "profit": profit,
                "note_for_resort": "Provide welcome drink",
                "note_for_guest": "Carry valid ID proof",
            },
        )
    print("✅ Voucher - 10 examples added")


def seed_invoices():
    customers = list(Customer.objects.all()[:10])
    employees = list(Employee.objects.all()[:10])
    resorts = list(Resort.objects.all()[:10])
    accounts = list(Account.objects.all()[:10])

    for i in range(10):
        invoice_no = f"INV{2001 + i}"
        package_price = Decimal(str(22000 + i * 3500))
        tax = Decimal("1000.00")
        resort_price = Decimal(str(17000 + i * 2800))
        total = package_price + tax
        received = Decimal(str(12000 + i * 2500))
        pending = total - received
        profit = total - resort_price

        Invoice.objects.get_or_create(
            invoice_no=invoice_no,
            defaults={
                "customer": customers[i],
                "invoice_date": date.today() - timedelta(days=i),
                "sales_person": employees[i],
                "resort": resorts[i],
                "checkin_date": date.today() + timedelta(days=i + 3),
                "checkout_date": date.today() + timedelta(days=i + 6),
                "checkin_time": time(13, 0),
                "checkout_time": time(11, 0),
                "adults": 2,
                "children": i % 2,
                "pax_total": 2 + (i % 2),
                "pax_notes": "Invoice pax details",
                "nights": 3,
                "room_type": "Premium",
                "rooms": 1,
                "meals_plan": "Breakfast Only",
                "bank_account": accounts[i],
                "package_price": package_price,
                "tax": tax,
                "resort_price": resort_price,
                "total": total,
                "received": received,
                "pending": pending,
                "profit": profit,
                "notes": "Sample invoice note",
            },
        )
    print("✅ Invoice - 10 examples added")


def seed_blogs():
    categories = ["travel", "adventure", "culture", "food", "tips"]
    titles = [
        "Top 10 Places to Visit in Munnar",
        "A Complete Guide to Dubai Luxury Trips",
        "Best Beaches in Goa for Families",
        "Why Bali is Perfect for Honeymoon",
        "Singapore Travel Tips for First Timers",
        "Kashmir in Winter: What to Expect",
        "Thailand Adventure Activities You Should Try",
        "Vietnam Street Food You Must Taste",
        "Maldives Budget vs Luxury Travel",
        "How to Plan a Stress-Free Holiday",
    ]

    for i, title in enumerate(titles, start=1):
        Blog.objects.get_or_create(
            slug=slugify(title),
            defaults={
                "title": title,
                "excerpt": f"Short excerpt for {title}",
                "content": f"This is sample blog content for {title}.",
                "status": "published",
                "category": categories[(i - 1) % len(categories)],
                "package_id": str(i),
                "author_name": "Whyte House Team",
                "author_summary": "Travel writers and destination experts.",
                "reading_time": 3 + i,
                "publish_date": date.today() - timedelta(days=i),
                "featured_image_url": f"https://picsum.photos/seed/blog{i}/800/500",
                "hashtags": "#travel #holiday #whytehouse",
                "tags": "travel,holiday,tourism",
            },
        )
    print("✅ Blog - 10 examples added")


def seed_feedback():
    data = [
        ("Rahul Nair", "rahul@example.com", "9876543210", "Travel Package", 5, "Excellent package and great support."),
        ("Anjali Menon", "anjali@example.com", "9847123456", "Customer Service", 4, "Friendly team and quick responses."),
        ("Arun Kumar", "arun@example.com", "9895012345", "Booking Experience", 5, "Smooth booking process."),
        ("Lakshmi Pillai", "lakshmi@example.com", "9567012345", "Property Management", 4, "Resort stay was comfortable."),
        ("Faisal Rahman", "faisal@example.com", "9745011122", "Website Experience", 3, "Website is good but can improve."),
        ("Neha Joseph", "neha@example.com", "9633123456", "Trip Management", 5, "Trip was well organized."),
        ("Vishnu Prasad", "vishnu@example.com", "9847019988", "Travel Package", 4, "Worth the money."),
        ("Ajith Das", "ajith@example.com", "9876123456", "Customer Service", 5, "Very helpful consultants."),
        ("Sandeep Varma", "sandeep@example.com", "9447012345", "Booking Experience", 4, "Easy and clear booking steps."),
        ("Priya Nambiar", "priya@example.com", "9656012345", "Other", 5, "Overall wonderful experience."),
    ]

    for i, (name, email, mobile, feedback_type, rating, feedback) in enumerate(data, start=1):
        Feedback.objects.get_or_create(
            email=email,
            feedback=feedback,
            defaults={
                "name": name,
                "mobile_number": mobile,
                "feedback_type": feedback_type,
                "rating": rating,
                "featured": i % 2 == 0,
            },
        )
    print("✅ Feedback - 10 examples added")


def main():
    print("\n--- Seeding Example Data ---\n")
    seed_blog_categories()
    seed_leads()
    seed_properties()
    seed_destinations()
    seed_travel_packages()
    seed_employees()
    seed_accounts()
    seed_customers()
    seed_resorts()
    seed_meals()
    seed_inquiries()
    seed_vouchers()
    seed_invoices()
    seed_blogs()
    seed_feedback()
    print("\n🎉 All sample data inserted successfully.")
    print("Note: BlogImage and FeedbackImage are not included because they require actual image files.\n")


if __name__ == "__main__":
    main()