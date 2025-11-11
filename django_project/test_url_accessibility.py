#!/usr/bin/env python
"""
Test URL accessibility and session handling
"""
import os
import django
import requests
from urllib.parse import urljoin

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.urls import reverse
from home.urls import urlpatterns

def test_url_accessibility():
    """Test if all URLs are accessible"""
    print("=== Testing URL Accessibility ===\n")
    
    base_url = "http://localhost:8000"
    
    # Test public URLs (should work without authentication)
    public_urls = [
        ('index', 'Home Page'),
        ('about', 'About Page'),
        ('products', 'Products Page'),
        ('contact', 'Contact Page'),
        ('career', 'Career Page'),
        ('signin', 'Sign In Page'),
        ('signup', 'Sign Up Page'),
    ]
    
    print("Testing Public URLs:")
    for url_name, description in public_urls:
        try:
            url_path = reverse(url_name)
            full_url = urljoin(base_url, url_path)
            
            response = requests.get(full_url, timeout=5)
            status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
            print(f"  {description}: {url_path} - {status}")
            
        except Exception as e:
            print(f"  {description}: {url_path} - ❌ Error: {str(e)}")
    
    print("\nTesting Admin URLs (will require authentication):")
    admin_urls = [
        ('admin_dashboard', 'Admin Dashboard'),
        ('admin_contacts', 'Admin Contacts'),
        ('admin_products', 'Admin Products'),
        ('admin_applications', 'Admin Applications'),
    ]
    
    for url_name, description in admin_urls:
        try:
            url_path = reverse(url_name)
            full_url = urljoin(base_url, url_path)
            
            response = requests.get(full_url, timeout=5)
            if response.status_code == 302:
                status = "✅ Redirects (needs auth)"
            elif response.status_code == 200:
                status = "✅ OK"
            else:
                status = f"❌ {response.status_code}"
            
            print(f"  {description}: {url_path} - {status}")
            
        except Exception as e:
            print(f"  {description}: {url_path} - ❌ Error: {str(e)}")

def check_server_status():
    """Check if Django server is running"""
    print("\n=== Server Status Check ===\n")
    
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200:
            print("✅ Django server is running and accessible")
            print(f"✅ Response time: {response.elapsed.total_seconds():.2f} seconds")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server")
        print("   Make sure the server is running: python manage.py runserver")
        return False
    except requests.exceptions.Timeout:
        print("❌ Server response timeout")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def show_all_urls():
    """Show all available URLs"""
    print("\n=== All Available URLs ===\n")
    
    for pattern in urlpatterns:
        try:
            url_name = pattern.name
            if url_name:
                url_path = reverse(url_name)
                print(f"  {url_name}: {url_path}")
        except:
            pass

def main():
    print("=== Tecosoft URL Accessibility Test ===\n")
    
    # Check if server is running
    if not check_server_status():
        return
    
    # Show all URLs
    show_all_urls()
    
    # Test URL accessibility
    test_url_accessibility()
    
    print("\n=== Troubleshooting Tips ===")
    print("If you're getting 'not found' errors:")
    print("1. Check if the Django server is still running")
    print("2. Clear your browser cache and cookies")
    print("3. Try logging out and logging back in")
    print("4. Check the Django server console for error messages")
    print("5. Restart the Django server if needed")
    
    print("\n=== Session Settings ===")
    from django.conf import settings
    print(f"SESSION_COOKIE_AGE: {settings.SESSION_COOKIE_AGE} seconds ({settings.SESSION_COOKIE_AGE/3600:.1f} hours)")
    print(f"SESSION_EXPIRE_AT_BROWSER_CLOSE: {settings.SESSION_EXPIRE_AT_BROWSER_CLOSE}")
    print(f"SESSION_SAVE_EVERY_REQUEST: {getattr(settings, 'SESSION_SAVE_EVERY_REQUEST', False)}")

if __name__ == '__main__':
    main()