// Global variables
let currentDataset = null;
let currentModel = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initParticles();
    initPageNavigation();
    initThemeToggle();
    initMobileMenu();
    initSmoothScrolling();
    showLanding();
});

// Initialize particles background
function initParticles() {
    if (typeof particlesJS !== 'undefined') {
        particlesJS('particles-js', {
            particles: {
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: '#00c8ff' },
                shape: { type: 'circle' },
                opacity: { value: 0.5, random: false },
                size: { value: 3, random: true },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: '#00c8ff',
                    opacity: 0.4,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 6,
                    direction: 'none',
                    random: false,
                    straight: false,
                    out_mode: 'out',
                    bounce: false
                }
            },
            interactivity: {
                detect_on: 'canvas',
                events: {
                    onhover: { enable: true, mode: 'repulse' },
                    onclick: { enable: true, mode: 'push' },
                    resize: true
                }
            },
            retina_detect: true
        });
    }
}

// Initialize page navigation
function initPageNavigation() {
    // Get navigation buttons
    const startBuildingBtn = document.getElementById('startBuildingBtn');
    const getStartedBtn = document.getElementById('getStartedBtn');
    const ctaGetStartedBtn = document.getElementById('ctaGetStartedBtn');

    // Add event listeners to all navigation buttons
    const navButtons = [startBuildingBtn, getStartedBtn, ctaGetStartedBtn];
    navButtons.forEach((btn) => {
        if (btn) {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                showPlatform();
            });
        }
    });
}

// Show platform (embedded Streamlit app)
function showPlatform() {
    const landingPage = document.getElementById('landingPage');
    
    // Hide landing page
    landingPage.style.display = 'none';
    
    // Create or show embedded Streamlit section
    let streamlitSection = document.getElementById('streamlitSection');
    if (!streamlitSection) {
        streamlitSection = document.createElement('div');
        streamlitSection.id = 'streamlitSection';
        streamlitSection.className = 'page';
        streamlitSection.innerHTML = `
            <div class="platform-container">
                <div class="platform-section">
                    <div class="section-header">
                        <button onclick="showLanding()" class="btn btn-outline">
                            <i class="fas fa-arrow-left"></i> Back to Home
                        </button>
                        <h2>AutoML Platform</h2>
                        <p>Build your machine learning models with our no-code interface</p>
                    </div>
                    <div id="loadingIndicator" style="text-align: center; padding: 2rem;">
                        <i class="fas fa-spinner fa-spin" style="font-size: 2rem; color: var(--primary);"></i>
                        <p>Loading AutoML Platform...</p>
                    </div>
                    <iframe 
                        src="https://zero-code-automl.streamlit.app/?embedded=true"
                        style="width: 100%; height: 800px; border: none; border-radius: 16px; display: none;"
                        title="AutoML Platform"
                        allow="camera; microphone"
                        onload="document.getElementById('loadingIndicator').style.display='none'; this.style.display='block';">
                    </iframe>
                </div>
            </div>
        `;
        document.body.appendChild(streamlitSection);
    }
    
    // Show the embedded section
    streamlitSection.style.display = 'block';
}

// Show landing page
function showLanding() {
    const landingPage = document.getElementById('landingPage');
    const streamlitSection = document.getElementById('streamlitSection');
    
    landingPage.style.display = 'block';
    if (streamlitSection) {
        streamlitSection.style.display = 'none';
    }
}

// Initialize theme toggle
function initThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    
    // Check for saved theme preference or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    body.setAttribute('data-theme', savedTheme);
    
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = body.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            body.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Add animation class
            body.classList.add('theme-transition');
            setTimeout(() => {
                body.classList.remove('theme-transition');
            }, 300);
        });
    }
}

// Initialize mobile menu
function initMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');
    
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
        });
        
        // Close mobile menu when clicking on a link
        const navItems = navLinks.querySelectorAll('a');
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                navLinks.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
            });
        });
    }
}

// Initialize smooth scrolling
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href === '#' || href === '#platform') return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

