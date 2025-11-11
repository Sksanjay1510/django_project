#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    
    from django.core.management import execute_from_command_line
    
    # Default port
    port = '8080'  # Change this to your desired port
    
    # Check if port is provided as argument
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = sys.argv[1]
    
    # Run server
    execute_from_command_line(['manage.py', 'runserver', f'0.0.0.0:{port}'])