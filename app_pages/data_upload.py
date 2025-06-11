import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def show_page():
    """Display the Data Upload & Analysis page"""
    st.markdown('<h1 class="main-header">📊 Data Upload & Analysis</h1>', unsafe_allow_html=True)
    
    # Check if we already have analysis results
    if st.session_state.data is not None and st.session_state.data_analysis_results:
        st.markdown('<div class="success-message">✅ Data analysis results loaded</div>', unsafe_allow_html=True)
        
        # Display preserved results
        df = st.session_state.data
        results = st.session_state.data_analysis_results
        
        # Display metrics
        st.subheader("📋 Dataset Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📏 Rows", results['rows'])
        with col2:
            st.metric("📊 Columns", results['columns'])
        with col3:
            st.metric("❌ Missing Values", results['missing_values'])
        with col4:
            st.metric("💾 Memory Usage", results['memory_usage'])
        
        # Display preserved dataframes
        st.subheader("👀 Data Preview")
        st.dataframe(results['data_preview'], use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("ℹ️ Data Types")
            st.dataframe(results['data_info'], use_container_width=True)
        
        with col2:
            st.subheader("📈 Statistical Summary")
            st.dataframe(results['statistical_summary'], use_container_width=True)
        
        # Display preserved visualizations
        if 'correlation_fig' in results:
            st.subheader("🔥 Data Visualizations")
            st.write("**Correlation Heatmap**")
            st.plotly_chart(results['correlation_fig'], use_container_width=True)
        
        if 'distribution_fig' in results:
            st.write("**Distribution Analysis**")
            st.plotly_chart(results['distribution_fig'], use_container_width=True)
            
        if 'missing_values_fig' in results:
            st.write("**Missing Values Analysis**")
            st.plotly_chart(results['missing_values_fig'], use_container_width=True)
    
    # File upload section
    st.subheader("📁 Upload Your Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", help="Upload a CSV file to begin analysis")
    
    if uploaded_file is not None:
        # Only reprocess if it's a new file or user requests reanalysis
        if st.session_state.data is None or st.button("🔄 Reanalyze Data", help="Click to reanalyze the uploaded data"):
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.data = df
                st.session_state.original_data = df.copy()
                
                # Reset preprocessing and training states
                st.session_state.preprocessing_completed = False
                st.session_state.model_trained = False
                st.session_state.evaluation_completed = False
                
                # Store analysis results
                results = {}
                results['rows'] = df.shape[0]
                results['columns'] = df.shape[1]
                results['missing_values'] = df.isnull().sum().sum()
                results['memory_usage'] = f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
                results['data_preview'] = df.head(10)
                results['data_info'] = df.dtypes.to_frame('Data Type')
                results['statistical_summary'] = df.describe()
                
                # Generate and store visualizations
                numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if len(numeric_columns) > 1:
                    # Correlation heatmap
                    corr_matrix = df[numeric_columns].corr()
                    fig_corr = px.imshow(corr_matrix, 
                                       text_auto=True, 
                                       aspect="auto",
                                       color_continuous_scale='RdBu_r',
                                       title="Feature Correlation Matrix")
                    fig_corr.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#FAFAFA',
                        title_font_size=16
                    )
                    results['correlation_fig'] = fig_corr
                
                # Distribution plot for numeric columns
                if len(numeric_columns) > 0:
                    fig_hist = px.histogram(df, x=numeric_columns[0], nbins=30, 
                                          title=f"Distribution of {numeric_columns[0]}")
                    fig_hist.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#FAFAFA',
                        title_font_size=16
                    )
                    results['distribution_fig'] = fig_hist
                
                # Missing values visualization
                missing_data = df.isnull().sum()
                if missing_data.sum() > 0:
                    fig_missing = px.bar(x=missing_data.index, y=missing_data.values,
                                       title="Missing Values by Column",
                                       labels={'x': 'Columns', 'y': 'Missing Count'})
                    fig_missing.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#FAFAFA',
                        title_font_size=16
                    )
                    results['missing_values_fig'] = fig_missing
                
                # Store results in session state
                st.session_state.data_analysis_results = results
                st.rerun()
                
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
