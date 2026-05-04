from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from admin_panel.models import TravelPackage, Property, Inquiry, Lead, Blog, Destination
from admin_panel.models import Feedback, BlogCategory, PackageBooking
from django.shortcuts import render, get_object_or_404
from admin_panel.models import Blog


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
    
    # Get selected destination from URL parameter
    selected_dest_id = request.GET.get('dest')
    
    # Get international destinations for side tabs (limited to 3, only popular)
    side_tab_destinations = Destination.objects.filter(
        category='International',
        is_popular=True,
        is_active=True,
        packages__active=True
    ).distinct().order_by('name')[:3]
    
    # Get international destinations for filter tabs (limited to 4, only popular)
    filter_destinations = Destination.objects.filter(
        category='International',
        is_popular=True,
        is_active=True,
        packages__active=True
    ).distinct().order_by('name')[:4]
    
    # Build destination data with ALL packages for each destination
    destination_data = []
    for dest in filter_destinations:
        packages_list = TravelPackage.objects.filter(active=True, destination=dest)
        destination_data.append({
            'destination': dest,
            'packages': packages_list
        })
    
    # Get all package IDs already shown in destination sections
    shown_package_ids = []
    for data in destination_data:
        shown_package_ids.extend([pkg.id for pkg in data['packages']])
    
    # Get 4 featured packages for the gallery section, excluding already shown ones
    featured_packages = list(TravelPackage.objects.filter(
        active=True, 
        category='International'
    ).exclude(id__in=shown_package_ids)[:4])
    
    # If we don't have 4 unique packages, fill with any available packages
    if len(featured_packages) < 4:
        additional_packages = list(TravelPackage.objects.filter(
            active=True, 
            category='International'
        )[:4])
        featured_packages = additional_packages
    
    # fetch testimonials that have been marked featured
    featured_feedbacks = Feedback.objects.filter(featured=True).order_by('-created_at')[:6]
    
    context = {
        'packages': packages,
        'featured_packages': featured_packages,
        'side_tab_destinations': side_tab_destinations,
        'filter_destinations': filter_destinations,
        'destination_data': destination_data,
        'featured_feedbacks': featured_feedbacks,
        'selected_dest_id': int(selected_dest_id) if selected_dest_id else None,
    }
    
    return render(request, 'user/international.html', context)
def domestic(request):
    packages = TravelPackage.objects.filter(active=True, category='Domestic')[:6]
    
    # Get domestic destinations for the explorer section
    domestic_destinations = Destination.objects.filter(category='Domestic', is_active=True).order_by('name')[:4]
    
    # Get featured package for each destination (Kozhikode, Munnar, Wayanad, Ooty)
    kozhikode_package = TravelPackage.objects.filter(active=True, category='Domestic', destination__name__icontains='Kozhikode').first()
    munnar_package = TravelPackage.objects.filter(active=True, category='Domestic', destination__name__icontains='Munnar').first()
    wayanad_package = TravelPackage.objects.filter(active=True, category='Domestic', destination__name__icontains='Wayanad').first()
    ooty_package = TravelPackage.objects.filter(active=True, category='Domestic', destination__name__icontains='Ooty').first()
    
    # Get ALL domestic destinations for gallery (show 3 at a time with navigation)
    gallery_destinations = Destination.objects.filter(category='Domestic', is_active=True).order_by('name')
    
    # Get all properties for hospitality section (show 3 at a time)
    properties = Property.objects.filter(is_active=True)
    
    context = {
        'packages': packages,
        'domestic_destinations': domestic_destinations,
        'gallery_destinations': gallery_destinations,
        'properties': properties,
        'kozhikode_package': kozhikode_package,
        'munnar_package': munnar_package,
        'wayanad_package': wayanad_package,
        'ooty_package': ooty_package,
    }
    
    return render(request, 'user/domestic.html', context)


def about(request):
    return render(request, 'user/about.html')






def blog_list(request):
    from admin_panel.models import BlogCategory
    
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    
    blogs = Blog.objects.filter(status="published").order_by("-publish_date")

    if q:
        blogs = blogs.filter(title__icontains=q)
    
    if category:
        blogs = blogs.filter(category__slug=category)

    for b in blogs:
        raw = getattr(b, "tags", "") or getattr(b, "hashtags", "") or getattr(b, "hashtag", "") or ""
        b.tag_list = [t.strip() for t in str(raw).split(",") if t.strip()]
    
    all_count = Blog.objects.filter(status="published").count()
    categories = [(cat.slug, cat.name) for cat in BlogCategory.objects.filter(is_active=True).order_by('order', 'name')]
    category_counts = {cat[0]: Blog.objects.filter(status="published", category__slug=cat[0]).count() for cat in categories}

    return render(request, "user/blog.html", {
        "blogs": blogs, 
        "q": q,
        "selected_category": category,
        "all_count": all_count,
        "category_counts": category_counts,
        "categories": categories
    })


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status="published")
    raw = getattr(blog, "tags", "") or getattr(blog, "hashtags", "") or getattr(blog, "hashtag", "") or ""
    tags = [t.strip() for t in str(raw).split(",") if t.strip()]

    # Replace {{image1}}, {{image2}}, etc. with actual image HTML
    content = blog.content
    content_images = blog.images.all().order_by('order')
    
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
                            <img src="{img.image.url}" alt="Image {image_num}" data-gallery-order="{idx}">
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
                            <img src="{img.image.url}" alt="Image {image_num}" data-gallery-order="{idx}">
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
                        <img src="{img.image.url}" alt="Image {image_num}" data-gallery-order="{idx}">
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
                        <img src="{img.image.url}" alt="Image {image_num}" data-gallery-order="{idx}">
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
        country_code = '+91'
        package = (request.POST.get('package') or '').strip()
        place = (request.POST.get('place') or '').strip()
        message = (request.POST.get('message') or '').strip()
        subject = (request.POST.get('subject') or 'General').strip()
        
        full_phone = phone
        
        # Map contact form dropdown options to Lead model choices
        subject_mapping = {
            'Package related': 'General',
            'Holiday Package': 'General', 
            'Property Management': 'Hospitality',
            'General Enquiry': 'General',
            # Add any other mappings as needed
        }
        
        # Map the subject to the correct enquiry type
        enquiry_type = subject_mapping.get(subject, 'General')
        print(f"DEBUG: Contact form subject='{subject}' mapped to enquiry_type='{enquiry_type}'")

        # Basic validation for essential fields only
        if not name or not phone:
            messages.error(request, 'Name and mobile number are required.')
            return render(request, 'user/contact.html', {
                'form_data': {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'package': package,
                    'message': message,
                    'subject': subject
                }
            })

        # Create Lead record
        try:
            lead = Lead.objects.create(
                full_name=name,
                mobile_number=full_phone,
                email=email,
                place=place or None,
                source='Website',
                enquiry_type=enquiry_type,
                message=message,
                package=package,
                package_name=package if subject in ('Package related', 'Holiday Package') else None,
                remarks=f'Subject: {subject}\n{message}'
            )
            print(f"DEBUG: Created new lead {lead.id} with enquiry_type={enquiry_type}")
        except Exception as e:
            print(f"DEBUG: Failed to create lead: {str(e)}")
            messages.error(request, 'There was an error processing your request. Please try again.')
            return render(request, 'user/contact.html', {
                'form_data': {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'package': package,
                    'message': message,
                    'subject': subject
                }
            })

        # Create inquiry with separate fields
        try:
            inquiry = Inquiry.objects.create(
                lead=lead,
                name=name,
                email=email,
                phone=full_phone,
                package=package or 'General Inquiry',
                message=message,
                status='New'
            )
            print(f"DEBUG: Created inquiry with ID {inquiry.id} for lead {lead.id}")
        except Exception as e:
            print(f"DEBUG: Failed to create inquiry: {str(e)}")
            # Don't fail silently - this is important for debugging
            import traceback
            traceback.print_exc()
        
        # If successful, add success message and redirect
        return render(request, 'user/contact.html', {'success': True})

    return render(request, 'user/contact.html', {'default_subject': request.GET.get('subject', '')})

def packages(request):
    country = request.GET.get('country', 'all')
    search_query = request.GET.get('search', '').strip()
    
    # Filter packages
    if country == 'all':
        all_packages = TravelPackage.objects.filter(active=True)
    else:
        all_packages = TravelPackage.objects.filter(active=True, country__iexact=country)
    
    # Apply search filter
    if search_query:
        all_packages = all_packages.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(destination__name__icontains=search_query)
        )
    
    return render(request, 'user/packages.html', {
        'packages': all_packages, 
        'selected_country': country,
        'search_query': search_query
    })

def domestic_packages(request):
    destination_id = request.GET.get('dest')
    search_query = request.GET.get('search', '').strip()
    
    # Get all domestic destinations
    destinations = Destination.objects.filter(category='Domestic', is_active=True).order_by('name')
    
    # Filter packages
    packages = TravelPackage.objects.filter(active=True, category='Domestic')
    
    # Apply search filter
    if search_query:
        packages = packages.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(destination__name__icontains=search_query)
        )
    
    # Apply destination filter
    if destination_id:
        try:
            destination_id = int(destination_id)
            selected_dest = Destination.objects.get(id=destination_id)
            # Show packages assigned to this destination OR packages where location matches destination name
            packages = packages.filter(
                Q(destination_id=destination_id) |
                Q(location__icontains=selected_dest.name)
            )
        except (ValueError, TypeError, Destination.DoesNotExist):
            pass
    
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
        'category': 'Domestic',
        'search_query': search_query
    }
    return render(request, 'user/packages.html', context)

def international_packages(request):
    destination_id = request.GET.get('dest')
    search_query = request.GET.get('search', '').strip()
    
    # Get all international destinations
    destinations = Destination.objects.filter(category='International', is_active=True).order_by('name')
    
    # Filter packages
    packages = TravelPackage.objects.filter(active=True, category='International')
    
    # Apply search filter
    if search_query:
        packages = packages.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(destination__name__icontains=search_query)
        )
    
    # Apply destination filter
    if destination_id:
        try:
            destination_id = int(destination_id)
            selected_dest = Destination.objects.get(id=destination_id)
            # Show packages assigned to this destination OR packages where location matches destination name
            packages = packages.filter(
                Q(destination_id=destination_id) |
                Q(location__icontains=selected_dest.name)
            )
        except (ValueError, TypeError, Destination.DoesNotExist):
            pass
    
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
        'category': 'International',
        'search_query': search_query
    }
    return render(request, 'user/packages.html', context)

def package_detail(request, slug):
    from datetime import datetime
    package = get_object_or_404(TravelPackage, id=slug, active=True)
    
    if request.method == 'POST':
        import re
        
        form_type = request.POST.get('form_type', 'booking').strip()
        
        # ============ BOOKING FORM ============
        if form_type == 'booking':
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            adults = request.POST.get('adults', '1').strip()
            children = request.POST.get('children', '0').strip()
            start_date = request.POST.get('start_date', '').strip()
            
            # Collect child ages
            child_ages = []
            children_count = int(children) if children.isdigit() else 0
            for i in range(1, children_count + 1):
                age = request.POST.get(f'child_age_{i}', '').strip()
                if age:
                    child_ages.append(age)
            
            # Validation
            errors = []
            
            # Name validation
            if not name or len(name) < 2:
                errors.append('Name is required and must be at least 2 characters.')
            
            # Email validation
            email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not email or not re.match(email_pattern, email):
                errors.append('Please enter a valid email address.')
            
            # Phone validation (exactly 10 digits)
            phone_digits = re.sub(r'\D', '', phone)
            
            if not phone:
                errors.append('Phone number is required.')
            elif len(phone_digits) != 10:
                errors.append('Phone number must be exactly 10 digits.')
            elif not phone_digits.isdigit():
                errors.append('Phone number must contain only digits.')
            
            # Start date validation
            if not start_date:
                errors.append('Start date is required.')
            else:
                from django.utils import timezone
                try:
                    date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                    today = timezone.now().date()
                    if date_obj.date() < today:
                        errors.append('Start date cannot be in the past.')
                except ValueError:
                    errors.append('Please enter a valid date.')
            
            if errors:
                for error in errors:
                    messages.error(request, error)
                return render(request, 'user/package_detail.html', {
                    'package': package,
                    'today': timezone.now(),
                    'form_data': {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'adults': adults,
                        'children': children,
                        'start_date': start_date
                    }
                })
            
            adults_int = int(adults) if str(adults).isdigit() else 1
            children_int = int(children) if str(children).isdigit() else 0
            remarks = f'Package: {package.name} | Adults: {adults_int} | Children: {children_int} | Start Date: {start_date}'
            if child_ages:
                remarks += f' | Child Ages: {", ".join(child_ages)}'
            Lead.objects.create(
                full_name=name,
                mobile_number=phone,
                email=email,
                source='Website',
                enquiry_type=package.category,
                package_name=package.name,
                remarks=remarks
            )
            
            messages.success(request, 'Booking request submitted! Our team will contact you soon.')
            return redirect('user_panel:package_detail', slug=slug)
        
        # ============ MESSAGE FORM ============
        elif form_type == 'message':
            message_name = request.POST.get('message_name', '').strip()
            message_phone = request.POST.get('message_phone', '').strip()
            message_email = request.POST.get('message_email', '').strip()
            message_text = request.POST.get('message_text', '').strip()
            
            # Validation
            errors = []
            
            # Name validation
            if not message_name or len(message_name) < 2:
                errors.append('Name is required and must be at least 2 characters.')
            
            # Email validation
            email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not message_email or not re.match(email_pattern, message_email):
                errors.append('Please enter a valid email address.')
            
            # Phone validation (exactly 10 digits)
            phone_digits = re.sub(r'\D', '', message_phone)
            
            if not message_phone:
                errors.append('Phone number is required.')
            elif len(phone_digits) != 10:
                errors.append('Phone number must be exactly 10 digits.')
            elif not phone_digits.isdigit():
                errors.append('Phone number must contain only digits.')
            
            # Message validation
            if not message_text or len(message_text) < 10:
                errors.append('Message is required and must be at least 10 characters.')
            
            if errors:
                from django.utils import timezone
                for error in errors:
                    messages.error(request, error)
                return render(request, 'user/package_detail.html', {
                    'package': package,
                    'today': timezone.now()
                })
            
            # If validation passes, create customer and lead
            name_parts = message_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            lead = Lead.objects.create(
                full_name=message_name,
                mobile_number=message_phone,
                email=message_email,
                source='Website',
                enquiry_type=package.category,
                package_name=package.name,
                message=message_text,
                remarks=f'Package Inquiry: {package.name}\n\nMessage: {message_text}'
            )

            try:
                Inquiry.objects.create(
                    lead=lead,
                    name=message_name,
                    email=message_email,
                    phone=message_phone,
                    package=package.name,
                    message=message_text,
                    status='New'
                )
            except Exception:
                pass
            
            messages.success(request, 'Your message has been sent successfully! Our team will contact you soon.')
            return redirect('user_panel:package_detail', slug=slug)
    
    import json
    from decimal import Decimal
    from django.utils import timezone

    # No resort or meal options for TravelPackage
    room_options = []
    meal_options = []

    # Transport options - removed as model doesn't have this field
    transport_options = []

    itinerary_days = [d.strip() for d in package.itinerary.split('|||') if d.strip()] if package.itinerary else []

    return render(request, 'user/package_detail.html', {
        'package': package,
        'today': timezone.now(),
        'itinerary_days': itinerary_days,
        'room_options_json': json.dumps(room_options),
        'meal_options_json': json.dumps(meal_options),
        'transport_options_json': json.dumps(transport_options),
        'has_pricing_options': bool(room_options or meal_options or transport_options),
    })

def hospitality_enquiry(request):
    if request.method == 'POST':
        import re
        
        name = (request.POST.get('name') or '').strip()
        email = (request.POST.get('email') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        property_type = (request.POST.get('property_type') or '').strip()
        checkin_date = (request.POST.get('checkin_date') or '').strip()
        checkout_date = (request.POST.get('checkout_date') or '').strip()
        message = (request.POST.get('message') or '').strip()

        # Validation
        errors = []
        
        # Name validation
        if not name or len(name) < 2:
            errors.append('Name is required and must be at least 2 characters.')
        
        # Email validation
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not email or not re.match(email_pattern, email):
            errors.append('Please enter a valid email address.')
        
        # Phone validation
        phone_digits = re.sub(r'\D', '', phone)
        
        if not phone:
            errors.append('Phone number is required.')
        elif len(phone_digits) < 10:
            errors.append('Phone number must be at least 10 digits.')
        
        # Message validation
        if not message or len(message) < 10:
            errors.append('Message is required and must be at least 10 characters.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('user_panel:hospitality_enquiry')

        # Find existing lead by phone (or create new)
        lead = Lead.objects.filter(mobile_number=phone).first()

        if lead:
            # Update basic info if needed
            if lead.full_name != name:
                lead.full_name = name
            lead.source = 'Website'
            lead.enquiry_type = 'Hospitality'
            lead.email = email
            lead.save()
        else:
            lead = Lead.objects.create(
                full_name=name,
                mobile_number=phone,
                email=email,
                place=None,
                source='Website',
                enquiry_type='Hospitality',
                remarks=''
            )

        # Create inquiry with separate fields
        try:
            inquiry = Inquiry.objects.create(
                lead=lead,
                name=name,
                email=email,
                phone=phone,
                package=property_type or 'Hospitality Enquiry',
                message=message,
                status='New'
            )
        except Exception as e:
            pass
        
        return redirect('user_panel:hospitality_enquiry')

    return render(request, 'user/hospitality_enquiry.html')

def hospitality(request):
    """
    Display all hospitality properties
    """
    properties = Property.objects.filter(is_active=True)
    
    # Get featured testimonials for the testimonial section
    testimonials = Feedback.objects.filter(featured=True).order_by('-created_at')[:6]
    
    return render(request, 'user/hospitality.html', {
        'properties': properties,
        'testimonials': testimonials
    })

def hospitality_detail(request, property_id):
    """
    Display detailed information about a specific hospitality property
    """
    property = get_object_or_404(Property, id=property_id)
    # Get related properties (same type or location)
    related_properties = Property.objects.filter(
        Q(property_type=property.property_type) | Q(location=property.location)
    ).exclude(id=property.id)[:3]
    
    return render(request, 'user/hospitality_detail.html', {
        'property': property,
        'related_properties': related_properties
    })

def property_enquiry(request, property_id):
    """
    Display property enquiry form and handle form submission
    """
    property = get_object_or_404(Property, id=property_id)
    
    if request.method == 'POST':
        import re
        from admin_panel.models import Customer
        
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        
        errors = []
        
        if not name or len(name) < 2:
            errors.append('Name is required and must be at least 2 characters.')
        
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not email or not re.match(email_pattern, email):
            errors.append('Please enter a valid email address.')
        
        phone_digits = re.sub(r'\D', '', phone)
        if not phone or len(phone_digits) < 10:
            errors.append('Phone number must be at least 10 digits.')
        
        if not message or len(message) < 10:
            errors.append('Message is required and must be at least 10 characters.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'user/property_enquiry.html', {'property': property})
        
        lead = Lead.objects.filter(mobile_number=phone).first()
        
        if lead:
            if lead.full_name != name:
                lead.full_name = name
            lead.source = 'Website'
            lead.enquiry_type = 'Hospitality'
            lead.email = email
            lead.property_name = property.name
            lead.message = message
            lead.save()
        else:
            lead = Lead.objects.create(
                full_name=name,
                mobile_number=phone,
                email=email,
                place=property.location,
                source='Website',
                enquiry_type='Hospitality',
                property_name=property.name,
                message=message,
                remarks=f'Property: {property.name}'
            )
        
        try:
            inquiry = Inquiry.objects.create(
                lead=lead,
                name=name,
                email=email,
                phone=phone,
                package=f'Property: {property.name}',
                message=message,
                status='New'
            )
        except Exception:
            pass
        
        messages.success(request, 'Thank you! Your inquiry has been submitted. Our team will contact you soon.')
        return render(request, 'user/property_enquiry.html', {'property': property, 'success': True})
    
    return render(request, 'user/property_enquiry.html', {'property': property})

def feedback_form_submit(request):
    """
    Handle user feedback form submission from user feedback template
    """
    if request.method == "POST":
        try:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            mobile_number = request.POST.get('mobile_number', '').strip()
            rating = request.POST.get('rating', '')
            feedback_text = request.POST.get('feedback', '').strip()
            
            if not all([name, email, mobile_number, rating, feedback_text]):
                return JsonResponse({'success': False, 'error': 'All fields are required'})
            
            Feedback.objects.create(
                name=name,
                email=email,
                mobile_number=mobile_number,
                rating=int(rating),
                feedback=feedback_text
            )
            
            # after submission send admin to feedback management page for immediate review
            return JsonResponse({'success': True, 'message': 'Thank you! Your feedback has been submitted successfully.', 'redirect': '/admin/feedback/'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def feedback_page(request):
    return render(request, 'user/feedback.html')


def terms_of_service(request):
    return render(request, 'user/terms_of_service.html')


def license(request):
    return render(request, 'user/license.html')


def faq(request):
    return render(request, 'user/faq.html')


def feedback_form(request):
    """Render a simple feedback form (no sidebar). On POST, save and show
    success message on the same page.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        feedback_type = request.POST.get('feedback_type', '').strip()
        rating = request.POST.get('rating', '')
        feedback_text = request.POST.get('feedback', '').strip()
        images = request.FILES.getlist('feedback_images')

        if not all([name, email, feedback_type, rating, feedback_text]):
            return render(request, 'user/feedback_form.html', {
                'error': 'Please fill required fields.',
                'feedback_type_choices': Feedback.FEEDBACK_TYPE_CHOICES
            })

        feedback = Feedback.objects.create(
            name=name,
            email=email,
            mobile_number=mobile_number,
            feedback_type=feedback_type,
            rating=int(rating),
            feedback=feedback_text
        )
        
        # Save multiple images
        from admin_panel.models import FeedbackImage
        for image in images:
            FeedbackImage.objects.create(feedback=feedback, image=image)
        
        # show success message on the same page
        return render(request, 'user/feedback_form.html', {'success': True})

    return render(request, 'user/feedback_form.html', {
        'feedback_type_choices': Feedback.FEEDBACK_TYPE_CHOICES
    })



