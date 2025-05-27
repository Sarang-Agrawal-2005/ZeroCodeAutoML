import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import streamlit as st
import pandas.api.types as ptypes  # pandas type checks

def preprocess_data(X: pd.DataFrame, y: pd.Series, test_size=0.2, random_state=42):
    """
    Preprocesses data by encoding categorical variables, scaling features,
    and splitting into train/test sets.

    Returns:
    X_train_scaled, X_test_scaled, y_train, y_test, scaler, label_encoders
    """

    # Encode categorical columns in features
    label_encoders = {}
    X_encoded = X.copy()
    for col in X.select_dtypes(include=['object', 'category']).columns:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X_encoded[col].astype(str))
        label_encoders[col] = le

    # If target is categorical, encode it too
    y_encoded = y
    if y.dtype == 'object' or str(y.dtype).startswith('category'):
        le_target = LabelEncoder()
        y_encoded = le_target.fit_transform(y.astype(str))
        label_encoders['target'] = le_target

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y_encoded, test_size=test_size, random_state=random_state
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, label_encoders

def get_user_input(X: pd.DataFrame, label_encoders: dict):
    """
    Dynamically creates Streamlit inputs for each feature column.
    Applies label encoding where needed.
    Returns a single-row DataFrame of user inputs or None if no input yet.
    """

    st.write("🔧 Enter values for each feature to predict:")

    input_data = {}
    for col in X.columns:
        dtype = X[col].dtype

        if pd.api.types.is_numeric_dtype(dtype):
            val = st.number_input(f"{col}", value=float(X[col].median()))
        else:
            val = st.text_input(f"{col}", value=str(X[col].mode()[0]))

        input_data[col] = val

    if st.button("Predict"):
        input_df = pd.DataFrame([input_data])

        # Apply label encoders to categorical columns
        for col in input_df.columns:
            if col in label_encoders:
                le = label_encoders[col]
                try:
                    input_df[col] = le.transform([input_df[col][0]])
                except ValueError:
                    st.error(f"Unknown category '{input_df[col][0]}' in column '{col}'. Please enter a known category.")
                    return None
            else:
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce')

        return input_df

    return None

