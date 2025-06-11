from sklearn.linear_model import LinearRegression
import streamlit as st

def get_model_params_ui(problem_type):
    """
    Display Streamlit UI widgets for Linear Regression parameters.
    """
    fit_intercept = st.checkbox("Fit Intercept", value=True)
    n_jobs = st.slider("Number of Jobs for parallelism (n_jobs)", 1, 8, 1)

    return {
        "fit_intercept": fit_intercept,
        "n_jobs": n_jobs
    }

def get_model(params,problem_type):
    """
    Returns an untrained LinearRegression model instance with given parameters.
    """
    model = LinearRegression(
        fit_intercept=params["fit_intercept"],
        n_jobs=params["n_jobs"]
    )
    return model
