#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from home.models import User, Notification

def test_notifications():
    print("=== Testing Notification System ===")
    
    # Get the user
    try:
        user = User.objects.get(email='sksachin1510@gmail.com')
        print(f"✓ Found user: {user.username} - {user.email}")
    except User.DoesNotExist:
        print("✗ User not found!")
        return
    
    # Check notifications
    notifications = Notification.objects.filter(user=user)
    print(f"✓ Total notifications for user: {notifications.count()}")
    
    unread_count = notifications.filter(is_read=False).count()
    print(f"✓ Unread notifications: {unread_count}")
    
    for n in notifications:
        print(f"  - {n.title} (Read: {n.is_read}, Type: {n.notification_type})")
    
    # Test context processor
    from home.context_processors import notification_count
    
    class MockRequest:
        def __init__(self, user):
            self.user = user
    
    request = MockRequest(user)
    context = notification_count(request)
    print(f"✓ Context processor returns: {context}")

if __name__ == '__main__':
    test_notifications()