import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import (accuracy_score, classification_report, mean_squared_error, 
                           r2_score, confusion_matrix, precision_score, recall_score, f1_score)

def show_page():
    """Display the Model Evaluation page"""
    #st.markdown('<h1 class="main-header">📈 Model Evaluation</h1>', unsafe_allow_html=True)
    
    if not st.session_state.model_trained:
        st.info('''Please train a model first in the "Model Training" page''')
        st.stop()
    
    # Display model info
    st.subheader("Model Information")
    results = st.session_state.training_results
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model", results['model_name'])
    with col2:
        st.metric("Problem Type", results['problem_type'].title())
    with col3:
        st.metric("Training Score", f"{results['training_score']:.4f}")
    
    # Check if we already have evaluation results
    if st.session_state.evaluation_completed and st.session_state.evaluation_results:
        #st.markdown('<div class="success-message">✅ Model evaluation results loaded</div>', unsafe_allow_html=True)
        
        eval_results = st.session_state.evaluation_results
        problem_type = st.session_state.problem_type
        
        if problem_type == "classification":
            st.subheader("Classification Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Accuracy", f"{eval_results['accuracy']:.4f}")
            with col2:
                st.metric("Precision", f"{eval_results['precision']:.4f}")
            with col3:
                st.metric("Recall", f"{eval_results['recall']:.4f}")
            with col4:
                st.metric("F1-Score", f"{eval_results['f1_score']:.4f}")
            
            st.subheader("Detailed Classification Report")
            st.dataframe(eval_results['classification_report'], use_container_width=True)
            
            st.subheader("Confusion Matrix")
            st.plotly_chart(eval_results['confusion_matrix_fig'], use_container_width=True)
            
        else:  # Regression
            st.subheader("Regression Metrics")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("MSE", f"{eval_results['mse']:.4f}")
            with col2:
                st.metric("RMSE", f"{eval_results['rmse']:.4f}")
            with col3:
                st.metric("R² Score", f"{eval_results['r2']:.4f}")
            
            st.subheader("Actual vs Predicted Values")
            st.plotly_chart(eval_results['scatter_fig'], use_container_width=True)
            
            st.subheader("Residuals Analysis")
            st.plotly_chart(eval_results['residuals_fig'], use_container_width=True)
    
    else:
        # Perform evaluation
        if st.button("🔍 Run Evaluation", use_container_width=True):
            try:
                with st.spinner("Evaluating model... Please wait"):
                    model = st.session_state.model
                    X_test = st.session_state.X_test
                    y_test = st.session_state.y_test
                    problem_type = st.session_state.problem_type
                    
                    # Make predictions
                    y_pred = model.predict(X_test)
                    evaluation_results = {}
                    
                    if problem_type == "classification":
                        # Classification metrics
                        accuracy = accuracy_score(y_test, y_pred)
                        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
                        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
                        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
                        
                        # Classification report
                        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
                        
                        # Confusion matrix
                        cm = confusion_matrix(y_test, y_pred)
                        
                        # Store results
                        evaluation_results['accuracy'] = accuracy
                        evaluation_results['precision'] = precision
                        evaluation_results['recall'] = recall
                        evaluation_results['f1_score'] = f1
                        evaluation_results['classification_report'] = pd.DataFrame(report).transpose()
                        
                        # Create confusion matrix figure
                        fig_cm = px.imshow(cm, 
                                         text_auto=True, 
                                         aspect="auto",
                                         title="Confusion Matrix",
                                         color_continuous_scale='Blues',
                                         labels=dict(x="Predicted", y="Actual"))
                        fig_cm.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#FAFAFA',
                            title_font_size=16
                        )
                        evaluation_results['confusion_matrix_fig'] = fig_cm
                        
                    else:  # Regression
                        # Regression metrics
                        mse = mean_squared_error(y_test, y_pred)
                        rmse = np.sqrt(mse)
                        r2 = r2_score(y_test, y_pred)
                        
                        evaluation_results['mse'] = mse
                        evaluation_results['rmse'] = rmse
                        evaluation_results['r2'] = r2
                        
                        # Actual vs Predicted scatter plot
                        fig_scatter = px.scatter(x=y_test, y=y_pred, 
                                               labels={'x': 'Actual Values', 'y': 'Predicted Values'},
                                               title="Actual vs Predicted Values")
                        
                        # Add perfect prediction line
                        min_val = min(min(y_test), min(y_pred))
                        max_val = max(max(y_test), max(y_pred))
                        fig_scatter.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val],
                                                       mode='lines', name='Perfect Prediction',
                                                       line=dict(color='red', dash='dash')))
                        
                        fig_scatter.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#FAFAFA',
                            title_font_size=16
                        )
                        evaluation_results['scatter_fig'] = fig_scatter
                        
                        # Residuals plot
                        residuals = y_test - y_pred
                        fig_residuals = px.scatter(x=y_pred, y=residuals,
                                                 labels={'x': 'Predicted Values', 'y': 'Residuals'},
                                                 title="Residuals vs Predicted Values")
                        
                        # Add horizontal line at y=0
                        fig_residuals.add_hline(y=0, line_dash="dash", line_color="red")
                        
                        fig_residuals.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#FAFAFA',
                            title_font_size=16
                        )
                        evaluation_results['residuals_fig'] = fig_residuals
                    
                    # Store evaluation results
                    st.session_state.evaluation_results = evaluation_results
                    st.session_state.evaluation_completed = True
                    
                    st.success("🎉 Model evaluation completed successfully!")
                    st.balloons()
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error during evaluation: {str(e)}")
