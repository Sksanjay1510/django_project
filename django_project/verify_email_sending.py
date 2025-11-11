#!/usr/bin/env python
"""
Verify email sending functionality with detailed debugging
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_django_email():
    """Test Django's email functionality"""
    print("=== Testing Django Email Functionality ===\n")
    
    test_email = "varshith182001@gmail.com"  # Using the contact email from database
    
    try:
        print(f"Sending test email to: {test_email}")
        print(f"From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"SMTP Host: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        print(f"TLS: {settings.EMAIL_USE_TLS}")
        print(f"Username: {settings.EMAIL_HOST_USER}")
        print()
        
        result = send_mail(
            subject='Test Email from Tecosoft Admin Panel',
            message='''This is a test email to verify that the Tecosoft admin reply functionality is working correctly.

If you receive this email, it means:
✅ Django email configuration is correct
✅ Gmail SMTP is working
✅ Admin reply emails should be delivered

This email was sent from the Tecosoft admin system.

Best regards,
Tecosoft Team''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        print(f"✅ Email sent successfully!")
        print(f"✅ send_mail returned: {result}")
        print(f"✅ Check {test_email} inbox for the test email")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

def test_raw_smtp():
    """Test raw SMTP connection"""
    print("\n=== Testing Raw SMTP Connection ===\n")
    
    try:
        print("Connecting to Gmail SMTP...")
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        print("✅ TLS connection established")
        
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print("✅ SMTP authentication successful")
        
        # Create test message
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = "varshith182001@gmail.com"
        msg['Subject'] = "Raw SMTP Test from Tecosoft"
        
        body = "This is a raw SMTP test to verify the email configuration."
        msg.attach(MIMEText(body, 'plain'))
        
        server.send_message(msg)
        print("✅ Raw SMTP email sent successfully")
        
        server.quit()
        print("✅ SMTP connection closed")
        
        return True
        
    except Exception as e:
        print(f"❌ Raw SMTP failed: {str(e)}")
        return False

def check_email_settings():
    """Check email settings for common issues"""
    print("\n=== Email Settings Analysis ===\n")
    
    issues = []
    
    # Check basic settings
    if not settings.EMAIL_HOST:
        issues.append("EMAIL_HOST is not set")
    
    if not settings.EMAIL_HOST_USER:
        issues.append("EMAIL_HOST_USER is not set")
    
    if not settings.EMAIL_HOST_PASSWORD:
        issues.append("EMAIL_HOST_PASSWORD is not set")
    
    if settings.EMAIL_PORT != 587:
        issues.append(f"EMAIL_PORT is {settings.EMAIL_PORT}, should be 587 for Gmail")
    
    if not settings.EMAIL_USE_TLS:
        issues.append("EMAIL_USE_TLS should be True for Gmail")
    
    if settings.EMAIL_BACKEND != 'django.core.mail.backends.smtp.EmailBackend':
        issues.append(f"EMAIL_BACKEND is {settings.EMAIL_BACKEND}, should be SMTP for production")
    
    if issues:
        print("❌ Issues found:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("✅ All email settings look correct")
    
    # Check password format
    password = settings.EMAIL_HOST_PASSWORD
    if len(password) == 16 and ' ' in password:
        print("✅ Gmail app password format looks correct (16 chars with spaces)")
    else:
        print("⚠️  Gmail app password format might be incorrect")
        print("   Expected: 16 characters with spaces (e.g., 'abcd efgh ijkl mnop')")
    
    return len(issues) == 0

def main():
    print("=== Tecosoft Email Verification Tool ===\n")
    
    # Check settings first
    settings_ok = check_email_settings()
    
    if not settings_ok:
        print("\n❌ Please fix email settings before testing")
        return
    
    # Test Django email
    django_ok = test_django_email()
    
    # Test raw SMTP
    smtp_ok = test_raw_smtp()
    
    print("\n=== Summary ===")
    print(f"Django Email: {'✅ Working' if django_ok else '❌ Failed'}")
    print(f"Raw SMTP: {'✅ Working' if smtp_ok else '❌ Failed'}")
    
    if django_ok and smtp_ok:
        print("\n🎉 Email functionality is working correctly!")
        print("If admin replies are not being received:")
        print("1. Check the recipient's spam/junk folder")
        print("2. Verify the recipient email address is correct")
        print("3. Check if the recipient's email provider is blocking emails")
    else:
        print("\n❌ Email functionality has issues")
        print("Common solutions:")
        print("1. Verify Gmail app password is correct")
        print("2. Ensure 2-factor authentication is enabled on Gmail")
        print("3. Check if Gmail account is locked or suspended")
        print("4. Try generating a new app password")

if __name__ == '__main__':
    main()