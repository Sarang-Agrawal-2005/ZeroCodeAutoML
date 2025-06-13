import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_page():
    """Display the Data Upload & Analysis page"""
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload your dataset in CSV format"
    )
    
    if uploaded_file is not None:
        try:
            # Load data
            df = pd.read_csv(uploaded_file)
            st.session_state.data = df
            
            # Check if this is a new file or existing analysis
            file_changed = (
                not hasattr(st.session_state, 'uploaded_filename') or 
                st.session_state.uploaded_filename != uploaded_file.name or
                not hasattr(st.session_state, 'analysis_completed') or
                not st.session_state.analysis_completed
            )
            
            # Store filename
            st.session_state.uploaded_filename = uploaded_file.name
            
            if file_changed:
                # Generate new analysis
                with st.spinner("Analyzing your data... Please wait"):
                    # Dataset overview
                    st.subheader("📋 Dataset Overview")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Rows", df.shape[0])
                    with col2:
                        st.metric("Total Columns", df.shape[1])
                    with col3:
                        st.metric("Missing Values", df.isnull().sum().sum())
                    with col4:
                        st.metric("Duplicate Rows", df.duplicated().sum())
                    
                    # Store analysis results
                    analysis_results = {
                        'basic_stats': {
                            'rows': df.shape[0],
                            'columns': df.shape[1],
                            'missing_values': df.isnull().sum().sum(),
                            'duplicates': df.duplicated().sum()
                        },
                        'column_info': [],
                        'visualizations': {}
                    }
                    
                    # Create info dataframe
                    for col in df.columns:
                        analysis_results['column_info'].append({
                            'Column': col,
                            'Data Type': str(df[col].dtype),
                            'Non-Null Count': df[col].count(),
                            'Missing Count': df[col].isnull().sum(),
                            'Missing %': f"{(df[col].isnull().sum() / len(df) * 100):.1f}%",
                            'Unique Values': df[col].nunique()
                        })
                    
                    # Sample data
                    st.subheader("Data Sample")
                    st.dataframe(df.head(min(100,df.shape[0])), use_container_width=True)
                    
                    # Feature Analysis
                    st.subheader("Feature Analysis")
                    
                    # Default to first column for initial analysis
                    selected_column = df.columns[0]
                    
                    # Generate and store correlation plot
                    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
                    if len(numeric_columns) > 1:
                        corr_matrix = df[numeric_columns].corr()
                        fig_corr = px.imshow(
                            corr_matrix,
                            text_auto=True,
                            aspect="auto",
                            title="Feature Correlation HeatMap",
                            color_continuous_scale="RdBu_r"
                        )
                        fig_corr.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#FAFAFA',
                            title_font_size=16,
                            height=600
                        )
                        st.plotly_chart(fig_corr, use_container_width=True)
                        analysis_results['visualizations']['correlation_fig'] = fig_corr
                    
                    # Generate and store missing values plot
                    if df.isnull().sum().sum() > 0:
                        missing_data = df.isnull().sum().sort_values(ascending=False)
                        missing_data = missing_data[missing_data > 0]
                        
                        if len(missing_data) > 0:
                            fig_missing = px.bar(
                                x=missing_data.index,
                                y=missing_data.values,
                                title="Missing Values by Column",
                                labels={'x': 'Columns', 'y': 'Missing Count'}
                            )
                            fig_missing.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font_color='#FAFAFA',
                                title_font_size=16,
                                xaxis_tickangle=45
                            )
                            st.plotly_chart(fig_missing, use_container_width=True)
                            analysis_results['visualizations']['missing_values_fig'] = fig_missing
                    
                    # Additional feature: Compare multiple distributions
                    st.subheader("Compare Multiple Features")
                    
                    # Multi-select for comparing distributions
                    compare_columns = st.multiselect(
                        "Select columns to compare (max 10):",
                        options=[col for col in df.columns if df[col].dtype in ['int64', 'float64']],
                        max_selections=10,
                        help="Only numeric columns can be compared"
                    )
                    
                    if len(compare_columns) > 1:
                        # Create subplot for comparison
                        rows = (len(compare_columns) + 1) // 2
                        cols = 2 if len(compare_columns) > 1 else 1
                        
                        fig_compare = make_subplots(
                            rows=rows, cols=cols,
                            subplot_titles=compare_columns,
                            vertical_spacing=0.1
                        )
                        
                        for i, col in enumerate(compare_columns):
                            row = (i // 2) + 1
                            col_pos = (i % 2) + 1
                            
                            fig_compare.add_histogram(
                                x=df[col], 
                                name=col,
                                row=row, col=col_pos,
                                nbinsx=20
                            )
                        
                        fig_compare.update_layout(
                            height=300 * rows,
                            showlegend=False,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#FAFAFA'
                        )
                        
                        st.plotly_chart(fig_compare, use_container_width=True)
                    
                    # Store results in session state
                    st.session_state.analysis_results = analysis_results
                    st.session_state.analysis_completed = True
                    
                    st.success("✅ Data analysis completed! You can now proceed to 'Dataset Preparation' page to prepare your dataset for modelling.")
            
            else:
                # Display stored results
                display_stored_analysis(df)
                
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.info("Please make sure your file is a valid CSV format.")
    
    # Display stored results if no file uploaded but analysis exists
    elif (hasattr(st.session_state, 'analysis_completed') and 
          st.session_state.analysis_completed and 
          hasattr(st.session_state, 'data')):
        display_stored_analysis(st.session_state.data)
    
    else:
        st.info("👆 Please upload a CSV file to begin analysis")
        
        # Show example of expected format
        st.subheader("📝 Expected File Format")
        example_data = pd.DataFrame({
            'age': [25, 34, 28, 52, 46, 30, 40, 23, 60, 36],
            'gender': ['Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Male', 'Female', 'Male', 'Female'],
            'income': [48000, 52000, 61000, 72000, 83000, 49000, 67000, 41000, 90000, 55000],
            'education': ['Bachelors', 'Masters', 'PhD', 'Bachelors', 'Masters', 'High School', 'PhD', 'Bachelors', 'PhD', 'Masters'],
            'employed': [True, True, False, True, True, False, True, False, True, True],
            'join_date': pd.to_datetime([
                '2020-01-15', '2019-11-22', '2021-06-10', '2018-03-30', '2017-07-19',
                '2022-08-05', '2016-04-12', '2023-01-01', '2015-12-09', '2020-05-17'
            ]),
            'credit_score': [680, 720, 710, 690, 740, 660, 730, 650, 780, 700],
            'loan_amount': [20000, 15000, 30000, 25000, 18000, 22000, 27000, 16000, 32000, 21000],
            'married': [False, True, False, True, True, False, True, False, True, True],
            'target': [0, 1, 0, 1, 1, 0, 1, 0, 1, 1]  # For example, 1 = loan approved
        })
        st.dataframe(example_data, use_container_width=True)
        st.caption("Example: Your CSV should have columns for features and a target variable")

def display_stored_analysis(df):
    """Display stored analysis results with interactive widgets"""
    
    if not hasattr(st.session_state, 'analysis_results'):
        return
    
    results = st.session_state.analysis_results
    
    st.success(f"📁 **Dataset:** {st.session_state.uploaded_filename}")
    
    # Dataset overview
    st.subheader("📋 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rows", results['basic_stats']['rows'])
    with col2:
        st.metric("Total Columns", results['basic_stats']['columns'])
    with col3:
        st.metric("Missing Values", results['basic_stats']['missing_values'])
    with col4:
        st.metric("Duplicate Rows", results['basic_stats']['duplicates'])
    
    # Sample data
    st.subheader("Data Sample")
    st.dataframe(df.head(min(100,df.shape[0])), use_container_width=True)
    
    # Enhanced distribution visualization with user control
    st.subheader("Feature Analysis")
    
    # Let user select which column to visualize
    selected_column = st.selectbox(
        "Select feature for analysis:",
        options=df.columns.tolist(),
        help="Choose any column to see its distribution"
    )
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if selected_column:
            # Check if column is numeric or categorical
            if df[selected_column].dtype in ['int64', 'float64']:
                # Numeric column - histogram
                bins = st.slider("Number of bins:", min_value=10, max_value=100, value=30)
                
                fig_hist = px.histogram(
                    df, 
                    x=selected_column, 
                    nbins=bins,
                    title=f"Distribution of {selected_column}",
                    marginal="box"  # Add box plot on top
                )
                
                # Add statistical annotations
                mean_val = df[selected_column].mean()
                median_val = df[selected_column].median()
                
                fig_hist.add_vline(x=mean_val, line_dash="dash", line_color="red", 
                                  annotation_text=f"Mean: {mean_val:.2f}")
                fig_hist.add_vline(x=median_val, line_dash="dash", line_color="green", 
                                  annotation_text=f"Median: {median_val:.2f}")
                
            else:
                # Categorical column - bar chart
                value_counts = df[selected_column].value_counts()
                
                # Option to limit number of categories shown
                max_categories = st.slider("Number of classes displayed:", 
                                         min_value=5, max_value=min(100, len(value_counts)), 
                                         value=min(20, len(value_counts)))
                
                top_categories = value_counts.head(max_categories)
                
                fig_hist = px.bar(
                    x=top_categories.index, 
                    y=top_categories.values,
                    title=f"Distribution of {selected_column}",
                    labels={'x': selected_column, 'y': 'Count'}
                )
                
                # Rotate x-axis labels if they're long
                fig_hist.update_xaxes(tickangle=45)
            
            # Apply consistent styling
            fig_hist.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#FAFAFA',
                title_font_size=16,
                height=500
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Display statistics for the selected column
        st.subheader("📈 Statistics")
        
        if df[selected_column].dtype in ['int64', 'float64']:
            # Numeric statistics
            stats_data = {
                "Data Type": f"{df[selected_column].dtype}",
                "Mean": f"{df[selected_column].mean():.3f}",
                "Median": f"{df[selected_column].median():.3f}",
                "Std Dev": f"{df[selected_column].std():.3f}",
                "Min": f"{df[selected_column].min():.3f}",
                "Max": f"{df[selected_column].max():.3f}",
                "Missing Values": df[selected_column].isnull().sum(),
            }
        else:
            # Categorical statistics
            stats_data = {
                "Data Type": f"{df[selected_column].dtype}",
                "Unique Values": df[selected_column].nunique(),
                "Most Frequent Value": df[selected_column].mode().iloc[0] if len(df[selected_column].mode()) > 0 else "N/A",
                "Least Frequent Value": df[selected_column].value_counts().idxmin() if not df[selected_column].empty else "N/A",
                "Missing Values": df[selected_column].isnull().sum(),
            }
        
        for key, value in stats_data.items():
            st.metric(key, value)
    
    # Safe access to stored visualizations with error handling
    if 'visualizations' in results:
        if 'correlation_fig' in results['visualizations']:
            st.plotly_chart(results['visualizations']['correlation_fig'], use_container_width=True)
        
        if 'missing_values_fig' in results['visualizations']:
            st.plotly_chart(results['visualizations']['missing_values_fig'], use_container_width=True)
    else:
        # Regenerate visualizations if missing
        regenerate_visualizations(df, results)
    
    # Additional feature: Compare multiple distributions
    st.subheader("Compare Multiple Features")
    
    # Multi-select for comparing distributions
    compare_columns = st.multiselect(
        "Select columns to compare (max 10):",
        options=[col for col in df.columns if df[col].dtype in ['int64', 'float64']],
        max_selections=10,
        help="Only numeric columns can be compared"
    )
    
    if len(compare_columns) > 1:
        # Create subplot for comparison
        rows = (len(compare_columns) + 1) // 2
        cols = 2 if len(compare_columns) > 1 else 1
        
        fig_compare = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=compare_columns,
            vertical_spacing=0.1
        )
        
        for i, col in enumerate(compare_columns):
            row = (i // 2) + 1
            col_pos = (i % 2) + 1
            
            fig_compare.add_histogram(
                x=df[col], 
                name=col,
                row=row, col=col_pos,
                nbinsx=20
            )
        
        fig_compare.update_layout(
            height=300 * rows,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FAFAFA'
        )
        
        st.plotly_chart(fig_compare, use_container_width=True)
    
    st.success("✅ Data analysis completed! You can now proceed to 'Dataset Preparation' page to prepare your dataset for modelling.")

def regenerate_visualizations(df, results):
    """Regenerate missing visualizations"""
    
    if 'visualizations' not in results:
        results['visualizations'] = {}
    
    # Generate correlation plot
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_columns) > 1:
        corr_matrix = df[numeric_columns].corr()
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Feature Correlation HeatMap",
            color_continuous_scale="RdBu_r"
        )
        fig_corr.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FAFAFA',
            title_font_size=16,
            height=600
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        results['visualizations']['correlation_fig'] = fig_corr
    
    # Generate missing values plot
    if df.isnull().sum().sum() > 0:
        missing_data = df.isnull().sum().sort_values(ascending=False)
        missing_data = missing_data[missing_data > 0]
        
        if len(missing_data) > 0:
            fig_missing = px.bar(
                x=missing_data.index,
                y=missing_data.values,
                title="Missing Values by Column",
                labels={'x': 'Columns', 'y': 'Missing Count'}
            )
            fig_missing.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#FAFAFA',
                title_font_size=16,
                xaxis_tickangle=45
            )
            st.plotly_chart(fig_missing, use_container_width=True)
            results['visualizations']['missing_values_fig'] = fig_missing
    
    # Update session state with regenerated visualizations
    st.session_state.analysis_results = results
