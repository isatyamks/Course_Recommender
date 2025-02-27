// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Form validation for signup
    const signupForm = document.querySelector('form[action="/signup"]');
    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            const linkedin = document.getElementById('linkedin').value.trim();
            const github = document.getElementById('github').value.trim();
            
            if (!linkedin || !github) {
                event.preventDefault();
                alert('LinkedIn and GitHub usernames are required!');
            }
        });
    }
    
    // Animation for course cards
    const courseCards = document.querySelectorAll('.course-card');
    if (courseCards.length > 0) {
        // Add a slight delay to each card for a staggered animation effect
        courseCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100 * index);
        });
    }
    
    // Add active class to current nav item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav ul li a');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentPath) {
            link.classList.add('active');
        }
    });
});