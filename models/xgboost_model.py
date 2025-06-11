# models/xgboost_model.py
from xgboost import XGBRegressor, XGBClassifier
import streamlit as st

def get_model_params_ui(problem_type):
    """
    Use Streamlit widgets to collect XGBoost model parameters dynamically.
    Returns a dictionary of parameters.
    """
    st.markdown("### XGBoost Parameters")

    n_estimators = st.slider("Number of Estimators", 50, 1000, 100, step=50)
    learning_rate = st.slider("Learning Rate", 0.001, 0.5, 0.1, step=0.01)
    max_depth = st.slider("Max Depth", 1, 20, 6)
    subsample = st.slider("Subsample Ratio", 0.1, 1.0, 1.0, step=0.1)
    colsample_bytree = st.slider("Column Subsample by Tree", 0.1, 1.0, 1.0, step=0.1)

    return {
        'n_estimators': n_estimators,
        'learning_rate': learning_rate,
        'max_depth': max_depth,
        'subsample': subsample,
        'colsample_bytree': colsample_bytree
    }

def get_model(params, problem_type):
    """
    Instantiate and return an XGBoost model (regressor or classifier) based on params.
    """
    common_params = {
        'n_estimators': params['n_estimators'],
        'learning_rate': params['learning_rate'],
        'max_depth': params['max_depth'],
        'subsample': params['subsample'],
        'colsample_bytree': params['colsample_bytree'],
        'random_state': 42,
        'verbosity': 0,
        'use_label_encoder': False
    }

    if problem_type == 'regression':
        model = XGBRegressor(**common_params)
    else:
        model = XGBClassifier(**common_params)
    
    return model
