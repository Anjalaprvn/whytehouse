from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from admin_panel.models import TravelPackage, Property, Inquiry, Lead

def index(request):
    packages = TravelPackage.objects.filter(active=True, category='International')[:6]
    return render(request, 'user/international.html', {'packages': packages})

def domestic(request):
    packages = TravelPackage.objects.filter(active=True, category='Domestic')[:6]
    return render(request, 'user/domestic.html', {'packages': packages})

def about(request):
    return render(request, 'user/about.html')

def blog(request):
    return render(request, 'user/blog.html')

def blog_detail(request, slug):
    return render(request, 'user/blog_detail.html')

def contact(request):
    if request.method == 'POST':
        name = (request.POST.get('name') or '').strip()
        email = (request.POST.get('email') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        package = (request.POST.get('package') or '').strip()
        message = (request.POST.get('message') or '').strip()

        if not (name and email and phone and message):
            messages.error(request, 'Please fill all required fields.')
            return redirect('contact')

        # ✅ 1) Find existing lead by phone (or create new)
        lead = Lead.objects.filter(mobile_number=phone).first()

        if lead:
            # Update basic info if needed (optional)
            if lead.full_name != name:
                lead.full_name = name
            # Keep latest message in remarks (optional)
            lead.remarks = (lead.remarks or "") + f"\n\n[{package or 'General Inquiry'}] {email}: {message}"
            lead.source = 'Website'
            lead.save()
        else:
            lead = Lead.objects.create(
                full_name=name,
                mobile_number=phone,
                place=None,
                source='Website',
                remarks=f"Email: {email}\nPackage: {package or 'General Inquiry'}\nMessage: {message}"
            )

        # ✅ 2) Create inquiry AND link it to lead
        Inquiry.objects.create(
            lead=lead,
            name=name,
            email=email,
            phone=phone,
            package=package or 'General Inquiry',
            message=message,
            status='New'
        )

        messages.success(request, 'Thank you! Your inquiry has been submitted successfully.')
        return redirect('contact')

    return render(request, 'user/contact.html')

def packages(request):
    country = request.GET.get('country', 'all')
    
    if country == 'all':
        all_packages = TravelPackage.objects.filter(active=True)
    else:
        all_packages = TravelPackage.objects.filter(active=True, country__iexact=country)
    
    return render(request, 'user/packages.html', {'packages': all_packages, 'selected_country': country})

def package_detail(request, slug):
    package = get_object_or_404(TravelPackage, id=slug, active=True)
    
    if request.method == 'POST':
        from admin_panel.models import Customer
        
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        guests = request.POST.get('guests', '1')
        start_date = request.POST.get('start_date', '').strip()
        
        if name and phone:
            # Split name into first and last
            name_parts = name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            Customer.objects.create(
                first_name=first_name,
                last_name=last_name,
                display_name=name,
                contact_number=phone,
                whatsapp_number=phone,
                same_as_whatsapp=True,
                customer_type='Individual',
                place=f'Booking: {package.name}'
            )
            
            Lead.objects.create(
                full_name=name,
                mobile_number=phone,
                source='Website',
                remarks=f'Package: {package.name} | Email: {email} | Guests: {guests} | Start Date: {start_date}'
            )
            
            messages.success(request, 'Booking request submitted! Our team will contact you soon.')
            return redirect('package_detail', slug=slug)
    
    return render(request, 'user/package_detail.html', {'package': package})

def hospitality(request):
    properties = Property.objects.all()
    return render(request, 'user/hospitality.html', {'properties': properties})