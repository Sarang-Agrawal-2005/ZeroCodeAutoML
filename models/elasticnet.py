from sklearn.linear_model import ElasticNet
import streamlit as st

def get_model_params_ui(problem_type):
    st.markdown("### ElasticNet Regression Parameters")

    if problem_type != 'regression':
        st.warning("⚠️ ElasticNet supports regression only.")
        return {}

    alpha = st.slider("Alpha (Regularization strength)", 0.0, 10.0, 1.0, 0.1)
    l1_ratio = st.slider("L1 Ratio (between Lasso and Ridge)", 0.0, 1.0, 0.5, 0.01)
    max_iter = st.slider("Max Iterations", 100, 5000, 1000, step=100)

    return {
        'alpha': alpha,
        'l1_ratio': l1_ratio,
        'max_iter': max_iter
    }

def get_model(params, problem_type):
    if problem_type != 'regression':
        raise ValueError("ElasticNet supports regression problems only")

    model = ElasticNet(
        alpha=params.get('alpha', 1.0),
        l1_ratio=params.get('l1_ratio', 0.5),
        max_iter=params.get('max_iter', 1000),
        random_state=42
    )
    return model
