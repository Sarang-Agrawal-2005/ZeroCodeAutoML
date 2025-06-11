from sklearn.linear_model import Ridge
import streamlit as st

def get_model_params_ui(problem_type):
    st.markdown("### Ridge Regression Parameters")

    if problem_type != 'regression':
        st.warning("⚠️ Ridge Regression supports regression only.")
        return {}

    alpha = st.slider("Alpha (Regularization strength)", 0.0, 10.0, 1.0, 0.1)
    solver = st.selectbox(
        "Solver",
        ["auto", "svd", "cholesky", "lsqr", "sparse_cg", "sag", "saga"],
        index=0
    )

    return {
        'alpha': alpha,
        'solver': solver
    }

def get_model(params, problem_type):
    if problem_type != 'regression':
        raise ValueError("Ridge regression only supports regression problems")

    model = Ridge(alpha=params.get('alpha', 1.0), solver=params.get('solver', 'auto'), random_state=42)
    return model
