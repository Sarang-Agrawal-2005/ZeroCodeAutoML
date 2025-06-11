import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import VarianceThreshold
from utils.preprocessing import remove_outliers_iqr, feature_selection_by_correlation

def show_page():
    """Display the Data Preprocessing page"""
    st.markdown('<h1 class="main-header">🔧 Data Preprocessing</h1>', unsafe_allow_html=True)
    
    if st.session_state.data is None:
        st.markdown('<div class="warning-message">⚠️ Please upload and analyze data first in the "Data Upload & Analysis" page.</div>', unsafe_allow_html=True)
        st.stop()
    
    # Check if we already have preprocessing results
    if st.session_state.preprocessing_completed and st.session_state.preprocessing_results:
        st.markdown('<div class="success-message">✅ Data preprocessing results loaded</div>', unsafe_allow_html=True)
        
        results = st.session_state.preprocessing_results
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Original Features", results.get('original_features', 'N/A'))
        with col2:
            st.metric("Final Features", results.get('final_features', 'N/A'))
        with col3:
            st.metric("Original Samples", results.get('original_samples', 'N/A'))
        with col4:
            st.metric("Final Samples", results.get('final_samples', 'N/A'))
        
        if results.get('dropped_features'):
            st.info(f"**Dropped Features:** {', '.join(results['dropped_features'][:5])}{'...' if len(results['dropped_features']) > 5 else ''}")
        
        st.info(f"**Target Column:** {results.get('target_column', 'N/A')}")
        st.info(f"**Problem Type:** {results.get('problem_type', 'N/A')}")
    
    df = st.session_state.data.copy()
    
    # Preprocessing configuration
    st.subheader("⚙️ Preprocessing Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        target_column = st.selectbox("🎯 Select Target Column", df.columns, 
                                   help="Choose the column you want to predict")
    
    with col2:
        test_size = st.slider("📊 Test Set Size", 0.1, 0.5, 0.2, 0.05,
                            help="Proportion of data to use for testing")
    
    if target_column:
        # Prepare initial data
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Handle missing values in target
        if y.isnull().sum() > 0:
            st.warning(f"Target column has {y.isnull().sum()} missing values. Removing these rows.")
            valid_indices = y.notna()
            X = X[valid_indices]
            y = y[valid_indices]
        
        # Determine problem type
        unique_values = y.nunique()
        if y.dtype == 'object' or str(y.dtype).startswith('category') or unique_values <= 10:
            problem_type = 'classification'
        else:
            problem_type = 'regression'
        
        st.info(f"🔍 Detected problem type: **{problem_type.capitalize()}**")
        
        # Preprocessing options
        st.subheader("🔧 Preprocessing Options")
        
        # Create tabs for different preprocessing categories
        tab1, tab2, tab3, tab4 = st.tabs(["🧹 Data Cleaning", "🎯 Feature Selection", "📊 Scaling & Transform", "🔍 Dimensionality"])
        
        with tab1:
            st.write("**Missing Values & Outliers**")
            col1, col2 = st.columns(2)
            
            with col1:
                handle_missing = st.selectbox("❓ Handle Missing Values", 
                                            ["Drop rows", "Drop columns (>50% missing)", "Fill with mean/mode"])
                
                remove_outliers = st.checkbox("🚫 Remove Outliers (IQR Method)", 
                                            help="Remove outliers using the Interquartile Range method")
            
            with col2:
                if remove_outliers:
                    st.info("Outliers will be removed using Q1 - 1.5*IQR and Q3 + 1.5*IQR thresholds")
                
                # Show missing value summary
                missing_summary = X.isnull().sum()
                if missing_summary.sum() > 0:
                    st.write("**Missing Values Summary:**")
                    missing_df = pd.DataFrame({
                        'Column': missing_summary.index,
                        'Missing Count': missing_summary.values,
                        'Missing %': (missing_summary.values / len(X) * 100).round(2)
                    })
                    st.dataframe(missing_df[missing_df['Missing Count'] > 0], use_container_width=True)
        
        with tab2:
            st.write("**Feature Selection Methods**")
            
            col1, col2 = st.columns(2)
            with col1:
                apply_variance_filter = st.checkbox("📉 Remove Low Variance Features")
                if apply_variance_filter:
                    variance_threshold = st.slider("Variance Threshold", 0.0, 1.0, 0.01, 0.01,
                                                  help="Features with variance below this threshold will be removed")
                else:
                    variance_threshold = 0.0
            
            with col2:
                apply_correlation_filter = st.checkbox("🔗 Correlation-based Selection")
                if apply_correlation_filter:
                    drop_high_corr = st.checkbox("Drop highly correlated features", value=True)
                    if drop_high_corr:
                        high_corr_threshold = st.slider("High correlation threshold", 0.5, 1.0, 0.8, 0.05)
                    else:
                        high_corr_threshold = 0.8
                    
                    drop_low_target_corr = st.checkbox("Drop features weakly correlated with target")
                    if drop_low_target_corr:
                        low_target_corr_threshold = st.slider("Low target correlation threshold", 0.0, 0.5, 0.1, 0.01)
                    else:
                        low_target_corr_threshold = 0.1
                else:
                    drop_high_corr = False
                    drop_low_target_corr = False
                    high_corr_threshold = 0.8
                    low_target_corr_threshold = 0.1
        
        with tab3:
            st.write("**Scaling and Transformation**")
            col1, col2 = st.columns(2)
            
            with col1:
                scaling_method = st.selectbox("📏 Scaling Method", 
                                            ["StandardScaler", "MinMaxScaler", "None"],
                                            help="Choose how to scale numerical features")
            
            with col2:
                encode_categorical = st.checkbox("🏷️ Encode Categorical Variables", value=True,
                                               help="Convert categorical variables to numerical using Label Encoding")
        
        with tab4:
            st.write("**Dimensionality Reduction**")
            col1, col2 = st.columns(2)
            
            with col1:
                apply_pca = st.checkbox("🎯 Apply PCA (Principal Component Analysis)")
                if apply_pca:
                    pca_variance = st.slider("Explained Variance Ratio", 0.8, 0.99, 0.95, 0.01,
                                           help="Keep components that explain this much variance")
                else:
                    pca_variance = 0.95
            
            with col2:
                if apply_pca:
                    st.info(f"PCA will reduce dimensions while preserving {pca_variance*100:.0f}% of variance")
        
        # Preprocess button
        if st.button("🚀 Apply Preprocessing", use_container_width=True):
            try:
                with st.spinner("Applying preprocessing... Please wait"):
                    # Start preprocessing pipeline
                    X_processed = X.copy()
                    y_processed = y.copy()
                    dropped_features = []
                    label_encoders = {}
                    preprocessing_summary = {
                        'original_features': X_processed.shape[1],
                        'original_samples': X_processed.shape[0]
                    }
                    
                    # Step 1: Handle missing values
                    if handle_missing == "Drop rows":
                        initial_rows = len(X_processed)
                        valid_indices = X_processed.notna().all(axis=1)
                        X_processed = X_processed[valid_indices]
                        y_processed = y_processed[valid_indices]
                        st.info(f"Dropped {initial_rows - len(X_processed)} rows with missing values")
                        
                    elif handle_missing == "Drop columns (>50% missing)":
                        missing_threshold = 0.5
                        missing_percentages = X_processed.isnull().sum() / len(X_processed)
                        columns_to_drop = missing_percentages[missing_percentages > missing_threshold].index.tolist()
                        X_processed = X_processed.drop(columns=columns_to_drop)
                        dropped_features.extend(columns_to_drop)
                        if columns_to_drop:
                            st.info(f"Dropped {len(columns_to_drop)} columns with >50% missing values")
                            
                    else:  # Fill with mean/mode
                        for col in X_processed.columns:
                            if X_processed[col].dtype in ['int64', 'float64']:
                                X_processed[col].fillna(X_processed[col].mean(), inplace=True)
                            else:
                                mode_val = X_processed[col].mode()
                                fill_val = mode_val[0] if not mode_val.empty else 'Unknown'
                                X_processed[col].fillna(fill_val, inplace=True)
                    
                    # Step 2: Remove outliers
                    if remove_outliers:
                        numeric_cols = X_processed.select_dtypes(include=[np.number]).columns
                        X_processed, outliers_removed = remove_outliers_iqr(X_processed, numeric_cols)
                        y_processed = y_processed.iloc[X_processed.index]
                        if outliers_removed > 0:
                            st.info(f"Removed {outliers_removed} outliers using IQR method")
                    
                    # Step 3: Encode categorical variables
                    if encode_categorical:
                        categorical_columns = X_processed.select_dtypes(include=['object']).columns
                        for col in categorical_columns:
                            le = LabelEncoder()
                            X_processed[col] = le.fit_transform(X_processed[col].astype(str))
                            label_encoders[col] = le
                        
                        if len(categorical_columns) > 0:
                            st.info(f"Encoded {len(categorical_columns)} categorical columns")
                    
                    # Encode target variable if classification
                    target_encoder = None
                    if problem_type == 'classification' and y_processed.dtype == 'object':
                        target_encoder = LabelEncoder()
                        y_processed = target_encoder.fit_transform(y_processed)
                    
                    # Step 4: Correlation-based feature selection
                    if apply_correlation_filter:
                        X_processed, corr_dropped = feature_selection_by_correlation(
                            X_processed, pd.Series(np.array(y_processed), index=X_processed.index),
                            drop_high_corr=drop_high_corr,
                            high_corr_threshold=high_corr_threshold,
                            drop_low_target_corr=drop_low_target_corr,
                            low_target_corr_threshold=low_target_corr_threshold
                        )
                        dropped_features.extend(corr_dropped)
                        if corr_dropped:
                            st.info(f"Correlation filter dropped {len(corr_dropped)} features")
                    
                    # Step 5: Variance-based feature selection
                    if apply_variance_filter:
                        selector = VarianceThreshold(threshold=variance_threshold)
                        X_processed = pd.DataFrame(
                            selector.fit_transform(X_processed),
                            columns=X_processed.columns[selector.get_support()],
                            index=X_processed.index
                        )
                        variance_dropped = X_processed.columns[~selector.get_support()].tolist()
                        dropped_features.extend(variance_dropped)
                        if variance_dropped:
                            st.info(f"Variance filter dropped {len(variance_dropped)} features")
                    
                    # Update preprocessing summary
                    preprocessing_summary.update({
                        'final_features': X_processed.shape[1],
                        'final_samples': X_processed.shape[0],
                        'total_dropped_features': len(dropped_features),
                        'target_column': target_column,
                        'problem_type': problem_type,
                        'dropped_features': dropped_features,
                        'test_size': test_size,
                        'preprocessing_config': {
                            'missing_strategy': handle_missing,
                            'remove_outliers': remove_outliers,
                            'scaling_method': scaling_method,
                            'apply_pca': apply_pca,
                            'variance_threshold': variance_threshold,
                            'correlation_filter': apply_correlation_filter,
                            'encode_categorical': encode_categorical
                        }
                    })
                    
                    # Store everything in session state
                    st.session_state.X_processed = X_processed
                    st.session_state.y_processed = y_processed
                    st.session_state.label_encoders = label_encoders
                    st.session_state.target_encoder = target_encoder
                    st.session_state.problem_type = problem_type
                    st.session_state.target_column = target_column
                    st.session_state.preprocessing_results = preprocessing_summary
                    st.session_state.preprocessing_completed = True
                    
                    # Reset training and evaluation states
                    st.session_state.model_trained = False
                    st.session_state.evaluation_completed = False
                    
                    # Display preprocessing summary
                    st.success("🎉 Preprocessing completed successfully!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Features: Before → After", 
                                f"{preprocessing_summary['original_features']} → {preprocessing_summary['final_features']}")
                    with col2:
                        st.metric("Samples: Before → After", 
                                f"{preprocessing_summary['original_samples']} → {preprocessing_summary['final_samples']}")
                    with col3:
                        st.metric("Dropped Features", len(dropped_features))
                    
                    st.balloons()
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error during preprocessing: {str(e)}")
