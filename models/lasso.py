from sklearn.linear_model import Lasso
import streamlit as st

def get_model_params_ui(problem_type):
    st.sidebar.markdown("### Lasso Regression Parameters")

    if problem_type != 'regression':
        st.warning("⚠️ Lasso Regression supports regression only.")
        return {}

    alpha = st.sidebar.slider("Alpha (Regularization strength)", 0.0, 10.0, 1.0, 0.1)
    max_iter = st.sidebar.slider("Max Iterations", 100, 5000, 1000, step=100)

    return {
        'alpha': alpha,
        'max_iter': max_iter
    }

def get_model(params, problem_type):
    if problem_type != 'regression':
        raise ValueError("Lasso regression only supports regression problems")

    model = Lasso(alpha=params.get('alpha', 1.0), max_iter=params.get('max_iter', 1000), random_state=42)
    return model
