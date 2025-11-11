"""
Custom middleware for Tecosoft application
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.http import Http404
import logging

logger = logging.getLogger(__name__)

class SessionTimeoutMiddleware:
    """
    Middleware to handle session timeouts gracefully
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """Handle exceptions gracefully"""
        if isinstance(exception, Http404):
            # Log the 404 error for debugging
            logger.warning(f"404 Error: {request.path} - User: {request.user}")
            
            # If user is trying to access admin pages but not authenticated
            if request.path.startswith('/admin-') and not request.user.is_authenticated:
                messages.warning(request, 'Your session has expired. Please log in again.')
                return redirect('signin')
            
            # If user is trying to access admin pages but not staff
            if request.path.startswith('/admin-') and request.user.is_authenticated and not request.user.is_staff:
                messages.error(request, 'You do not have permission to access the admin panel.')
                return redirect('index')
        
        return None

class ErrorHandlingMiddleware:
    """
    Middleware to provide better error handling and user feedback
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            
            # Handle 404 responses
            if response.status_code == 404:
                logger.warning(f"404 Response: {request.path} - User: {request.user}")
                
                # Check if it's an admin page
                if request.path.startswith('/admin-'):
                    if not request.user.is_authenticated:
                        messages.warning(request, 'Your session has expired. Please log in again.')
                        return redirect('signin')
                    elif not request.user.is_staff:
                        messages.error(request, 'Access denied. Admin privileges required.')
                        return redirect('index')
            
            return response
            
        except Exception as e:
            logger.error(f"Unexpected error in middleware: {str(e)} - Path: {request.path}")
            return None

class KeepAliveMiddleware:
    """
    Middleware to keep sessions alive and prevent timeouts during active use
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Refresh session for authenticated users
        if request.user.is_authenticated:
            request.session.modified = True
        
        response = self.get_response(request)
        return response