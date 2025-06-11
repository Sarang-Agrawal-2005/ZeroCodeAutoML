from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
import streamlit as st

def get_model_params_ui(problem_type):
    st.markdown("### Naive Bayes Parameters")
    
    # Naive Bayes is classification-only; no parameters for regression
    if problem_type != 'classification':
        st.warning("⚠️ Naive Bayes supports classification only.")
        return {}

    nb_type = st.selectbox(
        "Select Naive Bayes Type",
        ["GaussianNB", "MultinomialNB", "BernoulliNB"]
    )

    # MultinomialNB and BernoulliNB have alpha smoothing parameter
    alpha = 1.0
    if nb_type in ["MultinomialNB", "BernoulliNB"]:
        alpha = st.slider("Smoothing parameter alpha", 0.0, 5.0, 1.0, 0.1)

    return {
        'nb_type': nb_type,
        'alpha': alpha
    }

def get_model(params, problem_type):
    if problem_type != 'classification':
        raise ValueError("Naive Bayes only supports classification problems")

    nb_type = params.get('nb_type', "GaussianNB")
    alpha = params.get('alpha', 1.0)

    if nb_type == "GaussianNB":
        model = GaussianNB()
    elif nb_type == "MultinomialNB":
        model = MultinomialNB(alpha=alpha)
    elif nb_type == "BernoulliNB":
        model = BernoulliNB(alpha=alpha)
    else:
        model = GaussianNB()

    return model
