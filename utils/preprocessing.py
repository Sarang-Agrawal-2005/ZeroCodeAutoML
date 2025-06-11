import pandas as pd
import numpy as np

def remove_outliers_iqr(df, columns):
    """Remove outliers using IQR method"""
    df_clean = df.copy()
    outliers_removed = 0
    
    for column in columns:
        if df_clean[column].dtype in ['int64', 'float64']:
            Q1 = df_clean[column].quantile(0.25)
            Q3 = df_clean[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            initial_count = len(df_clean)
            df_clean = df_clean[(df_clean[column] >= lower_bound) & (df_clean[column] <= upper_bound)]
            outliers_removed += initial_count - len(df_clean)
    
    return df_clean, outliers_removed

def feature_selection_by_correlation(X, y, drop_high_corr=True, high_corr_threshold=0.8, 
                                   drop_low_target_corr=False, low_target_corr_threshold=0.1):
    """Feature selection based on correlation"""
    dropped_features = []
    X_processed = X.copy()
    
    # Calculate correlation matrix
    corr_matrix = X_processed.corr()
    
    # Drop highly correlated features
    if drop_high_corr:
        upper_triangle = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        high_corr_features = [column for column in upper_triangle.columns if any(upper_triangle[column].abs() > high_corr_threshold)]
        X_processed = X_processed.drop(columns=high_corr_features)
        dropped_features.extend(high_corr_features)
    
    # Drop features with low correlation to target
    if drop_low_target_corr:
        target_corr = X_processed.corrwith(pd.Series(y)).abs()
        low_target_corr_features = target_corr[target_corr < low_target_corr_threshold].index.tolist()
        X_processed = X_processed.drop(columns=low_target_corr_features)
        dropped_features.extend(low_target_corr_features)
    
    return X_processed, dropped_features
