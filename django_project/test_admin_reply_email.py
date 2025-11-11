#!/usr/bin/env python
"""
Test script to verify admin reply email functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from home.models import Contact, JobApplication, AdminReply, User

def test_email_configuration():
    """Test if email configuration is working"""
    print("Testing email configuration...")
    
    try:
        # Test basic email sending
        send_mail(
            subject='Test Email from Tecosoft Admin',
            message='This is a test email to verify the email configuration is working.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['test@example.com'],  # This will fail but we can see if config is correct
            fail_silently=False,
        )
        print("✓ Email configuration appears to be correct")
    except Exception as e:
        print(f"✗ Email configuration error: {e}")
        return False
    
    return True

def test_admin_reply_functionality():
    """Test the admin reply functionality"""
    print("\nTesting admin reply functionality...")
    
    # Check if there are any contacts to reply to
    contacts = Contact.objects.all()[:1]
    if contacts:
        contact = contacts[0]
        print(f"✓ Found contact: {contact.first_name} {contact.last_name} ({contact.email})")
        
        # Check if there are admin users
        admin_users = User.objects.filter(is_staff=True)[:1]
        if admin_users:
            admin_user = admin_users[0]
            print(f"✓ Found admin user: {admin_user.username}")
            
            # Create a test reply (without actually sending email)
            reply = AdminReply(
                reply_type='contact',
                contact=contact,
                admin_user=admin_user,
                subject='Test Reply',
                message='This is a test reply to verify the functionality.',
                is_sent=False
            )
            
            print("✓ Admin reply object can be created")
            print(f"✓ Reply would be sent to: {contact.email}")
            
        else:
            print("✗ No admin users found")
    else:
        print("✗ No contacts found to test with")
    
    # Check job applications
    applications = JobApplication.objects.all()[:1]
    if applications:
        application = applications[0]
        print(f"✓ Found job application: {application.first_name} {application.last_name} ({application.email})")
    else:
        print("✗ No job applications found to test with")

def main():
    print("=== Tecosoft Admin Reply Email Test ===\n")
    
    # Test email configuration
    email_ok = test_email_configuration()
    
    # Test admin reply functionality
    test_admin_reply_functionality()
    
    print("\n=== Email Settings ===")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    print("\n=== Instructions ===")
    print("1. Make sure your Gmail app password is correct")
    print("2. Test by replying to a contact form or job application in the admin panel")
    print("3. Check the recipient's email inbox for the reply")
    print("4. If emails aren't being sent, check the Django logs for error messages")

if __name__ == '__main__':
    main()