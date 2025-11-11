/**
 * Session Handler for Tecosoft
 * Handles session timeouts and keeps the session alive
 */

(function() {
    'use strict';
    
    // Configuration
    const SESSION_CHECK_INTERVAL = 5 * 60 * 1000; // Check every 5 minutes
    const SESSION_WARNING_TIME = 10 * 60 * 1000; // Warn 10 minutes before expiry
    const KEEP_ALIVE_INTERVAL = 15 * 60 * 1000; // Send keep-alive every 15 minutes
    
    let sessionWarningShown = false;
    let keepAliveTimer = null;
    let sessionCheckTimer = null;
    
    /**
     * Send a keep-alive request to maintain the session
     */
    function sendKeepAlive() {
        fetch('/keep-alive/', {
            method: 'GET',
            credentials: 'same-origin',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).then(response => {
            if (response.status === 401 || response.status === 403) {
                handleSessionExpired();
            } else if (response.ok) {
                console.log('Session keep-alive successful');
                sessionWarningShown = false;
                return response.json();
            }
        }).then(data => {
            if (data && data.status === 'ok') {
                console.log('User session active:', data.user);
            }
        }).catch(error => {
            console.warn('Keep-alive request failed:', error);
        });
    }
    
    /**
     * Handle session expiration
     */
    function handleSessionExpired() {
        if (sessionWarningShown) return;
        
        sessionWarningShown = true;
        
        // Show user-friendly message
        if (window.location.pathname.startsWith('/admin-')) {
            showSessionExpiredModal();
        }
    }
    
    /**
     * Show session expired modal
     */
    function showSessionExpiredModal() {
        // Create modal HTML
        const modalHTML = `
            <div class="modal fade" id="sessionExpiredModal" tabindex="-1" data-bs-backdrop="static">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header bg-warning text-dark">
                            <h5 class="modal-title">
                                <i class="fas fa-exclamation-triangle me-2"></i>Session Expired
                            </h5>
                        </div>
                        <div class="modal-body">
                            <p>Your session has expired due to inactivity.</p>
                            <p>Please log in again to continue using the admin panel.</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" onclick="window.location.href='/signin/'">
                                <i class="fas fa-sign-in-alt me-2"></i>Log In Again
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Add modal to page
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('sessionExpiredModal'));
        modal.show();
    }
    
    /**
     * Check if user is on admin pages
     */
    function isAdminPage() {
        return window.location.pathname.startsWith('/admin-');
    }
    
    /**
     * Initialize session handler
     */
    function initSessionHandler() {
        // Only run on admin pages for authenticated users
        if (!isAdminPage()) return;
        
        console.log('Session handler initialized for admin pages');
        
        // Start keep-alive timer
        keepAliveTimer = setInterval(sendKeepAlive, KEEP_ALIVE_INTERVAL);
        
        // Send initial keep-alive
        setTimeout(sendKeepAlive, 1000);
        
        // Handle page visibility changes
        document.addEventListener('visibilitychange', function() {
            if (!document.hidden && isAdminPage()) {
                // Page became visible, send keep-alive
                sendKeepAlive();
            }
        });
        
        // Handle beforeunload to clean up timers
        window.addEventListener('beforeunload', function() {
            if (keepAliveTimer) {
                clearInterval(keepAliveTimer);
            }
            if (sessionCheckTimer) {
                clearInterval(sessionCheckTimer);
            }
        });
    }
    
    /**
     * Handle AJAX errors globally
     */
    function setupGlobalErrorHandling() {
        // Intercept fetch requests
        const originalFetch = window.fetch;
        window.fetch = function(...args) {
            return originalFetch.apply(this, args).then(response => {
                if (response.status === 403 || response.status === 401) {
                    if (isAdminPage()) {
                        handleSessionExpired();
                    }
                }
                return response;
            });
        };
        
        // Handle jQuery AJAX errors if jQuery is available
        if (window.jQuery) {
            jQuery(document).ajaxError(function(event, xhr, settings) {
                if (xhr.status === 403 || xhr.status === 401) {
                    if (isAdminPage()) {
                        handleSessionExpired();
                    }
                }
            });
        }
    }
    
    /**
     * Show connection status
     */
    function showConnectionStatus() {
        // Create status indicator
        const statusHTML = `
            <div id="connectionStatus" style="
                position: fixed;
                top: 10px;
                right: 10px;
                z-index: 9999;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
                display: none;
            ">
                <i class="fas fa-wifi"></i> <span id="statusText">Connected</span>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', statusHTML);
        
        const statusEl = document.getElementById('connectionStatus');
        const statusText = document.getElementById('statusText');
        
        // Show status on admin pages
        if (isAdminPage()) {
            statusEl.style.display = 'block';
            statusEl.style.backgroundColor = '#28a745';
            statusEl.style.color = 'white';
        }
        
        // Update status based on network
        window.addEventListener('online', function() {
            statusEl.style.backgroundColor = '#28a745';
            statusText.textContent = 'Connected';
            sendKeepAlive();
        });
        
        window.addEventListener('offline', function() {
            statusEl.style.backgroundColor = '#dc3545';
            statusText.textContent = 'Offline';
        });
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initSessionHandler();
            setupGlobalErrorHandling();
            showConnectionStatus();
        });
    } else {
        initSessionHandler();
        setupGlobalErrorHandling();
        showConnectionStatus();
    }
    
})();