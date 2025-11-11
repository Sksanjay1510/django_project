#!/usr/bin/env python
"""
Test the complete admin reply workflow
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from home.views import admin_contact_detail
from home.models import Contact, AdminReply

def test_complete_workflow():
    """Test the complete admin reply workflow"""
    print("=== Testing Complete Admin Reply Workflow ===\n")
    
    # Get test data
    contact = Contact.objects.first()
    if not contact:
        print("❌ No contacts found")
        return
    
    User = get_user_model()
    admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        print("❌ No admin users found")
        return
    
    print(f"✓ Testing with contact: {contact.first_name} {contact.last_name} ({contact.email})")
    print(f"✓ Testing with admin: {admin_user.username}")
    
    # Create a request factory
    factory = RequestFactory()
    
    # Create POST request (simulating form submission)
    post_data = {
        'action': 'send_reply',
        'subject': 'Test Reply - Complete Workflow',
        'message': 'This is a test reply to verify the complete admin workflow is functioning correctly.'
    }
    
    request = factory.post(f'/admin-contact/{contact.id}/', post_data)
    request.user = admin_user
    
    # Add session middleware
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    
    # Add messages framework
    setattr(request, '_messages', FallbackStorage(request))
    
    print("✓ Simulating admin reply submission...")
    
    # Count replies before
    replies_before = AdminReply.objects.filter(contact=contact).count()
    
    try:
        # Call the view
        response = admin_contact_detail(request, contact.id)
        
        print(f"✓ View executed successfully")
        print(f"✓ Response status: {response.status_code}")
        
        # Count replies after
        replies_after = AdminReply.objects.filter(contact=contact).count()
        
        if replies_after > replies_before:
            print(f"✓ New reply created ({replies_after - replies_before} new replies)")
            
            # Get the latest reply
            latest_reply = AdminReply.objects.filter(contact=contact).order_by('-created_at').first()
            
            print(f"✓ Reply subject: {latest_reply.subject}")
            print(f"✓ Reply admin: {latest_reply.admin_user.username}")
            print(f"✓ Email sent: {'YES' if latest_reply.is_sent else 'NO'}")
            
            if latest_reply.is_sent:
                print(f"✅ EMAIL SUCCESSFULLY SENT to {contact.email}")
                print(f"✅ Sent at: {latest_reply.sent_at}")
            else:
                print(f"❌ EMAIL NOT SENT")
                
        else:
            print("❌ No new reply was created")
        
        # Check messages
        messages = list(request._messages)
        if messages:
            print("\n=== Messages ===")
            for message in messages:
                print(f"{message.tags}: {message}")
        
    except Exception as e:
        print(f"❌ Error in view: {str(e)}")
        import traceback
        traceback.print_exc()

def show_email_status():
    """Show current email status"""
    print("\n=== Current Email Status ===")
    
    total_replies = AdminReply.objects.count()
    sent_replies = AdminReply.objects.filter(is_sent=True).count()
    failed_replies = AdminReply.objects.filter(is_sent=False).count()
    
    print(f"Total replies: {total_replies}")
    print(f"Successfully sent: {sent_replies}")
    print(f"Failed to send: {failed_replies}")
    
    if total_replies > 0:
        success_rate = (sent_replies / total_replies) * 100
        print(f"Success rate: {success_rate:.1f}%")
    
    # Show recent replies
    recent_replies = AdminReply.objects.order_by('-created_at')[:3]
    if recent_replies:
        print("\nRecent replies:")
        for reply in recent_replies:
            status = "✅ Sent" if reply.is_sent else "❌ Failed"
            recipient = "Unknown"
            
            if reply.contact:
                recipient = reply.contact.email
            elif reply.job_application:
                recipient = reply.job_application.email
            
            print(f"  - {reply.subject} → {recipient} ({status})")

if __name__ == '__main__':
    show_email_status()
    test_complete_workflow()
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("1. If the test shows 'EMAIL SUCCESSFULLY SENT', check the recipient's inbox")
    print("2. Check spam/junk folder - Gmail might be filtering the emails")
    print("3. Try sending a reply through the actual admin interface")
    print("4. Ask the recipient to check their email and spam folder")
    print("="*60)