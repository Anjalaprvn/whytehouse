from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import random
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime
from .models import Lead, Property, Amenity, TravelPackage, Inquiry

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
def lead_management(request):
    leads = Lead.objects.all().order_by('-created_at')
    context = {'leads': leads}
    return render(request, 'admin/lead/lead.html', context)

def add_lead(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        place = request.POST.get('place')
        source = request.POST.get('source')   # ✅ changed
        remarks = request.POST.get('remarks')

        Lead.objects.create(
            full_name=full_name,
            mobile_number=mobile_number,
            place=place,
            source=source,   # ✅ changed
            remarks=remarks
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
#hospitality
def hospitality_management(request):
    properties = Property.objects.all().order_by('-created_at')
    context = {'properties': properties}
    return render(request, 'admin/hospitality/hospitality_management.html', context)


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

# Travel Packages
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
        itinerary = '\n'.join(request.POST.getlist('itinerary[]'))
        inclusions = '\n'.join(request.POST.getlist('inclusions[]'))
        exclusions = '\n'.join(request.POST.getlist('exclusions[]'))
        
        TravelPackage.objects.create(
            name=request.POST.get('name'),
            category=request.POST.get('category'),
            price=request.POST.get('price'),
            duration=request.POST.get('duration'),
            location=request.POST.get('location'),
            country=request.POST.get('country'),
            description=request.POST.get('description'),
            itinerary=itinerary,
            inclusions=inclusions,
            exclusions=exclusions,
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


def customer_inquiries(request):
    inquiries = Inquiry.objects.all().order_by('-created_at')

    context = {
        'inquiries': inquiries,
        'total_count': inquiries.count(),
        'new_count': inquiries.filter(status='New').count(),
        'contacted_count': inquiries.filter(status='Contacted').count(),
        'converted_count': inquiries.filter(status='Converted').count(),
        'junk_count': inquiries.filter(status='Junk').count(),
    }

    return render(request, 'admin/enquiry/customer_inquiries', context)