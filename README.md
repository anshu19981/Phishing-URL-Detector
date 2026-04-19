# 🛡️ Phishing URL Detector AI

A high-performance Machine Learning solution designed to identify and classify malicious URLs in real-time. By leveraging lexical analysis and supervised learning, this tool helps protect users from phishing attempts and cyber threats.

## 🚀 Live Demo
Access the interactive web application here:
**[Insert your Hugging Face or Streamlit Link Here]**

## 📊 Project Overview
Phishing is one of the most common cyber-attacks. This project focuses on analyzing the structure (lexical features) of a URL to determine if it is **Safe** or **Phishing** without needing to visit the website itself.

### Key Performance Metrics:
* **Accuracy:** 91.38%
* **ROC AUC Score:** 0.9691
* **Dataset:** 822,000+ URLs sourced from Kaggle (Phishing and Legitimate URLs).
* **Model:** Random Forest Classifier.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Machine Learning:** Scikit-Learn, Pandas, Numpy
* **Model Persistence:** Joblib
* **Deployment:** Hugging Face Spaces / Streamlit Cloud

## 🧠 Feature Engineering
The model makes predictions based on **20 custom lexical features** extracted from the URL string, including:
* `url_length`: Total character count of the URL.
* `domain_length`: Length of the primary domain.
* `num_slash`: Count of forward slashes (indicates depth).
* `suspicious_keywords`: Detection of terms like 'login', 'verify', 'update', 'secure', 'bank'.
* `has_ip_address`: Checks if an IP address is used instead of a hostname.
* `has_https`: Validates the use of secure protocols.
* `num_digits`, `num_dots`, `num_hyphens`: Counts of specific characters often manipulated in phishing links.

## 📂 Project Structure
```text
├── app.py                      # Streamlit web application interface
├── phishing_detector_model.pkl  # Trained Random Forest model (86MB)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
