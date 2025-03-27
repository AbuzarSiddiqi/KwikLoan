// Common animations and functionalities for all pages

document.addEventListener('DOMContentLoaded', () => {
    // Initialize GSAP and ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);
    
    // Navbar animations
    gsap.from('.navbar', {
        duration: 0.8,
        y: -50,
        opacity: 0,
        ease: 'power3.out'
    });
    
    // Page transitions
    const links = document.querySelectorAll('a:not([target="_blank"])');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // Skip for hash links and links with prevent-transition class
            if (this.getAttribute('href').startsWith('#') || 
                this.classList.contains('prevent-transition')) {
                return;
            }
            
            e.preventDefault();
            const href = this.getAttribute('href');
            
            // Animate content out
            gsap.to('main', {
                opacity: 0,
                y: 20,
                duration: 0.3,
                onComplete: () => {
                    window.location.href = href;
                }
            });
        });
    });
    
    // Fade in content on page load
    gsap.from('main', {
        opacity: 0,
        y: 20,
        duration: 0.5,
        delay: 0.1
    });
    
    // Input field animations on focus
    const formControls = document.querySelectorAll('.form-control, .form-select');
    
    formControls.forEach(input => {
        input.addEventListener('focus', function() {
            gsap.to(this, {
                scale: 1.02,
                duration: 0.2,
                ease: 'power1.out'
            });
        });
        
        input.addEventListener('blur', function() {
            gsap.to(this, {
                scale: 1,
                duration: 0.2,
                ease: 'power1.out'
            });
        });
    });
    
    // Animate buttons on hover
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            if (!this.hasAttribute('disabled')) {
                gsap.to(this, {
                    y: -3,
                    duration: 0.2,
                    ease: 'power1.out'
                });
            }
        });
        
        button.addEventListener('mouseleave', function() {
            if (!this.hasAttribute('disabled')) {
                gsap.to(this, {
                    y: 0,
                    duration: 0.2,
                    ease: 'power1.out'
                });
            }
        });
    });
});

// Animations and interactive elements for the futuristic UI

document.addEventListener('DOMContentLoaded', function() {
  // Animate elements with fade-in class
  const fadeElements = document.querySelectorAll('.fade-in');
  fadeElements.forEach((el, index) => {
    el.style.animationDelay = `${index * 0.1}s`;
  });

  // Animate probability bar on result page
  const probabilityBar = document.querySelector('.probability-fill');
  if (probabilityBar) {
    const probabilityValue = parseFloat(probabilityBar.getAttribute('data-value'));
    setTimeout(() => {
      probabilityBar.style.width = `${probabilityValue}%`;
    }, 300);
  }

  // Parallax effect for hero section
  const hero = document.querySelector('.hero');
  if (hero) {
    document.addEventListener('mousemove', (e) => {
      const x = e.clientX / window.innerWidth;
      const y = e.clientY / window.innerHeight;
      
      hero.querySelectorAll('.parallax').forEach(el => {
        const speed = parseFloat(el.getAttribute('data-speed'));
        const moveX = (x - 0.5) * speed * 50;
        const moveY = (y - 0.5) * speed * 50;
        
        el.style.transform = `translate(${moveX}px, ${moveY}px)`;
      });
    });
  }

  // Floating animation for cards
  const floatingCards = document.querySelectorAll('.bank-card');
  floatingCards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.2}s`;
  });

  // Form validation with visual feedback
  const predictionForm = document.getElementById('prediction-form');
  if (predictionForm) {
    predictionForm.addEventListener('submit', function(e) {
      const formInputs = this.querySelectorAll('input, select');
      let isValid = true;
      
      formInputs.forEach(input => {
        if (!input.value) {
          isValid = false;
          input.classList.add('error');
          const errorMsg = document.createElement('div');
          errorMsg.className = 'error-message';
          errorMsg.textContent = 'This field is required';
          
          if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('error-message')) {
            input.insertAdjacentElement('afterend', errorMsg);
          }
        } else {
          input.classList.remove('error');
          if (input.nextElementSibling && input.nextElementSibling.classList.contains('error-message')) {
            input.nextElementSibling.remove();
          }
        }
      });
      
      if (!isValid) {
        e.preventDefault();
      } else {
        // Add loading animation
        const submitBtn = this.querySelector('button[type="submit"]');
        submitBtn.innerHTML = '<span class="loader"></span> Processing...';
        submitBtn.disabled = true;
      }
    });

    // Real-time validation
    formInputs.forEach(input => {
      input.addEventListener('input', function() {
        if (this.value) {
          this.classList.remove('error');
          if (this.nextElementSibling && this.nextElementSibling.classList.contains('error-message')) {
            this.nextElementSibling.remove();
          }
        }
      });
    });
  }

  // Animate numbers counting up
  const animateCounters = document.querySelectorAll('.animate-counter');
  animateCounters.forEach(counter => {
    const target = parseInt(counter.getAttribute('data-target'));
    const duration = 1500; // ms
    const step = Math.max(1, Math.ceil(target / (duration / 16))); // 60fps approx
    
    let current = 0;
    const counterInterval = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(counterInterval);
      }
      counter.textContent = current;
    }, 16);
  });
});

// Enhanced form interactions
document.addEventListener('DOMContentLoaded', function() {
  // Add special effects for select elements
  const selectElements = document.querySelectorAll('select.glass-select');
  
  selectElements.forEach(select => {
    // Add focus effect
    select.addEventListener('focus', function() {
      this.parentElement.classList.add('select-focus');
      gsap.to(this, {
        borderColor: '#00d4ff',
        boxShadow: '0 0 15px rgba(0, 212, 255, 0.3), 0 0 30px rgba(0, 212, 255, 0.1)',
        duration: 0.3
      });
    });
    
    // Remove focus effect
    select.addEventListener('blur', function() {
      this.parentElement.classList.remove('select-focus');
      gsap.to(this, {
        borderColor: 'rgba(0, 212, 255, 0.15)',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        duration: 0.3
      });
    });
    
    // Add change animation
    select.addEventListener('change', function() {
      if (this.value) {
        gsap.fromTo(this, 
          { backgroundColor: 'rgba(0, 212, 255, 0.1)' },
          { backgroundColor: 'rgba(255, 255, 255, 0.05)', duration: 0.5, ease: 'power2.out' }
        );
      }
    });
  });
  
  // Add special effects for input elements
  const inputElements = document.querySelectorAll('input.glass-input');
  
  inputElements.forEach(input => {
    // Add focus effect
    input.addEventListener('focus', function() {
      gsap.to(this, {
        borderColor: '#00d4ff',
        boxShadow: '0 0 15px rgba(0, 212, 255, 0.3), 0 0 30px rgba(0, 212, 255, 0.1)',
        duration: 0.3
      });
    });
    
    // Remove focus effect
    input.addEventListener('blur', function() {
      gsap.to(this, {
        borderColor: this.value ? 'rgba(0, 212, 255, 0.3)' : 'rgba(0, 212, 255, 0.15)',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        duration: 0.3
      });
    });
  });
});

// Intersection Observer for scroll animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animated');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.addEventListener('DOMContentLoaded', () => {
  const elements = document.querySelectorAll('.scroll-animation');
  elements.forEach(el => {
    observer.observe(el);
  });
});
