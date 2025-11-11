#!/usr/bin/env python
"""
Test user management functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth import get_user_model
from home.models import User

def test_user_management():
    """Test user management operations"""
    print("=== Testing User Management Functionality ===\n")
    
    # Get current user count
    initial_count = User.objects.count()
    print(f"Initial user count: {initial_count}")
    
    # Create a test user for deletion
    test_username = "test_delete_user"
    test_email = "test_delete@example.com"
    
    # Check if test user already exists
    if User.objects.filter(username=test_username).exists():
        print(f"Test user '{test_username}' already exists, deleting first...")
        User.objects.filter(username=test_username).delete()
    
    # Create test user
    try:
        test_user = User.objects.create_user(
            username=test_username,
            email=test_email,
            password="testpassword123",
            first_name="Test",
            last_name="User"
        )
        print(f"✅ Created test user: {test_user.username} ({test_user.email})")
        
        # Verify user was created
        new_count = User.objects.count()
        print(f"✅ User count after creation: {new_count}")
        
        # Test user deletion
        user_id = test_user.id
        test_user.delete()
        print(f"✅ Deleted test user with ID: {user_id}")
        
        # Verify user was deleted
        final_count = User.objects.count()
        print(f"✅ User count after deletion: {final_count}")
        
        if final_count == initial_count:
            print("✅ User deletion test PASSED")
        else:
            print("❌ User deletion test FAILED")
            
    except Exception as e:
        print(f"❌ Error during user management test: {str(e)}")

def show_user_statistics():
    """Show current user statistics"""
    print("\n=== Current User Statistics ===")
    
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    superusers = User.objects.filter(is_superuser=True).count()
    
    print(f"Total Users: {total_users}")
    print(f"Active Users: {active_users}")
    print(f"Staff Users: {staff_users}")
    print(f"Superusers: {superusers}")
    
    # Show recent users
    recent_users = User.objects.order_by('-date_joined')[:5]
    if recent_users:
        print("\nRecent Users:")
        for user in recent_users:
            status = "Active" if user.is_active else "Inactive"
            role = "Staff" if user.is_staff else "Regular"
            if user.is_superuser:
                role = "Superuser"
            print(f"  - {user.username} ({user.email}) - {status} {role}")

def check_protected_users():
    """Check which users are protected from deletion"""
    print("\n=== Protected Users (Cannot be deleted) ===")
    
    superusers = User.objects.filter(is_superuser=True)
    if superusers:
        print("Superusers:")
        for user in superusers:
            print(f"  - {user.username} ({user.email})")
    else:
        print("No superusers found")
    
    print("\nNote: Users cannot delete their own accounts")

def main():
    print("=== Tecosoft User Management Test ===\n")
    
    show_user_statistics()
    check_protected_users()
    test_user_management()
    
    print("\n=== User Deletion Instructions ===")
    print("1. Go to Admin Panel → Users: http://localhost:8000/admin-users/")
    print("2. Find the user you want to delete")
    print("3. Click the red trash icon in the Actions column")
    print("4. Confirm the deletion in the popup dialog")
    print("5. The user will be permanently removed from the system")
    
    print("\n=== Important Notes ===")
    print("- Superusers cannot be deleted (protected)")
    print("- You cannot delete your own account")
    print("- Deletion is permanent and cannot be undone")
    print("- Consider deactivating users instead of deleting them")
    print("- Use the pause/play button to activate/deactivate users")

if __name__ == '__main__':
    main()