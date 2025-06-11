import streamlit as st

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="ML Model Builder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.session_state import initialize_session_state
from utils.styling import apply_custom_css
from app_pages import data_upload, data_preprocessing, model_training, model_evaluation

# Initialize session state and apply styling
initialize_session_state()
apply_custom_css()

# Sidebar navigation
st.sidebar.title("🚀 Navigation")
st.sidebar.markdown("---")

if st.sidebar.button("📊 Data Upload & Analysis", use_container_width=True):
    st.session_state.current_page = "Data Upload & Analysis"
if st.sidebar.button("🔧 Data Preprocessing", use_container_width=True):
    st.session_state.current_page = "Data Preprocessing"
if st.sidebar.button("🤖 Model Training", use_container_width=True):
    st.session_state.current_page = "Model Training"
if st.sidebar.button("📈 Model Evaluation", use_container_width=True):
    st.session_state.current_page = "Model Evaluation"

# Route to appropriate page
page = st.session_state.current_page

if page == "Data Upload & Analysis":
    data_upload.show_page()
elif page == "Data Preprocessing":
    data_preprocessing.show_page()
elif page == "Model Training":
    model_training.show_page()
elif page == "Model Evaluation":
    model_evaluation.show_page()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; padding: 20px;'>
        🤖 ML Model Builder | Built with Streamlit | 
        <a href='#' style='color: #FF6B6B;'>Documentation</a> | 
        <a href='#' style='color: #FF6B6B;'>GitHub</a>
    </div>
    """, 
    unsafe_allow_html=True
)
