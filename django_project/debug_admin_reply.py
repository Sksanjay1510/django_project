#!/usr/bin/env python
"""
Debug script to test admin reply functionality step by step
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from home.models import Contact, JobApplication, AdminReply, User

def test_admin_reply_via_web():
    """Test admin reply functionality through web interface"""
    print("=== Testing Admin Reply via Web Interface ===\n")
    
    # Create a test client
    client = Client()
    
    # Get or create admin user
    User = get_user_model()
    admin_user, created = User.objects.get_or_create(
        username='testadmin',
        defaults={
            'email': 'admin@tecosoft.com',
            'first_name': 'Test',
            'last_name': 'Admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✓ Created test admin user")
    else:
        print("✓ Using existing admin user")
    
    # Login as admin
    login_success = client.login(username='testadmin', password='admin123')
    if not login_success:
        print("❌ Failed to login as admin")
        return
    print("✓ Logged in as admin")
    
    # Get a contact to reply to
    contact = Contact.objects.first()
    if not contact:
        print("❌ No contacts found to test with")
        return
    
    print(f"✓ Found contact: {contact.first_name} {contact.last_name} ({contact.email})")
    
    # Test sending a reply via POST request
    url = reverse('admin_contact_detail', args=[contact.id])
    print(f"✓ Testing reply at URL: {url}")
    
    reply_data = {
        'action': 'send_reply',
        'subject': 'Test Reply via Web Interface',
        'message': 'This is a test reply sent through the web interface to verify email functionality.'
    }
    
    print("✓ Sending reply via POST request...")
    response = client.post(url, reply_data)
    
    print(f"✓ Response status: {response.status_code}")
    
    # Check if reply was created
    latest_reply = AdminReply.objects.filter(contact=contact).order_by('-created_at').first()
    if latest_reply:
        print(f"✓ Reply created: {latest_reply.subject}")
        print(f"✓ Email sent status: {latest_reply.is_sent}")
        if latest_reply.is_sent:
            print(f"✓ Email sent at: {latest_reply.sent_at}")
            print(f"✓ Email sent to: {contact.email}")
        else:
            print("❌ Email was not sent")
    else:
        print("❌ No reply was created")
    
    # Check Django messages
    if hasattr(response, 'context') and response.context:
        messages = list(response.context.get('messages', []))
        if messages:
            print("\n=== Django Messages ===")
            for message in messages:
                print(f"{message.tags}: {message}")
        else:
            print("✓ No Django messages (this might indicate an issue)")

def check_email_settings():
    """Check email configuration"""
    print("\n=== Email Configuration Check ===")
    from django.conf import settings
    
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    # Test basic email sending
    try:
        from django.core.mail import send_mail
        print("\n✓ Django mail module imported successfully")
        
        # Try to send a test email (this will fail but we can see if there are config issues)
        send_mail(
            'Test Email',
            'This is a test.',
            settings.DEFAULT_FROM_EMAIL,
            ['test@example.com'],
            fail_silently=True,  # Don't fail if email can't be sent
        )
        print("✓ send_mail function executed without errors")
        
    except Exception as e:
        print(f"❌ Email configuration error: {e}")

def check_database_state():
    """Check current database state"""
    print("\n=== Database State ===")
    
    contacts_count = Contact.objects.count()
    applications_count = JobApplication.objects.count()
    replies_count = AdminReply.objects.count()
    admin_users_count = User.objects.filter(is_staff=True).count()
    
    print(f"Contacts: {contacts_count}")
    print(f"Job Applications: {applications_count}")
    print(f"Admin Replies: {replies_count}")
    print(f"Admin Users: {admin_users_count}")
    
    # Show recent replies
    recent_replies = AdminReply.objects.order_by('-created_at')[:3]
    if recent_replies:
        print("\nRecent Replies:")
        for reply in recent_replies:
            status = "✓ Sent" if reply.is_sent else "❌ Not Sent"
            print(f"  - {reply.subject} ({status})")

def main():
    print("=== Tecosoft Admin Reply Debug Tool ===\n")
    
    check_email_settings()
    check_database_state()
    test_admin_reply_via_web()
    
    print("\n=== Recommendations ===")
    print("1. Check Django server logs for any error messages")
    print("2. Try sending a reply through the admin interface manually")
    print("3. Check the recipient's email inbox (including spam folder)")
    print("4. Verify Gmail app password is correct and 2FA is enabled")

if __name__ == '__main__':
    main()