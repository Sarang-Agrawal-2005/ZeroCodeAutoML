# ML Model Generator

A Streamlit web app to train, evaluate, and predict using multiple machine learning models — easily switch between models, tune hyperparameters, and upload your own datasets.

---

## Features

* Upload your own CSV dataset
* Support for multiple models:

  * Random Forest (regression)
  * Linear Regression
  * Logistic Regression (classification)
  * Decision Tree (classification/regression)
  * Gradient Boosting (classification/regression)
* Interactive hyperparameter tuning with Streamlit UI
* Data preprocessing (encoding, scaling, train/test split)
* Visualizations:

  * Correlation heatmap
  * Actual vs Predicted scatter plot
  * Residual distribution plot
* Model evaluation metrics display
* Predict using custom user input

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/ml_model_generator.git
cd ml_model_generator
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
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

Upload your CSV dataset, select the model, adjust hyperparameters, and start training!

---

## Folder Structure

```
ml_model_generator/
├── app.py                   # Main Streamlit app
├── models/                  # Model modules (random_forest.py, linear_regression.py, etc.)
├── utils/                   # Preprocessing and evaluation utility functions
├── requirements.txt         # Project dependencies
└── README.md                # This file
```

---

## Contributing

Contributions are welcome! Feel free to open issues or pull requests.

---

## License

MIT License

---


