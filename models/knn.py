# models/knn.py
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
import streamlit as st

def get_model_params_ui(problem_type):
    """
    Use Streamlit widgets to collect model parameters dynamically.
    Returns a dictionary of parameters.
    """
    st.markdown("### K-Nearest Neighbors Parameters")

    n_neighbors = st.slider("Number of Neighbors (k)", 1, 50, 5)
    weights = st.selectbox("Weight Function", ['uniform', 'distance'])

    if problem_type == 'regression':
        algorithm_options = ['auto', 'ball_tree', 'kd_tree', 'brute']
    else:
        algorithm_options = ['auto', 'ball_tree', 'kd_tree', 'brute']

    algorithm = st.selectbox("Algorithm", algorithm_options)

    return {
        'n_neighbors': n_neighbors,
        'weights': weights,
        'algorithm': algorithm
    }

def get_model(params, problem_type):
    """
    Instantiate and return a KNN model (regressor or classifier) based on params.
    """
    if problem_type == 'regression':
        model = KNeighborsRegressor(
            n_neighbors=params['n_neighbors'],
            weights=params['weights'],
            algorithm=params['algorithm']
        )
    else:
        model = KNeighborsClassifier(
            n_neighbors=params['n_neighbors'],
            weights=params['weights'],
            algorithm=params['algorithm']
        )
    return model
