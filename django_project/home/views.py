# Footer and support/info pages
def news(request):
    return render(request, 'home/news.html')

def partners(request):
    return render(request, 'home/partners.html')

def documentation(request):
    return render(request, 'home/documentation.html')

def help_center(request):
    return render(request, 'home/help_center.html')

def status(request):
    return render(request, 'home/status.html')

def privacy_policy(request):
    return render(request, 'home/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'home/terms_of_service.html')
# Get Started view for requirements and meeting request
from django.shortcuts import render
def get_started(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        requirements = request.POST.get('requirements', '').strip()
        meeting = request.POST.get('meeting', '').strip()
        return render(request, 'home/get_started.html', {
            'success': True,
            'name': name
        })
    return render(request, 'home/get_started.html')
def product_eagle_pro(request):
    return render(request, 'home/product_eagle_pro.html')

def product_eagle_mini(request):
    return render(request, 'home/product_eagle_mini.html')

def product_sparrow(request):
    return render(request, 'home/product_sparrow.html')
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import redirect
from .models import *

# Create your views here.
# from django.http import HttpResponse
def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def products(request):
    # Get active products for display
    products = Product.objects.filter(is_active=True).order_by('-is_featured', '-created_at')
    
    # Group products by type for better organization
    gateways = products.filter(product_type='gateway')
    sensors = products.filter(product_type='sensor')
    software = products.filter(product_type='software')
    services = products.filter(product_type='service')
    
    context = {
        'products': products,
        'gateways': gateways,
        'sensors': sensors,
        'software': software,
        'services': services,
    }
    return render(request, 'home/products.html', context)

def contact(request):
    if request.method == 'POST':
        print(request.POST)  # Debug: print all POST data to console
        first_name = request.POST.get('firstName', '').strip()
        last_name = request.POST.get('lastName', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        company = request.POST.get('company', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        is_subscribed = bool(request.POST.get('newsletter'))

        # Only save if required fields are present
        if first_name and last_name and email and subject and message:
            # Save to database
            contact_obj = Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                company=company,
                subject=subject,
                message=message,
                is_subscribed=is_subscribed
            )
            
            # Send email notification
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                
                # Email to admin
                admin_subject = f"New Contact Form Submission: {subject}"
                admin_message = f"""
New contact form submission received:

Name: {first_name} {last_name}
Email: {email}
Phone: {phone}
Company: {company}
Subject: {subject}

Message:
{message}

Newsletter Subscription: {'Yes' if is_subscribed else 'No'}

---
This message was sent from the Tecosoft website contact form.
                """
                
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['sanjay953818@gmail.com'],
                    fail_silently=False,
                )
                
                # Confirmation email to user
                user_subject = "Thank you for contacting Tecosoft"
                user_message = f"""
Dear {first_name},

Thank you for contacting Tecosoft. We have received your message regarding "{subject}" and will get back to you within 24 hours.

Your message:
{message}

Best regards,
The Tecosoft Team

---
This is an automated confirmation email. Please do not reply to this email.
                """
                
                send_mail(
                    user_subject,
                    user_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True,  # Don't fail if user email fails
                )
                
                from django.contrib import messages
                messages.success(request, "Your message has been sent successfully! We'll get back to you within 24 hours.")
                
            except Exception as e:
                print(f"Email sending failed: {e}")
                from django.contrib import messages
                messages.success(request, "Your message has been received! We'll get back to you soon.")
            
            return redirect('contact')
        else:
            from django.contrib import messages
            messages.error(request, "Please fill in all required fields.")
    return render(request, 'home/contact.html')

def career(request):
    if request.method == 'POST':
        # Handle job application form submission
        first_name = request.POST.get('firstName', '').strip()
        last_name = request.POST.get('lastName', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        experience_years = request.POST.get('experience', '').strip()
        location = request.POST.get('location', '').strip()
        cover_letter = request.POST.get('coverLetter', '').strip()
        portfolio = request.POST.get('portfolio', '').strip()
        position = request.POST.get('selectedPosition', '').strip()
        resume = request.FILES.get('resume')
        
        # Check if required fields are present
        if first_name and last_name and email and position and resume:
            try:
                # Find or create a career/job posting for the position
                career_obj, created = Career.objects.get_or_create(
                    title=position,
                    defaults={
                        'slug': position.lower().replace(' ', '-'),
                        'description': f'Position for {position}',
                        'requirements': 'Requirements will be updated by admin',
                        'location': location or 'Remote',
                        'job_type': 'full-time',
                        'experience_level': 'mid',
                    }
                )
                
                # Create job application
                JobApplication.objects.create(
                    career=career_obj,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    experience_years=experience_years or '0-2',
                    resume=resume,
                    cover_letter=cover_letter,
                    status='pending'
                )
                
                messages.success(request, f'Thank you {first_name}! Your application for {position} has been submitted successfully. We will review it and get back to you within 3-5 business days.')
                return redirect('career')
                
            except Exception as e:
                messages.error(request, 'There was an error submitting your application. Please try again.')
                print(f"Error creating job application: {e}")
        else:
            messages.error(request, 'Please fill in all required fields including uploading your resume.')
    
    # Get active career positions for display
    careers = Career.objects.filter(is_active=True).order_by('-is_featured', '-created_at')
    context = {'careers': careers}
    return render(request, 'home/career.html', context)
      

def signin(request):
    from django.contrib.auth import authenticate, login
    
    if request.method == 'POST':
        email_or_username = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        print(f"=== LOGIN ATTEMPT ===")
        print(f"Email/Username: '{email_or_username}'")
        print(f"Password length: {len(password)}")
        
        if email_or_username and password:
            # Try authentication with email or username
            user = authenticate(request, username=email_or_username, password=password)
            print(f"Authentication result: {user}")
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                    print(f"Login successful for {user.username} ({user.email})")
                    
                    if user.is_staff:
                        return redirect('admin_dashboard')
                    else:
                        return redirect('index')
                else:
                    messages.error(request, 'Your account is disabled. Please contact support.')
            else:
                print(f"Authentication failed for: {email_or_username}")
                messages.error(request, 'Invalid email/username or password. Please check your credentials.')
        else:
            messages.error(request, 'Please enter both email and password.')
    
    return render(request, 'home/signin.html')

def signup(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('firstName', '').strip()
        last_name = request.POST.get('lastName', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirmPassword', '').strip()
        company_name = request.POST.get('companyName', '').strip()
        phone_number = request.POST.get('phoneNumber', '').strip()
        account_type = request.POST.get('accountType', 'individual')
        
        print(f"=== SIGNUP ATTEMPT ===")
        print(f"Email: {email}")
        print(f"Name: {first_name} {last_name}")
        
        # Validation
        if not all([first_name, last_name, email, password, confirm_password]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'home/signup.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'home/signup.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'home/signup.html')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'home/signup.html')
        
        try:
            # Create username from email (before @ symbol)
            username = email.split('@')[0]
            
            # Make sure username is unique
            original_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                phone_number=phone_number,
                account_type=account_type,
                is_verified=False
            )
            
            print(f"User created successfully: {user.username} ({user.email})")
            
            messages.success(request, f'Account created successfully! You can now login with your email: {email}')
            return redirect('signin')
            
        except Exception as e:
            print(f"Error creating user: {e}")
            messages.error(request, 'There was an error creating your account. Please try again.')
    
    return render(request, 'home/signup.html')

def signout(request):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

# Custom Admin Views
def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Get counts for dashboard
    users_count = User.objects.count()
    products_count = Product.objects.count()
    contacts_count = Contact.objects.count()
    careers_count = Career.objects.count()
    applications_count = JobApplication.objects.count()
    testimonials_count = Testimonial.objects.count()
    
    # Get recent data
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_contacts = Contact.objects.order_by('-created_at')[:5]
    recent_applications = JobApplication.objects.order_by('-created_at')[:5]
    
    context = {
        'users_count': users_count,
        'products_count': products_count,
        'contacts_count': contacts_count,
        'careers_count': careers_count,
        'applications_count': applications_count,
        'testimonials_count': testimonials_count,
        'recent_users': recent_users,
        'recent_contacts': recent_contacts,
        'recent_applications': recent_applications,
    }
    return render(request, 'home/admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_users(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_user':
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            password = request.POST.get('password', '').strip()
            password_confirm = request.POST.get('password_confirm', '').strip()
            phone_number = request.POST.get('phone_number', '').strip()
            company_name = request.POST.get('company_name', '').strip()
            account_type = request.POST.get('account_type', 'individual')
            is_staff = request.POST.get('is_staff') == 'on'
            is_active = request.POST.get('is_active') == 'on'
            
            # Validation
            if not username or not email or not password:
                messages.error(request, 'Username, email, and password are required.')
            elif password != password_confirm:
                messages.error(request, 'Passwords do not match.')
            elif len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
            else:
                try:
                    # Create user
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                    )
                    
                    # Set additional fields
                    user.phone_number = phone_number
                    user.company_name = company_name
                    user.account_type = account_type
                    user.is_staff = is_staff
                    user.is_active = is_active
                    user.save()
                    
                    messages.success(request, f'User "{username}" created successfully!')
                    
                except Exception as e:
                    messages.error(request, f'Error creating user: {str(e)}')
        
        elif action == 'delete_user':
            user_id = request.POST.get('user_id')
            if user_id:
                try:
                    user_to_delete = User.objects.get(id=user_id)
                    
                    # Prevent deletion of superusers and the current user
                    if user_to_delete.is_superuser:
                        messages.error(request, 'Cannot delete superuser accounts.')
                    elif user_to_delete.id == request.user.id:
                        messages.error(request, 'Cannot delete your own account.')
                    else:
                        username = user_to_delete.username
                        user_to_delete.delete()
                        messages.success(request, f'User "{username}" deleted successfully!')
                        
                except User.DoesNotExist:
                    messages.error(request, 'User not found.')
                except Exception as e:
                    messages.error(request, f'Error deleting user: {str(e)}')
            else:
                messages.error(request, 'Invalid user ID.')
        
        elif action == 'toggle_user_status':
            user_id = request.POST.get('user_id')
            if user_id:
                try:
                    user_to_toggle = User.objects.get(id=user_id)
                    
                    # Prevent deactivating superusers and the current user
                    if user_to_toggle.is_superuser and user_to_toggle.is_active:
                        messages.error(request, 'Cannot deactivate superuser accounts.')
                    elif user_to_toggle.id == request.user.id:
                        messages.error(request, 'Cannot deactivate your own account.')
                    else:
                        user_to_toggle.is_active = not user_to_toggle.is_active
                        user_to_toggle.save()
                        status = "activated" if user_to_toggle.is_active else "deactivated"
                        messages.success(request, f'User "{user_to_toggle.username}" {status} successfully!')
                        
                except User.DoesNotExist:
                    messages.error(request, 'User not found.')
                except Exception as e:
                    messages.error(request, f'Error updating user status: {str(e)}')
            else:
                messages.error(request, 'Invalid user ID.')
        
        elif action == 'bulk_action':
            bulk_action = request.POST.get('bulk_action')
            selected_users = request.POST.getlist('selected_users')
            
            if not selected_users:
                messages.error(request, 'No users selected.')
            elif not bulk_action:
                messages.error(request, 'No action selected.')
            else:
                try:
                    users_to_process = User.objects.filter(id__in=selected_users)
                    
                    # Filter out protected users
                    protected_users = []
                    processable_users = []
                    
                    for user in users_to_process:
                        if user.is_superuser or user.id == request.user.id:
                            protected_users.append(user.username)
                        else:
                            processable_users.append(user)
                    
                    if protected_users:
                        messages.warning(request, f'Skipped protected users: {", ".join(protected_users)}')
                    
                    if processable_users:
                        if bulk_action == 'delete':
                            count = len(processable_users)
                            for user in processable_users:
                                user.delete()
                            messages.success(request, f'Successfully deleted {count} user(s).')
                            
                        elif bulk_action == 'activate':
                            count = User.objects.filter(id__in=[u.id for u in processable_users]).update(is_active=True)
                            messages.success(request, f'Successfully activated {count} user(s).')
                            
                        elif bulk_action == 'deactivate':
                            count = User.objects.filter(id__in=[u.id for u in processable_users]).update(is_active=False)
                            messages.success(request, f'Successfully deactivated {count} user(s).')
                    else:
                        messages.warning(request, 'No users could be processed (all were protected).')
                        
                except Exception as e:
                    messages.error(request, f'Error processing bulk action: {str(e)}')
        
        return redirect('admin_users')
    
    users = User.objects.all().order_by('-date_joined')
    active_users_count = users.filter(is_active=True).count()
    staff_users_count = users.filter(is_staff=True).count()
    
    # New users this month
    from django.utils import timezone
    from datetime import datetime, timedelta
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_users_count = users.filter(date_joined__gte=thirty_days_ago).count()
    
    context = {
        'users': users,
        'active_users_count': active_users_count,
        'staff_users_count': staff_users_count,
        'new_users_count': new_users_count,
    }
    return render(request, 'home/admin/users.html', context)

@login_required
@user_passes_test(is_admin)
def admin_products(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_product':
            name = request.POST.get('name', '').strip()
            product_type = request.POST.get('product_type', 'gateway')
            short_description = request.POST.get('short_description', '').strip()
            description = request.POST.get('description', '').strip()
            price = request.POST.get('price', '').strip()
            features_text = request.POST.get('features', '').strip()
            is_featured = request.POST.get('is_featured') == 'on'
            is_active = request.POST.get('is_active') == 'on'
            image = request.FILES.get('image')
            
            if name and short_description and description:
                # Generate slug from name
                from django.utils.text import slugify
                slug = slugify(name)
                
                # Ensure slug is unique
                original_slug = slug
                counter = 1
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{original_slug}-{counter}"
                    counter += 1
                
                # Process features
                features = []
                if features_text:
                    features = [f.strip() for f in features_text.split('\n') if f.strip()]
                
                # Process price
                product_price = None
                if price:
                    try:
                        product_price = float(price)
                    except ValueError:
                        product_price = None
                
                product = Product.objects.create(
                    name=name,
                    slug=slug,
                    product_type=product_type,
                    short_description=short_description,
                    description=description,
                    price=product_price,
                    features=features,
                    is_featured=is_featured,
                    is_active=is_active,
                    image=image
                )
                
                messages.success(request, f'Product "{name}" added successfully!')
            else:
                messages.error(request, 'Please fill in all required fields.')
        
        elif action == 'edit_product':
            product_id = request.POST.get('product_id')
            if product_id:
                try:
                    product = Product.objects.get(id=product_id)
                    
                    # Update product fields
                    name = request.POST.get('name', '').strip()
                    product_type = request.POST.get('product_type', 'gateway')
                    short_description = request.POST.get('short_description', '').strip()
                    description = request.POST.get('description', '').strip()
                    price = request.POST.get('price', '').strip()
                    features_text = request.POST.get('features', '').strip()
                    is_featured = request.POST.get('is_featured') == 'on'
                    is_active = request.POST.get('is_active') == 'on'
                    image = request.FILES.get('image')
                    
                    if name and short_description and description:
                        # Update slug if name changed
                        if product.name != name:
                            from django.utils.text import slugify
                            slug = slugify(name)
                            
                            # Ensure slug is unique (excluding current product)
                            original_slug = slug
                            counter = 1
                            while Product.objects.filter(slug=slug).exclude(id=product.id).exists():
                                slug = f"{original_slug}-{counter}"
                                counter += 1
                            product.slug = slug
                        
                        # Process features
                        features = []
                        if features_text:
                            features = [f.strip() for f in features_text.split('\n') if f.strip()]
                        
                        # Process price
                        product_price = None
                        if price:
                            try:
                                product_price = float(price)
                            except ValueError:
                                product_price = None
                        
                        # Update product
                        product.name = name
                        product.product_type = product_type
                        product.short_description = short_description
                        product.description = description
                        product.price = product_price
                        product.features = features
                        product.is_featured = is_featured
                        product.is_active = is_active
                        
                        if image:
                            product.image = image
                        
                        product.save()
                        messages.success(request, f'Product "{name}" updated successfully!')
                    else:
                        messages.error(request, 'Please fill in all required fields.')
                        
                except Product.DoesNotExist:
                    messages.error(request, 'Product not found.')
            else:
                messages.error(request, 'Invalid product ID.')
        
        elif action == 'delete_product':
            product_id = request.POST.get('product_id')
            if product_id:
                try:
                    product = Product.objects.get(id=product_id)
                    product_name = product.name
                    product.delete()
                    messages.success(request, f'Product "{product_name}" deleted successfully!')
                except Product.DoesNotExist:
                    messages.error(request, 'Product not found.')
            else:
                messages.error(request, 'Invalid product ID.')
        
        return redirect('admin_products')
    
    products = Product.objects.all().order_by('-created_at')
    active_products_count = products.filter(is_active=True).count()
    featured_products_count = products.filter(is_featured=True).count()
    
    context = {
        'products': products,
        'active_products_count': active_products_count,
        'featured_products_count': featured_products_count,
    }
    return render(request, 'home/admin/products.html', context)

@login_required
@user_passes_test(is_admin)
def admin_contacts(request):
    contacts = Contact.objects.all().order_by('-created_at')
    context = {'contacts': contacts}
    return render(request, 'home/admin/contacts.html', context)

@login_required
@user_passes_test(is_admin)
def admin_careers(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_career':
            title = request.POST.get('title', '').strip()
            location = request.POST.get('location', '').strip()
            job_type = request.POST.get('job_type', 'full-time')
            experience_level = request.POST.get('experience_level', 'mid')
            description = request.POST.get('description', '').strip()
            requirements = request.POST.get('requirements', '').strip()
            salary_range = request.POST.get('salary_range', '').strip()
            is_featured = request.POST.get('is_featured') == 'on'
            is_active = request.POST.get('is_active') == 'on'
            
            if title and location and description and requirements:
                # Generate slug from title
                from django.utils.text import slugify
                slug = slugify(title)
                
                # Ensure slug is unique
                original_slug = slug
                counter = 1
                while Career.objects.filter(slug=slug).exists():
                    slug = f"{original_slug}-{counter}"
                    counter += 1
                
                career = Career.objects.create(
                    title=title,
                    slug=slug,
                    location=location,
                    job_type=job_type,
                    experience_level=experience_level,
                    description=description,
                    requirements=requirements,
                    salary_range=salary_range if salary_range else None,
                    is_featured=is_featured,
                    is_active=is_active
                )
                
                messages.success(request, f'Career position "{title}" added successfully!')
            else:
                messages.error(request, 'Please fill in all required fields.')
        
        elif action == 'edit_career':
            career_id = request.POST.get('career_id')
            if career_id:
                try:
                    career = Career.objects.get(id=career_id)
                    
                    # Update career fields
                    career.title = request.POST.get('title', '').strip()
                    career.location = request.POST.get('location', '').strip()
                    career.job_type = request.POST.get('job_type', 'full-time')
                    career.experience_level = request.POST.get('experience_level', 'mid')
                    career.description = request.POST.get('description', '').strip()
                    career.requirements = request.POST.get('requirements', '').strip()
                    career.salary_range = request.POST.get('salary_range', '').strip() or None
                    career.is_featured = request.POST.get('is_featured') == 'on'
                    career.is_active = request.POST.get('is_active') == 'on'
                    
                    if career.title and career.location and career.description and career.requirements:
                        # Update slug if title changed
                        from django.utils.text import slugify
                        new_slug = slugify(career.title)
                        if new_slug != career.slug:
                            # Ensure slug is unique
                            original_slug = new_slug
                            counter = 1
                            while Career.objects.filter(slug=new_slug).exclude(id=career.id).exists():
                                new_slug = f"{original_slug}-{counter}"
                                counter += 1
                            career.slug = new_slug
                        
                        career.save()
                        messages.success(request, f'Career position "{career.title}" updated successfully!')
                    else:
                        messages.error(request, 'Please fill in all required fields.')
                        
                except Career.DoesNotExist:
                    messages.error(request, 'Career position not found.')
            else:
                messages.error(request, 'Invalid career ID.')
        
        elif action == 'delete_career':
            career_id = request.POST.get('career_id')
            if career_id:
                try:
                    career = Career.objects.get(id=career_id)
                    career_title = career.title
                    career.delete()
                    messages.success(request, f'Career position "{career_title}" deleted successfully!')
                except Career.DoesNotExist:
                    messages.error(request, 'Career position not found.')
            else:
                messages.error(request, 'Invalid career ID.')
        
        return redirect('admin_careers')
    
    careers = Career.objects.all().order_by('-created_at')
    context = {'careers': careers}
    return render(request, 'home/admin/careers.html', context)

@login_required
@user_passes_test(is_admin)
def admin_applications(request):
    applications = JobApplication.objects.all().order_by('-created_at')
    context = {'applications': applications}
    return render(request, 'home/admin/applications.html', context)

@login_required
@user_passes_test(is_admin)
def admin_testimonials(request):
    testimonials = Testimonial.objects.all().order_by('-created_at')
    context = {'testimonials': testimonials}
    return render(request, 'home/admin/testimonials.html', context)

@login_required
@user_passes_test(is_admin)
def admin_faqs(request):
    faqs = FAQ.objects.all().order_by('order', '-created_at')
    context = {'faqs': faqs}
    return render(request, 'home/admin/faqs.html', context)

@login_required
@user_passes_test(is_admin)
def admin_settings(request):
    settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_settings':
            # Update basic information
            settings.site_name = request.POST.get('site_name', settings.site_name)
            settings.site_description = request.POST.get('site_description', settings.site_description)
            settings.contact_email = request.POST.get('contact_email', settings.contact_email)
            settings.contact_phone = request.POST.get('contact_phone', settings.contact_phone)
            settings.contact_address = request.POST.get('contact_address', settings.contact_address)
            
            # Update social media links
            settings.social_facebook = request.POST.get('social_facebook') or None
            settings.social_twitter = request.POST.get('social_twitter') or None
            settings.social_linkedin = request.POST.get('social_linkedin') or None
            settings.social_youtube = request.POST.get('social_youtube') or None
            
            # Update technical settings
            settings.google_analytics_id = request.POST.get('google_analytics_id') or None
            settings.maintenance_mode = request.POST.get('maintenance_mode') == 'on'
            
            try:
                settings.save()
                messages.success(request, 'Site settings updated successfully!')
            except Exception as e:
                messages.error(request, f'Error updating settings: {str(e)}')
        else:
            messages.error(request, 'Invalid action received.')
        
        return redirect('admin_settings')
    
    context = {'settings': settings}
    return render(request, 'home/admin/settings.html', context)

# Job Application Management Views
@login_required
@user_passes_test(is_admin)
def admin_application_detail(request, application_id):
    from django.shortcuts import get_object_or_404
    application = get_object_or_404(JobApplication, id=application_id)
    replies = AdminReply.objects.filter(job_application=application).order_by('-created_at')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_status':
            new_status = request.POST.get('status')
            notes = request.POST.get('notes', '')
            application.status = new_status
            application.notes = notes
            application.save()
            messages.success(request, f'Application status updated to {new_status}')
            
        elif action == 'send_reply':
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            
            if subject and message:
                reply = AdminReply.objects.create(
                    reply_type='job_application',
                    job_application=application,
                    admin_user=request.user,
                    subject=subject,
                    message=message,
                    is_sent=False,  # Will be set to True after successful email send
                    sent_at=None
                )
                
                # Send email to the applicant
                try:
                    from django.core.mail import send_mail
                    from django.conf import settings
                    
                    # Prepare email content
                    email_subject = f"Re: Your Application for {application.career.title} - {subject}"
                    email_message = f"""Dear {application.first_name} {application.last_name},

Thank you for your interest in the {application.career.title} position at Tecosoft.

{message}

Best regards,
{request.user.first_name} {request.user.last_name}
Tecosoft Team

---
This is a reply to your job application submitted on {application.created_at.strftime('%B %d, %Y')}.
If you have any questions, please don't hesitate to contact us.

Tecosoft - Leading Industry 4.0 Solutions
Email: {settings.DEFAULT_FROM_EMAIL}
"""
                    
                    # Send email
                    send_mail(
                        subject=email_subject,
                        message=email_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[application.email],
                        fail_silently=False,
                    )
                    
                    # Mark reply as sent
                    reply.is_sent = True
                    reply.sent_at = timezone.now()
                    reply.save()
                    
                    messages.success(request, f'Reply sent successfully to {application.email}!')
                    
                except Exception as e:
                    messages.error(request, f'Failed to send email: {str(e)}')
                    # Keep the reply but mark as not sent
                    reply.is_sent = False
                    reply.save()
            else:
                messages.error(request, 'Please provide both subject and message.')
        
        return redirect('admin_application_detail', application_id=application.id)
    
    context = {
        'application': application,
        'replies': replies,
        'status_choices': JobApplication._meta.get_field('status').choices,
    }
    return render(request, 'home/admin/application_detail.html', context)

@login_required
@user_passes_test(is_admin)
def admin_contact_detail(request, contact_id):
    from django.shortcuts import get_object_or_404
    contact = get_object_or_404(Contact, id=contact_id)
    replies = AdminReply.objects.filter(contact=contact).order_by('-created_at')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'mark_read':
            contact.is_read = True
            contact.save()
            messages.success(request, 'Contact marked as read')
            
        elif action == 'send_reply':
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            
            if subject and message:
                reply = AdminReply.objects.create(
                    reply_type='contact',
                    contact=contact,
                    admin_user=request.user,
                    subject=subject,
                    message=message,
                    is_sent=False,  # Will be set to True after successful email send
                    sent_at=None
                )
                
                # Send email to the contact person
                try:
                    from django.core.mail import send_mail
                    from django.conf import settings
                    
                    # Prepare email content
                    email_subject = f"Re: Your Inquiry - {subject}"
                    email_message = f"""Dear {contact.first_name} {contact.last_name},

Thank you for contacting Tecosoft regarding {contact.get_subject_display()}.

{message}

Best regards,
{request.user.first_name} {request.user.last_name}
Tecosoft Team

---
This is a reply to your inquiry submitted on {contact.created_at.strftime('%B %d, %Y')}.
If you have any further questions, please don't hesitate to contact us.

Tecosoft - Leading Industry 4.0 Solutions
Email: {settings.DEFAULT_FROM_EMAIL}
"""
                    
                    # Send email
                    send_mail(
                        subject=email_subject,
                        message=email_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[contact.email],
                        fail_silently=False,
                    )
                    
                    # Mark reply as sent and contact as read
                    reply.is_sent = True
                    reply.sent_at = timezone.now()
                    reply.save()
                    
                    contact.is_read = True
                    contact.save()
                    
                    messages.success(request, f'Reply sent successfully to {contact.email}!')
                    
                except Exception as e:
                    messages.error(request, f'Failed to send email: {str(e)}')
                    # Keep the reply but mark as not sent
                    reply.is_sent = False
                    reply.save()
                    
                    # Still mark contact as read since admin attempted to reply
                    contact.is_read = True
                    contact.save()
            else:
                messages.error(request, 'Please provide both subject and message.')
        
        return redirect('admin_contact_detail', contact_id=contact.id)
    
    context = {
        'contact': contact,
        'replies': replies,
    }
    return render(request, 'home/admin/contact_detail.html', context)

@login_required
@user_passes_test(is_admin)
def admin_replies(request):
    replies = AdminReply.objects.all().order_by('-created_at')
    context = {'replies': replies}
    return render(request, 'home/admin/replies.html', context)

# Bulk Actions
@login_required
@user_passes_test(is_admin)
def admin_bulk_actions(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        model_type = request.POST.get('model_type')
        selected_ids = request.POST.getlist('selected_items')
        
        if not selected_ids:
            messages.error(request, 'No items selected.')
            return redirect(request.META.get('HTTP_REFERER', 'admin_dashboard'))
        
        if model_type == 'applications' and action == 'update_status':
            new_status = request.POST.get('bulk_status')
            JobApplication.objects.filter(id__in=selected_ids).update(status=new_status)
            messages.success(request, f'Updated {len(selected_ids)} applications to {new_status}')
            
        elif model_type == 'contacts' and action == 'mark_read':
            Contact.objects.filter(id__in=selected_ids).update(is_read=True)
            messages.success(request, f'Marked {len(selected_ids)} contacts as read')
            
        elif action == 'delete':
            if model_type == 'applications':
                JobApplication.objects.filter(id__in=selected_ids).delete()
            elif model_type == 'contacts':
                Contact.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f'Deleted {len(selected_ids)} items')
    
    return redirect(request.META.get('HTTP_REFERER', 'admin_dashboard'))

# Add timezone import at the top
from django.utils import timezone
# User Notifications
@login_required
def notifications(request):
    """Display user notifications"""
    user_notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    # Mark notifications as read when viewed
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        if notification_id:
            try:
                notification = Notification.objects.get(id=notification_id, user=request.user)
                notification.is_read = True
                notification.save()
                messages.success(request, 'Notification marked as read.')
            except Notification.DoesNotExist:
                messages.error(request, 'Notification not found.')
        return redirect('notifications')
    
    context = {
        'notifications': user_notifications,
        'unread_count': user_notifications.filter(is_read=False).count(),
    }
    return render(request, 'home/notifications.html', context)

@login_required
def mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        messages.success(request, 'Notification marked as read.')
    except Notification.DoesNotExist:
        messages.error(request, 'Notification not found.')
    
    return redirect('notifications')

@login_required
def mark_all_notifications_read(request):
    """Mark all user notifications as read"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, 'All notifications marked as read.')
    return redirect('notifications')
# Session Keep-Alive
@login_required
def keep_alive(request):
    """Simple endpoint to keep sessions alive"""
    from django.http import JsonResponse
    
    if request.user.is_authenticated:
        return JsonResponse({
            'status': 'ok',
            'user': request.user.username,
            'is_staff': request.user.is_staff
        })
    else:
        return JsonResponse({'status': 'unauthorized'}, status=401)