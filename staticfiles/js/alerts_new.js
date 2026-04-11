// Wait for SweetAlert2 and DOM to be ready
function initializeAlerts() {
    // Check if Swal exists
    if (typeof Swal === 'undefined') {
        console.error('SweetAlert2 not loaded');
        setTimeout(initializeAlerts, 500);
        return;
    }

    console.log('✅ Alerts initialized with SweetAlert2');

    window.showSuccess = (title = 'Success!', text = '') => {
        Swal.fire({
            title: title,
            html: text,
            icon: 'success',
            confirmButtonText: 'OK',
            confirmButtonColor: '#10b981',
            timer: 4000,
            timerProgressBar: true,
            buttonsStyling: true,
        });
    };

    window.showError = (title = 'Error!', text = 'Something went wrong') => {
        Swal.fire({
            title: title,
            text: text,
            icon: 'error',
            confirmButtonText: 'OK',
            confirmButtonColor: '#ef4444',
            buttonsStyling: true,
        });
    };

    window.showWarning = (title = 'Warning!', text = '') => {
        Swal.fire({
            title: title,
            text: text,
            icon: 'warning',
            confirmButtonText: 'OK',
            confirmButtonColor: '#f59e0b',
            buttonsStyling: true,
        });
    };

    window.showInfo = (title = 'Info', text = '') => {
        Swal.fire({
            title: title,
            text: text,
            icon: 'info',
            confirmButtonText: 'OK',
            confirmButtonColor: '#3b82f6',
            buttonsStyling: true,
        });
    };

    window.showConfirm = (title = 'Are you sure?', text = '', callback) => {
        Swal.fire({
            title: title,
            text: text,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#ef4444',
            cancelButtonColor: '#6b7280',
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'Cancel',
            buttonsStyling: true,
        }).then((result) => {
            if (callback) callback(result.isConfirmed);
        });
    };

    window.showDeleteConfirm = (title = 'Delete?', text = 'This action cannot be undone!', callback) => {
        Swal.fire({
            title: title,
            text: text,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#dc2626',
            cancelButtonColor: '#6b7280',
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'Cancel',
            buttonsStyling: true,
        }).then((result) => {
            if (callback) callback(result.isConfirmed);
        });
    };

    window.showLoading = (title = 'Loading...', text = 'Please wait') => {
        Swal.fire({
            title: title,
            text: text,
            icon: 'info',
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });
    };

    window.closeAlert = () => {
        Swal.close();
    };

    window.showLoginAlert = (userName, loginTime, loginDate) => {
        Swal.fire({
            title: '✅ Login Successful!',
            html: `
                <div class="text-left">
                    <p class="text-lg font-semibold text-gray-800 mb-3">${userName}</p>
                    <div class="bg-blue-50 p-4 rounded-lg space-y-2">
                        <p><i class="fas fa-clock text-blue-600 mr-2"></i><strong>Login Time:</strong> ${loginTime}</p>
                        <p><i class="fas fa-calendar text-blue-600 mr-2"></i><strong>Date:</strong> ${loginDate}</p>
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
        });
    };

    window.showLogoutAlert = (userName, logoutTime, sessionDuration) => {
        Swal.fire({
            title: '👋 Logged Out',
            html: `
                <div class="text-left">
                    <p class="text-lg font-semibold text-gray-800 mb-3">Goodbye, ${userName}!</p>
                    <div class="bg-amber-50 p-4 rounded-lg space-y-2">
                        <p><i class="fas fa-sign-out-alt text-amber-600 mr-2"></i><strong>Logout Time:</strong> ${logoutTime}</p>
                        <p><i class="fas fa-hourglass-end text-amber-600 mr-2"></i><strong>Session Duration:</strong> ${sessionDuration}</p>
                    </div>
                    <p class="text-gray-600 text-sm mt-3"><i class="fas fa-info-circle mr-1"></i> Thank you for using our system!</p>
                </div>
            `,
            icon: 'info',
            confirmButtonColor: '#3b82f6',
            confirmButtonText: 'Back to Login',
            timer: 5000,
            timerProgressBar: true,
            buttonsStyling: true,
            allowOutsideClick: false,
        });
    };

    window.confirmSubmit = (formId, message = 'Are you sure you want to submit this form?') => {
        Swal.fire({
            title: 'Confirm Action',
            text: message,
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3b82f6',
            cancelButtonColor: '#6b7280',
            confirmButtonText: 'Yes, submit!',
            cancelButtonText: 'Cancel',
            buttonsStyling: true,
        }).then((result) => {
            if (result.isConfirmed) {
                document.getElementById(formId).submit();
            }
        });
    };

    // Handle Django Messages Framework
    const messages = document.querySelectorAll('[data-message]');
    
    if (messages.length > 0) {
        console.log('📨 Found', messages.length, 'message(s)');
        
        messages.forEach(function(message) {
            const text = message.getAttribute('data-message');
            const tags = message.getAttribute('data-tags') || 'info';
            
            console.log('Message text:', text);
            console.log('Message tags:', tags);
            
            // Check if this is a login message
            if (text.includes('Welcome back') || text.includes('Login time')) {
                const timeMatch = text.match(/Login time: (\d{1,2}:\d{2} (?:AM|PM))/);
                const dateMatch = text.match(/on ([^!]+)!/);
                const userMatch = text.match(/Welcome back, ([^!]+)!/);
                
                const loginTime = timeMatch ? timeMatch[1] : 'Unknown';
                const loginDate = dateMatch ? dateMatch[1] : 'Today';
                const userName = userMatch ? userMatch[1] : 'User';
                
                console.log('🔐 Showing login alert');
                showLoginAlert(userName, loginTime, loginDate);
            }
            // Check if this is a logout message
            else if (text.includes('Goodbye') || text.includes('Logout time')) {
                const userMatch = text.match(/Goodbye ([^!]+)!/);
                const timeMatch = text.match(/Logout time: (\d{1,2}:\d{2} (?:AM|PM))/);
                const durationMatch = text.match(/Session duration: ([^$]+)/);
                
                const userName = userMatch ? userMatch[1] : 'User';
                const logoutTime = timeMatch ? timeMatch[1] : 'Unknown';
                const sessionDuration = durationMatch ? durationMatch[1] : 'N/A';
                
                console.log('🚪 Showing logout alert');
                showLogoutAlert(userName, logoutTime, sessionDuration);
            }
            else if (tags.includes('success')) {
                showSuccess('Success!', text);
            } else if (tags.includes('error')) {
                showError('Error!', text);
            } else if (tags.includes('warning')) {
                showWarning('Warning!', text);
            } else if (tags.includes('info')) {
                showInfo('Info', text);
            }
        });
    }
}

// Initialize alerts when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeAlerts);
} else {
    initializeAlerts();
}
