#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth import authenticate
from home.models import User

def test_authentication():
    print("=== Authentication Test ===")
    
    # Get all users
    users = User.objects.all()
    print(f"Total users in database: {users.count()}")
    
    for user in users:
        print(f"\nUser: {user.username}")
        print(f"Email: {user.email}")
        print(f"Is Staff: {user.is_staff}")
        print(f"Is Active: {user.is_active}")
        print(f"Has usable password: {user.has_usable_password()}")
        
        # Test common passwords
        test_passwords = ['admin123', 'password', 'admin', '123456', 'tecosoft']
        
        for pwd in test_passwords:
            if user.check_password(pwd):
                print(f"✓ Password '{pwd}' works for {user.username}")
                
                # Test authentication
                auth_user = authenticate(username=user.username, password=pwd)
                if auth_user:
                    print(f"✓ Authentication successful for {user.username} with password '{pwd}'")
                else:
                    print(f"✗ Authentication FAILED for {user.username} with password '{pwd}'")
                break
        else:
            print(f"✗ None of the test passwords work for {user.username}")
            print("  You may need to reset the password")

if __name__ == "__main__":
    test_authentication()