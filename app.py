import streamlit as st
import pandas as pd
import numpy as np
import importlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

from utils.preprocessing import preprocess_data, get_user_input, feature_selection_by_correlation
from utils.evaluation import evaluate_model

# --- Page Config ---
st.set_page_config(layout="wide", page_title="ZeroCodeAutoML")

# --- Custom Styles ---
st.markdown("""
    <style>
        .main-title {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            color: #4CAF50;
            padding: 20px 0;
        }
        .block-box {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
#st.markdown("<div class='main-title'>🔧 ZeroCodeAutoML</div>", unsafe_allow_html=True)

# --- File Upload ---
#st.markdown("<div class='block-box'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("📁 Upload CSV File", type="csv")
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = df.dropna()

    #st.markdown("<div class='block-box'>", unsafe_allow_html=True)
    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())
    st.markdown("</div>", unsafe_allow_html=True)

    df_encoded = df.copy()
    for col in df_encoded.select_dtypes(include='object').columns:
        df_encoded[col] = LabelEncoder().fit_transform(df_encoded[col])

    numeric_df = df_encoded.select_dtypes(include=[np.number])
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    #st.markdown("<div class='block-box'>", unsafe_allow_html=True)
    st.subheader("📌 Feature Correlation Heatmap")
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    target_column = st.selectbox("🎯 Select Target Column", df.columns)

    if target_column:
        X = df.drop(columns=[target_column])
        y = df[target_column]
        label_encoders = {}
        X_processed = X.copy()

        for col in X_processed.columns:
            if X_processed[col].dtype == 'object':
                X_processed[col] = X_processed[col].fillna(X_processed[col].mode()[0])
            else:
                X_processed[col] = X_processed[col].fillna(X_processed[col].median())

        st.sidebar.subheader("🤖 Choose a Machine Learning Model")
        model_options = {
            "Linear Regression": "linear_regression",
            "Logistic Regression": "logistic_regression",
            "Decision Tree": "decision_tree",
            "Random Forest": "random_forest",
            "Gradient Boosting": "gradient_boosting",
            "K-Nearest Neighbors": "knn",
            "Support Vector Machine": "svm",
            "XGBoost": "xgboost",
            "Naive Bayes": "naive_bayes",
            "Ridge Regression": "ridge",
            "Lasso Regression": "lasso",
            "ElasticNet": "elasticnet"
        }
        selected_model_name = st.sidebar.selectbox("📌 Select Model", list(model_options.keys()))

        problem_type = 'regression'
        if y.dtype == 'object' or str(y.dtype).startswith('category') or y.nunique() <= 10:
            problem_type = 'classification'

        st.info(f"🔍 Detected problem type: **{problem_type.capitalize()}**")

        if selected_model_name in ["Linear Regression", "Ridge Regression", "Lasso Regression", "ElasticNet"] and problem_type != "regression":
            st.warning(f"⚠️ {selected_model_name} requires a numeric target.")
            st.stop()

        if selected_model_name in ["Logistic Regression", "Naive Bayes"] and problem_type != "classification":
            st.warning(f"⚠️ {selected_model_name} requires a categorical/discrete target.")
            st.stop()

        for col in X_processed.select_dtypes(include=['object', 'category']).columns:
            le = LabelEncoder()
            X_processed[col] = le.fit_transform(X_processed[col].astype(str))
            label_encoders[col] = le

        y_encoded = y
        if y.dtype == 'object' or str(y.dtype).startswith('category'):
            le_target = LabelEncoder()
            y_encoded = le_target.fit_transform(y.astype(str))
            label_encoders['target'] = le_target

        X = X_processed
        y = y_encoded

        #st.markdown("<div class='block-box'>", unsafe_allow_html=True)
        st.subheader("🔍 Feature Selection and Preprocessing")

        drop_high_corr = st.checkbox("Drop Highly Correlated Features", value=False)
        high_corr_threshold = st.slider("High Correlation Threshold", 0.5, 0.99, 0.8) if drop_high_corr else 0.8

        drop_low_target_corr = st.checkbox("Drop Weakly Correlated Features", value=False)
        low_target_corr_threshold = st.slider("Low Target Correlation Threshold", 0.0, 1.0, 0.1) if drop_low_target_corr else 0.1

        if not isinstance(y, pd.Series):
            y = pd.Series(data=np.array(y))

        X, dropped = feature_selection_by_correlation(X, y, drop_high_corr, high_corr_threshold, drop_low_target_corr, low_target_corr_threshold)

        use_feature_selection = st.checkbox("Drop low-variance features")
        variance_threshold = st.slider("Variance threshold", 0.0, 0.1, 0.01) if use_feature_selection else 0.0

        use_outlier_removal = st.checkbox("Remove outliers (IQR method)")
        use_pca = st.checkbox("Apply PCA (dimensionality reduction)")
        n_components = st.slider("Number of PCA components", 1, X.shape[1], max(1, X.shape[1] // 2)) if use_pca and X.shape[1] > 1 else None

        st.markdown("</div>", unsafe_allow_html=True)

        X_train, X_test, y_train, y_test, scaler, pca, dropped_variance = preprocess_data(
            X, y, variance_threshold, use_outlier_removal, use_pca, n_components)

        dropped_total = set(dropped + dropped_variance)
        if dropped_total:
            st.success(f"Dropped {len(dropped_total)} features: {', '.join(dropped_total)}")
        else:
            st.info("No features were dropped.")

        model_module_path = f"models.{model_options[selected_model_name]}"
        model_module = importlib.import_module(model_module_path)

        model_params = model_module.get_model_params_ui(problem_type=problem_type)
        model = model_module.get_model(model_params, problem_type=problem_type)

        with st.spinner("Training the model..."):
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

        #st.markdown("<div class='block-box'>", unsafe_allow_html=True)
        st.subheader("📈 Model Evaluation Metrics")
        metrics = evaluate_model(y_test, y_pred)
        for k, v in metrics.items():
            st.markdown(f"- **{k}:** `{v}`")

        st.subheader("📉 Actual vs Predicted")
        fig, ax = plt.subplots()
        sns.scatterplot(x=y_test, y=y_pred, ax=ax)
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        ax.set_xlabel("Actual")
        ax.set_ylabel("Predicted")
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        #st.markdown("<div class='block-box'>", unsafe_allow_html=True)
        st.subheader("🧮 Predict with Custom Input")
        user_input_df = get_user_input(X, label_encoders)
        if user_input_df is not None:
            user_scaled = scaler.transform(user_input_df)
            user_pred = model.predict(user_scaled)[0]

            if 'target' in label_encoders:
                user_pred = label_encoders['target'].inverse_transform([int(round(user_pred))])[0]
                st.success(f"🎯 Predicted {target_column}: `{user_pred}`")
            else:
                st.success(f"🎯 Predicted {target_column}: `{user_pred:.2f}`")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("👆 Upload a dataset to get started.")
