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
    return render(request, 'home/products.html')

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
            Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                company=company,
                subject=subject,
                message=message,
                is_subscribed=is_subscribed
            )
            from django.contrib import messages
            messages.success(request, "Your message has been sent!")
            return redirect('contact')
        else:
            from django.contrib import messages
            messages.error(request, "Please fill in all required fields.")
    return render(request, 'home/contact.html')

def career(request):
    print("Career page")
    return render(request, 'home/career.html')
      

def signin(request):
    return render(request, 'home/signin.html')

def signup(request):
    return render(request, 'home/signup.html')

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
    users = User.objects.all().order_by('-date_joined')
    context = {'users': users}
    return render(request, 'home/admin/users.html', context)

@login_required
@user_passes_test(is_admin)
def admin_products(request):
    products = Product.objects.all().order_by('-created_at')
    context = {'products': products}
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
    settings = SiteSettings.objects.first()
    if not settings:
        settings = SiteSettings.objects.create()
    
    context = {'settings': settings}
    return render(request, 'home/admin/settings.html', context)