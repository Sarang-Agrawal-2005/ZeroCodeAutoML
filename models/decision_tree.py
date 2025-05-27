from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
import streamlit as st

def get_model_params_ui():
    """
    Display Streamlit widgets to select Decision Tree hyperparameters.
    """
    max_depth = st.slider("Maximum Depth", 1, 50, 10)
    min_samples_split = st.slider("Minimum Samples Split", 2, 20, 2)
    min_samples_leaf = st.slider("Minimum Samples Leaf", 1, 20, 1)
    criterion_options_reg = ['squared_error', 'friedman_mse', 'absolute_error', 'poisson']
    criterion_options_clf = ['gini', 'entropy', 'log_loss']

    problem_type = st.radio("Problem Type", options=['regression', 'classification'])

    if problem_type == 'regression':
        criterion = st.selectbox("Criterion", criterion_options_reg, index=0)
    else:
        criterion = st.selectbox("Criterion", criterion_options_clf, index=0)

    return {
        'max_depth': max_depth,
        'min_samples_split': min_samples_split,
        'min_samples_leaf': min_samples_leaf,
        'criterion': criterion,
        'problem_type': problem_type
    }

def get_model(params):
    """
    Return a Decision Tree model instance (regressor or classifier) based on params.
    """
    if params['problem_type'] == 'regression':
        model = DecisionTreeRegressor(
            max_depth=params['max_depth'],
            min_samples_split=params['min_samples_split'],
            min_samples_leaf=params['min_samples_leaf'],
            criterion=params['criterion'],
            random_state=42
        )
    else:
        model = DecisionTreeClassifier(
            max_depth=params['max_depth'],
            min_samples_split=params['min_samples_split'],
            min_samples_leaf=params['min_samples_leaf'],
            criterion=params['criterion'],
            random_state=42
        )
    return model
