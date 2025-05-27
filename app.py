import streamlit as st
import pandas as pd
import numpy as np
import importlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder


from utils.preprocessing import preprocess_data, get_user_input
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

        # --- Preprocessing ---
        X_train, X_test, y_train, y_test, scaler, label_encoders = preprocess_data(X, y)

        # --- Model Selection ---
        st.subheader("🤖 Choose a Machine Learning Model")
        model_options = {
            "Linear Regression": "linear_regression",
            "Logistic Regression": "logistic_regression",
            "Decision Tree": "decision_tree",
            "Random Forest": "random_forest",
            "Gradient Boosting": "gradient_boosting"
        }
        selected_model_name = st.selectbox("📌 Select Model", list(model_options.keys()))
        model_module_name = model_options[selected_model_name]

        # --- Import Model Dynamically ---
        model_module = importlib.import_module(f"models.{model_module_name}")
        model_params = model_module.get_model_params_ui()
        model = model_module.get_model(model_params)


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
            st.success(f"🎯 Predicted {target_column}: `{user_pred:.2f}`")

else:
    st.info("👆 Upload a dataset to get started.")
