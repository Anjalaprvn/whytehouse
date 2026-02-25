from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from admin_panel.models import TravelPackage, Property, Inquiry

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
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        package = request.POST.get('package', '').strip()
        message = request.POST.get('message', '').strip()
        
        if name and email and phone and message:
            Inquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                package=package or 'General Inquiry',
                message=message
            )
            messages.success(request, 'Thank you! Your inquiry has been submitted successfully.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill all required fields.')
    
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
    return render(request, 'user/package_detail.html', {'package': package})

def hospitality(request):
    properties = Property.objects.all()
    return render(request, 'user/hospitality.html', {'properties': properties})