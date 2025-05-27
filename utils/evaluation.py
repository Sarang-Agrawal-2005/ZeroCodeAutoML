from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error,
    explained_variance_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
import numpy as np

def evaluate_regression(y_true, y_pred):
    """
    Calculate and return common regression metrics as a dict.
    """
    mse = float(mean_squared_error(y_true, y_pred))
    rmse = float(np.sqrt(mse))
    mae = float(mean_absolute_error(y_true, y_pred))
    mape = float(mean_absolute_percentage_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    explained_var = float(explained_variance_score(y_true, y_pred))

    return {
        "Mean Squared Error (MSE)": round(mse, 4),
        "Root Mean Squared Error (RMSE)": round(rmse, 4),
        "Mean Absolute Error (MAE)": round(mae, 4),
        "Mean Absolute Percentage Error (MAPE)": f"{mape:.2%}",  # formatted as string
        "R² Score": round(r2, 4),
        "Explained Variance Score": round(explained_var, 4),
    }

def evaluate_classification(y_true, y_pred):
    """
    Calculate and return common classification metrics as a dict.
    """
    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, average='weighted', zero_division=0))
    rec = float(recall_score(y_true, y_pred, average='weighted', zero_division=0))
    f1 = float(f1_score(y_true, y_pred, average='weighted', zero_division=0))
    cm = confusion_matrix(y_true, y_pred)

    return {
        "Accuracy": round(acc, 4),
        "Precision": round(prec, 4),
        "Recall": round(rec, 4),
        "F1 Score": round(f1, 4),
        "Confusion Matrix": cm.tolist()  # convert numpy array to list for display
    }

def evaluate_model(y_true, y_pred):
    """
    Auto-detects problem type (regression or classification)
    and returns appropriate evaluation metrics.
    """
    # If output is continuous float-like => regression
    if (y_pred.dtype.kind in 'fc') and len(set(y_true)) > 10:
        return evaluate_regression(y_true, y_pred)
    else:
        return evaluate_classification(y_true, y_pred)
