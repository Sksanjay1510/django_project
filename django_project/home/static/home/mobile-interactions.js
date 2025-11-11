/* Mobile Interactions and Device Compatibility JavaScript */
/* Ensures proper functionality across all devices and screen sizes */

(function() {
    'use strict';
    
    // ===== DEVICE DETECTION =====
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    const isTablet = /iPad|Android/i.test(navigator.userAgent) && window.innerWidth >= 768;
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    
    // ===== MOBILE MENU FUNCTIONALITY =====
    document.addEventListener('DOMContentLoaded', function() {
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        // Ensure mobile menu works properly
        if (navbarToggler && navbarCollapse) {
            navbarToggler.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Toggle the collapse class
                navbarCollapse.classList.toggle('show');
                
                // Update aria attributes
                const isExpanded = navbarCollapse.classList.contains('show');
                navbarToggler.setAttribute('aria-expanded', isExpanded);
                
                // Add/remove body scroll lock on mobile
                if (isMobile) {
                    if (isExpanded) {
                        document.body.style.overflow = 'hidden';
                    } else {
                        document.body.style.overflow = '';
                    }
                }
            });
        }
        
        // Close mobile menu when clicking nav links
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 768) {
                    navbarCollapse.classList.remove('show');
                    navbarToggler.setAttribute('aria-expanded', 'false');
                    document.body.style.overflow = '';
                }
            });
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (window.innerWidth < 768) {
                const isClickInsideNav = navbarCollapse.contains(e.target) || navbarToggler.contains(e.target);
                
                if (!isClickInsideNav && navbarCollapse.classList.contains('show')) {
                    navbarCollapse.classList.remove('show');
                    navbarToggler.setAttribute('aria-expanded', 'false');
                    document.body.style.overflow = '';
                }
            }
        });
        
        // Handle window resize
        window.addEventListener('resize', function() {
            if (window.innerWidth >= 768) {
                navbarCollapse.classList.remove('show');
                navbarToggler.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }
        });
    });
    
    // ===== TOUCH OPTIMIZATIONS =====
    if (isTouchDevice) {
        // Add touch-friendly classes
        document.body.classList.add('touch-device');
        
        // Improve button touch targets
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.style.minHeight = '44px';
            btn.style.minWidth = '44px';
        });
        
        // Add touch feedback
        document.addEventListener('touchstart', function(e) {
            if (e.target.classList.contains('btn') || e.target.classList.contains('nav-link')) {
                e.target.style.transform = 'scale(0.95)';
            }
        });
        
        document.addEventListener('touchend', function(e) {
            if (e.target.classList.contains('btn') || e.target.classList.contains('nav-link')) {
                setTimeout(() => {
                    e.target.style.transform = '';
                }, 150);
            }
        });
    }
    
    // ===== MOBILE FORM OPTIMIZATIONS =====
    const formInputs = document.querySelectorAll('input, textarea, select');
    formInputs.forEach(input => {
        // Prevent zoom on iOS when focusing inputs
        if (isMobile) {
            input.style.fontSize = '16px';
        }
        
        // Add touch-friendly styling
        input.addEventListener('focus', function() {
            this.style.borderColor = '#3b82f6';
            this.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
        });
        
        input.addEventListener('blur', function() {
            this.style.borderColor = '';
            this.style.boxShadow = '';
        });
    });
    
    // ===== MOBILE TABLE OPTIMIZATIONS =====
    const tables = document.querySelectorAll('.table-responsive');
    tables.forEach(table => {
        if (isMobile) {
            // Add swipe indicator for mobile tables
            const indicator = document.createElement('div');
            indicator.innerHTML = '<small class="text-muted"><i class="fas fa-arrows-alt-h"></i> Swipe to see more</small>';
            indicator.style.textAlign = 'center';
            indicator.style.padding = '0.5rem';
            indicator.style.backgroundColor = '#f8fafc';
            indicator.style.borderRadius = '0 0 8px 8px';
            table.appendChild(indicator);
        }
    });
    
    // ===== PERFORMANCE OPTIMIZATIONS =====
    
    // Debounce scroll events
    let scrollTimeout;
    window.addEventListener('scroll', function() {
        if (scrollTimeout) {
            clearTimeout(scrollTimeout);
        }
        scrollTimeout = setTimeout(function() {
            // Handle scroll events here
            const navbar = document.querySelector('.navbar');
            if (navbar) {
                if (window.scrollY > 50) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            }
        }, 10);
    });
    
    // Optimize animations for mobile
    if (isMobile) {
        // Reduce animation duration on mobile
        const style = document.createElement('style');
        style.textContent = `
            * {
                animation-duration: 0.3s !important;
                transition-duration: 0.3s !important;
            }
        `;
        document.head.appendChild(style);
    }
    
    // ===== ACCESSIBILITY IMPROVEMENTS =====
    
    // Add keyboard navigation support
    document.addEventListener('keydown', function(e) {
        // Close mobile menu with Escape key
        if (e.key === 'Escape') {
            const navbarCollapse = document.querySelector('.navbar-collapse');
            const navbarToggler = document.querySelector('.navbar-toggler');
            
            if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                navbarCollapse.classList.remove('show');
                navbarToggler.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
                navbarToggler.focus();
            }
        }
    });
    
    // Improve focus management
    const focusableElements = document.querySelectorAll('a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])');
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.style.outline = '2px solid #3b82f6';
            this.style.outlineOffset = '2px';
        });
        
        element.addEventListener('blur', function() {
            this.style.outline = '';
            this.style.outlineOffset = '';
        });
    });
    
    console.log('Mobile interactions initialized successfully');
    console.log('Device info:', {
        isMobile: isMobile,
        isTablet: isTablet,
        isTouchDevice: isTouchDevice,
        screenWidth: window.innerWidth,
        screenHeight: window.innerHeight
    });
    
})();