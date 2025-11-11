#!/usr/bin/env python
"""
Test script to actually send a reply email
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from home.models import Contact, AdminReply, User

def send_test_reply():
    """Send a test reply email"""
    print("=== Testing Admin Reply Email Functionality ===\n")
    
    # Get the first contact
    contact = Contact.objects.first()
    if not contact:
        print("No contacts found. Please create a contact first.")
        return
    
    # Get an admin user
    admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        print("No admin users found. Please create an admin user first.")
        return
    
    print(f"Sending test reply to: {contact.first_name} {contact.last_name} ({contact.email})")
    print(f"From admin: {admin_user.username}")
    
    # Create the reply
    reply = AdminReply.objects.create(
        reply_type='contact',
        contact=contact,
        admin_user=admin_user,
        subject='Test Reply from Tecosoft Admin',
        message='This is a test reply to verify that the email functionality is working correctly.',
        is_sent=False
    )
    
    try:
        # Prepare email content
        email_subject = f"Re: Your Inquiry - {reply.subject}"
        email_message = f"""Dear {contact.first_name} {contact.last_name},

Thank you for contacting Tecosoft regarding {contact.get_subject_display()}.

{reply.message}

Best regards,
{admin_user.first_name} {admin_user.last_name}
Tecosoft Team

---
This is a reply to your inquiry submitted on {contact.created_at.strftime('%B %d, %Y')}.
If you have any further questions, please don't hesitate to contact us.

Tecosoft - Leading Industry 4.0 Solutions
Email: {settings.DEFAULT_FROM_EMAIL}
"""
        
        print(f"\nEmail Subject: {email_subject}")
        print(f"Recipient: {contact.email}")
        print(f"From: {settings.DEFAULT_FROM_EMAIL}")
        print("\nSending email...")
        
        # Send email
        send_mail(
            subject=email_subject,
            message=email_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact.email],
            fail_silently=False,
        )
        
        # Mark reply as sent
        reply.is_sent = True
        reply.sent_at = timezone.now()
        reply.save()
        
        print("✅ Email sent successfully!")
        print(f"✅ Reply marked as sent in database")
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        reply.is_sent = False
        reply.save()
        
        # Print troubleshooting info
        print("\n=== Troubleshooting Information ===")
        print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        print("\nPossible issues:")
        print("1. Gmail app password might be incorrect")
        print("2. Gmail account might have 2FA disabled")
        print("3. Network connectivity issues")
        print("4. Gmail might be blocking the connection")

if __name__ == '__main__':
    send_test_reply()