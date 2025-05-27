from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
import streamlit as st

def get_model_params_ui():
    """
    Streamlit UI to get Gradient Boosting hyperparameters.
    """
    problem_type = st.radio("Problem Type", options=['regression', 'classification'])

    n_estimators = st.slider("Number of Trees (n_estimators)", 50, 500, 100, step=10)
    learning_rate = st.slider("Learning Rate", 0.01, 1.0, 0.1, step=0.01, format="%.2f")
    max_depth = st.slider("Max Depth of Trees", 1, 20, 3)
    subsample = st.slider("Subsample (for Stochastic Gradient Boosting)", 0.1, 1.0, 1.0, step=0.05, format="%.2f")

    return {
        "problem_type": problem_type,
        "n_estimators": n_estimators,
        "learning_rate": learning_rate,
        "max_depth": max_depth,
        "subsample": subsample
    }

def get_model(params):
    """
    Instantiate and return a Gradient Boosting model based on parameters.
    """
    if params["problem_type"] == "regression":
        model = GradientBoostingRegressor(
            n_estimators=params["n_estimators"],
            learning_rate=params["learning_rate"],
            max_depth=params["max_depth"],
            subsample=params["subsample"],
            random_state=42
        )
    else:
        model = GradientBoostingClassifier(
            n_estimators=params["n_estimators"],
            learning_rate=params["learning_rate"],
            max_depth=params["max_depth"],
            subsample=params["subsample"],
            random_state=42
        )
    return model
