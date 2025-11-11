#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    print("=== Testing Email Configuration ===")
    print(f"Email Host: {settings.EMAIL_HOST}")
    print(f"Email User: {settings.EMAIL_HOST_USER}")
    print(f"Email Port: {settings.EMAIL_PORT}")
    print(f"Use TLS: {settings.EMAIL_USE_TLS}")
    
    try:
        print("\nSending test email...")
        send_mail(
            'Test Email from Tecosoft Django',
            'This is a test email to verify your email configuration is working correctly.',
            settings.DEFAULT_FROM_EMAIL,
            ['sanjay953818@gmail.com'],
            fail_silently=False,
        )
        print("✓ Email sent successfully!")
        print("✓ Check your inbox at sanjay953818@gmail.com")
        
    except Exception as e:
        print(f"✗ Email failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you've enabled 2-Factor Authentication")
        print("2. Generate an App Password (not your regular password)")
        print("3. Update EMAIL_HOST_PASSWORD in settings.py")
        print("4. Check your internet connection")

if __name__ == '__main__':
    test_email()