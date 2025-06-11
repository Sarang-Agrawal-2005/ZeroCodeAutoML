import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>              
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #FF6B6B;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #262730;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #FF6B6B;
            margin: 0.5rem 0;
        }
        .success-message {
            background-color: #1B4D3E;
            color: #4ADE80;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #4ADE80;
            margin: 1rem 0;
        }
        .warning-message {
            background-color: #4D3319;
            color: #FBBF24;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #FBBF24;
            margin: 1rem 0;
        }
        .stButton > button {
            background-color: #FF6B6B;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #FF5252;
            transform: translateY(-2px);
        }
    </style>
    """, unsafe_allow_html=True)
