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
    initPlatformFeatures();
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
                        <h2>ZeroML Platform</h2>
                        <p>Build your machine learning models with our no-code interface</p>
                    </div>
                    <div id="loadingIndicator" style="text-align: center; padding: 2rem;">
                        <i class="fas fa-spinner fa-spin" style="font-size: 2rem; color: var(--primary);"></i>
                        <p>Loading ZeroML Platform...</p>
                    </div>
                    <iframe 
                        src="https://zero-code-automl.streamlit.app/?embed=true"
                        style="width: 100%; height: 800px; border: none; border-radius: 16px; display: none;"
                        title="ZeroML Platform"
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

// Initialize platform features (keeping original functionality for reference)
function initPlatformFeatures() {
    initFileUpload();
    initModelSelection();
    initTraining();
    initPrediction();
    initTabs();
}

// File upload functionality
function initFileUpload() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const uploadProgress = document.getElementById('uploadProgress');
    
    if (!uploadZone || !fileInput) return;
    
    uploadZone.addEventListener('click', () => fileInput.click());
    
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });
    
    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });
    
    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
}

// Handle file upload
function handleFileUpload(file) {
    if (!file.name.endsWith('.csv')) {
        showNotification('Error', 'Please upload a CSV file', 'error');
        return;
    }
    
    const uploadProgress = document.getElementById('uploadProgress');
    const progressBar = uploadProgress.querySelector('.progress-bar');
    
    uploadProgress.style.display = 'block';
    
    // Simulate upload progress
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 30;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            setTimeout(() => {
                uploadProgress.style.display = 'none';
                processFile(file);
            }, 500);
        }
        progressBar.style.width = progress + '%';
    }, 200);
}

// Process uploaded file
function processFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const csv = e.target.result;
        const lines = csv.split('\n');
        const headers = lines[0].split(',');
        
        currentDataset = {
            name: file.name,
            headers: headers,
            data: lines.slice(1).map(line => line.split(','))
        };
        
        showDataPreview();
        showNotification('Success', 'Dataset uploaded successfully!', 'success');
    };
    reader.readAsText(file);
}

// Show data preview
function showDataPreview() {
    const previewContainer = document.getElementById('dataPreview');
    const previewTable = document.getElementById('previewTable');
    
    if (!currentDataset || !previewTable) return;
    
    const thead = previewTable.querySelector('thead tr');
    const tbody = previewTable.querySelector('tbody');
    
    // Clear existing content
    thead.innerHTML = '';
    tbody.innerHTML = '';
    
    // Add headers
    currentDataset.headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header.trim();
        thead.appendChild(th);
    });
    
    // Add data rows (first 10 rows)
    currentDataset.data.slice(0, 10).forEach(row => {
        const tr = document.createElement('tr');
        row.forEach(cell => {
            const td = document.createElement('td');
            td.textContent = cell.trim();
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    
    previewContainer.style.display = 'block';
}

// Initialize model selection
function initModelSelection() {
    const modelCards = document.querySelectorAll('.model-card');
    
    modelCards.forEach(card => {
        card.addEventListener('click', () => {
            // Remove active class from all cards
            modelCards.forEach(c => c.classList.remove('active'));
            // Add active class to clicked card
            card.classList.add('active');
            
            currentModel = {
                name: card.querySelector('h3').textContent,
                type: card.dataset.model
            };
            
            showNotification('Model Selected', `${currentModel.name} selected`, 'info');
        });
    });
}

// Initialize training
function initTraining() {
    const trainBtn = document.getElementById('trainModel');
    
    if (trainBtn) {
        trainBtn.addEventListener('click', () => {
            if (!currentDataset) {
                showNotification('Error', 'Please upload a dataset first', 'error');
                return;
            }
            
            if (!currentModel) {
                showNotification('Error', 'Please select a model first', 'error');
                return;
            }
            
            startTraining();
        });
    }
}

// Start training process
function startTraining() {
    const trainingProgress = document.getElementById('trainingProgress');
    const progressBar = trainingProgress.querySelector('.progress-bar');
    const progressText = trainingProgress.querySelector('.progress-text');
    
    trainingProgress.style.display = 'block';
    
    let progress = 0;
    const stages = [
        'Preprocessing data...',
        'Training model...',
        'Validating results...',
        'Generating metrics...'
    ];
    
    let stageIndex = 0;
    
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        
        if (progress >= (stageIndex + 1) * 25 && stageIndex < stages.length - 1) {
            stageIndex++;
        }
        
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            setTimeout(() => {
                trainingProgress.style.display = 'none';
                showResults();
            }, 1000);
        }
        
        progressBar.style.width = progress + '%';
        progressText.textContent = stages[stageIndex];
    }, 300);
}

// Show training results
function showResults() {
    const resultsContainer = document.getElementById('trainingResults');
    
    // Generate mock results
    const accuracy = (85 + Math.random() * 10).toFixed(2);
    const precision = (80 + Math.random() * 15).toFixed(2);
    const recall = (75 + Math.random() * 20).toFixed(2);
    const f1Score = (78 + Math.random() * 17).toFixed(2);
    
    document.getElementById('accuracyValue').textContent = accuracy + '%';
    document.getElementById('precisionValue').textContent = precision + '%';
    document.getElementById('recallValue').textContent = recall + '%';
    document.getElementById('f1Value').textContent = f1Score + '%';
    
    resultsContainer.style.display = 'block';
    
    showNotification('Training Complete', 'Model trained successfully!', 'success');
}

// Initialize prediction
function initPrediction() {
    const predictBtn = document.getElementById('makePrediction');
    
    if (predictBtn) {
        predictBtn.addEventListener('click', () => {
            if (!currentModel) {
                showNotification('Error', 'Please train a model first', 'error');
                return;
            }
            
            makePrediction();
        });
    }
}

// Make prediction
function makePrediction() {
    const predictionResult = document.getElementById('predictionResult');
    const predictionValue = document.getElementById('predictionValue');
    const confidence = document.getElementById('confidence');
    
    // Generate mock prediction
    const result = Math.random() > 0.5 ? 'Positive' : 'Negative';
    const conf = (70 + Math.random() * 25).toFixed(1);
    
    predictionValue.textContent = result;
    confidence.textContent = conf + '%';
    
    predictionResult.style.display = 'block';
    
    showNotification('Prediction Complete', 'Prediction generated successfully!', 'success');
}

// Initialize tabs
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.dataset.tab;
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// Show notification
function showNotification(title, message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <h4>${title}</h4>
            <p>${message}</p>
        </div>
        <button class="notification-close">&times;</button>
    `;
    
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Auto hide
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, duration);
    
    // Manual close
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    });
}

// Reset platform
function resetPlatform() {
    currentDataset = null;
    currentModel = null;
    
    // Hide all sections
    document.getElementById('dataPreview').style.display = 'none';
    document.getElementById('trainingProgress').style.display = 'none';
    document.getElementById('trainingResults').style.display = 'none';
    document.getElementById('predictionResult').style.display = 'none';
    
    // Clear model selection
    document.querySelectorAll('.model-card').forEach(card => {
        card.classList.remove('active');
    });
    
    // Reset file input
    const fileInput = document.getElementById('fileInput');
    if (fileInput) fileInput.value = '';
    
    showNotification('Platform Reset', 'All data cleared successfully', 'info');
}
