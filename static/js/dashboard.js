// Dashboard specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Handle enrollment button clicks
    const enrollButtons = document.querySelectorAll('.enroll-btn');
    
    enrollButtons.forEach(button => {
        button.addEventListener('click', function() {
            const courseTitle = this.parentElement.querySelector('h3').textContent;
            
            // Change button text and style
            this.textContent = 'Enrolled!';
            this.classList.add('enrolled');
            this.disabled = true;
            
            // Show enrollment confirmation
            const notification = document.createElement('div');
            notification.classList.add('notification');
            notification.innerHTML = `<p>You've successfully enrolled in "${courseTitle}"</p>`;
            document.body.appendChild(notification);
            
            // Remove notification after 3 seconds
            setTimeout(() => {
                notification.classList.add('fade-out');
                setTimeout(() => {
                    notification.remove();
                }, 500);
            }, 3000);
            
            // In a real application, this would send an AJAX request to the server
            console.log(`Enrolled in: ${courseTitle}`);
        });
    });
    
    // Add CSS for notifications and enrolled button state
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #2ecc71;
            color: white;
            padding: 15px 25px;
            border-radius: 5px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
            z-index: 1000;
            animation: slide-in 0.5s ease-out;
        }
        
        @keyframes slide-in {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .fade-out {
            animation: fade-out 0.5s ease-out;
        }
        
        @keyframes fade-out {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        
        .enrolled {
            background-color: #95a5a6 !important;
            cursor: default !important;
        }
    `;
    document.head.appendChild(style);
});