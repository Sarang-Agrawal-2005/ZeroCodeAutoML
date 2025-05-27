from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import streamlit as st

def get_model_params_ui():
    """
    Use Streamlit widgets to collect model parameters dynamically.
    Returns a dictionary of parameters.
    """
    n_estimators = st.slider("Number of Trees (n_estimators)", 10, 500, 100, step=10)
    max_depth = st.slider("Max Depth of Trees", 1, 50, 10)
    criterion_options = ['squared_error', 'absolute_error']  # Regression criteria
    criterion = st.selectbox("Criterion", criterion_options, index=0)

    return {
        'n_estimators': n_estimators,
        'max_depth': max_depth,
        'criterion': criterion
    }

def get_model(params, problem_type='regression'):
    """
    Instantiate and return a Random Forest model.
    problem_type: 'regression' or 'classification' (default: regression)
    """
    if problem_type == 'regression':
        model = RandomForestRegressor(
            n_estimators=params['n_estimators'],
            max_depth=params['max_depth'],
            criterion=params['criterion'],
            random_state=42
        )
    else:
        # For classification
        model = RandomForestClassifier(
            n_estimators=params['n_estimators'],
            max_depth=params['max_depth'],
            criterion='gini',  # typical default for classification
            random_state=42
        )
    return model
