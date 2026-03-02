from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.text import slugify
from django.db import transaction
from django.urls import reverse
import random
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime


from .models import Account, Customer, Resort, Meal, Voucher, Invoice, Lead, Property, TravelPackage, Inquiry, Destination
from .models import Employee,Blog,BlogImage

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.utils import timezone
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
# Create your views here.
def home(request):
    return redirect('login')



def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        
        if user is not None and user.email:
            otp = random.randint(100000, 999999)
            request.session['admin_otp'] = otp
            request.session['admin_username'] = username

            send_mail(
                subject="Admin Login OTP for safe and secure login",
                message=f"Your OTP is {otp}",
                from_email="whytehousee@gmail.com",
                recipient_list=[user.email],
            )
            return redirect('admin_panel:verify_otp')
        else:
            context = {'error': 'Invalid credentials or email not configured'}
            return render(request, "admin/login.html", context)

    return render(request, "admin/login.html")

def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST.get("otp", "")
        real_otp = str(request.session.get("admin_otp", ""))

        if user_otp == real_otp:
            request.session['admin_logged_in'] = True
            return redirect('dashboard')
        else:
            context = {'error': 'Invalid OTP. Please try again.'}
            return render(request, "admin/verify_otp.html", context)

    return render(request, "admin/verify_otp.html")

def resend_otp(request):
   
    username = request.session.get('admin_username')
    
    if username:
        try:
            user = User.objects.get(username=username)
            if user.email:
                
                otp = random.randint(100000, 999999)
                request.session['admin_otp'] = otp
                
               
                send_mail(
                    subject="Admin Login OTP for safe and secure login",
                    message=f"Your OTP is {otp}",
                    from_email="whytehousee@gmail.com",
                    recipient_list=[user.email],
                )
        except User.DoesNotExist:
            pass
    
    return redirect('verify_otp')

def forgot_password(request):
    return render(request, 'admin/forgotpassword.html')

def dashboard(request):
    from django.db.models import Sum, Count
    from datetime import datetime, timedelta
    
    # Stats
    total_vouchers = Voucher.objects.count()
    total_invoices = Invoice.objects.count()
    total_profit = Invoice.objects.aggregate(Sum('profit'))['profit__sum'] or 0
    new_leads = Lead.objects.filter(created_at__gte=datetime.now() - timedelta(days=30)).count()
    total_customers = Customer.objects.count()
    
    # Upcoming bookings (vouchers with future check-in dates)
    upcoming_bookings = Voucher.objects.filter(checkin_date__gte=datetime.now()).order_by('checkin_date')[:3]
    
    # Recent invoices
    recent_invoices = Invoice.objects.select_related('customer').order_by('-created_at')[:5]
    
    # Recent leads
    recent_leads = Lead.objects.order_by('-created_at')[:5]
    
    context = {
        'total_vouchers': total_vouchers,
        'total_invoices': total_invoices,
        'total_profit': total_profit,
        'new_leads': new_leads,
        'total_customers': total_customers,
        'upcoming_bookings': upcoming_bookings,
        'recent_invoices': recent_invoices,
        'recent_leads': recent_leads,
    }
    return render(request, 'admin/index.html', context)

# LEADS
def lead_management(request):
    enquiry_type = request.GET.get('type', '')
    source_filter = request.GET.get('source', '')
    new_leads = request.GET.get('new', '')
    
    # If General enquiry type is selected, redirect to customer inquiries page
    if enquiry_type == 'General':
        return redirect('admin_panel:customer_inquiries')
    
    leads = Lead.objects.all()
    
    if enquiry_type:
        leads = leads.filter(enquiry_type=enquiry_type)
    
    if source_filter:
        leads = leads.filter(source=source_filter)
    
    if new_leads == 'true':
        leads = leads.filter(source='Enquire Now')
    
    leads = leads.order_by('-created_at')
    
    # Count Inquiries for general (not Leads)
    general_count = Inquiry.objects.count()
    international_count = Lead.objects.filter(enquiry_type='International').count()
    domestic_count = Lead.objects.filter(enquiry_type='Domestic').count()
    new_leads_count = Lead.objects.filter(source='Enquire Now').count()
    
    context = {
        'leads': leads,
        'selected_type': enquiry_type,
        'selected_source': source_filter,
        'selected_new': new_leads,
        'general_count': general_count,
        'international_count': international_count,
        'domestic_count': domestic_count,
        'new_leads_count': new_leads_count,
    }
    return render(request, 'admin/lead/lead.html', context)

def add_lead(request):
    if request.method == "POST":
        Lead.objects.create(
            full_name=request.POST.get('full_name'),
            mobile_number=request.POST.get('mobile_number'),
            place=request.POST.get('place'),
            source=request.POST.get('source'),
            enquiry_type=request.POST.get('enquiry_type', 'General'),
            remarks=request.POST.get('remarks')
        )
        messages.success(request, "Lead added successfully!")
        return redirect('admin_panel:leads')
    return render(request, 'admin/lead/lead_add.html')

def edit_lead(request, id):
    lead = get_object_or_404(Lead, id=id)
    if request.method == "POST":
        lead.full_name = request.POST.get('full_name')
        lead.mobile_number = request.POST.get('mobile_number')
        lead.place = request.POST.get('place')
        lead.source = request.POST.get('source')
        lead.enquiry_type = request.POST.get('enquiry_type', 'General')
        lead.status = request.POST.get('status', 'New')
        lead.remarks = request.POST.get('remarks')
        lead.save()
        messages.success(request, "Lead updated successfully!")
        return redirect('admin_panel:leads')
    return render(request, 'admin/lead/lead_edit.html', {'lead': lead})

def delete_lead(request, lead_id):
    if request.method != 'POST':
        return redirect('admin_panel:leads')
    
    lead = get_object_or_404(Lead, id=lead_id)
    lead.delete()
    messages.success(request, 'Lead deleted successfully!')
    return redirect('admin_panel:leads')

def view_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    return render(request, 'admin/lead/lead_view.html', {'lead': lead})

# HOSPITALITY
def hospitality_management(request):
    properties = Property.objects.all().order_by("-created_at")
    return render(request, "admin/hospitality/hospitality_management.html", {"properties": properties})

def add_property(request):
    if request.method == "POST":
        
        new_amenities = request.POST.getlist("new_amenities[]")

        
        amenities_text = ", ".join([a.strip() for a in new_amenities if a.strip()])

        Property.objects.create(
            name=request.POST.get("name"),
            property_type=request.POST.get("property_type"),
            location=request.POST.get("location"),
            website=request.POST.get("website") or None,
            address=request.POST.get("address"),
            summary=request.POST.get("summary"),
            owner_name=request.POST.get("owner_name") or None,
            owner_contact=request.POST.get("owner_contact") or None,
            amenities=amenities_text,
            image=request.FILES.get("image"),
        )

        messages.success(request, "Property added successfully!")
        return redirect("admin_panel:admin_hospitality")

    return render(request, "admin/hospitality/hospitality_add.html")

def edit_property(request, property_id):
    prop = get_object_or_404(Property, id=property_id)

    if request.method == "POST":
        prop.name = request.POST.get("name")
        prop.property_type = request.POST.get("property_type")
        prop.location = request.POST.get("location")
        prop.website = request.POST.get("website") or None
        prop.address = request.POST.get("address")
        prop.summary = request.POST.get("summary")
        prop.owner_name = request.POST.get("owner_name") or None
        prop.owner_contact = request.POST.get("owner_contact") or None

        new_amenities = request.POST.getlist("new_amenities[]")
        prop.amenities = ", ".join([a.strip() for a in new_amenities if a.strip()])

        if request.FILES.get("image"):
            prop.image = request.FILES.get("image")

        prop.save()

        messages.success(request, "Property updated successfully!")
        return redirect("admin_panel:admin_hospitality")

    return render(
        request,
        "admin/hospitality/hospitality_edit.html",
        {"property": prop}
    )

def delete_property(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    prop.delete()
    messages.success(request, "Property deleted successfully!")
    return redirect("admin_panel:admin_hospitality")

# TRAVEL PACKAGES
def travel_packages(request):
    category = request.GET.get('cat', 'Domestic')
    destination_id = request.GET.get('dest')
    
    # Get destinations for the selected category
    destinations = Destination.objects.filter(category=category).order_by('name')
    
    # Get packages based on category and destination
    packages = TravelPackage.objects.filter(category=category)
    if destination_id:
        packages = packages.filter(destination_id=destination_id)
    packages = packages.order_by('-created_at')
    
    # Count packages by destination
    destination_counts = {}
    for dest in destinations:
        destination_counts[dest.id] = TravelPackage.objects.filter(category=category, destination=dest).count()
    
    domestic_count = TravelPackage.objects.filter(category='Domestic').count()
    international_count = TravelPackage.objects.filter(category='International').count()
    
    # Get selected destination object
    selected_destination_obj = None
    if destination_id:
        try:
            selected_destination_obj = Destination.objects.get(id=destination_id)
        except Destination.DoesNotExist:
            pass
    
    context = {
        'packages': packages,
        'destinations': destinations,
        'destination_counts': destination_counts,
        'selected_category': category,
        'selected_destination': int(destination_id) if destination_id else None,
        'selected_destination_obj': selected_destination_obj,
        'domestic_count': domestic_count,
        'international_count': international_count,
    }
    return render(request, 'admin/packages/travel_packages.html', context)

def travel_package_add(request):
    # Get category and destination from URL parameters
    default_category = request.GET.get('category', 'Domestic')
    destination_id = request.GET.get('destination')
    
    # Get the selected destination object
    selected_destination_obj = None
    if destination_id:
        try:
            selected_destination_obj = Destination.objects.get(id=destination_id)
        except Destination.DoesNotExist:
            pass
    
    if request.method == "POST":
        destination_id = request.POST.get('destination')
        destination = None
        if destination_id:
            try:
                destination = Destination.objects.get(id=destination_id)
            except Destination.DoesNotExist:
                pass
        
        category = request.POST.get('category')
        TravelPackage.objects.create(
            name=request.POST.get('name'),
            category=category,
            destination=destination,
            price=request.POST.get('price'),
            duration=request.POST.get('duration'),
            location=request.POST.get('location'),
            country=request.POST.get('country'),
            description=request.POST.get('description'),
            itinerary='\n'.join(request.POST.getlist('itinerary[]')),
            inclusions='\n'.join(request.POST.getlist('inclusions[]')),
            exclusions='\n'.join(request.POST.getlist('exclusions[]')),
            meta_title=request.POST.get('meta_title'),
            meta_description=request.POST.get('meta_description'),
            active=request.POST.get('active') == 'on',
            image=request.FILES.get('image')
        )
        messages.success(request, "Package added successfully!")
        
        # Redirect back to the same category and destination
        url = reverse('admin_panel:travel_packages')
        if destination:
            return redirect(f'{url}?cat={category}&dest={destination.id}')
        else:
            return redirect(f'{url}?cat={category}')
    
    context = {
        'default_category': default_category,
        'selected_destination_id': int(destination_id) if destination_id else None,
        'selected_destination_obj': selected_destination_obj,
    }
    return render(request, 'admin/packages/travel_package_add.html', context)

def travel_package_edit(request, package_id):
    package = get_object_or_404(TravelPackage, id=package_id)
    
    # Get all destinations
    destinations = Destination.objects.all().order_by('category', 'name')
    
    if request.method == "POST":
        destination_id = request.POST.get('destination')
        destination = None
        if destination_id:
            try:
                destination = Destination.objects.get(id=destination_id)
            except Destination.DoesNotExist:
                pass
        
        # Get the category from POST
        new_category = request.POST.get('category')
        
        package.name = request.POST.get('name')
        package.category = new_category
        package.destination = destination
        package.price = request.POST.get('price')
        package.duration = request.POST.get('duration')
        package.location = request.POST.get('location')
        package.country = request.POST.get('country')
        package.description = request.POST.get('description')
        package.itinerary = request.POST.get('itinerary')
        package.inclusions = request.POST.get('inclusions')
        package.exclusions = request.POST.get('exclusions')
        package.meta_title = request.POST.get('meta_title')
        package.meta_description = request.POST.get('meta_description')
        package.active = request.POST.get('active') == 'on'
        if request.FILES.get('image'):
            package.image = request.FILES.get('image')
        if request.FILES.get('story_main_image'):
            package.story_main_image = request.FILES.get('story_main_image')
        if request.FILES.get('story_side_image1'):
            package.story_side_image1 = request.FILES.get('story_side_image1')
        if request.FILES.get('story_side_image2'):
            package.story_side_image2 = request.FILES.get('story_side_image2')
        package.save()
        messages.success(request, "Package updated successfully!")
        
        # Redirect back to the same category and destination using the NEW category
        url = reverse('admin_panel:travel_packages')
        if destination:
            return redirect(f'{url}?cat={new_category}&dest={destination.id}')
        else:
            return redirect(f'{url}?cat={new_category}')
    
    context = {
        'package': package,
        'destinations': destinations,
    }
    return render(request, 'admin/packages/travel_package_edit.html', context)

def travel_package_delete(request, package_id):
    package = get_object_or_404(TravelPackage, id=package_id)
    category = package.category
    destination_id = package.destination_id if package.destination else None
    package.delete()
    messages.success(request, "Package deleted successfully!")
    
    # Redirect back to the same category and destination
    url = reverse('admin_panel:travel_packages')
    if destination_id:
        return redirect(f'{url}?cat={category}&dest={destination_id}')
    else:
        return redirect(f'{url}?cat={category}')

# CUSTOMER INQUIRIES
def customer_inquiries(request):
    status_filter = request.GET.get('status')
    
    # Get all inquiries
    inquiries = Inquiry.objects.all()
    
    # Apply status filter if provided
    if status_filter:
        inquiries = inquiries.filter(status=status_filter)
    
    inquiries = inquiries.order_by('-created_at')
    
    # Count by status (from all inquiries, not just filtered)
    all_inquiries = Inquiry.objects.all()
    new_count = all_inquiries.filter(status='New').count()
    contacted_count = all_inquiries.filter(status='Contacted').count()
    converted_count = all_inquiries.filter(status='Converted').count()
    junk_count = all_inquiries.filter(status='Junk').count()
    
    print(f"DEBUG customer_inquiries: Total={all_inquiries.count()}, New={new_count}, Contacted={contacted_count}, Converted={converted_count}, Junk={junk_count}")
    
    context = {
        'inquiries': inquiries,
        'total_count': all_inquiries.count(),
        'new_count': new_count,
        'contacted_count': contacted_count,
        'converted_count': converted_count,
        'junk_count': junk_count,
    }
    return render(request, 'admin/enquiry/customer_inquiries.html', context)

def view_inquiry(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    return render(request, 'admin/enquiry/customer_inquiry_view.html', {'inquiry': inquiry})

def update_inquiry_status(request, inquiry_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        print(f"DEBUG: Updating inquiry_id={inquiry_id} to status={new_status}")
        
        if new_status in ['New', 'Contacted', 'Converted', 'Junk']:
            inquiry = get_object_or_404(Inquiry, id=inquiry_id)
            print(f"DEBUG: Found Inquiry (ID={inquiry.id}, Name={inquiry.name}), updating status from {inquiry.status} to {new_status}")
            inquiry.status = new_status
            inquiry.save()
            print(f"DEBUG: Inquiry saved, new status is {inquiry.status}")
            messages.success(request, f'Inquiry status updated to {new_status}')
            return redirect('admin_panel:view_inquiry', inquiry_id=inquiry_id)
    
    return redirect('admin_panel:customer_inquiries')

def blog_list(request):
    return render(request, 'admin/blog/blog_list.html')

#EMPLOYEE-----------------------------------------------------------------

def employee_list(request):
    employees = Employee.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        employees = employees.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(position__icontains=search_query) |
            Q(department__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        employees = employees.filter(status=status_filter)
    
    department_filter = request.GET.get('department', '')
    if department_filter:
        employees = employees.filter(department=department_filter)
    
    departments = Employee.objects.values_list('department', flat=True).distinct().order_by('department')
    department_count = departments.count()
    
    active_count = employees.filter(status='active').count()
    inactive_count = employees.filter(status='inactive').count()
    
    context = {
        'employees': employees,
        'search_query': search_query,
        'status_filter': status_filter,
        'department_filter': department_filter,
        'departments': departments,
        'active_count': active_count,
        'department_count': department_count,
        'now': datetime.now().strftime('%B %d, %Y')
    }
    return render(request, "admin/employee/employee.html", context)

def add_employee(request):
    if request.method == 'POST':
        try:
            employee = Employee.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                role=request.POST.get('role', ''),
                department=request.POST.get('department', ''),
                join_date=request.POST.get('join_date') or None,
                salary=request.POST.get('salary') or None,
                status=request.POST.get('status', 'Active'),
            )
            
            if request.FILES.get('profile_picture'):
                employee.profile_picture = request.FILES['profile_picture']
                employee.save()
            
            messages.success(request, f'Employee {employee.name} added successfully!')
            return redirect('employee:employee_list')
        except Exception as e:
            messages.error(request, f'Error adding employee: {str(e)}')
    return render(request, "admin/employee/add_employee.html")
           
    

def edit_employee(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found.')
        return redirect('employee:employee_list')
    
    if request.method == 'POST':
        try:
            employee.name = request.POST.get('name')
            employee.email = request.POST.get('email')
            employee.phone = request.POST.get('phone')
            employee.role = request.POST.get('role', '')
            employee.department = request.POST.get('department', '')
            employee.join_date = request.POST.get('join_date') or None
            employee.salary = request.POST.get('salary') or None
            employee.status = request.POST.get('status', 'Active')
            employee.save()
            
            messages.success(request, f'Employee {employee.name} updated successfully!')
            return redirect('employee:employee_list')
        except Exception as e:
            messages.error(request, f'Error updating employee: {str(e)}')
    
    return render(request, "admin/employee/edit_employee.html", {'employee': employee})

def delete_employee(request, pk):
    if request.method != 'POST':
        return redirect('employee:employee_list')
    
    try:
        employee = Employee.objects.get(pk=pk)
        employee_name = employee.name
        employee.delete()
        messages.success(request, f'Employee {employee_name} deleted successfully.')
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found.')
    except Exception as e:
        messages.error(request, f'Error deleting employee: {str(e)}')
    
    return redirect('employee:employee_list')

def view_employee(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
        return render(request, "admin/employee/view_employee.html", {'employee': employee})
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found.')
        return redirect('employee:employee_list')
#SALES--------------------------------------------------------------------
            #ACCOUNT

def account_list(request):
    accounts = Account.objects.all()
    return render(request, 'admin/sales/account/account.html', {
        'accounts': accounts
    })

def add_account(request):
    if request.method == 'POST':
        try:
            # Get form data
            account_name = request.POST.get('account_name', '').strip()
            account_number = request.POST.get('account_number', '').strip()
            bank_name = request.POST.get('bank_name', '').strip()
            ifsc_code = request.POST.get('ifsc_code', '').strip()
            account_type = request.POST.get('account_type', 'current')
            
            # Validation
            if not account_name or not account_number or not bank_name or not ifsc_code:
                messages.error(request, 'All fields are required.')
                return render(request, 'admin/sales/account/add_account.html')
            
            # Check for duplicate account number
            if Account.objects.filter(account_number=account_number).exists():
                messages.error(request, 'Account number already exists.')
                return render(request, 'admin/sales/account/add_account.html')
            
            # Create account
            account = Account.objects.create(
                account_name=account_name,
                account_number=account_number,
                bank_name=bank_name,
                ifsc_code=ifsc_code,
                account_type=account_type
            )
            
            messages.success(request, f"Account '{account_name}' added successfully!")
            return redirect('sales:account_list')
            
        except Exception as e:
            messages.error(request, f'Error adding account: {str(e)}')
            return render(request, 'admin/sales/account/add_account.html')
    
    return render(request, 'admin/sales/account/add_account.html')

def view_account(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        return render(request, 'admin/sales/account/view_account.html', {
            'account': account
        })
    except Account.DoesNotExist:
        messages.error(request, "Account not found.")
        return redirect("sales:account_list")


def edit_account(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        messages.error(request, "Account not found.")
        return redirect("sales:account_list")
    
    if request.method == "POST":
        try:
            # Get form data
            account_name = request.POST.get('account_name', '').strip()
            account_number = request.POST.get('account_number', '').strip()
            bank_name = request.POST.get('bank_name', '').strip()
            ifsc_code = request.POST.get('ifsc_code', '').strip()
            account_type = request.POST.get('account_type', '').strip()
            
            # Validation
            if not account_name or not account_number or not bank_name:
                messages.error(request, 'Account name, number, and bank name are required.')
                return render(request, 'admin/sales/account/edit_account.html', {
                    'account': account
                })
            
            # Update account
            account.account_name = account_name
            account.account_number = account_number
            account.bank_name = bank_name
            account.ifsc_code = ifsc_code
            account.account_type = account_type
            
            account.save()
            
            messages.success(request, f"Account '{account_name}' has been updated successfully!")
            return redirect("sales:account_list")
            
        except Exception as e:
            return render(request, 'admin/sales/account/edit_account.html', {
                'account': account,
                'error': f'Error updating account: {str(e)}'
            })
    
    return render(request, 'admin/sales/account/edit_account.html', {
        'account': account
    })


def delete_account(request, account_id):
    if request.method != 'POST':
        return redirect('sales:account_list')
    
    try:
        account = Account.objects.get(id=account_id)
        account_name = account.account_name
        account.delete()
        messages.success(request, f"Account '{account_name}' has been deleted successfully!")
    except Account.DoesNotExist:
        messages.error(request, "Account not found.")
    except Exception as e:
        messages.error(request, f"Error deleting account: {str(e)}")
    
    return redirect("sales:account_list")

        #CUSTOMER

def customer_list(request):
    customers = Customer.objects.all()
    print(f"=== CUSTOMER LIST DEBUG ===")
    print(f"Total customers in database: {customers.count()}")
    for customer in customers:
        print(f"  Customer {customer.id}: {customer.display_name} - {customer.contact_number}")
    return render(request, "admin/sales/customer/customer.html", {
        "customers": customers
    })

def add_customer(request):
    context = {"form": {}}

    if request.method == "POST":
        try:
            same_as_whatsapp = request.POST.get("same_as_whatsapp") == "on"

            customer_type = (request.POST.get("customer_type") or "Individual").strip()
            salutation = (request.POST.get("salutation") or "").strip()
            first_name = (request.POST.get("first_name") or "").strip()
            last_name = (request.POST.get("last_name") or "").strip()
            display_name = (request.POST.get("display_name") or "").strip()
            place = (request.POST.get("place") or "").strip()
            contact_number = (request.POST.get("contact_number") or "").strip()
            whatsapp_number = (request.POST.get("whatsapp_number") or "").strip()
            work_number = (request.POST.get("work_number") or "").strip()
            gst_number = (request.POST.get("gst_number") or "").strip()

            # Keep values in template if error
            context["form"] = {
                "customer_type": customer_type,
                "salutation": salutation,
                "first_name": first_name,
                "last_name": last_name,
                "display_name": display_name,
                "place": place,
                "contact_number": contact_number,
                "same_as_whatsapp": same_as_whatsapp,
                "whatsapp_number": whatsapp_number,
                "work_number": work_number,
                "gst_number": gst_number,
            }

            # Required validation
            if not first_name or not display_name or not contact_number:
                context["error"] = "First Name, Display Name, and Contact Number are required."
                return render(request, "admin/sales/customer/add_customer.html", context)

            # NO-JS WhatsApp logic
            if same_as_whatsapp:
                whatsapp_number = contact_number

            # IMPORTANT fallback:
            # If whatsapp_number is empty, set it to contact_number (prevents NOT NULL issues)
            if not whatsapp_number:
                whatsapp_number = contact_number

            # Optional: prevent duplicates if contact_number is unique
            if Customer.objects.filter(contact_number=contact_number).exists():
                context["error"] = "This Contact Number already exists."
                return render(request, "admin/sales/customer/add_customer.html", context)

            Customer.objects.create(
                customer_type=customer_type,
                salutation=salutation,
                first_name=first_name,
                last_name=last_name,
                display_name=display_name,
                place=place,
                contact_number=contact_number,
                same_as_whatsapp=same_as_whatsapp,
                whatsapp_number=whatsapp_number,
                work_number=work_number,
                gst_number=gst_number,
            )

            messages.success(request, f"Customer '{display_name}' added successfully!")
            return redirect("sales:customer_list")

        except IntegrityError as e:
            print("INTEGRITY ERROR:", str(e))
            context["error"] = f"Database error: {str(e)}"
            return render(request, "admin/sales/customer/add_customer.html", context)

        except Exception as e:
            import traceback
            traceback.print_exc()
            context["error"] = f"Error saving customer: {str(e)}"
            return render(request, "admin/sales/customer/add_customer.html", context)

    return render(request, "admin/sales/customer/add_customer.html", context)


def view_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        return render(request, "admin/sales/customer/view_customer.html", {
            "customer": customer
        })
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found.")
        return redirect("sales:customer_list")

def edit_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found.")
        return redirect("sales:customer_list")
    
    if request.method == "POST":
        try:
            same_as_whatsapp = request.POST.get("same_as_whatsapp") == "on"
            contact_number = request.POST.get("contact_number", "").strip()
            
            # Validate required fields
            first_name = request.POST.get("first_name", "").strip()
            display_name = request.POST.get("display_name", "").strip()
            customer_type = request.POST.get("customer_type", "Individual")
            
            if not first_name or not display_name:
                return render(request, "admin/sales/customer/edit_customer.html", {
                    "customer": customer,
                    "error": "First Name and Display Name are required fields."
                })
            
            if same_as_whatsapp:
                whatsapp_number = contact_number
            else:
                whatsapp_number = request.POST.get("whatsapp_number", "").strip()
            
            # Update customer
            customer.customer_type = customer_type
            customer.salutation = request.POST.get("salutation", "")
            customer.first_name = first_name
            customer.last_name = request.POST.get("last_name", "").strip()
            customer.display_name = display_name
            customer.place = request.POST.get("place", "").strip()
            customer.contact_number = contact_number
            customer.same_as_whatsapp = same_as_whatsapp
            customer.whatsapp_number = whatsapp_number
            customer.work_number = request.POST.get("work_number", "").strip()
            customer.gst_number = request.POST.get("gst_number", "").strip()
            
            customer.save()
            
            messages.success(request, f"Customer '{display_name}' has been updated successfully!")
            return redirect("sales:customer_list")
            
        except Exception as e:
            return render(request, "admin/sales/customer/edit_customer.html", {
                "customer": customer,
                "error": f"Error updating customer: {str(e)}"
            })
    
    return render(request, "admin/sales/customer/edit_customer.html", {
        "customer": customer
    })

def delete_customer(request, customer_id):
    if request.method != 'POST':
        return redirect('sales:customer_list')
    
    try:
        customer = Customer.objects.get(id=customer_id)
        customer_name = customer.display_name
        customer.delete()
        messages.success(request, f"Customer '{customer_name}' has been deleted successfully!")
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found.")
    except Exception as e:
        messages.error(request, f"Error deleting customer: {str(e)}")
    
    return redirect("sales:customer_list")


# RESORT VIEWS
def resort_list(request):
    resorts = Resort.objects.all()
    return render(request, "admin/sales/resort/resort.html", {"resorts": resorts})

def add_resort(request):
    if request.method == "POST":
        try:
            resort_name = request.POST.get("resort_name", "").strip()
            location = request.POST.get("location", "").strip()
            contact_person = request.POST.get("contact_person", "").strip()
            contact_number = request.POST.get("contact_number", "").strip()
            email = request.POST.get("email", "").strip()
            address = request.POST.get("address", "").strip()
            status = request.POST.get("status", "Active")
            
            if not resort_name or not location:
                messages.error(request, "Resort Name and Location are required.")
                return render(request, "admin/sales/resort/add_resort.html")
            
            if Resort.objects.filter(resort_name=resort_name).exists():
                messages.error(request, "Resort name already exists.")
                return render(request, "admin/sales/resort/add_resort.html")
            
            Resort.objects.create(
                resort_name=resort_name,
                location=location,
                contact_person=contact_person,
                contact_number=contact_number,
                email=email,
                address=address,
                status=status
            )
            messages.success(request, f"Resort '{resort_name}' added successfully!")
            return redirect("sales:resort_list")
        except Exception as e:
            messages.error(request, f"Error adding resort: {str(e)}")
            return render(request, "admin/sales/resort/add_resort.html")
    return render(request, "admin/sales/resort/add_resort.html")

def view_resort(request, resort_id):
    try:
        resort = Resort.objects.get(id=resort_id)
        return render(request, "admin/sales/resort/view_resort.html", {"resort": resort})
    except Resort.DoesNotExist:
        messages.error(request, "Resort not found.")
        return redirect("sales:resort_list")

def edit_resort(request, resort_id):
    try:
        resort = Resort.objects.get(id=resort_id)
    except Resort.DoesNotExist:
        messages.error(request, "Resort not found.")
        return redirect("sales:resort_list")
    
    if request.method == "POST":
        try:
            resort.resort_name = request.POST.get("resort_name", "").strip()
            resort.location = request.POST.get("resort_place", "").strip()  # Changed from "location" to "resort_place"
            resort.contact_person = request.POST.get("contact_person", "").strip()
            resort.contact_number = request.POST.get("contact_number", "").strip()
            resort.email = request.POST.get("email", "").strip()
            resort.address = request.POST.get("address", "").strip()
            resort.status = request.POST.get("status", "Active")
            resort.save()
            messages.success(request, f"Resort updated successfully!")
            return redirect("sales:resort_list")
        except Exception as e:
            return render(request, "admin/sales/resort/edit_resort.html", {
                "resort": resort,
                "error": f"Error updating resort: {str(e)}"
            })
    return render(request, "admin/sales/resort/edit_resort.html", {"resort": resort})

def delete_resort(request, resort_id):
    if request.method != 'POST':
        return redirect('sales:resort_list')
    
    try:
        resort = Resort.objects.get(id=resort_id)
        resort_name = resort.resort_name
        resort.delete()
        messages.success(request, f"Resort '{resort_name}' deleted successfully!")
    except Resort.DoesNotExist:
        messages.error(request, "Resort not found.")
    except Exception as e:
        messages.error(request, f"Error deleting resort: {str(e)}")
    return redirect("sales:resort_list")


# MEAL VIEWS
def meal_list(request):
    meals = Meal.objects.all()
    return render(request, "admin/sales/meals/meals.html", {"meals": meals})

def add_meal(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name", "").strip()
            description = request.POST.get("description", "").strip()
            included_meals = request.POST.getlist("included_meals")
            included_meals_str = ", ".join(included_meals) if included_meals else ""
            
            if not name:
                messages.error(request, "Meal Plan Name is required.")
                return render(request, "admin/sales/meals/add_meals.html")
            
            if Meal.objects.filter(name=name).exists():
                messages.error(request, "Meal plan name already exists.")
                return render(request, "admin/sales/meals/add_meals.html")
            
            Meal.objects.create(
                name=name,
                description=description,
                included_meals=included_meals_str
            )
            messages.success(request, f"Meal plan '{name}' added successfully!")
            return redirect("sales:meal_list")
        except Exception as e:
            messages.error(request, f"Error adding meal plan: {str(e)}")
            return render(request, "admin/sales/meals/add_meals.html")
    return render(request, "admin/sales/meals/add_meals.html")

def view_meal(request, meal_id):
    try:
        meal = Meal.objects.get(id=meal_id)
        return render(request, "admin/sales/meals/view_meals.html", {"meal": meal})
    except Meal.DoesNotExist:
        messages.error(request, "Meal not found.")
        return redirect("sales:meal_list")

def edit_meal(request, meal_id):
    try:
        meal = Meal.objects.get(id=meal_id)
    except Meal.DoesNotExist:
        messages.error(request, "Meal not found.")
        return redirect("sales:meal_list")
    
    if request.method == "POST":
        try:
            meal.meal_name = request.POST.get("meal_name", "").strip()
            meal.description = request.POST.get("description", "").strip()
            meal.price = request.POST.get("price", 0)
            meal.status = request.POST.get("status", "Available")
            meal.save()
            messages.success(request, f"Meal updated successfully!")
            return redirect("sales:meal_list")
        except Exception as e:
            return render(request, "admin/sales/meals/edit_meals.html", {
                "meal": meal,
                "error": f"Error updating meal: {str(e)}"
            })
    return render(request, "admin/sales/meals/edit_meals.html", {"meal": meal})

def delete_meal(request, meal_id):
    if request.method != 'POST':
        return redirect('sales:meal_list')
    
    try:
        meal = Meal.objects.get(id=meal_id)
        meal_name = meal.meal_name
        meal.delete()
        messages.success(request, f"Meal '{meal_name}' deleted successfully!")
    except Meal.DoesNotExist:
        messages.error(request, "Meal not found.")
    except Exception as e:
        messages.error(request, f"Error deleting meal: {str(e)}")
    return redirect("sales:meal_list")


# VOUCHER VIEWS
def voucher_list(request):
    vouchers = Voucher.objects.all()
    return render(request, "admin/sales/vouchers/vouchers.html", {"vouchers": vouchers})

def add_voucher(request):
    customers = Customer.objects.all()
    resorts = Resort.objects.all()
    accounts = Account.objects.all()
    employees = Employee.objects.filter(status='Active')
    meals = Meal.objects.all()
    
    if request.method == "POST":
        try:
            Voucher.objects.create(
                customer_id=request.POST.get("customer_id"),
                voucher_no=request.POST.get("voucher_no", "").strip(),
                voucher_date=request.POST.get("voucher_date"),
                sales_person_id=request.POST.get("sales_person") or None,
                resort_id=request.POST.get("resort") or None,
                checkin_date=request.POST.get("checkin_date"),
                checkout_date=request.POST.get("checkout_date"),
                checkin_time=request.POST.get("checkin_time"),
                checkout_time=request.POST.get("checkout_time"),
                adults=request.POST.get("adults", 0),
                children=request.POST.get("children", 0),
                nights=request.POST.get("nights", 1),
                pax_notes=request.POST.get("pax_notes", "").strip(),
                room_type=request.POST.get("room_type", "").strip(),
                no_of_rooms=request.POST.get("no_of_rooms", 1),
                meals_plan_id=request.POST.get("meals_plan") or None,
                bank_account_id=request.POST.get("bank_account") or None,
                package_price=request.POST.get("package_price", 0),
                resort_price=request.POST.get("resort_price", 0),
                total_amount=request.POST.get("total_amount", 0),
                received=request.POST.get("received", 0),
                pending=request.POST.get("pending", 0),
                from_whytehouse=request.POST.get("from_whytehouse", 0),
                profit=request.POST.get("profit", 0),
                note_for_resort=request.POST.get("note_for_resort", "").strip(),
                note_for_guest=request.POST.get("note_for_guest", "").strip()
            )
            messages.success(request, f"Voucher added successfully!")
            return redirect("sales:voucher_list")
        except Exception as e:
            messages.error(request, f"Error adding voucher: {str(e)}")
    return render(request, "admin/sales/vouchers/add_vouchers.html", {"customers": customers, "resorts": resorts, "accounts": accounts, "employees": employees, "meals": meals})

def view_voucher(request, voucher_id):
    try:
        voucher = Voucher.objects.get(id=voucher_id)
        return render(request, "admin/sales/vouchers/view_vouchers.html", {"voucher": voucher})
    except Voucher.DoesNotExist:
        messages.error(request, "Voucher not found.")
        return redirect("sales:voucher_list")

def edit_voucher(request, voucher_id):
    try:
        voucher = Voucher.objects.get(id=voucher_id)
    except Voucher.DoesNotExist:
        messages.error(request, "Voucher not found.")
        return redirect("sales:voucher_list")
    
    if request.method == "POST":
        try:
            voucher.voucher_code = request.POST.get("voucher_code", "").strip()
            voucher.discount_amount = request.POST.get("discount_amount", 0)
            voucher.discount_percentage = request.POST.get("discount_percentage", 0) or None
            voucher.description = request.POST.get("description", "").strip()
            voucher.valid_from = request.POST.get("valid_from")
            voucher.valid_till = request.POST.get("valid_till")
            voucher.status = request.POST.get("status", "Active")
            voucher.save()
            messages.success(request, f"Voucher updated successfully!")
            return redirect("sales:voucher_list")
        except Exception as e:
            return render(request, "admin/sales/vouchers/edit_vouchers.html", {
                "voucher": voucher,
                "error": f"Error updating voucher: {str(e)}"
            })
    return render(request, "admin/sales/vouchers/edit_vouchers.html", {"voucher": voucher})

def delete_voucher(request, voucher_id):
    if request.method != 'POST':
        return redirect('sales:voucher_list')
    
    try:
        voucher = Voucher.objects.get(id=voucher_id)
        voucher_no = voucher.voucher_no
        voucher.delete()
        messages.success(request, f"Voucher '{voucher_no}' deleted successfully!")
    except Voucher.DoesNotExist:
        messages.error(request, "Voucher not found.")
    except Exception as e:
        messages.error(request, f"Error deleting voucher: {str(e)}")
    return redirect("sales:voucher_list")


# INVOICE VIEWS
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-invoice_date', '-id')
    return render(request, "admin/sales/invoice/invoice.html", {"invoices": invoices})

def add_invoice(request):
    customers = Customer.objects.all()
    resorts = Resort.objects.all()
    accounts = Account.objects.all()
    employees = Employee.objects.filter(status='Active')
    
    if request.method == "POST":
        try:
            customer_id = request.POST.get("customer_id")
            invoice_no = request.POST.get("invoice_no", "").strip()
            invoice_date = request.POST.get("invoice_date")
            sales_person_id = request.POST.get("sales_person")
            resort_id = request.POST.get("resort")
            checkin_date = request.POST.get("checkin_date") or None
            checkout_date = request.POST.get("checkout_date") or None
            checkin_time = request.POST.get("checkin_time") or None
            checkout_time = request.POST.get("checkout_time") or None
            adults = request.POST.get("adults", 0)
            children = request.POST.get("children", 0)
            pax_total = request.POST.get("pax_total", 0)
            pax_notes = request.POST.get("pax_notes", "").strip()
            nights = request.POST.get("nights", 1)
            room_type = request.POST.get("room_type", "").strip()
            rooms = request.POST.get("rooms", 1)
            meals_plan = request.POST.get("meals_plan", "").strip()
            bank_account_id = request.POST.get("bank_account")
            package_price = request.POST.get("package_price", 0)
            tax = request.POST.get("tax", 0)
            resort_price = request.POST.get("resort_price", 0)
            total = request.POST.get("total", 0)
            received = request.POST.get("received", 0)
            pending = request.POST.get("pending", 0)
            profit = request.POST.get("profit", 0)
            notes = request.POST.get("notes", "").strip()
            
            if not customer_id or not invoice_no or not invoice_date:
                messages.error(request, "Customer, Invoice No, and Invoice Date are required.")
                return render(request, "admin/sales/invoice/add_invoice.html", {"customers": customers, "resorts": resorts, "accounts": accounts, "employees": employees})
            
            if Invoice.objects.filter(invoice_no=invoice_no).exists():
                messages.error(request, "Invoice number already exists.")
                return render(request, "admin/sales/invoice/add_invoice.html", {"customers": customers, "resorts": resorts, "accounts": accounts, "employees": employees})
            
            Invoice.objects.create(
                customer_id=customer_id,
                invoice_no=invoice_no,
                invoice_date=invoice_date,
                sales_person_id=sales_person_id if sales_person_id else None,
                resort_id=resort_id if resort_id else None,
                checkin_date=checkin_date,
                checkout_date=checkout_date,
                checkin_time=checkin_time,
                checkout_time=checkout_time,
                adults=adults,
                children=children,
                pax_total=pax_total,
                pax_notes=pax_notes,
                nights=nights,
                room_type=room_type,
                rooms=rooms,
                meals_plan=meals_plan,
                bank_account_id=bank_account_id if bank_account_id else None,
                package_price=package_price,
                tax=tax,
                resort_price=resort_price,
                total=total,
                received=received,
                pending=pending,
                profit=profit,
                notes=notes
            )
            messages.success(request, f"Invoice '{invoice_no}' added successfully!")
            return redirect("sales:invoice_list")
        except Exception as e:
            messages.error(request, f"Error adding invoice: {str(e)}")
            return render(request, "admin/sales/invoice/add_invoice.html", {"customers": customers, "resorts": resorts, "accounts": accounts, "employees": employees})
    return render(request, "admin/sales/invoice/add_invoice.html", {"customers": customers, "resorts": resorts, "accounts": accounts, "employees": employees})

def view_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        return render(request, "admin/sales/invoice/view_invoice.html", {"invoice": invoice})
    except Invoice.DoesNotExist:
        messages.error(request, "Invoice not found.")
        return redirect("sales:invoice_list")

def edit_invoice(request, invoice_id):
    customers = Customer.objects.all()
    resorts = Resort.objects.all()
    accounts = Account.objects.all()
    employees = Employee.objects.filter(status='Active')
    
    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        messages.error(request, "Invoice not found.")
        return redirect("sales:invoice_list")
    
    if request.method == "POST":
        try:
            invoice.customer_id = request.POST.get("customer_id")
            invoice.invoice_no = request.POST.get("invoice_no", "").strip()
            invoice.invoice_date = request.POST.get("invoice_date")
            invoice.sales_person_id = request.POST.get("sales_person") or None
            invoice.resort_id = request.POST.get("resort") or None
            invoice.checkin_date = request.POST.get("checkin_date") or None
            invoice.checkout_date = request.POST.get("checkout_date") or None
            invoice.checkin_time = request.POST.get("checkin_time") or None
            invoice.checkout_time = request.POST.get("checkout_time") or None
            invoice.adults = request.POST.get("adults", 0)
            invoice.children = request.POST.get("children", 0)
            invoice.pax_total = request.POST.get("pax_total", 0)
            invoice.pax_notes = request.POST.get("pax_notes", "").strip()
            invoice.nights = request.POST.get("nights", 1)
            invoice.room_type = request.POST.get("room_type", "").strip()
            invoice.rooms = request.POST.get("rooms", 1)
            invoice.meals_plan = request.POST.get("meals_plan", "").strip()
            invoice.bank_account_id = request.POST.get("bank_account") or None
            invoice.package_price = request.POST.get("package_price", 0)
            invoice.tax = request.POST.get("tax", 0)
            invoice.resort_price = request.POST.get("resort_price", 0)
            invoice.total = request.POST.get("total", 0)
            invoice.received = request.POST.get("received", 0)
            invoice.pending = request.POST.get("pending", 0)
            invoice.profit = request.POST.get("profit", 0)
            invoice.notes = request.POST.get("notes", "").strip()
            invoice.save()
            
            messages.success(request, f"Invoice '{invoice.invoice_no}' updated successfully!")
            return redirect("sales:invoice_list")
        except Exception as e:
            return render(request, "admin/sales/invoice/edit_invoice.html", {
                "invoice": invoice,
                "customers": customers,
                "resorts": resorts,
                "accounts": accounts,
                "employees": employees,
                "error": f"Error updating invoice: {str(e)}"
            })
    return render(request, "admin/sales/invoice/edit_invoice.html", {"invoice": invoice, "customers": customers, "resorts": resorts, "accounts": accounts, "employees": employees})

def delete_invoice(request, invoice_id):
    if request.method != 'POST':
        return redirect('sales:invoice_list')
    
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        invoice_no = invoice.invoice_no
        invoice.delete()
        messages.success(request, f"Invoice '{invoice_no}' deleted successfully!")
    except Invoice.DoesNotExist:
        messages.error(request, "Invoice not found.")
    except Exception as e:
        messages.error(request, f"Error deleting invoice: {str(e)}")
    return redirect("sales:invoice_list")

def blog_list(request):
    blogs = Blog.objects.all()

    search_query = request.GET.get("search", "").strip()
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(author_name__icontains=search_query) |
            Q(slug__icontains=search_query) |
            Q(status__icontains=search_query)
        )

    status_filter = request.GET.get("status", "").strip()
    if status_filter:
        blogs = blogs.filter(status=status_filter)

    published_count = blogs.filter(status="published").count()
    draft_count = blogs.filter(status="draft").count()

    context = {
        "blogs": blogs,
        "search_query": search_query,
        "status_filter": status_filter,
        "published_count": published_count,
        "draft_count": draft_count,
        "now": datetime.now().strftime("%B %d, %Y"),
    }
    return render(request, "admin/blog/blog.html", context)


def add_blog(request):
    if request.method == "POST":
        try:
            hashtags_value = (request.POST.get("hashtags") or "").strip()
            
            blog = Blog.objects.create(
                title=(request.POST.get("title") or "").strip(),
                slug=(request.POST.get("slug") or "").strip(),
                excerpt=(request.POST.get("excerpt") or "").strip(),
                content=(request.POST.get("content") or "").strip(),
                status=request.POST.get("status", "draft"),
                category=request.POST.get("category", "other"),
                package_id=(request.POST.get("package_id") or "").strip() or None,

                author_name=(request.POST.get("author_name") or "").strip(),
                author_summary=(request.POST.get("author_summary") or "").strip(),
                reading_time=int(request.POST.get("reading_time") or 1),
                publish_date=request.POST.get("publish_date"),

                featured_image_url=(request.POST.get("featured_image_url") or "").strip() or None,
                hashtags=hashtags_value,
                tags=hashtags_value,  # Save to both fields for compatibility
            )

            if request.FILES.get("featured_image"):
                blog.featured_image = request.FILES["featured_image"]
                blog.save()

            # Handle content images
            content_images = request.FILES.getlist("content_images")
            for idx, image_file in enumerate(content_images):
                BlogImage.objects.create(
                    blog=blog,
                    image=image_file,
                    order=idx
                )

            messages.success(request, "Blog created successfully!")
            return redirect("blog:blog_list")

        except Exception as e:
            messages.error(request, f"Error creating blog: {str(e)}")

    return render(request, "admin/blog/add_blog.html")


def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == "POST":
        try:
            hashtags_value = (request.POST.get("hashtags") or "").strip()
            
            blog.title = (request.POST.get("title") or "").strip()
            blog.slug = (request.POST.get("slug") or "").strip()
            blog.excerpt = (request.POST.get("excerpt") or "").strip()
            blog.content = (request.POST.get("content") or "").strip()
            blog.status = request.POST.get("status", "draft")
            blog.category = request.POST.get("category", "other")
            blog.package_id = (request.POST.get("package_id") or "").strip() or None

            blog.author_name = (request.POST.get("author_name") or "").strip()
            blog.author_summary = (request.POST.get("author_summary") or "").strip()
            blog.reading_time = int(request.POST.get("reading_time") or 1)
            blog.publish_date = request.POST.get("publish_date")

            blog.featured_image_url = (request.POST.get("featured_image_url") or "").strip() or None
            blog.hashtags = hashtags_value
            blog.tags = hashtags_value  # Save to both fields for compatibility

            if request.FILES.get("featured_image"):
                blog.featured_image = request.FILES["featured_image"]

            blog.save()

            # Handle deleted content images
            deleted_images = request.POST.get("deleted_images", "")
            if deleted_images:
                deleted_ids = [int(id) for id in deleted_images.split(",") if id.strip()]
                BlogImage.objects.filter(id__in=deleted_ids, blog=blog).delete()
                
                # Reorder remaining images
                remaining_images = blog.content_images.all().order_by('order')
                for idx, img in enumerate(remaining_images):
                    img.order = idx
                    img.save()

            # Handle new content images
            content_images = request.FILES.getlist("content_images")
            if content_images:
                # Get current max order
                current_max = blog.content_images.count()
                for idx, image_file in enumerate(content_images):
                    BlogImage.objects.create(
                        blog=blog,
                        image=image_file,
                        order=current_max + idx
                    )

            messages.success(request, "Blog updated successfully!")
            return redirect("blog:blog_list")

        except Exception as e:
            messages.error(request, f"Error updating blog: {str(e)}")

    return render(request, "admin/blog/edit_blog.html", {"blog": blog})


def view_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    tags = []
    if blog.hashtags:
        tags = [t.strip() for t in blog.hashtags.split(",") if t.strip()]

    # Replace {{image1}}, {{image2}}, etc. with actual image HTML
    content = blog.content
    content_images = blog.content_images.all()
    
    # Normalize line endings and split content
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Split by lines and process
    lines = content.split('\n')
    processed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # Check if this line contains an image tag
        has_image = False
        
        for idx, img in enumerate(content_images):
            image_num = idx + 1
            
            # Check for left positioned image
            placeholder_left = f"{{{{image{image_num}-left}}}}"
            if placeholder_left in line:
                # Get the text before the image tag (could be on same line or previous lines)
                text_content = line.replace(placeholder_left, '').strip()
                
                # If no text on this line, look at previous non-empty lines
                if not text_content and processed_lines:
                    # Get previous paragraph
                    prev_content = []
                    while processed_lines and not processed_lines[-1].startswith('<'):
                        prev_content.insert(0, processed_lines.pop())
                    text_content = ' '.join(prev_content)
                
                # Create side-by-side layout with image on left
                processed_lines.append(f'''
                    <div class="content-row">
                        <figure class="content-image-left">
                            <img src="{img.image.url}" alt="Content image {image_num}">
                        </figure>
                        <div class="content-text"><p>{text_content}</p></div>
                    </div>
                ''')
                has_image = True
                break
            
            # Check for right positioned image
            placeholder_right = f"{{{{image{image_num}-right}}}}"
            if placeholder_right in line:
                # Get the text before the image tag
                text_content = line.replace(placeholder_right, '').strip()
                
                # If no text on this line, look at previous non-empty lines
                if not text_content and processed_lines:
                    # Get previous paragraph
                    prev_content = []
                    while processed_lines and not processed_lines[-1].startswith('<'):
                        prev_content.insert(0, processed_lines.pop())
                    text_content = ' '.join(prev_content)
                
                # Create side-by-side layout with image on right
                processed_lines.append(f'''
                    <div class="content-row">
                        <div class="content-text"><p>{text_content}</p></div>
                        <figure class="content-image-right">
                            <img src="{img.image.url}" alt="Content image {image_num}">
                        </figure>
                    </div>
                ''')
                has_image = True
                break
            
            # Check for center positioned image
            placeholder_center = f"{{{{image{image_num}-center}}}}"
            if placeholder_center in line:
                text_content = line.replace(placeholder_center, '').strip()
                if text_content:
                    processed_lines.append(f'<p>{text_content}</p>')
                processed_lines.append(f'''
                    <figure class="content-image-center">
                        <img src="{img.image.url}" alt="Content image {image_num}">
                    </figure>
                ''')
                has_image = True
                break
            
            # Check for default (center) positioned image
            placeholder_default = f"{{{{image{image_num}}}}}"
            if placeholder_default in line:
                text_content = line.replace(placeholder_default, '').strip()
                if text_content:
                    processed_lines.append(f'<p>{text_content}</p>')
                processed_lines.append(f'''
                    <figure class="content-image-center">
                        <img src="{img.image.url}" alt="Content image {image_num}">
                    </figure>
                ''')
                has_image = True
                break
        
        # If no image found in this line, add it as regular text
        if not has_image and line:
            processed_lines.append(line)
        
        i += 1
    
    content = '\n'.join(processed_lines)

    return render(request, "admin/blog/view_blog.html", {"blog": blog, "tags": tags, "processed_content": content})


def delete_blog(request, blog_id):
    if request.method != "POST":
        return redirect("blog:blog_list")

    blog = get_object_or_404(Blog, id=blog_id)
    title = blog.title
    blog.delete()
    messages.success(request, f"Blog '{title}' deleted successfully!")
    return redirect("blog:blog_list")
# REPORT GENERATION VIEWS-----------------------------------------------------------

def customer_report(request):
    customers = Customer.objects.all().order_by("-created_at")

    if request.method == "POST" and request.POST.get("action") == "excel":
        wb = Workbook()
        ws = wb.active
        ws.title = "Customers"

        headers = ["Sl No", "First Name", "Last Name", "Display Name", "Place", "Mobile", "WhatsApp"]
        ws.append(headers)

        for i, c in enumerate(customers, start=1):
            ws.append([
                i,
                c.first_name or "",
                c.last_name or "",
                c.display_name or "",
                c.place or "",
                c.contact_number or "",
                c.whatsapp_number or "",
            ])

        # Auto width
        for col in range(1, len(headers) + 1):
            letter = get_column_letter(col)
            max_len = 0
            for cell in ws[letter]:
                if cell.value is not None:
                    max_len = max(max_len, len(str(cell.value)))
            ws.column_dimensions[letter].width = min(max_len + 3, 45)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        filename = f"customer_report_{timezone.now().strftime('%Y-%m-%d')}.xlsx"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        wb.save(response)
        return response

    return render(request, "admin/report/customer_report.html", {"customers": customers})

def invoice_report(request):
    resorts = Resort.objects.all().order_by("resort_name")
    invoices = Invoice.objects.none()
    employee_view = False
    employees = Employee.objects.none()

    selected = {"from_date": "", "to_date": "", "resort": "", "employee": ""}

    if request.method == "POST":
        action = request.POST.get("action")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        resort_id = request.POST.get("resort")
        employee_view = request.POST.get("employee_view") == "on"
        employee_id = request.POST.get("employee")

        selected = {
            "from_date": from_date or "",
            "to_date": to_date or "",
            "resort": resort_id or "",
            "employee": employee_id or "",
        }

        if from_date and to_date and resort_id:
            try:
                fd = datetime.strptime(from_date, "%Y-%m-%d").date()
                td = datetime.strptime(to_date, "%Y-%m-%d").date()
                
                # Filter employees who have invoices in the selected date range and resort
                if employee_view:
                    employee_ids = Invoice.objects.filter(
                        resort_id=resort_id,
                        invoice_date__range=(fd, td),
                        sales_person__isnull=False
                    ).values_list('sales_person_id', flat=True).distinct()
                    
                    employees = Employee.objects.filter(
                        id__in=employee_ids,
                        status="Active"
                    ).order_by("name")

                # Base queryset
                qs = Invoice.objects.select_related(
                    "customer", "resort", "sales_person", "bank_account"
                ).filter(resort_id=resort_id, invoice_date__range=(fd, td))

                # Employee filter
                if employee_view and employee_id:
                    qs = qs.filter(sales_person_id=employee_id)

                invoices = qs.order_by("-invoice_date", "-id")

                # Excel export
                if action == "excel":
                    wb = Workbook()
                    ws = wb.active
                    ws.title = "Invoice Report"

                    headers = [
                        "Invoice No", "Invoice Date",
                        "Customer", "Mobile",
                        "Sales Person",
                        "Resort",
                        "Check-in Date", "Check-out Date",
                        "Check-in Time", "Check-out Time",
                        "Adults", "Children", "Pax Total", "Pax Notes",
                        "Nights", "Room Type", "Rooms", "Meals Plan",
                        "Bank Account",
                        "Package Price", "Tax", "Resort Price",
                        "Total", "Received", "Pending", "Profit",
                        "Notes",
                    ]

                    for col, header in enumerate(headers, 1):
                        cell = ws.cell(row=1, column=col, value=header)
                        cell.font = Font(bold=True)
                        cell.alignment = Alignment(horizontal="center", vertical="center")

                    for row, inv in enumerate(invoices, start=2):
                        ws.cell(row=row, column=1, value=inv.invoice_no)
                        ws.cell(row=row, column=2, value=inv.invoice_date.strftime("%d/%m/%Y") if inv.invoice_date else "")

                        ws.cell(row=row, column=3, value=inv.customer.display_name if inv.customer else "")
                        ws.cell(row=row, column=4, value=getattr(inv.customer, "contact_number", "") if inv.customer else "")

                        ws.cell(row=row, column=5, value=inv.sales_person.name if inv.sales_person else "")
                        ws.cell(row=row, column=6, value=inv.resort.resort_name if inv.resort else "")

                        ws.cell(row=row, column=7, value=inv.checkin_date.strftime("%d/%m/%Y") if inv.checkin_date else "")
                        ws.cell(row=row, column=8, value=inv.checkout_date.strftime("%d/%m/%Y") if inv.checkout_date else "")

                        ws.cell(row=row, column=9, value=str(inv.checkin_time) if inv.checkin_time else "")
                        ws.cell(row=row, column=10, value=str(inv.checkout_time) if inv.checkout_time else "")

                        ws.cell(row=row, column=11, value=int(inv.adults or 0))
                        ws.cell(row=row, column=12, value=int(inv.children or 0))
                        ws.cell(row=row, column=13, value=int(inv.pax_total or 0))
                        ws.cell(row=row, column=14, value=inv.pax_notes or "")

                        ws.cell(row=row, column=15, value=int(inv.nights or 0))
                        ws.cell(row=row, column=16, value=inv.room_type or "")
                        ws.cell(row=row, column=17, value=int(inv.rooms or 0))
                        ws.cell(row=row, column=18, value=inv.meals_plan or "")

                        ws.cell(row=row, column=19, value=inv.bank_account.account_name if inv.bank_account else "")

                        ws.cell(row=row, column=20, value=float(inv.package_price or 0))
                        ws.cell(row=row, column=21, value=float(inv.tax or 0))
                        ws.cell(row=row, column=22, value=float(inv.resort_price or 0))

                        ws.cell(row=row, column=23, value=float(inv.total or 0))
                        ws.cell(row=row, column=24, value=float(inv.received or 0))
                        ws.cell(row=row, column=25, value=float(inv.pending or 0))
                        ws.cell(row=row, column=26, value=float(inv.profit or 0))

                        ws.cell(row=row, column=27, value=inv.notes or "")

                    # Auto width
                    for col in range(1, len(headers) + 1):
                        letter = get_column_letter(col)
                        max_len = 0
                        for c in ws[letter]:
                            if c.value:
                                max_len = max(max_len, len(str(c.value)))
                        ws.column_dimensions[letter].width = min(max_len + 3, 45)

                    response = HttpResponse(
                        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    filename = f"invoice_report_{fd.strftime('%d%m%Y')}_{td.strftime('%d%m%Y')}.xlsx"
                    response["Content-Disposition"] = f'attachment; filename="{filename}"'
                    wb.save(response)
                    return response

            except ValueError:
                messages.error(request, "Invalid date format.")

    return render(request, "admin/report/invoice_report.html", {
        "employees": employees,
        "resorts": resorts,
        "invoices": invoices,
        "employee_view": employee_view,
        "selected": selected,
    })



def voucher_report(request):
    resorts = Resort.objects.all().order_by("resort_name")
    vouchers = Voucher.objects.none()
    employee_view = False
    employees = Employee.objects.none()
    
    selected = {"from_date": "", "to_date": "", "resort": "", "employee": ""}
    
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        resort_id = request.POST.get("resort")
        employee_view = request.POST.get("employee_view") == "on"
        employee_id = request.POST.get("employee")
        action = request.POST.get("action")
        
        selected = {
            "from_date": from_date or "",
            "to_date": to_date or "",
            "resort": resort_id or "",
            "employee": employee_id or "",
        }
        
        if from_date and to_date and resort_id:
            try:
                fd = datetime.strptime(from_date, "%Y-%m-%d").date()
                td = datetime.strptime(to_date, "%Y-%m-%d").date()
                
                # Filter employees who have vouchers in the selected date range and resort
                if employee_view:
                    employee_ids = Voucher.objects.filter(
                        resort_id=resort_id,
                        voucher_date__range=(fd, td),
                        sales_person__isnull=False
                    ).values_list('sales_person_id', flat=True).distinct()
                    
                    employees = Employee.objects.filter(
                        id__in=employee_ids,
                        status="Active"
                    ).order_by("name")
                
                # Base queryset
                qs = Voucher.objects.select_related(
                    "customer", "resort", "sales_person", "bank_account", "meals_plan"
                ).filter(resort_id=resort_id, voucher_date__range=(fd, td))
                
                # Employee filter
                if employee_view and employee_id:
                    qs = qs.filter(sales_person_id=employee_id)
                
                vouchers = qs.order_by("-voucher_date", "-id")
                
                # Excel export
                if action == "excel":
                    wb = Workbook()
                    ws = wb.active
                    ws.title = "Voucher Report"
                    
                    # Header styling
                    header_fill = PatternFill(start_color="D4A017", end_color="D4A017", fill_type="solid")
                    header_font = Font(bold=True, color="FFFFFF")
                    
                    # Headers
                    headers = ["Voucher No", "Date", "Customer", "Resort", "Total Amount"]
                    if employee_view:
                        headers.insert(3, "Sales Person")
                    
                    for col_num, header in enumerate(headers, 1):
                        cell = ws.cell(row=1, column=col_num, value=header)
                        cell.fill = header_fill
                        cell.font = header_font
                        cell.alignment = Alignment(horizontal="center", vertical="center")
                    
                    # Data rows
                    for row_num, voucher in enumerate(vouchers, 2):
                        ws.cell(row=row_num, column=1, value=voucher.voucher_no)
                        ws.cell(row=row_num, column=2, value=voucher.voucher_date.strftime("%d/%m/%Y"))
                        ws.cell(row=row_num, column=3, value=voucher.customer.display_name if voucher.customer else "-")
                        
                        if employee_view:
                            ws.cell(row=row_num, column=4, value=voucher.sales_person.name if voucher.sales_person else "-")
                            ws.cell(row=row_num, column=5, value=voucher.resort.resort_name if voucher.resort else "-")
                            ws.cell(row=row_num, column=6, value=float(voucher.total))
                        else:
                            ws.cell(row=row_num, column=4, value=voucher.resort.resort_name if voucher.resort else "-")
                            ws.cell(row=row_num, column=5, value=float(voucher.total))
                    
                    # Auto-adjust column widths
                    for col in ws.columns:
                        max_length = 0
                        column = col[0].column_letter
                        for cell in col:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)
                        ws.column_dimensions[column].width = adjusted_width
                    
                    response = HttpResponse(
                        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    response["Content-Disposition"] = f'attachment; filename="voucher_report_{fd.strftime("%d%m%Y")}_{td.strftime("%d%m%Y")}.xlsx"'
                    wb.save(response)
                    return response
                
            except ValueError:
                messages.error(request, "Invalid date format.")
    
    return render(request, "admin/report/voucher_report.html", {
        "resorts": resorts,
        "vouchers": vouchers,
        "employees": employees,
        "employee_view": employee_view,
        "selected": selected,
    })

def leads_report(request):
    leads = Lead.objects.none()
    selected = {"from_date": "", "to_date": "", "enquiry_type": ""}
    
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        enquiry_type = request.POST.get("enquiry_type")
        action = request.POST.get("action")
        
        selected = {
            "from_date": from_date or "",
            "to_date": to_date or "",
            "enquiry_type": enquiry_type or "",
        }
        
        if from_date and to_date:
            try:
                fd = datetime.strptime(from_date, "%Y-%m-%d").date()
                td = datetime.strptime(to_date, "%Y-%m-%d").date()
                
                # Base queryset
                qs = Lead.objects.filter(created_at__date__range=(fd, td))
                
                # Enquiry type filter
                if enquiry_type:
                    qs = qs.filter(enquiry_type=enquiry_type)
                
                leads = qs.order_by("-created_at")
                
                # Excel export
                if action == "excel":
                    wb = Workbook()
                    ws = wb.active
                    ws.title = "Leads Report"
                    
                    # Header styling
                    header_fill = PatternFill(start_color="D4A017", end_color="D4A017", fill_type="solid")
                    header_font = Font(bold=True, color="FFFFFF")
                    
                    # Headers
                    headers = ["Full Name", "Mobile Number", "Place", "Source", "Enquiry Type", "Remarks", "Created Date"]
                    
                    for col_num, header in enumerate(headers, 1):
                        cell = ws.cell(row=1, column=col_num, value=header)
                        cell.fill = header_fill
                        cell.font = header_font
                        cell.alignment = Alignment(horizontal="center", vertical="center")
                    
                    # Data rows
                    for row_num, lead in enumerate(leads, 2):
                        ws.cell(row=row_num, column=1, value=lead.full_name)
                        ws.cell(row=row_num, column=2, value=lead.mobile_number)
                        ws.cell(row=row_num, column=3, value=lead.place or "-")
                        ws.cell(row=row_num, column=4, value=lead.get_source_display())
                        ws.cell(row=row_num, column=5, value=lead.get_enquiry_type_display())
                        ws.cell(row=row_num, column=6, value=lead.remarks or "-")
                        ws.cell(row=row_num, column=7, value=lead.created_at.strftime("%d/%m/%Y %H:%M"))
                    
                    # Auto-adjust column widths
                    for col in ws.columns:
                        max_length = 0
                        column = col[0].column_letter
                        for cell in col:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)
                        ws.column_dimensions[column].width = adjusted_width
                    
                    response = HttpResponse(
                        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    response["Content-Disposition"] = f'attachment; filename="leads_report_{fd.strftime("%d%m%Y")}_{td.strftime("%d%m%Y")}.xlsx"'
                    wb.save(response)
                    return response
                
            except ValueError:
                messages.error(request, "Invalid date format.")
    
    return render(request, "admin/report/leads_report.html", {
        "leads": leads,
        "selected": selected,
    })

def profit_report(request):
    resorts = Resort.objects.all().order_by("resort_name")
    invoices = Invoice.objects.none()
    employee_view = False
    employees = Employee.objects.none()
    
    selected = {"from_date": "", "to_date": "", "resort": "", "employee": ""}
    
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        resort_id = request.POST.get("resort")
        employee_view = request.POST.get("employee_view") == "on"
        employee_id = request.POST.get("employee")
        action = request.POST.get("action")
        
        selected = {
            "from_date": from_date or "",
            "to_date": to_date or "",
            "resort": resort_id or "",
            "employee": employee_id or "",
        }
        
        if from_date and to_date and resort_id:
            try:
                fd = datetime.strptime(from_date, "%Y-%m-%d").date()
                td = datetime.strptime(to_date, "%Y-%m-%d").date()
                
                # Filter employees who have invoices in the selected date range and resort
                if employee_view:
                    employee_ids = Invoice.objects.filter(
                        resort_id=resort_id,
                        invoice_date__range=(fd, td),
                        sales_person__isnull=False
                    ).values_list('sales_person_id', flat=True).distinct()
                    
                    employees = Employee.objects.filter(
                        id__in=employee_ids,
                        status="Active"
                    ).order_by("name")
                
                # Base queryset
                qs = Invoice.objects.select_related(
                    "customer", "resort", "sales_person"
                ).filter(resort_id=resort_id, invoice_date__range=(fd, td))
                
                # Employee filter
                if employee_view and employee_id:
                    qs = qs.filter(sales_person_id=employee_id)
                
                invoices = qs.order_by("-invoice_date", "-id")
                
                # Excel export
                if action == "excel":
                    wb = Workbook()
                    ws = wb.active
                    ws.title = "Profit Report"
                    
                    # Header styling
                    header_fill = PatternFill(start_color="D4A017", end_color="D4A017", fill_type="solid")
                    header_font = Font(bold=True, color="FFFFFF")
                    
                    # Headers
                    headers = ["Invoice No", "Date", "Customer", "Resort", "Total", "Resort Cost", "Profit"]
                    if employee_view:
                        headers.insert(3, "Sales Person")
                    
                    for col_num, header in enumerate(headers, 1):
                        cell = ws.cell(row=1, column=col_num, value=header)
                        cell.fill = header_fill
                        cell.font = header_font
                        cell.alignment = Alignment(horizontal="center", vertical="center")
                    
                    # Data rows
                    for row_num, invoice in enumerate(invoices, 2):
                        ws.cell(row=row_num, column=1, value=invoice.invoice_no)
                        ws.cell(row=row_num, column=2, value=invoice.invoice_date.strftime("%d/%m/%Y"))
                        ws.cell(row=row_num, column=3, value=invoice.customer.display_name if invoice.customer else "-")
                        
                        if employee_view:
                            ws.cell(row=row_num, column=4, value=invoice.sales_person.name if invoice.sales_person else "-")
                            ws.cell(row=row_num, column=5, value=invoice.resort.resort_name if invoice.resort else "-")
                            ws.cell(row=row_num, column=6, value=float(invoice.total))
                            ws.cell(row=row_num, column=7, value=float(invoice.resort_price))
                            ws.cell(row=row_num, column=8, value=float(invoice.profit))
                        else:
                            ws.cell(row=row_num, column=4, value=invoice.resort.resort_name if invoice.resort else "-")
                            ws.cell(row=row_num, column=5, value=float(invoice.total))
                            ws.cell(row=row_num, column=6, value=float(invoice.resort_price))
                            ws.cell(row=row_num, column=7, value=float(invoice.profit))
                    
                    # Auto-adjust column widths
                    for col in ws.columns:
                        max_length = 0
                        column = col[0].column_letter
                        for cell in col:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)
                        ws.column_dimensions[column].width = adjusted_width
                    
                    response = HttpResponse(
                        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    response["Content-Disposition"] = f'attachment; filename="profit_report_{fd.strftime("%d%m%Y")}_{td.strftime("%d%m%Y")}.xlsx"'
                    wb.save(response)
                    return response
                
            except ValueError:
                messages.error(request, "Invalid date format.")
    
    return render(request, "admin/report/profit_report.html", {
        "resorts": resorts,
        "invoices": invoices,
        "employees": employees,
        "employee_view": employee_view,
        "selected": selected,
    })

# DESTINATION VIEWS
def destination_list(request):
    category = request.GET.get('cat', 'Domestic')
    destinations = Destination.objects.filter(category=category).order_by('-created_at')
    domestic_count = Destination.objects.filter(category='Domestic').count()
    international_count = Destination.objects.filter(category='International').count()
    context = {
        'destinations': destinations,
        'selected_category': category,
        'domestic_count': domestic_count,
        'international_count': international_count,
    }
    return render(request, 'admin/destination/destination.html', context)

def add_destination(request):
    # Get category from URL parameter (from travel packages page)
    default_category = request.GET.get('category', 'Domestic')
    
    if request.method == "POST":
        category = request.POST.get('category')
        Destination.objects.create(
            name=request.POST.get('name'),
            country=request.POST.get('country'),
            category=category,
            description=request.POST.get('description'),
            is_popular=request.POST.get('is_popular') == 'on',
            image=request.FILES.get('image')
        )
        messages.success(request, "Destination added successfully!")
        
        # Redirect back to travel packages with the category
        url = reverse('admin_panel:travel_packages')
        return redirect(f'{url}?cat={category}')
    
    context = {'default_category': default_category}
    return render(request, 'admin/destination/add_destination.html', context)

def edit_destination(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    if request.method == "POST":
        destination.name = request.POST.get('name')
        destination.country = request.POST.get('country')
        destination.category = request.POST.get('category')
        destination.description = request.POST.get('description')
        destination.is_popular = request.POST.get('is_popular') == 'on'
        if request.FILES.get('image'):
            destination.image = request.FILES.get('image')
        destination.save()
        messages.success(request, "Destination updated successfully!")
        return redirect('admin_panel:destinations')
    return render(request, 'admin/destination/edit_destination.html', {'destination': destination})

def delete_destination(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    destination.delete()
    messages.success(request, "Destination deleted successfully!")
    return redirect('admin_panel:destinations')