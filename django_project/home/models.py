from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractUser):
    """Custom User model for Tecosoft application"""
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    # Additional fields
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    account_type = models.CharField(
        max_length=20,
        choices=[
            ('individual', 'Individual'),
            ('business', 'Business'),
            ('enterprise', 'Enterprise'),
        ],
        default='individual'
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self):
        return f"{self.username} - {self.email}"

class Product(models.Model):
    """Product model for Tecosoft products"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    product_type = models.CharField(
        max_length=20,
        choices=[
            ('gateway', 'IoT Gateway'),
            ('sensor', 'Sensor'),
            ('software', 'Software'),
            ('service', 'Service'),
        ],
        default='gateway'
    )
    specifications = models.JSONField(default=dict, blank=True)
    features = models.JSONField(default=list, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class Contact(models.Model):
    """Contact form submissions"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(
        max_length=20,
        choices=[
            ('general', 'General Inquiry'),
            ('sales', 'Sales & Pricing'),
            ('support', 'Technical Support'),
            ('demo', 'Request Demo'),
            ('partnership', 'Partnership'),
            ('other', 'Other'),
        ],
        default='general'
    )
    message = models.TextField()
    is_subscribed = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"

class Career(models.Model):
    """Job openings and career opportunities"""
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(
        max_length=20,
        choices=[
            ('full-time', 'Full-time'),
            ('part-time', 'Part-time'),
            ('contract', 'Contract'),
            ('internship', 'Internship'),
        ],
        default='full-time'
    )
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('entry', 'Entry Level'),
            ('mid', 'Mid Level'),
            ('senior', 'Senior Level'),
            ('lead', 'Lead'),
            ('executive', 'Executive'),
        ],
        default='mid'
    )
    salary_range = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Career"
        verbose_name_plural = "Careers"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.location}"

class JobApplication(models.Model):
    """Job applications submitted by candidates"""
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='applications')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    experience_years = models.CharField(
        max_length=20,
        choices=[
            ('0-2', '0-2 years'),
            ('3-5', '3-5 years'),
            ('6-10', '6-10 years'),
            ('10+', '10+ years'),
        ],
        default='0-2'
    )
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('reviewed', 'Reviewed'),
            ('shortlisted', 'Shortlisted'),
            ('interviewed', 'Interviewed'),
            ('hired', 'Hired'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.career.title}"

class Newsletter(models.Model):
    """Newsletter subscriptions"""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email

class Testimonial(models.Model):
    """Customer testimonials and reviews"""
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    testimonial = models.TextField()
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=5
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.company}"

class FAQ(models.Model):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=[
            ('general', 'General'),
            ('technical', 'Technical'),
            ('pricing', 'Pricing'),
            ('support', 'Support'),
            ('product', 'Product'),
        ],
        default='general'
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.question

class SiteSettings(models.Model):
    """Site-wide settings and configuration"""
    site_name = models.CharField(max_length=100, default="Tecosoft")
    site_description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(default="info@tecosoft.com")
    contact_phone = models.CharField(max_length=20, default="+91 9611851196")
    contact_address = models.TextField(default="Vijaynagar, Bangalore, Karnataka, India")
    social_facebook = models.URLField(blank=True, null=True)
    social_twitter = models.URLField(blank=True, null=True)
    social_linkedin = models.URLField(blank=True, null=True)
    social_youtube = models.URLField(blank=True, null=True)
    maintenance_mode = models.BooleanField(default=False)
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            return
        super().save(*args, **kwargs)
