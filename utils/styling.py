import streamlit as st
import streamlit.components.v1 as components

def apply_custom_css():
    """Apply comprehensive custom CSS styling with header/footer removal"""
    
    st.markdown("""
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* REMOVE ALL STREAMLIT BRANDING AND HOVERING ELEMENTS */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    
    /* Hide toolbar, decoration, and status widgets */
    [data-testid="stToolbar"] {
        visibility: hidden !important;
        height: 0% !important;
        position: fixed !important;
    }
    
    [data-testid="stDecoration"] {
        visibility: hidden !important;
        height: 0% !important;
        position: fixed !important;
    }
    
    [data-testid="stStatusWidget"] {
        visibility: hidden !important;
        height: 0% !important;
        position: fixed !important;
    }
    
    /* Hide the colored line at top */
    .stApp > header {
        background-color: transparent !important;
    }
    
    /* Hide running indicator */
    .stSpinner {
        visibility: hidden !important;
    }
    
    /* Remove top padding caused by hidden header */
    .main .block-container {
        padding-top: 1rem !important;
    }
    
    /* Your existing CSS variables */
    :root {
        --primary: #00c8ff;
        --primary-dark: #0099ff;
        --secondary: #9d4edd;
        --accent: #ff00ff;
        --background: #0a0e17;
        --background-light: #141a29;
        --card-bg: rgba(20, 26, 41, 0.7);
        --text-primary: #ffffff;
        --text-secondary: #a0a9c0;
        --text-muted: #6c7a94;
        --border-color: rgba(255, 255, 255, 0.1);
        --success: #00e676;
        --warning: #ffab00;
        --error: #ff5252;
        --info: #00b0ff;
        --transition-fast: 0.2s ease;
        --transition-normal: 0.3s ease;
        --transition-slow: 0.5s ease;
        --radius-sm: 4px;
        --radius-md: 8px;
        --radius-lg: 16px;
        --radius-xl: 24px;
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.2);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.3);
        --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    
    /* Animated particle background using pure CSS */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        background-color: var(--background);
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(0, 200, 255, 0.1) 0%, transparent 20%),
            radial-gradient(circle at 90% 80%, rgba(157, 78, 221, 0.1) 0%, transparent 20%),
            radial-gradient(2px 2px at 20px 30px, var(--primary), transparent),
            radial-gradient(2px 2px at 40px 70px, var(--secondary), transparent),
            radial-gradient(1px 1px at 90px 40px, var(--primary), transparent),
            radial-gradient(1px 1px at 130px 80px, var(--secondary), transparent),
            radial-gradient(2px 2px at 160px 30px, var(--primary), transparent),
            radial-gradient(1px 1px at 200px 50px, var(--accent), transparent),
            radial-gradient(2px 2px at 240px 90px, var(--primary), transparent),
            radial-gradient(1px 1px at 280px 20px, var(--secondary), transparent);
        background-repeat: repeat;
        background-size: 300px 200px;
        animation: particlesFloat 20s linear infinite;
        opacity: 0.6;
    }
    
    @keyframes particlesFloat {
        0% { 
            transform: translateY(0) translateX(0); 
            opacity: 0.6;
        }
        25% { 
            transform: translateY(-50px) translateX(10px); 
            opacity: 0.8;
        }
        50% { 
            transform: translateY(-100px) translateX(-5px); 
            opacity: 0.6;
        }
        75% { 
            transform: translateY(-150px) translateX(15px); 
            opacity: 0.4;
        }
        100% { 
            transform: translateY(-200px) translateX(0); 
            opacity: 0.6;
        }
    }
    
    /* Floating animation for cards */
    @keyframes floatAnimation {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* Gradient text animations */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main app styling */
    .stApp {
        background-color: var(--background);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        position: relative;
        min-height: 100vh;
    }
    
    /* Ensure content is above background */
    .main .block-container {
        position: relative;
        z-index: 1;
        background: transparent;
        padding-top: 1rem !important;
        max-width: 1200px;
    }
    
    /* Enhanced sidebar styling */
    .css-1d391kg, 
    [data-testid="stSidebar"],
    .css-1d391kg .css-1v0mbdj {
        background: rgba(20, 26, 41, 0.9) !important;
        border-right: 1px solid var(--border-color);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all var(--transition-normal) !important;
        box-shadow: 0 4px 14px rgba(0, 200, 255, 0.3) !important;
        width: 100% !important;
        position: relative !important;
        overflow: hidden !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(0, 200, 255, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Headers with gradient animation */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        font-family: 'Poppins', sans-serif;
        position: relative;
        z-index: 1;
    }
    
    h1 {
        background: linear-gradient(-45deg, var(--primary), var(--secondary), var(--accent), var(--primary));
        background-size: 400% 400%;
        animation: gradientShift 4s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Glass morphism containers */
    .element-container {
        background: rgba(20, 26, 41, 0.8) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
        border: 1px solid var(--border-color) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        position: relative !important;
        z-index: 1 !important;
        transition: all var(--transition-normal) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    .element-container:hover {
        animation: floatAnimation 3s ease-in-out infinite;
        border-color: rgba(0, 200, 255, 0.3) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    /* Enhanced input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background-color: rgba(10, 14, 23, 0.9) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        padding: 0.75rem !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        transition: all var(--transition-normal) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(0, 200, 255, 0.2) !important;
        outline: none !important;
    }
    
    /* Enhanced file uploader */
    .stFileUploader > div {
        border: 2px dashed var(--primary) !important;
        border-radius: var(--radius-lg) !important;
        background: linear-gradient(135deg, rgba(0, 200, 255, 0.1) 0%, rgba(157, 78, 221, 0.1) 100%) !important;
        padding: 3rem !important;
        text-align: center !important;
        transition: all var(--transition-normal) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--accent) !important;
        background: linear-gradient(135deg, rgba(0, 200, 255, 0.2) 0%, rgba(157, 78, 221, 0.2) 100%) !important;
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 35px rgba(0, 200, 255, 0.3) !important;
    }
    
    /* Enhanced metrics */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(0, 200, 255, 0.1) 0%, rgba(157, 78, 221, 0.1) 100%) !important;
        border: 1px solid rgba(0, 200, 255, 0.3) !important;
        border-radius: var(--radius-lg) !important;
        padding: 2rem !important;
        backdrop-filter: blur(15px) !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all var(--transition-normal) !important;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0, 200, 255, 0.3);
        border-color: rgba(0, 200, 255, 0.5);
    }
    
    /* Enhanced dataframes */
    .stDataFrame {
        background: rgba(20, 26, 41, 0.9) !important;
        border-radius: var(--radius-lg) !important;
        border: 1px solid rgba(0, 200, 255, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        position: relative !important;
        z-index: 1 !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* Enhanced progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent)) !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(0, 200, 255, 0.4) !important;
        animation: progressGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes progressGlow {
        0% { box-shadow: 0 4px 15px rgba(0, 200, 255, 0.4); }
        100% { box-shadow: 0 4px 25px rgba(0, 200, 255, 0.8); }
    }
    
    .stProgress {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 2px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Plotly charts enhancement */
    .stPlotlyChart {
        background: rgba(20, 26, 41, 0.8) !important;
        border-radius: var(--radius-lg) !important;
        border: 1px solid var(--border-color) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        position: relative !important;
        z-index: 1 !important;
        padding: 1rem !important;
    }
    
    /* Text elements */
    .stMarkdown {
        position: relative;
        z-index: 1;
        color: var(--text-primary);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        .stFileUploader > div {
            padding: 2rem 1rem;
        }
        
        .element-container {
            padding: 1rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def add_interactive_features():
    """Add interactive JavaScript features"""
    components.html("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Remove any remaining Streamlit elements that might appear
        const elementsToHide = [
            'header[data-testid="stHeader"]',
            '[data-testid="stToolbar"]',
            '[data-testid="stDecoration"]',
            '[data-testid="stStatusWidget"]',
            '.stSpinner'
        ];
        
        elementsToHide.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                el.style.display = 'none';
                el.style.visibility = 'hidden';
            });
        });
        
        // Add click animations to buttons
        document.addEventListener('click', function(e) {
            if (e.target.matches('.stButton > button')) {
                e.target.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    e.target.style.transform = 'scale(1)';
                }, 150);
            }
        });
    });
    </script>
    """, height=0)




