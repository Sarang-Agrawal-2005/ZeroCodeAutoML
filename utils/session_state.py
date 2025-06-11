import streamlit as st

def initialize_session_state():
    """Initialize all session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Data Upload & Analysis"
    
    # Data-related states
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'data_analysis_results' not in st.session_state:
        st.session_state.data_analysis_results = {}
    if 'original_data' not in st.session_state:
        st.session_state.original_data = None
    
    # Preprocessing states
    if 'preprocessing_completed' not in st.session_state:
        st.session_state.preprocessing_completed = False
    if 'preprocessing_results' not in st.session_state:
        st.session_state.preprocessing_results = {}
    if 'X_processed' not in st.session_state:
        st.session_state.X_processed = None
    if 'y_processed' not in st.session_state:
        st.session_state.y_processed = None
    
    # Model training states
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'training_results' not in st.session_state:
        st.session_state.training_results = {}
    if 'model_trained' not in st.session_state:
        st.session_state.model_trained = False
    if 'X_train' not in st.session_state:
        st.session_state.X_train = None
    if 'X_test' not in st.session_state:
        st.session_state.X_test = None
    if 'y_train' not in st.session_state:
        st.session_state.y_train = None
    if 'y_test' not in st.session_state:
        st.session_state.y_test = None
    if 'scaler' not in st.session_state:
        st.session_state.scaler = None
    if 'pca' not in st.session_state:
        st.session_state.pca = None
    if 'label_encoders' not in st.session_state:
        st.session_state.label_encoders = {}
    if 'problem_type' not in st.session_state:
        st.session_state.problem_type = None
    if 'target_column' not in st.session_state:
        st.session_state.target_column = None
    if 'target_encoder' not in st.session_state:
        st.session_state.target_encoder = None
    
    # Model evaluation states
    if 'evaluation_results' not in st.session_state:
        st.session_state.evaluation_results = {}
    if 'evaluation_completed' not in st.session_state:
        st.session_state.evaluation_completed = False
