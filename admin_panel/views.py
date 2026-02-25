from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
import random
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime
from .models import Account, Customer, Resort, Meal, Voucher, Invoice, Lead, Property, Amenity, TravelPackage, Inquiry
from .models import Employee

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
            return redirect('verify_otp')
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
    return render(request, 'admin/index.html')

# LEADS
def lead_management(request):
    leads = Lead.objects.all().order_by('-created_at')
    return render(request, 'admin/lead/lead.html', {'leads': leads})

def add_lead(request):
    if request.method == "POST":
        Lead.objects.create(
            full_name=request.POST.get('full_name'),
            mobile_number=request.POST.get('mobile_number'),
            place=request.POST.get('place'),
            source=request.POST.get('source'),
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
        lead.remarks = request.POST.get('remarks')
        lead.save()
        messages.success(request, "Lead updated successfully!")
        return redirect('admin_panel:leads')
    return render(request, 'admin/lead/lead_edit.html', {'lead': lead})

def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    lead.delete()
    messages.success(request, 'Lead deleted successfully!')
    return redirect('admin_panel:leads')

# HOSPITALITY
def hospitality_management(request):
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'admin/hospitality/hospitality_management.html', {'properties': properties})

def add_property(request):
    amenities = Amenity.objects.all()
    if request.method == "POST":
        selected_amenities = request.POST.getlist('amenities')
        new_amenity = request.POST.get('new_amenity', '').strip()
        if new_amenity:
            amenity_obj, created = Amenity.objects.get_or_create(name=new_amenity)
            selected_amenities.append(str(amenity_obj.id))
        property = Property.objects.create(
            name=request.POST.get("name"),
            property_type=request.POST.get("property_type"),
            location=request.POST.get("location"),
            website=request.POST.get("website"),
            address=request.POST.get("address"),
            summary=request.POST.get("summary"),
            owner_name=request.POST.get("owner_name"),
            owner_contact=request.POST.get("owner_contact"),
            image=request.FILES.get("image")
        )
        property.amenities.set(selected_amenities)
        messages.success(request, "Property added successfully!")
        return redirect("admin_panel:admin_hospitality")
    return render(request, "admin/hospitality/hospitality_add.html", {'amenities': amenities})

def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    amenities = Amenity.objects.all()
    if request.method == "POST":
        property.name = request.POST.get("name")
        property.property_type = request.POST.get("property_type")
        property.location = request.POST.get("location")
        property.website = request.POST.get("website")
        property.address = request.POST.get("address")
        property.summary = request.POST.get("summary")
        property.owner_name = request.POST.get("owner_name")
        property.owner_contact = request.POST.get("owner_contact")
        selected_amenities = request.POST.getlist('amenities')
        new_amenity = request.POST.get('new_amenity', '').strip()
        if new_amenity:
            amenity_obj, created = Amenity.objects.get_or_create(name=new_amenity)
            selected_amenities.append(str(amenity_obj.id))
        if request.FILES.get("image"):
            property.image = request.FILES.get("image")
        property.save()
        property.amenities.set(selected_amenities)
        messages.success(request, "Property updated successfully!")
        return redirect("admin_panel:admin_hospitality")
    return render(request, "admin/hospitality/hospitality_edit.html", {"property": property, "amenities": amenities})

def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    property.delete()
    return redirect('admin_panel:admin_hospitality')

# TRAVEL PACKAGES
def travel_packages(request):
    category = request.GET.get('cat', 'Domestic')
    packages = TravelPackage.objects.filter(category=category).order_by('-created_at')
    domestic_count = TravelPackage.objects.filter(category='Domestic').count()
    international_count = TravelPackage.objects.filter(category='International').count()
    context = {
        'packages': packages,
        'selected_category': category,
        'domestic_count': domestic_count,
        'international_count': international_count,
    }
    return render(request, 'admin/packages/travel_packages.html', context)

def travel_package_add(request):
    if request.method == "POST":
        TravelPackage.objects.create(
            name=request.POST.get('name'),
            category=request.POST.get('category'),
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
        return redirect('admin_panel:travel_packages')
    return render(request, 'admin/packages/travel_package_add.html')

def travel_package_edit(request, package_id):
    package = get_object_or_404(TravelPackage, id=package_id)
    if request.method == "POST":
        package.name = request.POST.get('name')
        package.category = request.POST.get('category')
        package.price = request.POST.get('price')
        package.duration = request.POST.get('duration')
        package.location = request.POST.get('location')
        package.country = request.POST.get('country')
        package.description = request.POST.get('description')
        package.itinerary = '\n'.join(request.POST.getlist('itinerary[]'))
        package.inclusions = '\n'.join(request.POST.getlist('inclusions[]'))
        package.exclusions = '\n'.join(request.POST.getlist('exclusions[]'))
        package.meta_title = request.POST.get('meta_title')
        package.meta_description = request.POST.get('meta_description')
        package.active = request.POST.get('active') == 'on'
        if request.FILES.get('image'):
            package.image = request.FILES.get('image')
        package.save()
        messages.success(request, "Package updated successfully!")
        return redirect('admin_panel:travel_packages')
    return render(request, 'admin/packages/travel_package_add.html', {'package': package})

def travel_package_delete(request, package_id):
    package = get_object_or_404(TravelPackage, id=package_id)
    package.delete()
    messages.success(request, "Package deleted successfully!")
    return redirect('admin_panel:travel_packages')

# CUSTOMER INQUIRIES
def customer_inquiries(request):
    status_filter = request.GET.get('status')
    
    if status_filter:
        inquiries = Inquiry.objects.filter(status=status_filter).order_by('-created_at')
    else:
        inquiries = Inquiry.objects.all().order_by('-created_at')
    
    context = {
        'inquiries': inquiries,
        'total_count': Inquiry.objects.count(),
        'new_count': Inquiry.objects.filter(status='New').count(),
        'contacted_count': Inquiry.objects.filter(status='Contacted').count(),
        'converted_count': Inquiry.objects.filter(status='Converted').count(),
        'junk_count': Inquiry.objects.filter(status='Junk').count(),
    }
    return render(request, 'admin/enquiry/customer_inquiries', context)

def view_inquiry(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    return render(request, 'admin/enquiry/customer_inquiry_view.html', {'inquiry': inquiry})

def update_inquiry_status(request, inquiry_id):
    if request.method == 'POST':
        inquiry = get_object_or_404(Inquiry, id=inquiry_id)
        new_status = request.POST.get('status')
        if new_status in ['New', 'Contacted', 'Converted', 'Junk']:
            inquiry.status = new_status
            inquiry.save()
            messages.success(request, f'Inquiry status updated to {new_status}')
        return redirect('admin_panel:customer_inquiries')
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
            resort.location = request.POST.get("location", "").strip()
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
    invoices = Invoice.objects.all()
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
        invoice_number = invoice.invoice_number
        invoice.delete()
        messages.success(request, f"Invoice '{invoice_number}' deleted successfully!")
    except Invoice.DoesNotExist:
        messages.error(request, "Invoice not found.")
    except Exception as e:
        messages.error(request, f"Error deleting invoice: {str(e)}")
    return redirect("sales:invoice_list")

# REPORT GENERATION VIEWS-----------------------------------------------------------
def invoice_report(request):
    from django.http import HttpResponse
    import openpyxl
    from openpyxl.styles import Font, Alignment
    
    employees = Employee.objects.filter(status='Active')
    resorts = Resort.objects.all()
    invoices = []
    employee_view = False
    
    if request.method == 'POST':
        action = request.POST.get('action')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        resort_id = request.POST.get('resort')
        employee_view = request.POST.get('employee_view') == 'on'
        employee_id = request.POST.get('employee')
        
        invoices = Invoice.objects.filter(invoice_date__range=[from_date, to_date])
        if resort_id:
            invoices = invoices.filter(resort_id=resort_id)
        if employee_view and employee_id:
            invoices = invoices.filter(sales_person_id=employee_id)
        
        if action == 'excel':
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = 'Invoice Report'
            
            headers = ['Invoice No', 'Date', 'Customer', 'Resort', 'Total', 'Received', 'Pending', 'Profit']
            if employee_view:
                headers.insert(3, 'Sales Person')
            
            for col, header in enumerate(headers, 1):
                cell = ws.cell(1, col, header)
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center')
            
            for row, inv in enumerate(invoices, 2):
                ws.cell(row, 1, inv.invoice_no)
                ws.cell(row, 2, str(inv.invoice_date))
                ws.cell(row, 3, inv.customer.display_name if inv.customer else '')
                col = 4
                if employee_view:
                    ws.cell(row, col, inv.sales_person.name if inv.sales_person else '')
                    col += 1
                ws.cell(row, col, inv.resort.resort_name if inv.resort else '')
                ws.cell(row, col+1, float(inv.total))
                ws.cell(row, col+2, float(inv.received))
                ws.cell(row, col+3, float(inv.pending))
                ws.cell(row, col+4, float(inv.profit))
            
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=invoice_report.xlsx'
            wb.save(response)
            return response
    
    return render(request, 'admin/report/invoice_report.html', {'employees': employees, 'resorts': resorts, 'invoices': invoices, 'employee_view': employee_view})

def voucher_report(request):
    return render(request, "admin/report/voucher_report.html")

def leads_report(request):
    return render(request, "admin/report/leads_report.html")

def profit_report(request):
    return render(request, "admin/report/profit_report.html")

def customer_report(request):
    return render(request, "admin/report/customer_report.html")

def blog_list(request):
    return render(request, "admin/blog/blog.html")
