import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

def show_page():
    """Display the Data Preprocessing page"""
    
    # Check if data exists
    if st.session_state.data is None:
        st.info('Please upload and analyze data first in the "Data Upload & Analysis" page')
        st.stop()
    
    df = st.session_state.data.copy()
    
    # Target column selection
    st.subheader("Target Selection")
    target_column = st.selectbox(
        "Select Target Column",
        options=df.columns.tolist(),
        help="Choose the column you want to predict"
    )
    
    # Test set size
    test_size = st.slider(
        "Test Set Size (%)",
        min_value=10,
        max_value=50,
        value=20,
        help="Percentage of data to use for testing"
    ) / 100
    
    # Problem type detection
    if df[target_column].dtype == 'object' or df[target_column].nunique() <= 10:
        problem_type = "classification"
        st.info(f"🎯 **Problem Type:** {problem_type} (Target has {df[target_column].nunique()} unique values)")
    else:
        problem_type = "regression"
        st.info(f"🎯 **Problem Type:** {problem_type} (Target is continuous)")
    
    # Preprocessing options in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🧹 Data Cleaning", "🎯 Feature Selection", "📏 Scaling & Transform", "📊 Dimensionality"])
    
    with tab1:
        st.subheader("Missing Values")
        missing_strategy = st.selectbox(
            "Missing Value Strategy",
            ["Drop rows with missing values", "Drop columns with >50% missing", "Fill with mean/mode"],
            help="Choose how to handle missing values"
        )
        
        st.subheader("Outlier Removal")
        remove_outliers = st.checkbox("Remove outliers using IQR method", help="Remove values outside Q1-1.5*IQR to Q3+1.5*IQR range")
    
    with tab2:
        st.subheader("Variance-based Selection")
        use_variance_filter = st.checkbox("Remove low-variance features")
        if use_variance_filter:
            variance_threshold = st.slider("Variance Threshold", 0.0, 1.0, 0.01, 0.01)
        
        st.subheader("Correlation-based Selection")
        remove_high_corr = st.checkbox("Remove highly correlated features")
        if remove_high_corr:
            high_corr_threshold = st.slider("High Correlation Threshold", 0.5, 1.0, 0.8, 0.05)
        
        remove_low_target_corr = st.checkbox("Remove features with low target correlation")
        if remove_low_target_corr:
            low_target_corr_threshold = st.slider("Low Target Correlation Threshold", 0.0, 0.5, 0.1, 0.05)
    
    with tab3:
        st.subheader("Feature Scaling")
        scaling_method = st.selectbox(
            "Scaling Method",
            ["None", "StandardScaler", "MinMaxScaler"],
            help="Choose scaling method for numerical features"
        )
    
    with tab4:
        st.subheader("Principal Component Analysis")
        use_pca = st.checkbox("Apply PCA for dimensionality reduction")
        if use_pca:
            pca_components = st.slider("Number of Components", 2, min(df.shape[1]-1, 50), 10)
    
    # Apply preprocessing button
    if st.button("Apply Preprocessing", use_container_width=True):
        try:
            with st.spinner("Applying preprocessing... Please wait"):
                st.info(f"**Target Column:** {target_column}")
                st.info(f"**Test Set Size:** {test_size * 100:.0f}%")
                # Initialize variables
                X = df.drop(columns=[target_column])
                y = df[target_column]
                dropped_features = []
                label_encoders = {}
                target_encoder = None
                preprocessing_messages = []  # Store all preprocessing messages
                
                # Store original dimensions
                original_features = X.shape[1]
                original_samples = X.shape[0]
                
                # 1. Handle missing values
                if missing_strategy == "Drop rows with missing values":
                    initial_rows = X.shape[0]
                    mask = ~(X.isnull().any(axis=1) | y.isnull())
                    X = X[mask]
                    y = y[mask]
                    message = f"Dropped {initial_rows - X.shape[0]} rows with missing values"
                    preprocessing_messages.append(message)
                    st.info(message)
                
                elif missing_strategy == "Drop columns with >50% missing":
                    missing_cols = X.columns[X.isnull().sum() / len(X) > 0.5].tolist()
                    if missing_cols:
                        X = X.drop(columns=missing_cols)
                        dropped_features.extend(missing_cols)
                        message = f"Dropped {len(missing_cols)} columns with >50% missing values"
                        preprocessing_messages.append(message)
                        st.info(message)
                
                elif missing_strategy == "Fill with mean/mode":
                    for col in X.columns:
                        if X[col].isnull().sum() > 0:
                            if X[col].dtype in ['int64', 'float64']:
                                X[col].fillna(X[col].mean(), inplace=True)
                            else:
                                X[col].fillna(X[col].mode()[0], inplace=True)
                    
                    if y.isnull().sum() > 0:
                        if y.dtype in ['int64', 'float64']:
                            y.fillna(y.mean(), inplace=True)
                        else:
                            y.fillna(y.mode()[0], inplace=True)
                    
                    message = "Filled missing values with mean (numerical) or mode (categorical)"
                    preprocessing_messages.append(message)
                    st.info(message)
                
                # 2. Remove outliers
                if remove_outliers:
                    numerical_cols = X.select_dtypes(include=[np.number]).columns
                    initial_rows = X.shape[0]
                    
                    for col in numerical_cols:
                        Q1 = X[col].quantile(0.25)
                        Q3 = X[col].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        
                        mask = (X[col] >= lower_bound) & (X[col] <= upper_bound)
                        X = X[mask]
                        y = y[mask]
                    
                    message = f"Removed {initial_rows - X.shape[0]} outlier rows using IQR method"
                    preprocessing_messages.append(message)
                    st.info(message)
                
                # 3. Encode categorical variables
                categorical_cols = X.select_dtypes(include=['object']).columns
                for col in categorical_cols:
                    le = LabelEncoder()
                    X[col] = le.fit_transform(X[col].astype(str))
                    label_encoders[col] = le
                
                if len(categorical_cols) > 0:
                    message = f"Applied Label Encoding to {len(categorical_cols)} categorical columns"
                    preprocessing_messages.append(message)
                    st.info(message)
                
                # 4. Encode target if classification
                if problem_type == "Classification" and y.dtype == 'object':
                    target_encoder = LabelEncoder()
                    y = target_encoder.fit_transform(y.astype(str))
                    message = "Applied Label Encoding to target column"
                    preprocessing_messages.append(message)
                    st.info(message)
                
                # 5. Feature selection - Correlation with target
                if remove_low_target_corr:
                    correlations = X.corrwith(y).abs()
                    low_corr_features = correlations[correlations < low_target_corr_threshold].index.tolist()
                    if low_corr_features:
                        X = X.drop(columns=low_corr_features)
                        dropped_features.extend(low_corr_features)
                        message = f"Removed {len(low_corr_features)} features with low target correlation"
                        preprocessing_messages.append(message)
                        st.info(message)
                
                # 6. Feature selection - High correlation between features
                if remove_high_corr:
                    corr_matrix = X.corr().abs()
                    upper_triangle = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
                    high_corr_features = [column for column in upper_triangle.columns if any(upper_triangle[column] > high_corr_threshold)]
                    if high_corr_features:
                        X = X.drop(columns=high_corr_features)
                        dropped_features.extend(high_corr_features)
                        message = f"Removed {len(high_corr_features)} highly correlated features"
                        preprocessing_messages.append(message)
                        st.info(message)
                
                # 7. Variance-based feature selection
                if use_variance_filter:
                    selector = VarianceThreshold(threshold=variance_threshold)
                    X_selected = selector.fit_transform(X)
                    selected_features = X.columns[selector.get_support()].tolist()
                    removed_features = X.columns[~selector.get_support()].tolist()
                    
                    if removed_features:
                        X = X[selected_features]
                        dropped_features.extend(removed_features)
                        message = f"Removed {len(removed_features)} low-variance features"
                        preprocessing_messages.append(message)
                        st.info(message)
                
                # 8. Scaling
                scaler = None
                if scaling_method == "StandardScaler":
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)
                    X = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
                    message = "Applied StandardScaler to numerical features"
                    preprocessing_messages.append(message)
                    st.info(message)
                elif scaling_method == "MinMaxScaler":
                    scaler = MinMaxScaler()
                    X_scaled = scaler.fit_transform(X)
                    X = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
                    message = "Applied MinMaxScaler to numerical features"
                    preprocessing_messages.append(message)
                    st.info(message)
                
                # Final processed data
                X_processed = X
                y_processed = y
                
                # Store final dimensions
                final_features = X_processed.shape[1]
                final_samples = X_processed.shape[0]
                
                # Create preprocessing configuration dictionary
                preprocessing_config = {
                    'missing_strategy': missing_strategy,
                    'remove_outliers': remove_outliers,
                    'use_variance_filter': use_variance_filter,
                    'variance_threshold': variance_threshold if use_variance_filter else None,
                    'remove_high_corr': remove_high_corr,
                    'high_corr_threshold': high_corr_threshold if remove_high_corr else None,
                    'remove_low_target_corr': remove_low_target_corr,
                    'low_target_corr_threshold': low_target_corr_threshold if remove_low_target_corr else None,
                    'scaling_method': scaling_method,
                    'apply_pca': use_pca,
                    'pca_components': pca_components if use_pca else None
                }

                # Create preprocessing summary
                preprocessing_summary = {
                    'original_features': original_features,
                    'final_features': final_features,
                    'original_samples': original_samples,
                    'final_samples': final_samples,
                    'dropped_features': dropped_features,
                    'target_column': target_column,
                    'problem_type': problem_type,
                    'test_size': test_size,
                    'preprocessing_messages': preprocessing_messages,
                    'preprocessing_config': preprocessing_config  
                }

                
                # Store everything in session state
                st.session_state.X_processed = X_processed
                st.session_state.y_processed = y_processed
                st.session_state.label_encoders = label_encoders
                st.session_state.target_encoder = target_encoder
                st.session_state.problem_type = problem_type
                st.session_state.target_column = target_column
                st.session_state.preprocessing_results = preprocessing_summary
                st.session_state.preprocessing_completed = True
                st.session_state.scaler = scaler
                
                # Reset downstream states
                st.session_state.model_trained = False
                st.session_state.evaluation_completed = False

                # Additional details
                if dropped_features:
                    st.info(f"**Dropped Features:** {', '.join(dropped_features[:5])}{'...' if len(dropped_features) > 5 else ''}")
                
                # Metrics display
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Features: Before → After", 
                            f"{preprocessing_summary['original_features']} → {preprocessing_summary['final_features']}")
                with col2:
                    st.metric("Samples: Before → After", 
                            f"{preprocessing_summary['original_samples']} → {preprocessing_summary['final_samples']}")
                with col3:
                    st.metric("Dropped Features", len(dropped_features))
                
                
                st.success("""✅ Preprocessing completed successfully! You can now proceed to the "Model Training" page.""")
                
                st.balloons()
                
        except Exception as e:
            st.error(f"❌ Error during preprocessing: {str(e)}")
    
    # Show existing results if preprocessing was completed previously
    elif (hasattr(st.session_state, 'preprocessing_completed') and 
          st.session_state.preprocessing_completed and 
          hasattr(st.session_state, 'preprocessing_results') and
          st.session_state.preprocessing_results):
        
        results = st.session_state.preprocessing_results

        
        
        # Display stored preprocessing messages
        if results.get('preprocessing_messages'):
            st.subheader("📋 Preprocessing Steps Applied")
            st.info(f"**Target Column:** {results.get('target_column', 'N/A')}")
            st.info(f"**Test Set Size:** {results.get('test_size', 0) * 100:.0f}%")
            for message in results['preprocessing_messages']:
                st.info(message)
        
        # Display metrics
        
        if results.get('dropped_features'):
            dropped_features_list = results['dropped_features']
            st.info(f"**Dropped Features:** {', '.join(dropped_features_list[:5])}{'...' if len(dropped_features_list) > 5 else ''}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Original Features", results.get('original_features', 'N/A'))
        with col2:
            st.metric("Final Features", results.get('final_features', 'N/A'))
        with col3:
            st.metric("Original Samples", results.get('original_samples', 'N/A'))
        with col4:
            st.metric("Final Samples", results.get('final_samples', 'N/A'))
        st.success("""✅ Preprocessing completed successfully! You can now proceed to the "Model Training" page.""")
        st.balloons()