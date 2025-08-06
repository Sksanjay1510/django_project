from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    User, Product, Contact, Career, JobApplication, 
    Newsletter, Testimonial, FAQ, SiteSettings
)

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom admin for User model"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'company_name', 'account_type', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('account_type', 'is_verified', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'company_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'company_name', 'account_type')}),
        ('Permissions', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'company_name', 'account_type'),
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin for Product model"""
    list_display = ('name', 'product_type', 'price', 'is_active', 'is_featured', 'created_at')
    list_filter = ('product_type', 'is_active', 'is_featured', 'created_at')
    search_fields = ('name', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active', 'is_featured')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'short_description', 'description', 'product_type')
        }),
        ('Pricing & Status', {
            'fields': ('price', 'is_active', 'is_featured')
        }),
        ('Media & Data', {
            'fields': ('image', 'specifications', 'features')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin for Contact model"""
    list_display = ('full_name', 'email', 'company', 'subject', 'is_read', 'is_subscribed', 'created_at')
    list_filter = ('subject', 'is_read', 'is_subscribed', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read', 'is_subscribed')
    actions = ['mark_as_read', 'mark_as_unread', 'export_contacts']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'company')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Preferences', {
            'fields': ('is_subscribed',)
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Full Name"
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} contacts marked as read.")
    mark_as_read.short_description = "Mark selected contacts as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"{queryset.count()} contacts marked as unread.")
    mark_as_unread.short_description = "Mark selected contacts as unread"
    
    def export_contacts(self, request, queryset):
        # This would typically export to CSV/Excel
        self.message_user(request, f"Export functionality for {queryset.count()} contacts.")
    export_contacts.short_description = "Export selected contacts"

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    """Admin for Career model"""
    list_display = ('title', 'location', 'job_type', 'experience_level', 'is_active', 'is_featured', 'applications_count', 'created_at')
    list_filter = ('job_type', 'experience_level', 'is_active', 'is_featured', 'created_at')
    search_fields = ('title', 'description', 'requirements', 'location')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'applications_count')
    list_editable = ('is_active', 'is_featured')
    
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'slug', 'description', 'requirements', 'location')
        }),
        ('Job Details', {
            'fields': ('job_type', 'experience_level', 'salary_range')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def applications_count(self, obj):
        return obj.applications.count()
    applications_count.short_description = "Applications"

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    """Admin for JobApplication model"""

    list_display = ('full_name', 'career', 'email', 'experience_years', 'status', 'created_at')
    list_filter = ('status', 'experience_years', 'career', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'cover_letter')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    actions = ['mark_as_reviewed', 'mark_as_shortlisted', 'mark_as_rejected']
    
    fieldsets = (
        ('Applicant Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'experience_years')
        }),
        ('Application Details', {
            'fields': ('career', 'resume', 'cover_letter')
        }),
        ('Status & Notes', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Full Name"
    
    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
        self.message_user(request, f"{queryset.count()} applications marked as reviewed.")
    mark_as_reviewed.short_description = "Mark selected applications as reviewed"
    
    def mark_as_shortlisted(self, request, queryset):
        queryset.update(status='shortlisted')
        self.message_user(request, f"{queryset.count()} applications marked as shortlisted.")
    mark_as_shortlisted.short_description = "Mark selected applications as shortlisted"
    
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} applications marked as rejected.")
    mark_as_rejected.short_description = "Mark selected applications as rejected"

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin for Newsletter model"""
    list_display = ('email', 'is_active', 'subscribed_at', 'unsubscribed_at')
    list_filter = ('is_active', 'subscribed_at', 'unsubscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at', 'unsubscribed_at')
    list_editable = ('is_active',)
    actions = ['activate_subscriptions', 'deactivate_subscriptions', 'export_emails']
    
    fieldsets = (
        ('Subscription Details', {
            'fields': ('email', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def activate_subscriptions(self, request, queryset):
        queryset.update(is_active=True, unsubscribed_at=None)
        self.message_user(request, f"{queryset.count()} subscriptions activated.")
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_active=False, unsubscribed_at=timezone.now())
        self.message_user(request, f"{queryset.count()} subscriptions deactivated.")
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"
    
    def export_emails(self, request, queryset):
        self.message_user(request, f"Export functionality for {queryset.count()} email addresses.")
    export_emails.short_description = "Export email addresses"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin for Testimonial model"""
    list_display = ('name', 'company', 'position', 'rating', 'is_featured', 'is_active', 'created_at')
    list_filter = ('rating', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'company', 'testimonial')
    readonly_fields = ('created_at',)
    list_editable = ('is_featured', 'is_active')
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'company', 'position')
        }),
        ('Testimonial Content', {
            'fields': ('testimonial', 'rating')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Admin for FAQ model"""
    list_display = ('question', 'category', 'is_active', 'order', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('question', 'answer')
    readonly_fields = ('created_at',)
    list_editable = ('is_active', 'order')
    
    fieldsets = (
        ('FAQ Content', {
            'fields': ('question', 'answer', 'category')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin for SiteSettings model"""
    list_display = ('site_name', 'contact_email', 'contact_phone', 'maintenance_mode', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_description')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'contact_address')
        }),
        ('Social Media', {
            'fields': ('social_facebook', 'social_twitter', 'social_linkedin', 'social_youtube'),
            'classes': ('collapse',)
        }),
        ('Technical Settings', {
            'fields': ('maintenance_mode', 'google_analytics_id'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of site settings
        return False

# Customize admin site
admin.site.site_header = "Tecosoft Administration"
admin.site.site_title = "Tecosoft Admin"
admin.site.index_title = "Welcome to Tecosoft Administration"

# Register admin actions
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)
make_active.short_description = "Mark selected items as active"

def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)
make_inactive.short_description = "Mark selected items as inactive"

# Add actions to relevant models
ProductAdmin.actions = [make_active, make_inactive] + list(ProductAdmin.actions)
CareerAdmin.actions = [make_active, make_inactive] + list(CareerAdmin.actions)
TestimonialAdmin.actions = [make_active, make_inactive] + list(TestimonialAdmin.actions)
FAQAdmin.actions = [make_active, make_inactive] + list(FAQAdmin.actions)
