#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from home.models import SiteSettings

def test_settings():
    print("=== Testing SiteSettings ===")
    
    # Get or create settings
    settings = SiteSettings.get_settings()
    print(f"Current settings ID: {settings.id}")
    print(f"Current site name: {settings.site_name}")
    print(f"Current contact email: {settings.contact_email}")
    
    # Test updating
    print("\n=== Testing Update ===")
    original_name = settings.site_name
    settings.site_name = "Test Updated Name"
    settings.contact_email = "test@example.com"
    
    try:
        settings.save()
        print("✓ Settings saved successfully")
        
        # Reload from database
        settings.refresh_from_db()
        print(f"✓ Updated site name: {settings.site_name}")
        print(f"✓ Updated contact email: {settings.contact_email}")
        
        # Restore original
        settings.site_name = original_name
        settings.contact_email = "info@tecosoft.com"
        settings.save()
        print("✓ Settings restored")
        
    except Exception as e:
        print(f"✗ Error saving settings: {e}")
    
    print("\n=== Settings Test Complete ===")

if __name__ == '__main__':
    test_settings()