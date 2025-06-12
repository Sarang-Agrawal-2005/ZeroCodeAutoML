import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from models import (
    random_forest, logistic_regression, linear_regression, 
    decision_tree, svm, knn, 
    gradient_boosting, naive_bayes, ridge, 
    lasso, xgboost_model, elasticnet
)

def create_model_from_module(model_name, params, problem_type):
    """Create model instance using the model module's get_model function"""
    model_mapping = {
        "Random Forest": random_forest,
        "Logistic Regression": logistic_regression,
        "Linear Regression": linear_regression,
        "Decision Tree": decision_tree,
        "SVM": svm,
        "K-Nearest Neighbors": knn,
        "Gradient Boosting": gradient_boosting,
        "Ridge Regression": ridge,
        "Lasso Regression": lasso,
        "Naive Bayes": naive_bayes,
        "XGBoost": xgboost_model,
        "ElasticNet": elasticnet
    }
    
    if model_name not in model_mapping:
        raise ValueError(f"Model {model_name} not found in available models")
    
    model_module = model_mapping[model_name]
    
    # Check if the module has a get_model function
    if hasattr(model_module, 'get_model'):
        return model_module.get_model(params, problem_type)
    else:
        raise AttributeError(f"Model {model_name} does not have a get_model function")

def show_page():
    """Display the Model Training page"""
    #st.markdown('<h1 class="main-header">🤖 Model Training</h1>', unsafe_allow_html=True)
    
    if not st.session_state.preprocessing_completed:
        st.info('''Please prepare your dataset first in the "Dataset Preparation" page''')
        st.stop()
    
    # Check if we already have training results
    # if st.session_state.model_trained and st.session_state.training_results:
    #     #st.markdown('<div class="success-message">✅ Model training results loaded</div>', unsafe_allow_html=True)
        
    #     results = st.session_state.training_results
        
    #     col1, col2, col3 = st.columns(3)
    #     with col1:
    #         st.info(f"**Model:** {results['model_name']}")
    #     with col2:
    #         st.info(f"**Problem Type:** {results['problem_type']}")
    #     with col3:
    #         st.metric("Training Score", f"{results.get('training_score', 0):.4f}")
    
    # Get preprocessed data
    X_processed = st.session_state.X_processed
    y_processed = st.session_state.y_processed
    problem_type = st.session_state.problem_type
    preprocessing_config = st.session_state.preprocessing_results['preprocessing_config']
    
    st.subheader("Model Selection & Hyperparameters")
    
    # Model selection
    if problem_type == 'classification':
        model_options = [
            "Logistic Regression","Random Forest", "Decision Tree", "SVM", 
            "K-Nearest Neighbors", "Gradient Boosting", "Naive Bayes", "XGBoost"
        ]
    else:
        model_options = [
            "Linear Regression","Random Forest", "Decision Tree", "SVM", 
            "K-Nearest Neighbors", "Gradient Boosting", "Ridge Regression", 
            "Lasso Regression", "XGBoost", "ElasticNet"
        ]
    
    selected_model_name = st.selectbox("🤖 Select Model", model_options)
    
    # Get hyperparameters based on selected model using model modules
    model_mapping = {
        "Random Forest": random_forest,
        "Logistic Regression": logistic_regression,
        "Linear Regression": linear_regression,
        "Decision Tree": decision_tree,
        "SVM": svm,
        "K-Nearest Neighbors": knn,
        "Gradient Boosting": gradient_boosting,
        "Ridge Regression": ridge,
        "Lasso Regression": lasso,
        "Naive Bayes": naive_bayes,
        "XGBoost": xgboost_model,
        "ElasticNet": elasticnet
    }
    
    if selected_model_name in model_mapping:
        try:
            model_module = model_mapping[selected_model_name]
            params = model_module.get_model_params_ui(problem_type)
            
            # Display current parameter values (optional)
            if params:
                with st.expander("📋 Current Model Parameters", expanded=False):
                    for param_name, param_value in params.items():
                        st.write(f"**{param_name}:** {param_value}")
            
        except Exception as e:
            st.error(f"Error getting parameters for {selected_model_name}: {e}")
            params = {}
    else:
        st.error(f"Model {selected_model_name} not found in available models.")
        params = {}
    
    # Train button
    if st.button("Train Model", use_container_width=True):
        try:
            with st.spinner("Training model... Please wait"):
                # Split the data
                test_size = st.session_state.preprocessing_results['test_size']
                X_train, X_test, y_train, y_test = train_test_split(
                    X_processed, y_processed, test_size=test_size, random_state=42, 
                    stratify=y_processed if problem_type == 'classification' else None
                )
                
                # Apply scaling if specified
                scaler = None
                pca = None
                
                if preprocessing_config['scaling_method'] != "None":
                    if preprocessing_config['scaling_method'] == "StandardScaler":
                        scaler = StandardScaler()
                    else:
                        scaler = MinMaxScaler()
                    
                    X_train = scaler.fit_transform(X_train)
                    X_test = scaler.transform(X_test)
                
                # Apply PCA if specified
                if preprocessing_config['apply_pca']:
                    pca = PCA(n_components=0.95)  # Keep 95% variance
                    X_train = pca.fit_transform(X_train)
                    X_test = pca.transform(X_test)
                
                # Create and train the model
                model = create_model_from_module(selected_model_name, params, problem_type)
                if model is None:
                    raise ValueError(f"Failed to create model: {selected_model_name}")
                model.fit(X_train, y_train)
                
                # Calculate training score
                training_score = model.score(X_train, y_train)
                
                # Store everything in session state
                st.session_state.model = model
                st.session_state.X_train = X_train
                st.session_state.X_test = X_test
                st.session_state.y_train = y_train
                st.session_state.y_test = y_test
                st.session_state.scaler = scaler
                st.session_state.pca = pca
                
                # Store training results
                training_results = {
                    'model_name': selected_model_name,
                    'problem_type': problem_type,
                    'training_score': training_score,
                    'hyperparameters': params,
                    'training_completed': True
                }
                
                st.session_state.training_results = training_results
                st.session_state.model_trained = True
                
                # Reset evaluation state
                st.session_state.evaluation_completed = False
                st.session_state.evaluation_results = {}
                
                st.success(f"🎉 Model trained successfully: **{selected_model_name}**")
                st.metric("Training Score", f"{training_score:.4f}")
                
                if pca is not None:
                    explained_var = pca.explained_variance_ratio_.sum()
                    st.info(f"PCA reduced to {pca.n_components_} components explaining {explained_var:.2%} of variance")
                
                st.balloons()
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error during training: {str(e)}")
