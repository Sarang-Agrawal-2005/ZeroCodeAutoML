import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import streamlit as st
import pandas.api.types as ptypes  # pandas type checks
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
from pandas.api.types import is_numeric_dtype
from typing import Union



def preprocess_data(
    X_processed: pd.DataFrame,
    y_encoded: Union[pd.Series, np.ndarray],
    variance_threshold=0.0,
    remove_outliers=False,
    apply_pca=False,
    pca_components=None,
    test_size=0.2,
    random_state=42
):
    """
    Preprocesses data with options for:
    - Outlier removal
    - Feature selection (low variance)
    - Scaling
    - PCA

    Returns:
    X_train_scaled, X_test_scaled, y_train, y_test, scaler, pca
    """

    
    # Outlier removal (IQR method)
    if remove_outliers:
        if isinstance(X_processed, pd.DataFrame) and isinstance(y_encoded, (pd.Series, np.ndarray)):
            Q1 = X_processed.quantile(0.25)
            Q3 = X_processed.quantile(0.75)
            IQR = Q3 - Q1

            # Calculate mask on X_processed (boolean Series aligned with X_processed)
            mask = ~((X_processed < (Q1 - 1.5 * IQR)) | (X_processed > (Q3 + 1.5 * IQR))).any(axis=1)

            # Ensure y_encoded is a Series with matching index
            if not isinstance(y_encoded, pd.Series):
                y_encoded = pd.Series(y_encoded, index=X_processed.index)
            else:
                if not y_encoded.index.equals(X_processed.index):
                    y_encoded.index = X_processed.index

            # Apply mask to both
            X_processed = X_processed.loc[mask]
            y_encoded = y_encoded.loc[mask]

            if X_processed.shape[0] == 0:
                st.warning(
                    "⚠️ All data rows were removed during outlier filtering.\n"
                    "This indicates that your data may contain extreme values or is too small.\n"
                    "Please review your dataset or consider disabling outlier removal."
                )
                st.stop()



    dropped_variance_features = []

    # Feature selection (low variance)
    if variance_threshold > 0.0:
        if X_processed.shape[0] == 0 or X_processed.shape[1] == 0:
            st.warning("⚠️ No data left after outlier removal or previous preprocessing steps.\n"
               "Please review your parameters or your dataset.")
            st.stop()

        selector = VarianceThreshold(threshold=variance_threshold)
        selector.fit(X_processed)
        mask = selector.get_support()
        dropped_variance_features = list(X_processed.columns[~mask])
        X_processed = pd.DataFrame(
            selector.fit_transform(X_processed),
            columns=X_processed.columns[mask],
            index=X_processed.index
        )

        if X_processed.shape[1] == 0:
            st.warning("⚠️ All features were removed due to low variance filtering.\n"
                "Try lowering the threshold or improving feature engineering.")
            st.stop()

    else:
        X_processed = X_processed.copy()

    if X_processed.shape[0] == 0 or X_processed.shape[1] == 0:
        st.warning("No data left after preprocessing steps. "
            "Please check if your feature selection or outlier removal parameters are too aggressive.")  
        st.stop()

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y_encoded, test_size=test_size, random_state=random_state
    )

    # Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # PCA
    pca = None
    if apply_pca and pca_components is not None:
        pca = PCA(n_components=pca_components)
        X_train_scaled = pca.fit_transform(X_train_scaled)
        X_test_scaled = pca.transform(X_test_scaled)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, pca, dropped_variance_features


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



def feature_selection_by_correlation(
    X: pd.DataFrame,
    y: pd.Series,
    drop_high_corr: bool = False,
    high_corr_threshold: float = 0.8,
    drop_low_target_corr: bool = False,
    low_target_corr_threshold: float = 0.1
):
    """
    Drops features based on correlation with other features and correlation with the target.

    Returns:
    - X_selected: DataFrame with selected features
    - dropped_features: List of dropped feature names
    """

    # Ensure both X and y are numeric
    numeric_X = X.select_dtypes(include=[np.number]).copy()
    numeric_y = y if is_numeric_dtype(y) else None

    # Drop y from X if it's accidentally included
    if y.name in numeric_X.columns:
        numeric_X.drop(columns=[y.name], inplace=True)  

    dropped_features = set()

    # Compute feature-feature correlation
    corr_matrix = numeric_X.corr().abs().fillna(0)

    if drop_high_corr:
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        for col in upper.columns:
            for idx in upper.index:
                value = upper.loc[idx, col]
                if pd.notna(value) and isinstance(value, (int, float)) and value > high_corr_threshold:
                    # Compare target correlation to decide which one to drop
                    col_corr = numeric_X[col].corr(numeric_y) if numeric_y is not None else 0
                    idx_corr = numeric_X[idx].corr(numeric_y) if numeric_y is not None else 0
                    if col_corr < idx_corr:
                        dropped_features.add(col)
                    else:
                        dropped_features.add(idx)

    if drop_low_target_corr and numeric_y is not None:
        target_corr = numeric_X.apply(lambda col: col.corr(numeric_y)).abs()
        for feature, corr_val in target_corr.items():
            if isinstance(corr_val, (int, float)) and corr_val < low_target_corr_threshold: # type: ignore
                dropped_features.add(feature)

    X_selected = X.drop(columns=list(dropped_features)) if dropped_features else X.copy()
    return X_selected, list(dropped_features)





def correlation_feature_selection_ui(X, y):
    st.header("Feature Selection by Correlation")

    drop_high_corr = st.checkbox("Drop features highly correlated with others")
    high_corr_threshold = st.slider(
        "High correlation threshold", min_value=0.5, max_value=1.0, value=0.8, step=0.05
    ) if drop_high_corr else 0.8

    drop_low_target_corr = st.checkbox("Drop features weakly correlated with the target")
    low_target_corr_threshold = st.slider(
        "Low target correlation threshold", min_value=0.0, max_value=0.5, value=0.1, step=0.01
    ) if drop_low_target_corr else 0.1

    if st.button("Apply Feature Selection"):
        X_new, dropped = feature_selection_by_correlation(
            X, y,
            drop_high_corr=drop_high_corr,
            high_corr_threshold=high_corr_threshold,
            drop_low_target_corr=drop_low_target_corr,
            low_target_corr_threshold=low_target_corr_threshold
        )
        if X_new.shape[1] == 0:
            st.warning(
                "⚠️ All features were dropped by the selection criteria.\n"
                "Try lowering the thresholds or review your data and feature engineering."
            )
            st.stop()
            return X  # return original data to avoid breaking the pipeline
        else:
            st.success(f"Dropped features: {dropped}")
            st.write(f"Remaining features: {list(X_new.columns)}")
            return X_new

    return X


# Usage example (replace with your data):
# X_processed = correlation_feature_selection_ui(X_processed, y_encoded)

     

