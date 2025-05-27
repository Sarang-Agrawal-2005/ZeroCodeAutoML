from sklearn.linear_model import LogisticRegression
import streamlit as st

def get_model_params_ui():
    """
    Display Streamlit UI to collect Logistic Regression hyperparameters.
    """
    penalty = st.selectbox(
        "Penalty",
        options=['l2', 'none', 'l1', 'elasticnet'],
        index=0,
        help="Regularization type"
    )

    solver_options = {
        'none': ['newton-cg', 'lbfgs', 'sag', 'saga'],
        'l2': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'],
        'l1': ['liblinear', 'saga'],
        'elasticnet': ['saga']
    }
    solver = st.selectbox(
        "Solver",
        options=solver_options[penalty],
        index=0,
        help="Algorithm to use in optimization"
    )

    c = st.number_input("Inverse of regularization strength (C)", min_value=0.01, max_value=10.0, value=1.0, step=0.01)

    max_iter = st.slider("Maximum iterations", 50, 500, 100, step=10)

    l1_ratio = None
    if penalty == 'elasticnet':
        l1_ratio = st.slider("L1 ratio (only for elasticnet)", 0.0, 1.0, 0.5, step=0.05)

    return {
        "penalty": penalty,
        "solver": solver,
        "C": c,
        "max_iter": max_iter,
        "l1_ratio": l1_ratio
    }

def get_model(params):
    """
    Returns a LogisticRegression model instance with given parameters.
    """
    # Prepare params dict for sklearn (exclude None values)
    model_params = {
        "penalty": params["penalty"],
        "solver": params["solver"],
        "C": params["C"],
        "max_iter": params["max_iter"],
        "random_state": 42
    }
    if params["penalty"] == "elasticnet":
        model_params["l1_ratio"] = params["l1_ratio"]
    else:
        model_params["l1_ratio"] = None

    # Some solvers require penalty='none' or others - sklearn manages internally

    model = LogisticRegression(**{k:v for k,v in model_params.items() if v is not None})
    return model
