#!/usr/bin/env python
"""
Monitor admin replies in real-time to see if emails are being sent
"""
import os
import django
import time
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from home.models import AdminReply

def monitor_replies():
    """Monitor admin replies in real-time"""
    print("=== Real-time Admin Reply Monitor ===")
    print("Monitoring admin replies... Press Ctrl+C to stop\n")
    
    last_count = AdminReply.objects.count()
    print(f"Current replies in database: {last_count}")
    
    try:
        while True:
            current_count = AdminReply.objects.count()
            
            if current_count > last_count:
                # New reply detected
                new_replies = AdminReply.objects.order_by('-created_at')[:current_count - last_count]
                
                for reply in new_replies:
                    print(f"\n🔔 NEW REPLY DETECTED!")
                    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"Subject: {reply.subject}")
                    print(f"Type: {reply.reply_type}")
                    
                    if reply.reply_type == 'contact' and reply.contact:
                        print(f"Recipient: {reply.contact.first_name} {reply.contact.last_name} ({reply.contact.email})")
                    elif reply.reply_type == 'job_application' and reply.job_application:
                        print(f"Recipient: {reply.job_application.first_name} {reply.job_application.last_name} ({reply.job_application.email})")
                    
                    print(f"Admin: {reply.admin_user.username}")
                    print(f"Email Sent: {'✅ YES' if reply.is_sent else '❌ NO'}")
                    
                    if reply.is_sent and reply.sent_at:
                        print(f"Sent At: {reply.sent_at}")
                    
                    print(f"Message: {reply.message[:100]}...")
                    print("-" * 50)
                
                last_count = current_count
            
            time.sleep(2)  # Check every 2 seconds
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")

def show_recent_replies():
    """Show recent replies for context"""
    print("\n=== Recent Replies (Last 5) ===")
    recent_replies = AdminReply.objects.order_by('-created_at')[:5]
    
    if not recent_replies:
        print("No replies found.")
        return
    
    for i, reply in enumerate(recent_replies, 1):
        status = "✅ Sent" if reply.is_sent else "❌ Not Sent"
        recipient = "Unknown"
        
        if reply.reply_type == 'contact' and reply.contact:
            recipient = f"{reply.contact.first_name} {reply.contact.last_name} ({reply.contact.email})"
        elif reply.reply_type == 'job_application' and reply.job_application:
            recipient = f"{reply.job_application.first_name} {reply.job_application.last_name} ({reply.job_application.email})"
        
        print(f"{i}. {reply.subject} - {status}")
        print(f"   To: {recipient}")
        print(f"   Created: {reply.created_at}")
        if reply.is_sent and reply.sent_at:
            print(f"   Sent: {reply.sent_at}")
        print()

if __name__ == '__main__':
    show_recent_replies()
    
    print("\n" + "="*60)
    print("INSTRUCTIONS:")
    print("1. Keep this script running")
    print("2. Go to your admin panel in the browser")
    print("3. Reply to a contact form or job application")
    print("4. Watch this console for real-time updates")
    print("="*60)
    
    monitor_replies()