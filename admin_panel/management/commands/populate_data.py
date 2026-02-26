from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import random
from admin_panel.models import (
    Account, Customer, Resort, Meal, Voucher, Invoice, 
    Employee, Lead, Property, Amenity, TravelPackage
)


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))

        # Create Accounts
        self.stdout.write('Creating bank accounts...')
        accounts_data = [
            {
                'account_name': 'Whyte House Primary Account',
                'account_number': 'ACC001234567890',
                'bank_name': 'State Bank of India',
                'ifsc_code': 'SBIN0001234',
                'account_type': 'current'
            },
            {
                'account_name': 'Whyte House Savings',
                'account_number': 'ACC009876543210',
                'bank_name': 'HDFC Bank',
                'ifsc_code': 'HDFC0002345',
                'account_type': 'savings'
            },
            {
                'account_name': 'Business Operations Account',
                'account_number': 'ACC005555666677',
                'bank_name': 'ICICI Bank',
                'ifsc_code': 'ICIC0003456',
                'account_type': 'current'
            },
        ]
        
        accounts = []
        for acc_data in accounts_data:
            account, created = Account.objects.get_or_create(
                account_number=acc_data['account_number'],
                defaults=acc_data
            )
            accounts.append(account)
            if created:
                self.stdout.write(f'  ✓ Created account: {account.account_name}')

        # Create Resorts
        self.stdout.write('Creating resorts...')
        resorts_data = [
            {
                'resort_name': 'Nilaya Resort & Spa',
                'location': 'Goa',
                'contact_person': 'Rajesh Kumar',
                'contact_number': '9876543210',
                'email': 'info@nilayaresort.com',
                'address': 'Arpora, North Goa, Goa 403518',
                'status': 'Active'
            },
            {
                'resort_name': 'Amber Palace Resort',
                'location': 'Jaipur',
                'contact_person': 'Priya Sharma',
                'contact_number': '9876543211',
                'email': 'contact@amberpalace.com',
                'address': 'Amer Road, Jaipur, Rajasthan 302002',
                'status': 'Active'
            },
            {
                'resort_name': 'Jungle Retreat',
                'location': 'Munnar',
                'contact_person': 'Thomas George',
                'contact_number': '9876543212',
                'email': 'info@jungleretreat.com',
                'address': 'Munnar Hills, Kerala 685612',
                'status': 'Active'
            },
            {
                'resort_name': 'Beach Paradise Resort',
                'location': 'Goa',
                'contact_person': 'Maria D\'Souza',
                'contact_number': '9876543213',
                'email': 'bookings@beachparadise.com',
                'address': 'Calangute Beach, Goa 403516',
                'status': 'Active'
            },
            {
                'resort_name': 'Mountain View Lodge',
                'location': 'Manali',
                'contact_person': 'Vikram Singh',
                'contact_number': '9876543214',
                'email': 'stay@mountainview.com',
                'address': 'Old Manali, Himachal Pradesh 175131',
                'status': 'Active'
            },
        ]
        
        resorts = []
        for resort_data in resorts_data:
            resort, created = Resort.objects.get_or_create(
                resort_name=resort_data['resort_name'],
                defaults=resort_data
            )
            resorts.append(resort)
            if created:
                self.stdout.write(f'  ✓ Created resort: {resort.resort_name}')

        # Create Meals
        self.stdout.write('Creating meal plans...')
        meals_data = [
            {
                'name': 'European Plan (EP)',
                'description': 'Room only, no meals included',
                'included_meals': 'None',
                'status': 'Available'
            },
            {
                'name': 'Continental Plan (CP)',
                'description': 'Room with breakfast',
                'included_meals': 'Breakfast',
                'status': 'Available'
            },
            {
                'name': 'Modified American Plan (MAP)',
                'description': 'Room with breakfast and dinner',
                'included_meals': 'Breakfast, Dinner',
                'status': 'Available'
            },
            {
                'name': 'American Plan (AP)',
                'description': 'Room with all meals',
                'included_meals': 'Breakfast, Lunch, Dinner',
                'status': 'Available'
            },
        ]
        
        meals = []
        for meal_data in meals_data:
            meal, created = Meal.objects.get_or_create(
                name=meal_data['name'],
                defaults=meal_data
            )
            meals.append(meal)
            if created:
                self.stdout.write(f'  ✓ Created meal plan: {meal.name}')

        # Get existing customers and employees
        customers = list(Customer.objects.all())
        employees = list(Employee.objects.all())

        if not customers:
            self.stdout.write(self.style.WARNING('  ⚠ No customers found. Please create customers first.'))
            return

        if not employees:
            self.stdout.write(self.style.WARNING('  ⚠ No employees found. Please create employees first.'))
            return

        # Create Invoices
        self.stdout.write('Creating invoices...')
        invoice_count = 0
        for i in range(15):
            customer = random.choice(customers)
            employee = random.choice(employees)
            resort = random.choice(resorts)
            account = random.choice(accounts)
            
            # Random date in the last 3 months
            days_ago = random.randint(1, 90)
            invoice_date = timezone.now().date() - timedelta(days=days_ago)
            checkin_date = invoice_date + timedelta(days=random.randint(1, 7))
            checkout_date = checkin_date + timedelta(days=random.randint(2, 7))
            nights = (checkout_date - checkin_date).days
            
            adults = random.randint(1, 4)
            children = random.randint(0, 2)
            rooms = random.randint(1, 3)
            
            package_price = Decimal(random.randint(5000, 20000))
            tax = package_price * Decimal('0.18')  # 18% GST
            resort_price = package_price * Decimal('0.70')  # 70% of package price
            total = package_price + tax
            received = total * Decimal(random.choice(['0.5', '0.75', '1.0']))
            pending = total - received
            profit = package_price - resort_price
            
            invoice_no = f'INV-{invoice_date.strftime("%Y%m")}-{str(i+1).zfill(4)}'
            
            invoice, created = Invoice.objects.get_or_create(
                invoice_no=invoice_no,
                defaults={
                    'customer': customer,
                    'invoice_date': invoice_date,
                    'sales_person': employee,
                    'resort': resort,
                    'checkin_date': checkin_date,
                    'checkout_date': checkout_date,
                    'checkin_time': '14:00',
                    'checkout_time': '11:00',
                    'adults': adults,
                    'children': children,
                    'pax_total': adults + children,
                    'pax_notes': f'{adults} adults, {children} children',
                    'nights': nights,
                    'room_type': random.choice(['Deluxe', 'Suite', 'Premium', 'Standard']),
                    'rooms': rooms,
                    'meals_plan': random.choice(['EP', 'CP', 'MAP', 'AP']),
                    'bank_account': account,
                    'package_price': package_price,
                    'tax': tax,
                    'resort_price': resort_price,
                    'total': total,
                    'received': received,
                    'pending': pending,
                    'profit': profit,
                    'notes': f'Booking for {customer.display_name}'
                }
            )
            if created:
                invoice_count += 1
                self.stdout.write(f'  ✓ Created invoice: {invoice_no}')

        # Create Vouchers
        self.stdout.write('Creating vouchers...')
        voucher_count = 0
        for i in range(10):
            customer = random.choice(customers)
            employee = random.choice(employees)
            resort = random.choice(resorts)
            meal = random.choice(meals)
            account = random.choice(accounts)
            
            days_ago = random.randint(1, 60)
            voucher_date = timezone.now().date() - timedelta(days=days_ago)
            checkin_date = voucher_date + timedelta(days=random.randint(1, 5))
            checkout_date = checkin_date + timedelta(days=random.randint(2, 5))
            nights = (checkout_date - checkin_date).days
            
            adults = random.randint(1, 4)
            children = random.randint(0, 2)
            rooms = random.randint(1, 2)
            
            package_price = Decimal(random.randint(8000, 25000))
            resort_price = package_price * Decimal('0.65')
            total_amount = package_price
            received = total_amount * Decimal(random.choice(['0.3', '0.5', '0.8', '1.0']))
            pending = total_amount - received
            from_whytehouse = Decimal(random.randint(1000, 5000))
            profit = package_price - resort_price - from_whytehouse
            
            voucher_no = f'VCH-{voucher_date.strftime("%Y%m")}-{str(i+1).zfill(4)}'
            
            voucher, created = Voucher.objects.get_or_create(
                voucher_no=voucher_no,
                defaults={
                    'customer': customer,
                    'voucher_date': voucher_date,
                    'sales_person': employee,
                    'resort': resort,
                    'checkin_date': checkin_date,
                    'checkout_date': checkout_date,
                    'checkin_time': '14:00',
                    'checkout_time': '11:00',
                    'adults': adults,
                    'children': children,
                    'nights': nights,
                    'pax_notes': f'{adults} adults, {children} children',
                    'room_type': random.choice(['Deluxe', 'Suite', 'Premium', 'Standard']),
                    'no_of_rooms': rooms,
                    'meals_plan': meal,
                    'bank_account': account,
                    'package_price': package_price,
                    'resort_price': resort_price,
                    'total_amount': total_amount,
                    'received': received,
                    'pending': pending,
                    'from_whytehouse': from_whytehouse,
                    'profit': profit,
                    'note_for_resort': 'Please ensure early check-in',
                    'note_for_guest': 'Enjoy your stay!'
                }
            )
            if created:
                voucher_count += 1
                self.stdout.write(f'  ✓ Created voucher: {voucher_no}')

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Data Population Complete!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'✓ Accounts: {len(accounts)}')
        self.stdout.write(f'✓ Resorts: {len(resorts)}')
        self.stdout.write(f'✓ Meal Plans: {len(meals)}')
        self.stdout.write(f'✓ Invoices: {invoice_count}')
        self.stdout.write(f'✓ Vouchers: {voucher_count}')
        self.stdout.write(self.style.SUCCESS('\nYou can now test the invoice report at:'))
        self.stdout.write(self.style.SUCCESS('http://127.0.0.1:8000/sales/reports/invoice/'))
