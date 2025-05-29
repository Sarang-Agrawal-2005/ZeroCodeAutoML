# ML Model Generator

A versatile Streamlit web app that enables easy training, evaluation, and prediction with multiple machine learning models. Upload your own datasets, switch between models seamlessly, and tune hyperparameters interactively.

---

## Features

* **Upload your own CSV dataset** for quick experimentation
* **Wide model support** for both regression and classification tasks:

  * Random Forest
  * Linear Regression
  * Logistic Regression
  * Decision Tree
  * Gradient Boosting
  * K-Nearest Neighbors (KNN)
  * Support Vector Machine (SVM)
  * XGBoost
  * Naive Bayes (classification only)
  * Ridge Regression
  * Lasso Regression
  * Elastic Net Regression
* **Automatic detection of problem type** (classification vs regression) based on target variable
* **Interactive hyperparameter tuning** via Streamlit sidebar widgets
* **Data preprocessing pipeline** including encoding, scaling, outlier removal, variance filtering, PCA, and train/test split
* **Feature selection** using correlation thresholds to drop redundant or irrelevant features
* **Visualizations:**

  * Correlation heatmap for feature analysis
  * Actual vs Predicted scatter plot
  * Residual distribution plot
* **Comprehensive model evaluation** with standard metrics displayed
* **Predict on custom user input** with proper handling of categorical and numerical features

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ml_model_generator.git
   cd ml_model_generator
   ```

2. (Optional but recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate       # Linux/macOS
   venv\Scripts\activate          # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

* Upload your CSV file
* Select your target column
* Choose your model and tune hyperparameters
* Preprocess and select features as needed
* Train the model and review evaluation metrics and plots
* Input custom data points for prediction

---

## Project Structure

```
ml_model_generator/
├── app.py                   # Main Streamlit application
├── models/                  # Model definitions with parameter UI
│   ├── random_forest.py
│   ├── linear_regression.py
│   ├── logistic_regression.py
│   ├── decision_tree.py
│   ├── gradient_boosting.py
│   ├── knn.py
│   ├── svm.py
│   ├── xgboost.py
│   ├── naive_bayes.py
│   ├── ridge.py
│   ├── lasso.py
│   └── elastic_net.py
├── utils/                   # Preprocessing, feature selection, and evaluation utilities
│   ├── preprocessing.py
│   └── evaluation.py
├── requirements.txt         # Python dependencies
└── README.md                # This documentation file
```

---

## Contributing

Contributions are welcome! Feel free to:

* Open issues to report bugs or request features
* Submit pull requests to improve functionality or add models

Please follow best practices for code style and testing.

---

## License

This project is licensed under the MIT License.

---


