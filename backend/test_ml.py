import os
import sys
import json

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.models.text_classifier_ensemble import ensemble_predict, load_vanguard_v85

text = """
Machine learning is a branch of Artificial Intelligence that focuses on developing models and algorithms that let computers learn from data without being explicitly programmed for every task.  In simple words, ML teaches systems to think and understand like humans by learning from the data.
how_machine_learning_works_.webphow_machine_learning_works:
Machine Learning is mainly divided into three core types:
Supervised Learning: Trains models on labeled data to predict or classify new, unseen data.  Unsupervised Learning: Finds patterns or groups in unlabeled data, like clustering or dimensionality reduction.  Reinforcement Learning: Learns through trial and error to maximize rewards, ideal for decision-making tasks.  Note: The following are not part of the original three core types of ML, but they have become increasingly important in real-world applications, especially in deep learning.
Additional Types: Self-Supervised Learning: It is often considered as a subset of unsupervised learning, but it has grown into its own field due to its success in training large-scale models.  It generates its own labels from the data, without any manual labeling.  Semi-Supervised Learning: This approach combines a small amount of labeled data with a large amount of unlabeled data.  It’s useful when labeling data is expensive or time-consuming.  Module 1: Machine Learning Pipeline This section covers preprocessing, exploratory data analysis and model evaluation to prepare data, uncover insights and build reliable models.  Data Preprocessing ML workflow Data Cleaning Data Preprocessing in Python Feature Scaling Feature Extraction Feature Engineering Feature Selection Techniques 2.  Exploratory Data Analysis Exploratory Data Analysis Exploratory Data Analysis in Python Advance EDA Time Series Data Visualization 3.  Model Evaluation Regularization in Machine Learning Confusion Matrix Precision, Recall and F1-Score AUC-ROC Curve Cross-validation Hyperparameter Tuning Module 2: Supervised Learning Supervised learning algorithms are generally categorized into two main types: Classification: where the goal is to predict discrete labels or categories Regression: where the aim is to
"""

load_vanguard_v85()
res = ensemble_predict(text)

with open("ml_res.json", "w") as f:
    json.dump(res, f, indent=2)
