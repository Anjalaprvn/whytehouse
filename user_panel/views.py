from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from admin_panel.models import TravelPackage, Property, Inquiry, Lead, Blog, Destination


def enquire_now(request):
    if request.method == 'POST':
        try:
            full_name = request.POST.get('full_name', '').strip()
            mobile_number = request.POST.get('mobile_number', '').strip()
            email = request.POST.get('email', '').strip()
            place = request.POST.get('place', '').strip()
            message = request.POST.get('message', '').strip()
            enquiry_type = request.POST.get('enquiry_type', 'General')
            
            if not full_name or not mobile_number:
                return JsonResponse({'success': False, 'error': 'Name and mobile number are required'})
            
            # Create lead with enquiry type based on page
            Lead.objects.create(
                full_name=full_name,
                mobile_number=mobile_number,
                place=place,
                source='Enquire Now',
                enquiry_type=enquiry_type,
                remarks=f'Email: {email}\nMessage: {message}'
            )
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def index(request):
    packages = TravelPackage.objects.filter(active=True, category='International')[:6]
    
    # Get 4 featured packages for the gallery section
    featured_packages = list(TravelPackage.objects.filter(active=True, category='International')[:4])
    print(f"DEBUG: Featured packages count: {len(featured_packages)}")
    for pkg in featured_packages:
        print(f"  - {pkg.name} (ID: {pkg.id})")
    
    # Get featured package for each destination (Vietnam=2, Malaysia=14, Thailand=8, Maldives=12)
    vietnam_package = TravelPackage.objects.filter(active=True, destination_id=2).first()
    malaysia_package = TravelPackage.objects.filter(active=True, destination_id=14).first()
    thailand_package = TravelPackage.objects.filter(active=True, destination_id=8).first()
    maldives_package = TravelPackage.objects.filter(active=True, destination_id=12).first()
    
    # Get destinations
    vietnam_dest = Destination.objects.filter(id=2).first()
    malaysia_dest = Destination.objects.filter(id=14).first()
    thailand_dest = Destination.objects.filter(id=8).first()
    maldives_dest = Destination.objects.filter(id=12).first()
    
    context = {
        'packages': packages,
        'featured_packages': featured_packages,
        'vietnam_package': vietnam_package,
        'malaysia_package': malaysia_package,
        'thailand_package': thailand_package,
        'maldives_package': maldives_package,
        'vietnam_dest': vietnam_dest,
        'malaysia_dest': malaysia_dest,
        'thailand_dest': thailand_dest,
        'maldives_dest': maldives_dest,
    }
    
    return render(request, 'user/international.html', context)
def domestic(request):
    packages = TravelPackage.objects.filter(active=True, category='Domestic')[:6]
    
    # Get domestic destinations for the explorer section
    domestic_destinations = Destination.objects.filter(category='Domestic').order_by('name')[:4]
    
    # Get first 3 domestic destinations for gallery
    gallery_destinations = Destination.objects.filter(category='Domestic').order_by('name')[:3]
    
    context = {
        'packages': packages,
        'domestic_destinations': domestic_destinations,
        'gallery_destinations': gallery_destinations,
    }
    
    return render(request, 'user/domestic.html', context)


def about(request):
    return render(request, 'user/about.html')




from django.shortcuts import render, get_object_or_404
from admin_panel.models import Blog

def blog_list(request):
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    
    blogs = Blog.objects.filter(status="published").order_by("-publish_date")

    if q:
        blogs = blogs.filter(title__icontains=q)
    
    if category:
        blogs = blogs.filter(category=category)

    for b in blogs:
        raw = getattr(b, "tags", "") or getattr(b, "hashtags", "") or getattr(b, "hashtag", "") or ""
        b.tag_list = [t.strip() for t in str(raw).split(",") if t.strip()]
    
    # Get category counts
    from django.db.models import Count
    all_count = Blog.objects.filter(status="published").count()
    category_counts = {}
    for cat_code, cat_name in Blog.CATEGORY_CHOICES:
        category_counts[cat_code] = Blog.objects.filter(status="published", category=cat_code).count()

    return render(request, "user/blog.html", {
        "blogs": blogs, 
        "q": q,
        "selected_category": category,
        "all_count": all_count,
        "category_counts": category_counts,
        "categories": Blog.CATEGORY_CHOICES
    })


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status="published")
    raw = getattr(blog, "tags", "") or getattr(blog, "hashtags", "") or getattr(blog, "hashtag", "") or ""
    tags = [t.strip() for t in str(raw).split(",") if t.strip()]

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

    return render(request, "user/blog_detail.html", {"blog": blog, "tags": tags, "processed_content": content})
def contact(request):
    if request.method == 'POST':
        import re
        
        name = (request.POST.get('name') or '').strip()
        email = (request.POST.get('email') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        package = (request.POST.get('package') or '').strip()
        message = (request.POST.get('message') or '').strip()
        source_page = (request.POST.get('source_page') or 'General').strip()

        # Validation
        errors = []
        
        # Name validation
        if not name or len(name) < 2:
            errors.append('Name is required and must be at least 2 characters.')
        
        # Email validation
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not email or not re.match(email_pattern, email):
            errors.append('Please enter a valid email address.')
        
        # Phone validation (international format: 10-15 digits with optional +, -, spaces, parentheses)
        phone_pattern = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$'
        phone_digits = re.sub(r'\D', '', phone)  # Extract only digits
        
        if not phone:
            errors.append('Phone number is required.')
        elif len(phone_digits) < 10:
            errors.append('Phone number must be at least 10 digits.')
        elif not re.match(phone_pattern, phone):
            errors.append('Please enter a valid phone number.')
        
        # Message validation
        if not message or len(message) < 10:
            errors.append('Message is required and must be at least 10 characters.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('user_panel:contact')

        # ✅ 1) Find existing lead by phone (or create new)
        lead = Lead.objects.filter(mobile_number=phone).first()

        if lead:
            # Update basic info if needed (optional)
            if lead.full_name != name:
                lead.full_name = name
            # Keep latest message in remarks (optional)
            lead.remarks = (lead.remarks or "") + f"\n\n[{package or 'General Inquiry'}] {email}: {message}"
            lead.source = 'Website'
            lead.enquiry_type = source_page  # Set enquiry type based on source page
            lead.save()
        else:
            lead = Lead.objects.create(
                full_name=name,
                mobile_number=phone,
                place=None,
                source='Website',
                enquiry_type=source_page,  # Set enquiry type based on source page
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
        return redirect('user_panel:contact')

    return render(request, 'user/contact.html')

def packages(request):
    country = request.GET.get('country', 'all')
    
    if country == 'all':
        all_packages = TravelPackage.objects.filter(active=True)
    else:
        all_packages = TravelPackage.objects.filter(active=True, country__iexact=country)
    
    return render(request, 'user/packages.html', {'packages': all_packages, 'selected_country': country})

def domestic_packages(request):
    destination_id = request.GET.get('dest')
    
    # Get all domestic destinations
    destinations = Destination.objects.filter(category='Domestic').order_by('name')
    
    # Filter packages
    packages = TravelPackage.objects.filter(active=True, category='Domestic')
    if destination_id:
        packages = packages.filter(destination_id=destination_id)
    packages = packages.order_by('-created_at')
    
    # Get selected destination object
    selected_destination = None
    if destination_id:
        try:
            selected_destination = Destination.objects.get(id=destination_id)
        except Destination.DoesNotExist:
            pass
    
    context = {
        'packages': packages,
        'destinations': destinations,
        'selected_destination': int(destination_id) if destination_id else None,
        'selected_destination_obj': selected_destination,
        'category': 'Domestic'
    }
    return render(request, 'user/packages.html', context)

def international_packages(request):
    destination_id = request.GET.get('dest')
    
    # Get all international destinations
    destinations = Destination.objects.filter(category='International').order_by('name')
    
    # Filter packages
    packages = TravelPackage.objects.filter(active=True, category='International')
    if destination_id:
        packages = packages.filter(destination_id=destination_id)
    packages = packages.order_by('-created_at')
    
    # Get selected destination object
    selected_destination = None
    if destination_id:
        try:
            selected_destination = Destination.objects.get(id=destination_id)
        except Destination.DoesNotExist:
            pass
    
    context = {
        'packages': packages,
        'destinations': destinations,
        'selected_destination': int(destination_id) if destination_id else None,
        'selected_destination_obj': selected_destination,
        'category': 'International'
    }
    return render(request, 'user/packages.html', context)

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