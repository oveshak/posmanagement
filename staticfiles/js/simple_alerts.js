// Simple, Direct Alert System
console.log('🚀 Starting simple alerts system...');

// Wait for SweetAlert2 to load
let maxRetries = 10;
let retryCount = 0;

function waitForSwal() {
    retryCount++;
    if (typeof Swal === 'undefined') {
        if (retryCount < maxRetries) {
            console.log(`⏳ Waiting for SweetAlert2... (${retryCount}/${maxRetries})`);
            setTimeout(waitForSwal, 100);
        } else {
            console.error('❌ SweetAlert2 failed to load after', maxRetries, 'retries');
        }
        return;
    }

    console.log('✅ SweetAlert2 loaded successfully!');
    setupAlerts();
}

function setupAlerts() {
    // Make functions globally available
    window.showLoginAlert = function(userName, loginTime, loginDate) {
        console.log('🔐 Showing login alert...');
        Swal.fire({
            title: '✅ Login Successful!',
            html: `
                <div style="text-align: left; font-family: Arial, sans-serif;">
                    <p style="font-size: 18px; font-weight: bold; color: #1f2937; margin-bottom: 15px;">${userName}</p>
                    <div style="background: #dbeafe; padding: 16px; border-radius: 8px; margin: 10px 0;">
                        <p style="margin: 8px 0;"><i class="fas fa-clock" style="color: #2563eb; margin-right: 8px;"></i><strong>Login Time:</strong> ${loginTime}</p>
                        <p style="margin: 8px 0;"><i class="fas fa-calendar" style="color: #2563eb; margin-right: 8px;"></i><strong>Date:</strong> ${loginDate}</p>
                    </div>
                </div>
            `,
            icon: 'success',
            confirmButtonColor: '#10b981',
            confirmButtonText: 'Continue',
            timer: 4000,
            timerProgressBar: true,
            buttonsStyling: true,
            allowOutsideClick: false,
            didOpen: function() {
                console.log('✓ Login alert displayed');
            }
        });
    };

    window.showLogoutAlert = function(userName, logoutTime, sessionDuration) {
        console.log('🚪 Showing logout alert...');
        Swal.fire({
            title: '👋 Logged Out',
            html: `
                <div style="text-align: left; font-family: Arial, sans-serif;">
                    <p style="font-size: 18px; font-weight: bold; color: #1f2937; margin-bottom: 15px;">Goodbye, ${userName}!</p>
                    <div style="background: #fef3c7; padding: 16px; border-radius: 8px; margin: 10px 0;">
                        <p style="margin: 8px 0;"><i class="fas fa-sign-out-alt" style="color: #b45309; margin-right: 8px;"></i><strong>Logout Time:</strong> ${logoutTime}</p>
                        <p style="margin: 8px 0;"><i class="fas fa-hourglass-end" style="color: #b45309; margin-right: 8px;"></i><strong>Session Duration:</strong> ${sessionDuration}</p>
                    </div>
                    <p style="color: #4b5563; font-size: 12px; margin-top: 12px;"><i class="fas fa-info-circle" style="margin-right: 4px;"></i>Thank you for using our system!</p>
                </div>
            `,
            icon: 'info',
            confirmButtonColor: '#3b82f6',
            confirmButtonText: 'Back to Login',
            timer: 5000,
            timerProgressBar: true,
            buttonsStyling: true,
            allowOutsideClick: false,
            didOpen: function() {
                console.log('✓ Logout alert displayed');
            }
        });
    };

    window.showSuccess = function(title = 'Success!', message = '') {
        Swal.fire({
            icon: 'success',
            title: title,
            html: message,
            timer: 3000,
            timerProgressBar: true,
            buttonsStyling: true,
        });
    };

    window.showError = function(title = 'Error!', message = '') {
        Swal.fire({
            icon: 'error',
            title: title,
            html: message,
            buttonsStyling: true,
        });
    };

    window.showInfo = function(title = 'Info', message = '') {
        Swal.fire({
            icon: 'info',
            title: title,
            html: message,
            buttonsStyling: true,
        });
    };

    // Check for login/logout alerts in page data
    checkForAlerts();
}

function checkForAlerts() {
    // Look for alert data in meta tags or data attributes
    const loginData = document.querySelector('[data-login-alert]');
    const logoutData = document.querySelector('[data-logout-alert]');

    if (loginData) {
        const userName = loginData.getAttribute('data-user-name');
        const loginTime = loginData.getAttribute('data-login-time');
        const loginDate = loginData.getAttribute('data-login-date');
        
        console.log('🔐 Found login data:', { userName, loginTime, loginDate });
        if (window.showLoginAlert) {
            setTimeout(() => {
                window.showLoginAlert(userName, loginTime, loginDate);
            }, 500);
        }
    }

    if (logoutData) {
        const userName = logoutData.getAttribute('data-user-name');
        const logoutTime = logoutData.getAttribute('data-logout-time');
        const sessionDuration = logoutData.getAttribute('data-session-duration');
        
        console.log('🚪 Found logout data:', { userName, logoutTime, sessionDuration });
        if (window.showLogoutAlert) {
            setTimeout(() => {
                window.showLogoutAlert(userName, logoutTime, sessionDuration);
            }, 500);
        }
    }
}

// Start when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', waitForSwal);
} else {
    waitForSwal();
}

console.log('✓ Simple alerts system ready');
