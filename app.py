import streamlit as st
import pandas as pd
import numpy as np
import importlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder


from utils.preprocessing import preprocess_data, get_user_input, feature_selection_by_correlation
from utils.evaluation import evaluate_model

# --- App Setup ---
st.set_page_config(layout="wide")
st.title("🔧 ZeroCodeAutoML")

# --- File Upload ---
uploaded_file = st.file_uploader("📁 Upload CSV File", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Drop missing values for simplicity
    df = df.dropna()

    st.subheader("📊 Dataset Preview")
    st.write(df.head())

    # Correlation heatmap
    df_encoded = df.copy()
    for col in df_encoded.select_dtypes(include='object').columns:
        df_encoded[col] = LabelEncoder().fit_transform(df_encoded[col])

    numeric_df = df_encoded.select_dtypes(include=[np.number])
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    st.pyplot(fig)

    # --- Select Target Column ---
    target_column = st.selectbox("🎯 Select Target Column", df.columns)

    

    if target_column:
        X = df.drop(columns=[target_column])
        y = df[target_column]

        label_encoders = {}
        X_processed = X.copy()

        # Handle missing values
        if True:
            for col in X_processed.columns:
                if X_processed[col].dtype == 'object':
                    X_processed[col] = X_processed[col].fillna(X_processed[col].mode()[0])
                else:
                    X_processed[col] = X_processed[col].fillna(X_processed[col].median())

        # --- Model Selection ---
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
        model_module_name = model_options[selected_model_name]

        problem_type = 'regression'
        if y.dtype == 'object' or str(y.dtype).startswith('category'):
            problem_type = 'classification'
    
        if pd.api.types.is_numeric_dtype(y):
            unique_values = y.nunique()
            if unique_values <= 10:  # tweak threshold if needed
                problem_type = 'classification'
            else:
                problem_type = 'regression'
    

        st.info(f"🔍 Detected problem type: **{problem_type.capitalize()}**")

        # --- Validate Target Compatibility with Model ---
        regression_only_models = [
            "Linear Regression",
            "Ridge Regression",
            "Lasso Regression",
            "ElasticNet"
        ]

        classification_only_models = [
            "Logistic Regression",
            "Naive Bayes"
        ]

        if selected_model_name in regression_only_models and problem_type != "regression":
            st.warning(f"⚠️ **{selected_model_name}** is a **regression model** and requires a **numeric target**. But the selected target column **'{target_column}'** appears to be categorical or discrete.")
            st.stop()

        elif selected_model_name in classification_only_models and problem_type != "classification":
            st.warning(f"⚠️ **{selected_model_name}** is a **classification model** and requires a **categorical/discrete target**. But **'{target_column}'** appears to be continuous.")
            st.stop()

            

        # Encode categorical columns
        for col in X_processed.select_dtypes(include=['object', 'category']).columns:
            le = LabelEncoder()
            X_processed[col] = le.fit_transform(X_processed[col].astype(str))
            label_encoders[col] = le

        # Encode target if categorical
        y_encoded = y
        if y.dtype == 'object' or str(y.dtype).startswith('category'):
            le_target = LabelEncoder()
            y_encoded = le_target.fit_transform(y.astype(str))
            label_encoders['target'] = le_target

        X = X_processed
        y = y_encoded

        st.subheader("🔍 Feature Selection and Data Preprocessing")

        drop_high_corr = st.checkbox("Drop Highly Correlated Features", value=False)
        high_corr_threshold = None
        if drop_high_corr:
            high_corr_threshold = st.slider("High Correlation Threshold", min_value=0.5, max_value=0.99, value=0.8, step=0.01)

        drop_low_target_corr = st.checkbox("Drop Features Weakly Correlated with Target", value=False)
        low_target_corr_threshold = None
        if drop_low_target_corr:
            low_target_corr_threshold = st.slider("Low Target Correlation Threshold", min_value=0.0, max_value=1.0, value=0.1, step=0.01)

        if not isinstance(y, pd.Series):
            y = pd.Series(y)     # type: ignore

        # Apply correlation-based feature selection
        X, dropped = feature_selection_by_correlation(
            X,
            y, # type: ignore
            drop_high_corr=drop_high_corr,
            high_corr_threshold=high_corr_threshold if high_corr_threshold is not None else 0.8,
            drop_low_target_corr=drop_low_target_corr,
            low_target_corr_threshold=low_target_corr_threshold if low_target_corr_threshold is not None else 0.1
        )



        # Data Preprocessing

        use_feature_selection = st.checkbox("Drop low-variance features")
        variance_threshold = 0.01
        if use_feature_selection:
            variance_threshold = st.slider("Variance threshold", 0.0, 0.1, 0.01)

        use_outlier_removal = st.checkbox("Remove outliers (IQR method)")
        use_pca = st.checkbox("Apply PCA (dimensionality reduction)")
        n_components = None
        if use_pca:
            if X.shape[1] > 1:
                n_components = st.slider(
                    "Number of PCA components", 1, X.shape[1], max(1, int(X.shape[1] / 2))
                )
            else:
                st.warning("Not enough features to apply PCA.")
                use_pca = False  # Disable PCA since it’s invalid



        # --- Preprocessing ---
        X_train, X_test, y_train, y_test, scaler, pca, dropped_variance = preprocess_data(
            X, y, # type: ignore
            variance_threshold=variance_threshold if use_feature_selection else 0.0,
            remove_outliers=use_outlier_removal,
            apply_pca=use_pca,
            pca_components=n_components
        )

        all_dropped_features = set(dropped + dropped_variance)
        if all_dropped_features:
            st.success(f"Dropped {len(all_dropped_features)} features: {', '.join(all_dropped_features)}")
        else:
            st.info("No features were dropped.")

        
        

        # --- Import Model Dynamically ---
        model_module_name = model_options[selected_model_name]
        model_module = importlib.import_module(f"models.{model_module_name}")

        model_params = model_module.get_model_params_ui(problem_type=problem_type)
        model = model_module.get_model(model_params, problem_type=problem_type)




        # --- Model Training ---
        with st.spinner("Training the model..."):
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

        # --- Evaluation ---
        st.subheader("📈 Model Evaluation Metrics")
        metrics = evaluate_model(y_test, y_pred)
        for k, v in metrics.items():
            st.markdown(f"- **{k}:** `{v}`")

        # --- Actual vs Predicted ---
        st.subheader("📉 Actual vs Predicted")
        fig, ax = plt.subplots()
        sns.scatterplot(x=y_test, y=y_pred, ax=ax)
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        ax.set_xlabel("Actual")
        ax.set_ylabel("Predicted")
        st.pyplot(fig)

        # --- Predict Custom Input ---
        st.subheader("🧮 Predict with Custom Input")
        user_input_df = get_user_input(X, label_encoders)
        if user_input_df is not None:
            user_scaled = scaler.transform(user_input_df)
            user_pred = model.predict(user_scaled)[0]

            # Decode prediction if target was categorical
            if 'target' in label_encoders:
                user_pred = label_encoders['target'].inverse_transform([int(round(user_pred))])[0]  # type: ignore
                st.success(f"🎯 Predicted {target_column}: `{user_pred}`")
            else:
                st.success(f"🎯 Predicted {target_column}: `{user_pred:.2f}`")


else:
    st.info("👆 Upload a dataset to get started.")





    
