import numpy as np
import pandas as pd
import tensorflow as tf
from joblib import load
import json

# Load the model, scaler, and feature names
try:
    model = tf.keras.models.load_model('heart_disease_model.h5')
    print("Model loaded successfully!")
    
    scaler = load('scaler.joblib')
    print("Scaler loaded successfully!")
    
    with open('feature_names.json', 'r') as f:
        feature_names = json.load(f)
    print("Feature names loaded successfully!")
    
except Exception as e:
    print(f"Error loading model assets: {e}")
    exit(1)

# Sample data for testing (values taken from the dataset)
# This is a sample with heart disease
sample_positive = {
    'age': 63,
    'sex': 1,  # 1 = male, 0 = female
    'cp': 3,   # chest pain type
    'trestbps': 145,  # resting blood pressure
    'chol': 233,  # cholesterol
    'fbs': 1,  # fasting blood sugar > 120 mg/dl
    'restecg': 0,  # resting electrocardiographic results
    'thalach': 150,  # maximum heart rate achieved
    'exang': 0,  # exercise induced angina
    'oldpeak': 2.3,  # ST depression induced by exercise
    'slope': 0,  # slope of the peak exercise ST segment
    'ca': 0,  # number of major vessels colored by fluoroscopy
    'thal': 1  # thalassemia
}

# Sample without heart disease
sample_negative = {
    'age': 67,
    'sex': 1,
    'cp': 0,
    'trestbps': 120,
    'chol': 229,
    'fbs': 0,
    'restecg': 0,
    'thalach': 129,
    'exang': 1,
    'oldpeak': 2.6,
    'slope': 1,
    'ca': 2,
    'thal': 3
}

def predict_heart_disease(patient_data):
    # Convert patient data dictionary to a list, maintaining feature order
    features = []
    for feature in feature_names:
        features.append(patient_data[feature])
    
    # Convert to numpy array and reshape for a single prediction
    features_array = np.array(features).reshape(1, -1)
    
    # Scale the features
    scaled_features = scaler.transform(features_array)
    
    # Make prediction
    prediction = model.predict(scaled_features)
    probability = prediction[0][0]
    
    return probability

# Run predictions on both samples
print("\n--- Heart Disease Risk Prediction ---")
print("Sample 1 (Expected positive): ", end="")
prob_positive = predict_heart_disease(sample_positive)
print(f"Probability: {prob_positive:.4f} - Risk: {'High' if prob_positive > 0.5 else 'Low'}")

print("Sample 2 (Expected negative): ", end="")
prob_negative = predict_heart_disease(sample_negative)
print(f"Probability: {prob_negative:.4f} - Risk: {'High' if prob_negative > 0.5 else 'Low'}") 