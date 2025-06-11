# models/svm.py
from sklearn.svm import SVR, SVC
import streamlit as st

def get_model_params_ui(problem_type):
    """
    Use Streamlit widgets to collect model parameters dynamically.
    Returns a dictionary of parameters.
    """
    st.markdown("### Support Vector Machine (SVM) Parameters")

    C = st.slider("Regularization Parameter (C)", 0.01, 10.0, 1.0, step=0.01)
    kernel = st.selectbox("Kernel", ['linear', 'poly', 'rbf', 'sigmoid'])
    gamma = st.selectbox("Gamma", ['scale', 'auto'])

    params = {
        'C': C,
        'kernel': kernel,
        'gamma': gamma
    }

    if problem_type == 'classification':
        decision_function_shape = st.sidebar.selectbox("Decision Function Shape", ['ovo', 'ovr'])
        params['decision_function_shape'] = decision_function_shape

    return params

def get_model(params, problem_type):
    """
    Instantiate and return an SVM model (regressor or classifier) based on params.
    """
    if problem_type == 'regression':
        model = SVR(
            C=params['C'],
            kernel=params['kernel'],
            gamma=params['gamma']
        )
    else:
        model = SVC(
            C=params['C'],
            kernel=params['kernel'],
            gamma=params['gamma'],
            decision_function_shape=params.get('decision_function_shape', 'ovr'),
            probability=True  # Enable probability estimates if needed for predict_proba
        )
    return model
