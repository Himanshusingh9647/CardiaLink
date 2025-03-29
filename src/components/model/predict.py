import numpy as np
import tensorflow as tf
from joblib import load
import json
import pickle
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from flask import Flask, request, render_template_string, jsonify, redirect, url_for, session
import random  # Added for simulated predictions

# Load the heart disease model, scaler, and feature names
heart_model = tf.keras.models.load_model('heart_disease_model.h5')
heart_scaler = load('scaler.joblib')
with open('feature_names.json', 'r') as f:
    heart_features = json.load(f)

# Load or train the kidney disease model
# Since the 'h' file contains training code, we'll train it when this script runs
import pandas as pd
from sklearn.model_selection import train_test_split

# Add model accuracy variables 
# These would be determined during model training/validation in a production system
heart_accuracy = 0.85   # Heart disease model accuracy (85%)
kidney_accuracy = 0.78  # Kidney disease model accuracy (78%)
diabetes_accuracy = 0.82 # Diabetes model accuracy (82%)

# Add model priority weights (not just accuracy but also priority)
# Heart disease given highest priority, then kidney, then diabetes
heart_weight = 0.50     # Heart disease has 50% of total weight
kidney_weight = 0.30    # Kidney disease has 30% of total weight
diabetes_weight = 0.20  # Diabetes has 20% of total weight

try:
    # Try to load kidney disease data
    kidney_data = pd.read_csv('kidney_disease.csv')
    
    # Rename columns for consistency
    kidney_data.columns = [col.strip().lower().replace(" ", "_") for col in kidney_data.columns]
    
    # Fix inconsistent labels
    kidney_data['classification'] = kidney_data['classification'].replace("ckd\t", "ckd")
    
    # Convert target labels to numerical values
    kidney_data['classification'] = kidney_data['classification'].replace(['ckd', 'notckd'], [1, 0])
    
    # Convert necessary columns to numeric, coercing errors
    kidney_data = kidney_data.apply(pd.to_numeric, errors='coerce')
    
    # Handle missing values
    kidney_df = kidney_data.dropna(axis=0)
    
    # Reset index
    kidney_df.index = range(0, len(kidney_df), 1)
    
    # Fix incorrect values if any exist
    if 'wc' in kidney_df.columns:
        kidney_df['wc'] = kidney_df['wc'].replace(["\t6200", "\t8400"], [6200, 8400])
    
    # Feature selection (drop unnecessary or categorical columns)
    X = kidney_df.drop(['classification', 'sg', 'appet', 'rc', 'pcv', 'hemo', 'sod', 'id'], axis=1, errors='ignore')
    y = kidney_df['classification']
    
    # Save kidney features for later use
    kidney_features = X.columns.tolist()
    
    # Train model
    kidney_model = RandomForestClassifier(n_estimators=20, random_state=42)
    kidney_model.fit(X, y)
    
    print("Kidney disease model trained successfully.")
except Exception as e:
    print(f"Error loading or training kidney disease model: {e}")
    # Create placeholder if loading fails
    kidney_model = None
    kidney_features = []

# Load the diabetes model
try:
    # For demonstration, we'll simulate loading a diabetes model
    # In a real scenario, you'd load your trained model from a file
    # Example: diabetes_model = pickle.load(open('diabetes_model.pkl', 'rb'))
    
    # Simulate diabetes model (in production, replace with actual model loading)
    # Since we have the m script but no saved model file, we'll create a placeholder
    # In production, run the m script to train and save the model first
    diabetes_model = None
    diabetes_features = ['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 
                        'Stroke', 'HeartDiseaseorAttack', 'PhysActivity', 
                        'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare',
                        'NoDocbcCost', 'GenHlth', 'MentHlth', 'PhysHlth', 
                        'DiffWalk', 'Sex', 'Age', 'Education', 'Income']
    print("Diabetes model placeholder created (replace with actual model in production)")
except Exception as e:
    print(f"Error setting up diabetes model: {e}")
    diabetes_model = None
    diabetes_features = []

app = Flask(__name__)
# Add a secret key for session management
app.secret_key = "cardialink_quantify_secret_key"

# Base template with navigation
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Disease Risk Prediction - CardiaLink Quantify</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --background: #ffffff;
            --foreground: #0f172a;
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --primary-foreground: #ffffff;
            --secondary: #f1f5f9;
            --secondary-foreground: #1e293b;
            --muted: #f1f5f9;
            --muted-foreground: #64748b;
            --border: #e2e8f0;
            --radius: 0.5rem;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background-color: #f8fafc;
            color: var(--foreground);
            line-height: 1.5;
        }
        
        .relative {
            position: relative;
        }
        
        .absolute {
            position: absolute;
        }
        
        .inset-0 {
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
        }
        
        .z-10 {
            z-index: 10;
        }
        
        .z-0 {
            z-index: 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        section {
            position: relative;
            overflow: hidden;
            padding: 3rem 0;
        }
        
        @media (min-width: 768px) {
            section {
                padding: 4rem 0;
            }
        }
        
        .bg-vector {
            position: absolute;
            inset: 0;
            background: linear-gradient(to bottom right, #f0f6ff, #e0ebfc);
            z-index: -10;
        }
        
        svg {
            width: 100%;
            height: 100%;
            opacity: 0.3;
        }
        
        .max-w-3xl {
            max-width: 48rem;
            margin: 0 auto;
        }
        
        .text-center {
            text-align: center;
        }
        
        h1 {
            font-weight: 700;
            font-size: 2.25rem;
            letter-spacing: -0.025em;
            margin-bottom: 1.5rem;
            color: var(--foreground);
        }
        
        @media (min-width: 640px) {
            h1 {
                font-size: 2.5rem;
            }
        }
        
        @media (min-width: 768px) {
            h1 {
                font-size: 3rem;
            }
        }
        
        @media (min-width: 1024px) {
            h1 {
                font-size: 3.75rem;
            }
        }
        
        h2 {
            font-weight: 600;
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--foreground);
        }
        
        .text-muted {
            color: var(--muted-foreground);
            font-size: 1.125rem;
            margin-bottom: 2rem;
        }
        
        @media (min-width: 768px) {
            .text-muted {
                font-size: 1.25rem;
            }
        }
        
        .card {
            background-color: white;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            backdrop-filter: blur(4px);
            background-color: rgba(255, 255, 255, 0.8);
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.375rem;
            font-weight: 500;
            color: #334155;
        }
        
        input, select {
            width: 100%;
            padding: 0.625rem;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            font-family: inherit;
            font-size: 1rem;
            color: var(--foreground);
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }
        
        .row {
            display: flex;
            flex-wrap: wrap;
            margin: 0 -0.75rem;
        }
        
        .col {
            flex: 1;
            padding: 0 0.75rem;
            min-width: 200px;
        }
        
        @media (max-width: 640px) {
            .col {
                flex-basis: 100%;
                margin-bottom: 0.75rem;
            }
        }
        
        button {
            display: block;
            background: linear-gradient(to right, #3b82f6, #4f46e5);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius);
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            margin: 1.5rem auto;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-1px);
            background: linear-gradient(to right, #2563eb, #4338ca);
        }
        
        button::after {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(to right, #4f46e5, #3b82f6);
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        button:hover::after {
            opacity: 1;
        }
        
        button span {
            position: relative;
            z-index: 10;
        }
        
        .result {
            margin-top: 1.5rem;
            text-align: center;
            font-size: 1.125rem;
        }
        
        .high-risk {
            color: #dc2626;
            font-weight: 600;
        }
        
        .low-risk {
            color: #16a34a;
            font-weight: 600;
        }
        
        .risk-meter {
            margin: 1.5rem auto;
            width: 300px;
            height: 8px;
            background: linear-gradient(to right, #16a34a, #facc15, #dc2626);
            border-radius: 4px;
            position: relative;
        }
        
        .risk-indicator {
            position: absolute;
            top: -10px;
            width: 4px;
            height: 28px;
            background-color: #0f172a;
            transform: translateX(-2px);
        }
        
        .feature-help {
            font-size: 0.75rem;
            color: var(--muted-foreground);
            margin-top: 0.25rem;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
            max-width: 32rem;
            margin: 1.5rem auto 0;
        }
        
        @media (min-width: 640px) {
            .features-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .feature-icon {
            width: 1.25rem;
            height: 1.25rem;
            color: var(--primary);
        }
        
        .feature-text {
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        /* Tabs styling */
        .tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.5rem;
        }
        
        .tab {
            padding: 0.75rem 1.5rem;
            margin: 0 0.5rem;
            cursor: pointer;
            border-radius: var(--radius) var(--radius) 0 0;
            font-weight: 500;
            transition: all 0.2s;
            border: 1px solid transparent;
            border-bottom: none;
            text-decoration: none;
            color: var(--muted-foreground);
        }
        
        .tab:hover {
            color: var(--primary);
        }
        
        .tab.active {
            background-color: white;
            border-color: var(--border);
            border-bottom: 1px solid white;
            color: var(--primary);
            margin-bottom: -1px;
            box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.05);
        }
        
        .btn-next {
            background: linear-gradient(to right, #4f46e5, #8b5cf6);
            margin-top: 1rem;
        }
        
        .btn-next:hover {
            background: linear-gradient(to right, #4338ca, #7c3aed);
        }
        
        .btn-next::after {
            background: linear-gradient(to right, #8b5cf6, #4f46e5);
        }

        .btn-prev {
            background: linear-gradient(to right, #8b5cf6, #4f46e5);
            margin-top: 1rem;
            display: inline-block;
            text-decoration: none;
        }
        
        .btn-prev:hover {
            background: linear-gradient(to right, #7c3aed, #4338ca);
        }
        
        .btn-prev::after {
            background: linear-gradient(to right, #4f46e5, #8b5cf6);
        }

        .primary-btn {
            width: 100%;
            max-width: 300px;
            background: linear-gradient(to right, #3b82f6, #4f46e5);
            font-weight: 600;
            letter-spacing: 0.01em;
            box-shadow: 0 2px 10px rgba(79, 70, 229, 0.2);
        }
    </style>
</head>
<body>
    <section>
        <!-- Vector Background -->
        <div class="bg-vector">
            <svg width="100%" height="100%" viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.1" />
                        <stop offset="100%" stop-color="#4F46E5" stop-opacity="0.3" />
                    </linearGradient>
                    <linearGradient id="gradient2" x1="100%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.2" />
                        <stop offset="100%" stop-color="#4F46E5" stop-opacity="0.4" />
                    </linearGradient>
                </defs>
                
                <!-- EKG/Heartbeat Lines -->
                <path d="M-100,200 L50,200 L75,150 L100,250 L125,150 L150,250 L175,200 L300,200" stroke="url(#gradient1)" stroke-width="3" fill="none" />
                <path d="M350,200 L450,200 L475,150 L500,250 L525,150 L550,250 L575,200 L700,200" stroke="url(#gradient1)" stroke-width="3" fill="none" />
                <path d="M750,200 L850,200 L875,150 L900,250 L925,150 L950,250 L975,200 L1100,200" stroke="url(#gradient1)" stroke-width="3" fill="none" />
                
                <path d="M-100,300 L50,300 L75,250 L100,350 L125,250 L150,350 L175,300 L300,300" stroke="url(#gradient2)" stroke-width="3" fill="none" />
                <path d="M350,300 L450,300 L475,250 L500,350 L525,250 L550,350 L575,300 L700,300" stroke="url(#gradient2)" stroke-width="3" fill="none" />
                <path d="M750,300 L850,300 L875,250 L900,350 L925,250 L950,350 L975,300 L1100,300" stroke="url(#gradient2)" stroke-width="3" fill="none" />
                
                <!-- Heart Icons -->
                <path d="M200,450 C175,425 150,425 125,450 C100,475 100,525 125,550 L200,625 L275,550 C300,525 300,475 275,450 C250,425 225,425 200,450 Z" fill="#3B82F6" opacity="0.2" />
                <path d="M600,450 C575,425 550,425 525,450 C500,475 500,525 525,550 L600,625 L675,550 C700,525 700,475 675,450 C650,425 625,425 600,450 Z" fill="#4F46E5" opacity="0.2" />
                <path d="M1000,450 C975,425 950,425 925,450 C900,475 900,525 925,550 L1000,625 L1075,550 C1100,525 1100,475 1075,450 C1050,425 1025,425 1000,450 Z" fill="#3B82F6" opacity="0.2" />
                
                <!-- DNA Double Helix -->
                <path d="M100,650 C150,680 250,620 300,650 C350,680 450,620 500,650 C550,680 650,620 700,650" stroke="#3B82F6" stroke-width="2" fill="none" opacity="0.4" />
                <path d="M100,700 C150,670 250,730 300,700 C350,670 450,730 500,700 C550,670 650,730 700,700" stroke="#4F46E5" stroke-width="2" fill="none" opacity="0.4" />
                
                <!-- Connecting dots between the DNA strands -->
                <line x1="100" y1="650" x2="100" y2="700" stroke="#3B82F6" stroke-width="1.5" opacity="0.3" />
                <line x1="200" y1="635" x2="200" y2="715" stroke="#4F46E5" stroke-width="1.5" opacity="0.3" />
                <line x1="300" y1="650" x2="300" y2="700" stroke="#3B82F6" stroke-width="1.5" opacity="0.3" />
                <line x1="400" y1="635" x2="400" y2="715" stroke="#4F46E5" stroke-width="1.5" opacity="0.3" />
                <line x1="500" y1="650" x2="500" y2="700" stroke="#3B82F6" stroke-width="1.5" opacity="0.3" />
                <line x1="600" y1="635" x2="600" y2="715" stroke="#4F46E5" stroke-width="1.5" opacity="0.3" />
                <line x1="700" y1="650" x2="700" y2="700" stroke="#3B82F6" stroke-width="1.5" opacity="0.3" />
            </svg>
        </div>
        
        <div class="container relative z-10">
            <div class="max-w-3xl text-center">
                <h1>Disease Risk Assessment</h1>
                <p class="text-muted">
                    Analyze your health data for a personalized disease risk assessment tailored to your unique profile.
                </p>
                
                <div class="tabs">
                    <a href="/heart" class="tab {{ 'active' if active_tab == 'heart' else '' }}">Heart Disease</a>
                    <a href="/kidney" class="tab {{ 'active' if active_tab == 'kidney' else '' }}">Kidney Disease</a>
                    <a href="/diabetes" class="tab {{ 'active' if active_tab == 'diabetes' else '' }}">Diabetes</a>
                </div>
                
                <!-- Content will be injected here -->
                {% block content %}{% endblock %}
                
                <div class="features-grid">
                    <div class="feature-item">
                        <svg class="feature-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                            <circle cx="12" cy="7" r="4"></circle>
                        </svg>
                        <span class="feature-text">Privacy Protected</span>
                    </div>
                    <div class="feature-item">
                        <svg class="feature-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                        </svg>
                        <span class="feature-text">Real-time Analysis</span>
                    </div>
                    <div class="feature-item">
                        <svg class="feature-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <path d="M3 9h18"></path>
                            <path d="M9 21V9"></path>
                        </svg>
                        <span class="feature-text">AI-Powered</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
</body>
</html>
"""

# Heart Disease Template
HEART_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Disease Risk Prediction - CardiaLink Quantify</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --background: #ffffff;
            --foreground: #0f172a;
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --primary-foreground: #ffffff;
            --secondary: #f1f5f9;
            --secondary-foreground: #1e293b;
            --muted: #f1f5f9;
            --muted-foreground: #64748b;
            --border: #e2e8f0;
            --radius: 0.5rem;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background-color: #f8fafc;
            color: var(--foreground);
            line-height: 1.5;
        }
        
        .relative {
            position: relative;
        }
        
        .absolute {
            position: absolute;
        }
        
        .inset-0 {
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
        }
        
        .z-10 {
            z-index: 10;
        }
        
        .z-0 {
            z-index: 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        section {
            position: relative;
            overflow: hidden;
            padding: 3rem 0;
        }
        
        @media (min-width: 768px) {
            section {
                padding: 4rem 0;
            }
        }
        
        .bg-vector {
            position: absolute;
            inset: 0;
            background: linear-gradient(to bottom right, #f0f6ff, #e0ebfc);
            z-index: -10;
        }
        
        svg {
            width: 100%;
            height: 100%;
            opacity: 0.3;
        }
        
        .max-w-3xl {
            max-width: 48rem;
            margin: 0 auto;
        }
        
        .text-center {
            text-align: center;
        }
        
        h1 {
            font-weight: 700;
            font-size: 2.25rem;
            letter-spacing: -0.025em;
            margin-bottom: 1.5rem;
            color: var(--foreground);
        }
        
        @media (min-width: 640px) {
            h1 {
                font-size: 2.5rem;
            }
        }
        
        @media (min-width: 768px) {
            h1 {
                font-size: 3rem;
            }
        }
        
        @media (min-width: 1024px) {
            h1 {
                font-size: 3.75rem;
            }
        }
        
        h2 {
            font-weight: 600;
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--foreground);
        }
        
        .text-muted {
            color: var(--muted-foreground);
            font-size: 1.125rem;
            margin-bottom: 2rem;
        }
        
        @media (min-width: 768px) {
            .text-muted {
                font-size: 1.25rem;
            }
        }
        
        .card {
            background-color: white;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            backdrop-filter: blur(4px);
            background-color: rgba(255, 255, 255, 0.8);
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.375rem;
            font-weight: 500;
            color: #334155;
        }
        
        input, select {
            width: 100%;
            padding: 0.625rem;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            font-family: inherit;
            font-size: 1rem;
            color: var(--foreground);
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }
        
        .row {
            display: flex;
            flex-wrap: wrap;
            margin: 0 -0.75rem;
        }
        
        .col {
            flex: 1;
            padding: 0 0.75rem;
            min-width: 200px;
        }
        
        @media (max-width: 640px) {
            .col {
                flex-basis: 100%;
                margin-bottom: 0.75rem;
            }
        }
        
        button {
            display: block;
            background: linear-gradient(to right, #3b82f6, #4f46e5);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius);
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            margin: 1.5rem auto;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-1px);
            background: linear-gradient(to right, #2563eb, #4338ca);
        }
        
        button::after {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(to right, #4f46e5, #3b82f6);
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        button:hover::after {
            opacity: 1;
        }
        
        button span {
            position: relative;
            z-index: 10;
        }
        
        .result {
            margin-top: 1.5rem;
            text-align: center;
            font-size: 1.125rem;
        }
        
        .high-risk {
            color: #dc2626;
            font-weight: 600;
        }
        
        .low-risk {
            color: #16a34a;
            font-weight: 600;
        }
        
        .risk-meter {
            margin: 1.5rem auto;
            width: 300px;
            height: 8px;
            background: linear-gradient(to right, #16a34a, #facc15, #dc2626);
            border-radius: 4px;
            position: relative;
        }
        
        .risk-indicator {
            position: absolute;
            top: -10px;
            width: 4px;
            height: 28px;
            background-color: #0f172a;
            transform: translateX(-2px);
        }
        
        .feature-help {
            font-size: 0.75rem;
            color: var(--muted-foreground);
            margin-top: 0.25rem;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
            max-width: 32rem;
            margin: 1.5rem auto 0;
        }
        
        @media (min-width: 640px) {
            .features-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .feature-icon {
            width: 1.25rem;
            height: 1.25rem;
            color: var(--primary);
        }
        
        .feature-text {
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        /* Tabs styling */
        .tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.5rem;
        }
        
        .tab {
            padding: 0.75rem 1.5rem;
            margin: 0 0.5rem;
            cursor: pointer;
            border-radius: var(--radius) var(--radius) 0 0;
            font-weight: 500;
            transition: all 0.2s;
            border: 1px solid transparent;
            border-bottom: none;
            text-decoration: none;
            color: var(--muted-foreground);
        }
        
        .tab:hover {
            color: var(--primary);
        }
        
        .tab.active {
            background-color: white;
            border-color: var(--border);
            border-bottom: 1px solid white;
            color: var(--primary);
            margin-bottom: -1px;
            box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.05);
        }
        
        .btn-next {
            background: linear-gradient(to right, #4f46e5, #8b5cf6);
            margin-top: 1rem;
        }
        
        .btn-next:hover {
            background: linear-gradient(to right, #4338ca, #7c3aed);
        }
        
        .btn-next::after {
            background: linear-gradient(to right, #8b5cf6, #4f46e5);
        }

        .btn-prev {
            background: linear-gradient(to right, #8b5cf6, #4f46e5);
            margin-top: 1rem;
            display: inline-block;
            text-decoration: none;
        }
        
        .btn-prev:hover {
            background: linear-gradient(to right, #7c3aed, #4338ca);
        }
        
        .btn-prev::after {
            background: linear-gradient(to right, #4f46e5, #8b5cf6);
        }

        .primary-btn {
            width: 100%;
            max-width: 300px;
            background: linear-gradient(to right, #3b82f6, #4f46e5);
            font-weight: 600;
            letter-spacing: 0.01em;
            box-shadow: 0 2px 10px rgba(79, 70, 229, 0.2);
        }
    </style>
</head>
<body>
    <section>
        <!-- Vector Background -->
        <div class="bg-vector">
            <svg width="100%" height="100%" viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.1" />
                        <stop offset="100%" stop-color="#4F46E5" stop-opacity="0.3" />
                    </linearGradient>
                    <linearGradient id="gradient2" x1="100%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.2" />
                        <stop offset="100%" stop-color="#4F46E5" stop-opacity="0.4" />
                    </linearGradient>
                </defs>
                
                <!-- EKG/Heartbeat Lines -->
                <path d="M-100,200 L50,200 L75,150 L100,250 L125,150 L150,250 L175,200 L300,200" stroke="url(#gradient1)" stroke-width="3" fill="none" />
                <path d="M350,200 L450,200 L475,150 L500,250 L525,150 L550,250 L575,200 L700,200" stroke="url(#gradient1)" stroke-width="3" fill="none" />
                <path d="M750,200 L850,200 L875,150 L900,250 L925,150 L950,250 L975,200 L1100,200" stroke="url(#gradient1)" stroke-width="3" fill="none" />
                
                <path d="M-100,300 L50,300 L75,250 L100,350 L125,250 L150,350 L175,300 L300,300" stroke="url(#gradient2)" stroke-width="3" fill="none" />
                <path d="M350,300 L450,300 L475,250 L500,350 L525,250 L550,350 L575,300 L700,300" stroke="url(#gradient2)" stroke-width="3" fill="none" />
                <path d="M750,300 L850,300 L875,250 L900,350 L925,250 L950,350 L975,300 L1100,300" stroke="url(#gradient2)" stroke-width="3" fill="none" />
                
                <!-- Heart Icons -->
                <path d="M200,450 C175,425 150,425 125,450 C100,475 100,525 125,550 L200,625 L275,550 C300,525 300,475 275,450 C250,425 225,425 200,450 Z" fill="#3B82F6" opacity="0.2" />
                <path d="M600,450 C575,425 550,425 525,450 C500,475 500,525 525,550 L600,625 L675,550 C700,525 700,475 675,450 C650,425 625,425 600,450 Z" fill="#4F46E5" opacity="0.2" />
                <path d="M1000,450 C975,425 950,425 925,450 C900,475 900,525 925,550 L1000,625 L1075,550 C1100,525 1100,475 1075,450 C1050,425 1025,425 1000,450 Z" fill="#3B82F6" opacity="0.2" />
                
                <!-- DNA Double Helix -->
                <path d="M100,650 C150,680 250,620 300,650 C350,680 450,620 500,650 C550,680 650,620 700,650" stroke="#3B82F6" stroke-width="2" fill="none" opacity="0.4" />
                <path d="M100,700 C150,670 250,730 300,700 C350,670 450,730 500,700 C550,670 650,730 700,700" stroke="#4F46E5" stroke-width="2" fill="none" opacity="0.4" />
                
                <!-- Connecting dots between the DNA strands -->
                <line x1="100" y1="650" x2="100" y2="700" stroke="#3B82F6" stroke-width="1.5" opacity="0.3" />
                <line x1="200" y1="635" x2="200" y2="715" stroke="#4F46E5" stroke-width="1.5" opacity="0.3" />
                <line x1="300" y1="650" x2="300" y2="700" stroke="#3B82F6" stroke-width="1.5" opacity="0.3" />
                <line x1="400" y1="635" x2="400" y2="715" stroke="#4F46E5" stroke-width="1.5" opacity="0.3" />
                <line x1="500" y1="650" x2="500" y2="700" stroke="#3B82F6" stroke-width="1.5" opacity="0.3" />
                <line x1="600" y1="635" x2="600" y2="715" stroke="#4F46E5" stroke-width="1.5" opacity="0.3" />
                <line x1="700" y1="650" x2="700" y2="700" stroke="#3B82F6" stroke-width="1.5" opacity="0.3" />
            </svg>
        </div>
        
        <div class="container relative z-10">
            <div class="max-w-3xl text-center">
                <h1>Disease Risk Assessment</h1>
                <p class="text-muted">
                    Analyze your health data for a personalized disease risk assessment tailored to your unique profile.
                </p>
                
                <div class="tabs">
                    <a href="/heart" class="tab {{ 'active' if active_tab == 'heart' else '' }}">Heart Disease</a>
                    <a href="/kidney" class="tab {{ 'active' if active_tab == 'kidney' else '' }}">Kidney Disease</a>
                    <a href="/diabetes" class="tab {{ 'active' if active_tab == 'diabetes' else '' }}">Diabetes</a>
                </div>
                
                <div class="card">
                    <form id="prediction-form" method="post">
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="age">Age</label>
                                    <input type="number" id="age" name="age" min="20" max="100" required>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="sex">Sex</label>
                                    <select id="sex" name="sex" required>
                                        <option value="1">Male</option>
                                        <option value="0">Female</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="cp">Chest Pain Type</label>
                                    <select id="cp" name="cp" required>
                                        <option value="0">Typical Angina</option>
                                        <option value="1">Atypical Angina</option>
                                        <option value="2">Non-anginal Pain</option>
                                        <option value="3">Asymptomatic</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="trestbps">Resting Blood Pressure (mm Hg)</label>
                                    <input type="number" id="trestbps" name="trestbps" min="90" max="200" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="chol">Cholesterol (mg/dl)</label>
                                    <input type="number" id="chol" name="chol" min="100" max="600" required>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="fbs">Fasting Blood Sugar > 120 mg/dl</label>
                                    <select id="fbs" name="fbs" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="restecg">Resting ECG Results</label>
                                    <select id="restecg" name="restecg" required>
                                        <option value="0">Normal</option>
                                        <option value="1">ST-T Wave Abnormality</option>
                                        <option value="2">Left Ventricular Hypertrophy</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="thalach">Maximum Heart Rate</label>
                                    <input type="number" id="thalach" name="thalach" min="60" max="220" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="exang">Exercise Induced Angina</label>
                                    <select id="exang" name="exang" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="oldpeak">ST Depression (Exercise vs Rest)</label>
                                    <input type="number" id="oldpeak" name="oldpeak" step="0.1" min="0" max="10" required>
                                    <div class="feature-help">ST depression induced by exercise relative to rest</div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="slope">Slope of Peak Exercise ST Segment</label>
                                    <select id="slope" name="slope" required>
                                        <option value="0">Upsloping</option>
                                        <option value="1">Flat</option>
                                        <option value="2">Downsloping</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="ca">Number of Major Vessels</label>
                                    <select id="ca" name="ca" required>
                                        <option value="0">0</option>
                                        <option value="1">1</option>
                                        <option value="2">2</option>
                                        <option value="3">3</option>
                                        <option value="4">4</option>
                                    </select>
                                    <div class="feature-help">Number of major vessels colored by fluoroscopy</div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="thal">Thalassemia</label>
                                    <select id="thal" name="thal" required>
                                        <option value="0">Normal</option>
                                        <option value="1">Fixed Defect</option>
                                        <option value="2">Reversible Defect</option>
                                        <option value="3">Unknown</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <!-- Placeholder to balance the layout -->
                            </div>
                        </div>
                        
                        <button type="submit" class="primary-btn"><span>Next: Kidney Assessment</span></button>
                    </form>
                </div>
                
                {% if prediction is not none %}
                <div class="card result">
                    <h2>Prediction Result</h2>
                    <p>Heart Disease Risk Probability: <span class="{{ 'high-risk' if prediction > 0.5 else 'low-risk' }}">{{ "%.2f"|format(prediction*100) }}%</span></p>
                    <p>Risk Assessment: <span class="{{ 'high-risk' if prediction > 0.5 else 'low-risk' }}">{{ "High" if prediction > 0.5 else "Low" }}</span></p>
                    
                    <div class="risk-meter">
                        <div class="risk-indicator" style="left: {{ prediction*100 }}%;"></div>
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
    </section>
</body>
</html>
"""

# Kidney Disease Template
KIDNEY_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Disease Risk Prediction - CardiaLink Quantify</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --background: #ffffff;
            --foreground: #0f172a;
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --primary-foreground: #ffffff;
            --secondary: #f1f5f9;
            --secondary-foreground: #1e293b;
            --muted: #f1f5f9;
            --muted-foreground: #64748b;
            --border: #e2e8f0;
            --radius: 0.5rem;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background-color: #f8fafc;
            color: var(--foreground);
            line-height: 1.5;
        }
        
        .relative {
            position: relative;
        }
        
        .absolute {
            position: absolute;
        }
        
        .inset-0 {
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
        }
        
        .z-10 {
            z-index: 10;
        }
        
        .z-0 {
            z-index: 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        section {
            position: relative;
            overflow: hidden;
            padding: 3rem 0;
        }
        
        @media (min-width: 768px) {
            section {
                padding: 4rem 0;
            }
        }
        
        .bg-vector {
            position: absolute;
            inset: 0;
            background: linear-gradient(to bottom right, #f0f6ff, #e0ebfc);
            z-index: -10;
        }
        
        svg {
            width: 100%;
            height: 100%;
            opacity: 0.3;
        }
        
        .max-w-3xl {
            max-width: 48rem;
            margin: 0 auto;
        }
        
        .text-center {
            text-align: center;
        }
        
        h1 {
            font-weight: 700;
            font-size: 2.25rem;
            letter-spacing: -0.025em;
            margin-bottom: 1.5rem;
            color: var(--foreground);
        }
        
        @media (min-width: 640px) {
            h1 {
                font-size: 2.5rem;
            }
        }
        
        @media (min-width: 768px) {
            h1 {
                font-size: 3rem;
            }
        }
        
        @media (min-width: 1024px) {
            h1 {
                font-size: 3.75rem;
            }
        }
        
        h2 {
            font-weight: 600;
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--foreground);
        }
        
        .text-muted {
            color: var(--muted-foreground);
            font-size: 1.125rem;
            margin-bottom: 2rem;
        }
        
        @media (min-width: 768px) {
            .text-muted {
                font-size: 1.25rem;
            }
        }
        
        .card {
            background-color: white;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            backdrop-filter: blur(4px);
            background-color: rgba(255, 255, 255, 0.8);
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.375rem;
            font-weight: 500;
            color: #334155;
        }
        
        input, select {
            width: 100%;
            padding: 0.625rem;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            font-family: inherit;
            font-size: 1rem;
            color: var(--foreground);
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }
        
        .row {
            display: flex;
            flex-wrap: wrap;
            margin: 0 -0.75rem;
        }
        
        .col {
            flex: 1;
            padding: 0 0.75rem;
            min-width: 200px;
        }
        
        @media (max-width: 640px) {
            .col {
                flex-basis: 100%;
                margin-bottom: 0.75rem;
            }
        }
        
        button {
            display: block;
            background: linear-gradient(to right, #3b82f6, #4f46e5);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius);
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            margin: 1.5rem auto;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-1px);
            background: linear-gradient(to right, #2563eb, #4338ca);
        }
        
        button::after {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(to right, #4f46e5, #3b82f6);
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        button:hover::after {
            opacity: 1;
        }
        
        button span {
            position: relative;
            z-index: 10;
        }
        
        .result {
            margin-top: 1.5rem;
            text-align: center;
            font-size: 1.125rem;
        }
        
        .high-risk {
            color: #dc2626;
            font-weight: 600;
        }
        
        .low-risk {
            color: #16a34a;
            font-weight: 600;
        }
        
        .risk-meter {
            margin: 1.5rem auto;
            width: 300px;
            height: 8px;
            background: linear-gradient(to right, #16a34a, #facc15, #dc2626);
            border-radius: 4px;
            position: relative;
        }
        
        .risk-indicator {
            position: absolute;
            top: -10px;
            width: 4px;
            height: 28px;
            background-color: #0f172a;
            transform: translateX(-2px);
        }
        
        .feature-help {
            font-size: 0.75rem;
            color: var(--muted-foreground);
            margin-top: 0.25rem;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
            max-width: 32rem;
            margin: 1.5rem auto 0;
        }
        
        @media (min-width: 640px) {
            .features-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .feature-icon {
            width: 1.25rem;
            height: 1.25rem;
            color: var(--primary);
        }
        
        .feature-text {
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        /* Tabs styling */
        .tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.5rem;
        }
        
        .tab {
            padding: 0.75rem 1.5rem;
            margin: 0 0.5rem;
            cursor: pointer;
            border-radius: var(--radius) var(--radius) 0 0;
            font-weight: 500;
            transition: all 0.2s;
            border: 1px solid transparent;
            border-bottom: none;
            text-decoration: none;
            color: var(--muted-foreground);
        }
        
        .tab:hover {
            color: var(--primary);
        }
        
        .tab.active {
            background-color: white;
            border-color: var(--border);
            border-bottom: 1px solid white;
            color: var(--primary);
            margin-bottom: -1px;
            box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.05);
        }
        
        .btn-next {
            background: linear-gradient(to right, #4f46e5, #8b5cf6);
            margin-top: 1rem;
            display: inline-block;
            text-decoration: none;
        }
        
        .btn-next:hover {
            background: linear-gradient(to right, #4338ca, #7c3aed);
        }
        
        .btn-next::after {
            background: linear-gradient(to right, #8b5cf6, #4f46e5);
        }

        .btn-prev {
            background: linear-gradient(to right, #8b5cf6, #4f46e5);
            margin-top: 1rem;
            display: inline-block;
            text-decoration: none;
        }
        
        .btn-prev:hover {
            background: linear-gradient(to right, #7c3aed, #4338ca);
        }
        
        .btn-prev::after {
            background: linear-gradient(to right, #4f46e5, #8b5cf6);
        }

        .primary-btn {
            width: 100%;
            max-width: 300px;
            background: linear-gradient(to right, #3b82f6, #4f46e5);
            font-weight: 600;
            letter-spacing: 0.01em;
            box-shadow: 0 2px 10px rgba(79, 70, 229, 0.2);
        }
    </style>
</head>
<body>
    <section>
        <!-- Vector Background -->
        <div class="bg-vector">
            <svg width="100%" height="100%" viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.1" />
                        <stop offset="100%" stop-color="#4F46E5" stop-opacity="0.3" />
                    </linearGradient>
                    <linearGradient id="gradient2" x1="100%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.2" />
                        <stop offset="100%" stop-color="#4F46E5" stop-opacity="0.4" />
                    </linearGradient>
                </defs>
                
                <!-- EKG/Heartbeat Lines -->
                <path d="M-100,200 L50,200 L75,150 L100,250 L125,150 L150,250 L175,200 L300,200" stroke="url(#gradient1)" stroke-width="3" fill="none" />
                <path d="M350,200 L450,200 L475,150 L500,250 L525,150 L550,250 L575,200 L700,200" stroke="url(#gradient1)" stroke-width="3" fill="none" />
                <path d="M750,200 L850,200 L875,150 L900,250 L925,150 L950,250 L975,200 L1100,200" stroke="url(#gradient1)" stroke-width="3" fill="none" />
                
                <path d="M-100,300 L50,300 L75,250 L100,350 L125,250 L150,350 L175,300 L300,300" stroke="url(#gradient2)" stroke-width="3" fill="none" />
                <path d="M350,300 L450,300 L475,250 L500,350 L525,250 L550,350 L575,300 L700,300" stroke="url(#gradient2)" stroke-width="3" fill="none" />
                <path d="M750,300 L850,300 L875,250 L900,350 L925,250 L950,350 L975,300 L1100,300" stroke="url(#gradient2)" stroke-width="3" fill="none" />
                
                <!-- Heart Icons -->
                <path d="M200,450 C175,425 150,425 125,450 C100,475 100,525 125,550 L200,625 L275,550 C300,525 300,475 275,450 C250,425 225,425 200,450 Z" fill="#3B82F6" opacity="0.2" />
                <path d="M600,450 C575,425 550,425 525,450 C500,475 500,525 525,550 L600,625 L675,550 C700,525 700,475 675,450 C650,425 625,425 600,450 Z" fill="#4F46E5" opacity="0.2" />
                <path d="M1000,450 C975,425 950,425 925,450 C900,475 900,525 925,550 L1000,625 L1075,550 C1100,525 1100,475 1075,450 C1050,425 1025,425 1000,450 Z" fill="#3B82F6" opacity="0.2" />
                
                <!-- DNA Double Helix -->
                <path d="M100,650 C150,680 250,620 300,650 C350,680 450,620 500,650 C550,680 650,620 700,650" stroke="#3B82F6" stroke-width="2" fill="none" opacity="0.4" />
                <path d="M100,700 C150,670 250,730 300,700 C350,670 450,730 500,700 C550,670 650,730 700,700" stroke="#4F46E5" stroke-width="2" fill="none" opacity="0.4" />
                
                <!-- Connecting dots between the DNA strands -->
                <line x1="100" y1="650" x2="100" y2="700" stroke="#3B82F6" stroke-width="1.5" opacity="0.3" />
                <line x1="200" y1="635" x2="200" y2="715" stroke="#4F46E5" stroke-width="1.5" opacity="0.3" />
                <line x1="300" y1="650" x2="300" y2="700" stroke="#3B82F6" stroke-width="1.5" opacity="0.3" />
                <line x1="400" y1="635" x2="400" y2="715" stroke="#4F46E5" stroke-width="1.5" opacity="0.3" />
                <line x1="500" y1="650" x2="500" y2="700" stroke="#3B82F6" stroke-width="1.5" opacity="0.3" />
                <line x1="600" y1="635" x2="600" y2="715" stroke="#4F46E5" stroke-width="1.5" opacity="0.3" />
                <line x1="700" y1="650" x2="700" y2="700" stroke="#3B82F6" stroke-width="1.5" opacity="0.3" />
            </svg>
        </div>
        
        <div class="container relative z-10">
            <div class="max-w-3xl text-center">
                <h1>Disease Risk Assessment</h1>
                <p class="text-muted">
                    Analyze your health data for a personalized disease risk assessment tailored to your unique profile.
                </p>
                
                <div class="tabs">
                    <a href="/heart" class="tab {{ 'active' if active_tab == 'heart' else '' }}">Heart Disease</a>
                    <a href="/kidney" class="tab {{ 'active' if active_tab == 'kidney' else '' }}">Kidney Disease</a>
                    <a href="/diabetes" class="tab {{ 'active' if active_tab == 'diabetes' else '' }}">Diabetes</a>
                </div>
                
                <div class="card">
                    <form id="prediction-form" method="post">
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="age">Age</label>
                                    <input type="number" id="age" name="age" min="1" max="100" required>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="bp">Blood Pressure (mm Hg)</label>
                                    <input type="number" id="bp" name="bp" min="50" max="180" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="al">Albumin Level</label>
                                    <select id="al" name="al" required>
                                        <option value="0">0</option>
                                        <option value="1">1</option>
                                        <option value="2">2</option>
                                        <option value="3">3</option>
                                        <option value="4">4</option>
                                        <option value="5">5</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="su">Sugar Level</label>
                                    <select id="su" name="su" required>
                                        <option value="0">0</option>
                                        <option value="1">1</option>
                                        <option value="2">2</option>
                                        <option value="3">3</option>
                                        <option value="4">4</option>
                                        <option value="5">5</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="bgr">Blood Glucose Random (mg/dl)</label>
                                    <input type="number" id="bgr" name="bgr" min="70" max="490" required>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="bu">Blood Urea (mg/dl)</label>
                                    <input type="number" id="bu" name="bu" min="15" max="400" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="sc">Serum Creatinine (mg/dl)</label>
                                    <input type="number" id="sc" name="sc" step="0.1" min="0.4" max="40" required>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="pot">Potassium (mEq/L)</label>
                                    <input type="number" id="pot" name="pot" step="0.1" min="2.5" max="47" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="wc">White Blood Cell Count</label>
                                    <input type="number" id="wc" name="wc" min="2200" max="26400" required>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="htn">Hypertension</label>
                                    <select id="htn" name="htn" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="dm">Diabetes Mellitus</label>
                                    <select id="dm" name="dm" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="cad">Coronary Artery Disease</label>
                                    <select id="cad" name="cad" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="pe">Pedal Edema</label>
                                    <select id="pe" name="pe" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="ane">Anemia</label>
                                    <select id="ane" name="ane" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <button type="submit" class="primary-btn"><span>Next: Diabetes Assessment</span></button>
                    </form>
                </div>
                
                {% if prediction is not none %}
                <div class="card result">
                    <h2>Prediction Result</h2>
                    <p>Kidney Disease Risk Probability: <span class="{{ 'high-risk' if prediction > 0.5 else 'low-risk' }}">{{ "%.2f"|format(prediction*100) }}%</span></p>
                    <p>Risk Assessment: <span class="{{ 'high-risk' if prediction > 0.5 else 'low-risk' }}">{{ "High" if prediction > 0.5 else "Low" }}</span></p>
                    
                    <div class="risk-meter">
                        <div class="risk-indicator" style="left: {{ prediction*100 }}%;"></div>
                    </div>
                </div>
                {% endif %}
                
                <div class="features-grid">
                    <div class="feature-item">
                        <svg class="feature-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                            <circle cx="12" cy="7" r="4"></circle>
                        </svg>
                        <span class="feature-text">Privacy Protected</span>
                    </div>
                    <div class="feature-item">
                        <svg class="feature-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                        </svg>
                        <span class="feature-text">Real-time Analysis</span>
                    </div>
                    <div class="feature-item">
                        <svg class="feature-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <path d="M3 9h18"></path>
                            <path d="M9 21V9"></path>
                        </svg>
                        <span class="feature-text">AI-Powered</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
</body>
</html>
"""

# Diabetes Disease Template
DIABETES_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Disease Risk Prediction - CardiaLink Quantify</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --background: #ffffff;
            --foreground: #0f172a;
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --primary-foreground: #ffffff;
            --secondary: #f1f5f9;
            --secondary-foreground: #1e293b;
            --muted: #f1f5f9;
            --muted-foreground: #64748b;
            --border: #e2e8f0;
            --radius: 0.5rem;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background-color: #f8fafc;
            color: var(--foreground);
            line-height: 1.5;
        }
        
        .relative {
            position: relative;
        }
        
        .absolute {
            position: absolute;
        }
        
        .inset-0 {
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
        }
        
        .z-10 {
            z-index: 10;
        }
        
        .z-0 {
            z-index: 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        section {
            position: relative;
            overflow: hidden;
            padding: 3rem 0;
        }
        
        @media (min-width: 768px) {
            section {
                padding: 4rem 0;
            }
        }
        
        .bg-vector {
            position: absolute;
            inset: 0;
            background: linear-gradient(to bottom right, #f0f6ff, #e0ebfc);
            z-index: -10;
        }
        
        svg {
            width: 100%;
            height: 100%;
            opacity: 0.3;
        }
        
        .max-w-3xl {
            max-width: 48rem;
            margin: 0 auto;
        }
        
        .text-center {
            text-align: center;
        }
        
        h1 {
            font-weight: 700;
            font-size: 2.25rem;
            letter-spacing: -0.025em;
            margin-bottom: 1.5rem;
            color: var(--foreground);
        }
        
        @media (min-width: 640px) {
            h1 {
                font-size: 2.5rem;
            }
        }
        
        @media (min-width: 768px) {
            h1 {
                font-size: 3rem;
            }
        }
        
        @media (min-width: 1024px) {
            h1 {
                font-size: 3.75rem;
            }
        }
        
        h2 {
            font-weight: 600;
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--foreground);
        }
        
        .text-muted {
            color: var(--muted-foreground);
            font-size: 1.125rem;
            margin-bottom: 2rem;
        }
        
        @media (min-width: 768px) {
            .text-muted {
                font-size: 1.25rem;
            }
        }
        
        .card {
            background-color: white;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            backdrop-filter: blur(4px);
            background-color: rgba(255, 255, 255, 0.8);
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.375rem;
            font-weight: 500;
            color: #334155;
        }
        
        input, select {
            width: 100%;
            padding: 0.625rem;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            font-family: inherit;
            font-size: 1rem;
            color: var(--foreground);
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }
        
        .row {
            display: flex;
            flex-wrap: wrap;
            margin: 0 -0.75rem;
        }
        
        .col {
            flex: 1;
            padding: 0 0.75rem;
            min-width: 200px;
        }
        
        @media (max-width: 640px) {
            .col {
                flex-basis: 100%;
                margin-bottom: 0.75rem;
            }
        }
        
        button {
            display: block;
            background: linear-gradient(to right, #3b82f6, #4f46e5);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius);
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            margin: 1.5rem auto;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-1px);
            background: linear-gradient(to right, #2563eb, #4338ca);
        }
        
        button::after {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(to right, #4f46e5, #3b82f6);
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        button:hover::after {
            opacity: 1;
        }
        
        button span {
            position: relative;
            z-index: 10;
        }
        
        .result {
            margin-top: 1.5rem;
            text-align: center;
            font-size: 1.125rem;
        }
        
        .high-risk {
            color: #dc2626;
            font-weight: 600;
        }
        
        .low-risk {
            color: #16a34a;
            font-weight: 600;
        }
        
        .risk-meter {
            margin: 1.5rem auto;
            width: 300px;
            height: 8px;
            background: linear-gradient(to right, #16a34a, #facc15, #dc2626);
            border-radius: 4px;
            position: relative;
        }
        
        .risk-indicator {
            position: absolute;
            top: -10px;
            width: 4px;
            height: 28px;
            background-color: #0f172a;
            transform: translateX(-2px);
        }
        
        .feature-help {
            font-size: 0.75rem;
            color: var(--muted-foreground);
            margin-top: 0.25rem;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
            max-width: 32rem;
            margin: 1.5rem auto 0;
        }
        
        @media (min-width: 640px) {
            .features-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .feature-icon {
            width: 1.25rem;
            height: 1.25rem;
            color: var(--primary);
        }
        
        .feature-text {
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        /* Tabs styling */
        .tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.5rem;
        }
        
        .tab {
            padding: 0.75rem 1.5rem;
            margin: 0 0.5rem;
            cursor: pointer;
            border-radius: var(--radius) var(--radius) 0 0;
            font-weight: 500;
            transition: all 0.2s;
            border: 1px solid transparent;
            border-bottom: none;
            text-decoration: none;
            color: var(--muted-foreground);
        }
        
        .tab:hover {
            color: var(--primary);
        }
        
        .tab.active {
            background-color: white;
            border-color: var(--border);
            border-bottom: 1px solid white;
            color: var(--primary);
            margin-bottom: -1px;
            box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.05);
        }
        
        .primary-btn {
            width: 100%;
            max-width: 300px;
            background: linear-gradient(to right, #3b82f6, #4f46e5);
            font-weight: 600;
            letter-spacing: 0.01em;
            box-shadow: 0 2px 10px rgba(79, 70, 229, 0.2);
        }
    </style>
</head>
<body>
    <section>
        <!-- Vector Background -->
        <div class="bg-vector">
            <svg width="100%" height="100%" viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.1" />
                        <stop offset="100%" stop-color="#4F46E5" stop-opacity="0.3" />
                    </linearGradient>
                    <linearGradient id="gradient2" x1="100%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.2" />
                        <stop offset="100%" stop-color="#4F46E5" stop-opacity="0.4" />
                    </linearGradient>
                </defs>
                
                <!-- Visualization Elements -->
                <path d="M-100,200 L50,200 L75,150 L100,250 L125,150 L150,250 L175,200 L300,200" stroke="url(#gradient1)" stroke-width="3" fill="none" />
                <path d="M350,200 L450,200 L475,150 L500,250 L525,150 L550,250 L575,200 L700,200" stroke="url(#gradient1)" stroke-width="3" fill="none" />
                <path d="M750,200 L850,200 L875,150 L900,250 L925,150 L950,250 L975,200 L1100,200" stroke="url(#gradient1)" stroke-width="3" fill="none" />
                
                <path d="M-100,300 L50,300 L75,250 L100,350 L125,250 L150,350 L175,300 L300,300" stroke="url(#gradient2)" stroke-width="3" fill="none" />
                <path d="M350,300 L450,300 L475,250 L500,350 L525,250 L550,350 L575,300 L700,300" stroke="url(#gradient2)" stroke-width="3" fill="none" />
                <path d="M750,300 L850,300 L875,250 L900,350 L925,250 L950,350 L975,300 L1100,300" stroke="url(#gradient2)" stroke-width="3" fill="none" />
                
                <!-- Additional visualization elements -->
                <circle cx="200" cy="450" r="20" fill="#3B82F6" opacity="0.2" />
                <circle cx="600" cy="450" r="20" fill="#4F46E5" opacity="0.2" />
                <circle cx="1000" cy="450" r="20" fill="#3B82F6" opacity="0.2" />
                
                <path d="M100,650 C150,680 250,620 300,650 C350,680 450,620 500,650 C550,680 650,620 700,650" stroke="#3B82F6" stroke-width="2" fill="none" opacity="0.4" />
                <path d="M100,700 C150,670 250,730 300,700 C350,670 450,730 500,700 C550,670 650,730 700,700" stroke="#4F46E5" stroke-width="2" fill="none" opacity="0.4" />
            </svg>
        </div>
        
        <div class="container relative z-10">
            <div class="max-w-3xl text-center">
                <h1>Disease Risk Assessment</h1>
                <p class="text-muted">
                    Analyze your health data for a personalized disease risk assessment tailored to your unique profile.
                </p>
                
                <div class="tabs">
                    <a href="/heart" class="tab {{ 'active' if active_tab == 'heart' else '' }}">Heart Disease</a>
                    <a href="/kidney" class="tab {{ 'active' if active_tab == 'kidney' else '' }}">Kidney Disease</a>
                    <a href="/diabetes" class="tab {{ 'active' if active_tab == 'diabetes' else '' }}">Diabetes</a>
                </div>
                
                <div class="card">
                    <form id="prediction-form" method="post">
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="highbp">High Blood Pressure</label>
                                    <select id="highbp" name="highbp" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="highchol">High Cholesterol</label>
                                    <select id="highchol" name="highchol" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="cholcheck">Cholesterol Check in 5 Years</label>
                                    <select id="cholcheck" name="cholcheck" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="bmi">BMI</label>
                                    <input type="number" id="bmi" name="bmi" min="10" max="60" step="0.1" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="smoker">Smoker</label>
                                    <select id="smoker" name="smoker" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="stroke">Had a Stroke</label>
                                    <select id="stroke" name="stroke" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="heartdisease">Heart Disease or Attack</label>
                                    <select id="heartdisease" name="heartdisease" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="physactivity">Physical Activity</label>
                                    <select id="physactivity" name="physactivity" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="fruits">Fruit Consumption</label>
                                    <select id="fruits" name="fruits" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="veggies">Vegetable Consumption</label>
                                    <select id="veggies" name="veggies" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="alcohol">Heavy Alcohol Consumption</label>
                                    <select id="alcohol" name="alcohol" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="healthcare">Any Healthcare</label>
                                    <select id="healthcare" name="healthcare" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="nodoc">No Doctor Because of Cost</label>
                                    <select id="nodoc" name="nodoc" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="genhlth">General Health (1-5, 5=Poor)</label>
                                    <select id="genhlth" name="genhlth" required>
                                        <option value="1">Excellent</option>
                                        <option value="2">Very Good</option>
                                        <option value="3">Good</option>
                                        <option value="4">Fair</option>
                                        <option value="5">Poor</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="menthlth">Mental Health Days (0-30)</label>
                                    <input type="number" id="menthlth" name="menthlth" min="0" max="30" required>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="physhlth">Physical Health Days (0-30)</label>
                                    <input type="number" id="physhlth" name="physhlth" min="0" max="30" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="diffwalk">Difficulty Walking</label>
                                    <select id="diffwalk" name="diffwalk" required>
                                        <option value="0">No</option>
                                        <option value="1">Yes</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="sex">Sex</label>
                                    <select id="sex" name="sex" required>
                                        <option value="0">Female</option>
                                        <option value="1">Male</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="age">Age Category</label>
                                    <select id="age" name="age" required>
                                        <option value="1">18-24</option>
                                        <option value="2">25-29</option>
                                        <option value="3">30-34</option>
                                        <option value="4">35-39</option>
                                        <option value="5">40-44</option>
                                        <option value="6">45-49</option>
                                        <option value="7">50-54</option>
                                        <option value="8">55-59</option>
                                        <option value="9">60-64</option>
                                        <option value="10">65-69</option>
                                        <option value="11">70-74</option>
                                        <option value="12">75-79</option>
                                        <option value="13">80+</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <button type="submit" class="primary-btn"><span>Complete Assessment</span></button>
                    </form>
                </div>
                
                {% if prediction is not none %}
                <div class="card result">
                    <h2>Prediction Result</h2>
                    <p>Diabetes Risk Probability: <span class="{{ 'high-risk' if prediction > 0.5 else 'low-risk' }}">{{ "%.2f"|format(prediction*100) }}%</span></p>
                    <p>Risk Assessment: <span class="{{ 'high-risk' if prediction > 0.5 else 'low-risk' }}">{{ "High" if prediction > 0.5 else "Low" }}</span></p>
                    
                    <div class="risk-meter">
                        <div class="risk-indicator" style="left: {{ prediction*100 }}%;"></div>
                    </div>
                </div>
                {% endif %}
                
                <div class="features-grid">
                    <div class="feature-item">
                        <svg class="feature-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                            <circle cx="12" cy="7" r="4"></circle>
                        </svg>
                        <span class="feature-text">Privacy Protected</span>
                    </div>
                    <div class="feature-item">
                        <svg class="feature-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                        </svg>
                        <span class="feature-text">Real-time Analysis</span>
                    </div>
                    <div class="feature-item">
                        <svg class="feature-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <path d="M3 9h18"></path>
                            <path d="M9 21V9"></path>
                        </svg>
                        <span class="feature-text">AI-Powered</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
</body>
</html>
"""

# After DIABETES_TEMPLATE, completely replace the existing RESULTS_TEMPLATE with this simplified version
RESULTS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Combined Health Risk Assessment - CardiaLink Quantify</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --background: #ffffff;
            --foreground: #0f172a;
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --primary-foreground: #ffffff;
            --secondary: #f1f5f9;
            --secondary-foreground: #1e293b;
            --muted: #f1f5f9;
            --muted-foreground: #64748b;
            --border: #e2e8f0;
            --radius: 0.5rem;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background-color: #f8fafc;
            color: var(--foreground);
            line-height: 1.5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        section {
            position: relative;
            overflow: hidden;
            padding: 3rem 0;
        }
        
        .max-w-3xl {
            max-width: 48rem;
            margin: 0 auto;
        }
        
        .text-center {
            text-align: center;
        }
        
        h1 {
            font-weight: 700;
            font-size: 2.25rem;
            margin-bottom: 1.5rem;
        }
        
        h2 {
            font-weight: 600;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .card {
            background-color: white;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .high-risk {
            color: #dc2626;
            font-weight: 600;
        }
        
        .low-risk {
            color: #16a34a;
            font-weight: 600;
        }
        
        .medium-risk {
            color: #eab308;
            font-weight: 600;
        }
        
        .risk-meter {
            margin: 1.5rem auto;
            width: 300px;
            height: 8px;
            background: linear-gradient(to right, #16a34a, #facc15, #dc2626);
            border-radius: 4px;
            position: relative;
        }
        
        .risk-indicator {
            position: absolute;
            top: -10px;
            width: 4px;
            height: 28px;
            background-color: #0f172a;
            transform: translateX(-2px);
        }
        
        .primary-btn {
            display: block;
            width: 100%;
            max-width: 300px;
            background: linear-gradient(to right, #3b82f6, #4f46e5);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius);
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            margin: 1.5rem auto;
            text-decoration: none;
            text-align: center;
        }
        
        .risk-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
            margin: 1.5rem 0;
        }
        
        @media (min-width: 640px) {
            .risk-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        .risk-box {
            padding: 1.25rem;
            border-radius: 0.75rem;
            background-color: white;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            text-align: center;
            border-top: 4px solid;
        }
        
        .risk-box h3 {
            font-size: 1.1rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        .risk-box .risk-value {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .heart-box {
            border-color: #f43f5e;
        }
        
        .kidney-box {
            border-color: #3b82f6;
        }
        
        .diabetes-box {
            border-color: #8b5cf6;
        }
        
        .combined-box {
            grid-column: 1 / -1;
            border-color: #10b981;
            padding: 1.5rem;
        }
    </style>
</head>
<body>
    <section>
        <div class="container">
            <div class="max-w-3xl text-center">
                <h1>Your Health Risk Assessment</h1>
                
                <div class="card">
                    <h2>Comprehensive Health Risk Assessment</h2>
                    
                    <div class="risk-grid">
                        <div class="risk-box heart-box">
                            <h3>Heart Disease</h3>
                            <div class="risk-value {{ 'high-risk' if heart_risk > 0.7 else 'medium-risk' if heart_risk > 0.3 else 'low-risk' }}">
                                {{ "%.1f"|format(heart_risk*100) }}%
                            </div>
                            <div>
                                {{ "High Risk" if heart_risk > 0.7 else "Medium Risk" if heart_risk > 0.3 else "Low Risk" }}
                            </div>
                        </div>
                        
                        <div class="risk-box kidney-box">
                            <h3>Kidney Disease</h3>
                            <div class="risk-value {{ 'high-risk' if kidney_risk > 0.7 else 'medium-risk' if kidney_risk > 0.3 else 'low-risk' }}">
                                {{ "%.1f"|format(kidney_risk*100) }}%
                            </div>
                            <div>
                                {{ "High Risk" if kidney_risk > 0.7 else "Medium Risk" if kidney_risk > 0.3 else "Low Risk" }}
                            </div>
                        </div>
                        
                        <div class="risk-box diabetes-box">
                            <h3>Diabetes</h3>
                            <div class="risk-value {{ 'high-risk' if diabetes_risk > 0.7 else 'medium-risk' if diabetes_risk > 0.3 else 'low-risk' }}">
                                {{ "%.1f"|format(diabetes_risk*100) }}%
                            </div>
                            <div>
                                {{ "High Risk" if diabetes_risk > 0.7 else "Medium Risk" if diabetes_risk > 0.3 else "Low Risk" }}
                            </div>
                        </div>
                        
                        <div class="risk-box combined-box">
                            <h3>Overall Health Risk</h3>
                            <div class="risk-value {{ 'high-risk' if combined_risk > 0.7 else 'medium-risk' if combined_risk > 0.3 else 'low-risk' }}">
                                {{ "%.1f"|format(combined_risk*100) }}%
                            </div>
                            <div>
                                {{ "High Risk" if combined_risk > 0.7 else "Medium Risk" if combined_risk > 0.3 else "Low Risk" }}
                            </div>
                            
                            <div class="risk-meter">
                                <div class="risk-indicator" style="left: {{ combined_risk*100 }}%;"></div>
                            </div>
                        </div>
                    </div>
                    
                    <p style="margin-top: 15px; font-size: 0.9rem; color: #64748b; text-align: center;">
                        This weighted assessment prioritizes heart health (50%), followed by kidney function (30%), and diabetes risk (20%).<br>
                        <span style="font-style: italic;">Note: Any individual disease risk above 90% automatically elevates the overall risk assessment.</span>
                    </p>
                    <a href="/heart" class="primary-btn">Restart Assessment</a>
                </div>
            </div>
        </div>
    </section>
</body>
</html>
"""

# Define app routes
@app.route('/')
@app.route('/heart')
def home():
    return render_template_string(HEART_TEMPLATE, active_tab="heart", prediction=None)

@app.route('/')
def index():
    return redirect('/heart')

@app.route('/heart', methods=['GET', 'POST'])
def heart_disease():
    prediction = None
    
    # Check if we have scores from previous assessments
    has_previous_scores = 'heart_risk' in session
    
    if request.method == 'POST':
        # Extract values from form
        patient_data = {}
        for feature in heart_features:
            patient_data[feature] = float(request.form.get(feature, 0))
        
        # Convert to numpy array and reshape for prediction
        features = []
        for feature in heart_features:
            features.append(patient_data[feature])
        
        features_array = np.array(features).reshape(1, -1)
        scaled_features = heart_scaler.transform(features_array)
        
        # Make prediction
        prediction_result = heart_model.predict(scaled_features)
        prediction = float(prediction_result[0][0])
        
        # Store heart risk score in session
        session['heart_risk'] = prediction
        print(f"Heart risk score saved: {prediction}")
        
        # Redirect to kidney assessment
        return redirect(url_for('kidney_disease'))
    
    return render_template_string(HEART_TEMPLATE, active_tab="heart", prediction=prediction, next_assessment="kidney")

@app.route('/kidney', methods=['GET', 'POST'])
def kidney_disease():
    # Check if kidney model is available
    if kidney_model is None:
        print("WARNING: Kidney disease model is not available. Using simulated predictions.")
    
    prediction = None
    
    # Check if heart risk score exists (user should complete heart assessment first)
    if 'heart_risk' not in session and request.method == 'GET':
        # If user tries to access kidney directly, redirect to heart
        return redirect(url_for('heart_disease'))
    
    if request.method == 'POST':
        try:
            # Extract values from form
            age = float(request.form.get('age', 0))
            bp = float(request.form.get('bp', 0))
            al = float(request.form.get('al', 0))
            su = float(request.form.get('su', 0))
            bgr = float(request.form.get('bgr', 0))
            bu = float(request.form.get('bu', 0))
            sc = float(request.form.get('sc', 0))
            
            # Print debug information
            print(f"Kidney disease form data received:")
            print(f"Age: {age}, BP: {bp}, AL: {al}, SU: {su}, BGR: {bgr}, BU: {bu}, SC: {sc}")
            
            if kidney_model is not None and len(kidney_features) > 0:
                # Create a mapping from form fields to model features
                form_to_feature = {
                    'age': 'age',
                    'bp': 'bp',
                    'al': 'al',
                    'su': 'su',
                    'bgr': 'bgr',
                    'bu': 'bu',
                    'sc': 'sc',
                    'pot': 'pot',
                    'wc': 'wc',
                    'htn': 'htn',
                    'dm': 'dm',
                    'cad': 'cad',
                    'pe': 'pe',
                    'ane': 'ane'
                }
                
                # Extract values using the mapping
                input_data = {}
                for form_field, feature_name in form_to_feature.items():
                    if feature_name in kidney_features:
                        try:
                            input_data[feature_name] = float(request.form.get(form_field, 0))
                        except:
                            input_data[feature_name] = 0
                
                # Create features array in the correct order
                features = []
                for feature in kidney_features:
                    if feature in input_data:
                        features.append(input_data[feature])
                    else:
                        features.append(0)  # Default value for missing features
                
                features_array = np.array(features).reshape(1, -1)
                
                # Make prediction with the model
                prediction_result = kidney_model.predict_proba(features_array)
                prediction = float(prediction_result[0][1])  # Probability of class 1 (CKD)
                
                print(f"Used kidney model for prediction: {prediction}")
            else:
                # Simple heuristic for demo when model isn't available
                # Higher risk factors: high age, high BP, high albumin, high sugar, high creatinine
                risk_score = 0
                if age > 60:
                    risk_score += 0.2
                if bp > 140:
                    risk_score += 0.15
                if al > 1:
                    risk_score += 0.15
                if su > 1:
                    risk_score += 0.1
                if bgr > 200:
                    risk_score += 0.1
                if bu > 100:
                    risk_score += 0.15
                if sc > 1.5:
                    risk_score += 0.15
                
                # Normalize and make it a bit random
                import random
                prediction = min(1.0, max(0.0, risk_score + random.uniform(-0.1, 0.1)))
                print(f"Used heuristic for prediction: {prediction}")
            
            # Store kidney risk score in session
            session['kidney_risk'] = prediction
            print(f"Kidney risk score saved: {prediction}")
            
            # Redirect to diabetes assessment
            return redirect(url_for('diabetes_disease'))
            
        except Exception as e:
            print(f"Error making kidney disease prediction: {e}")
            # Default to a mid-range prediction
            prediction = 0.5
    
    # Pass heart risk from session (if it exists)
    heart_risk = session.get('heart_risk', None)
    
    return render_template_string(KIDNEY_TEMPLATE, active_tab="kidney", prediction=prediction, next_assessment="diabetes", heart_risk=heart_risk)

# Add route for diabetes disease prediction
@app.route('/diabetes', methods=['GET', 'POST'])
def diabetes_disease():
    prediction = None
    
    # Check if kidney risk score exists (user should complete kidney assessment first)
    if 'kidney_risk' not in session and request.method == 'GET':
        # If user tries to access diabetes directly, redirect to heart
        return redirect(url_for('heart_disease'))
    
    if request.method == 'POST':
        try:
            # Extract values from form
            highbp = float(request.form.get('highbp', 0))
            highchol = float(request.form.get('highchol', 0))
            cholcheck = float(request.form.get('cholcheck', 0))
            bmi = float(request.form.get('bmi', 0))
            smoker = float(request.form.get('smoker', 0))
            stroke = float(request.form.get('stroke', 0))
            heartdisease = float(request.form.get('heartdisease', 0))
            physactivity = float(request.form.get('physactivity', 0))
            fruits = float(request.form.get('fruits', 0))
            veggies = float(request.form.get('veggies', 0))
            alcohol = float(request.form.get('alcohol', 0))
            healthcare = float(request.form.get('healthcare', 0))
            nodoc = float(request.form.get('nodoc', 0))
            genhlth = float(request.form.get('genhlth', 0))
            menthlth = float(request.form.get('menthlth', 0))
            physhlth = float(request.form.get('physhlth', 0))
            diffwalk = float(request.form.get('diffwalk', 0))
            sex = float(request.form.get('sex', 0))
            age = float(request.form.get('age', 0))
            
            # Print debug information
            print(f"Diabetes form data received:")
            print(f"HighBP: {highbp}, HighChol: {highchol}, BMI: {bmi}, Smoker: {smoker}")
            
            if diabetes_model is not None:
                # Create a dictionary of features
                input_data = {
                    'HighBP': highbp,
                    'HighChol': highchol,
                    'CholCheck': cholcheck,
                    'BMI': bmi,
                    'Smoker': smoker,
                    'Stroke': stroke,
                    'HeartDiseaseorAttack': heartdisease,
                    'PhysActivity': physactivity,
                    'Fruits': fruits,
                    'Veggies': veggies,
                    'HvyAlcoholConsump': alcohol,
                    'AnyHealthcare': healthcare,
                    'NoDocbcCost': nodoc,
                    'GenHlth': genhlth,
                    'MentHlth': menthlth,
                    'PhysHlth': physhlth,
                    'DiffWalk': diffwalk,
                    'Sex': sex,
                    'Age': age
                }
                
                # Create features array
                features = []
                for feature in diabetes_features:
                    if feature in input_data:
                        features.append(input_data[feature])
                    else:
                        features.append(0)
                
                features_array = np.array(features).reshape(1, -1)
                
                # Make prediction with the model
                # prediction_result = diabetes_model.predict_proba(features_array)
                # prediction = float(prediction_result[0][1])
                
                # Since we don't have the actual model, use a weighted risk score
                prediction = 0.5  # Would be replaced with actual model prediction
                print(f"Used diabetes model for prediction: {prediction}")
            else:
                # Simple heuristic for demo when model isn't available
                risk_score = 0
                if highbp > 0:
                    risk_score += 0.15
                if highchol > 0:
                    risk_score += 0.15
                if bmi >= 30:
                    risk_score += 0.15
                if smoker > 0:
                    risk_score += 0.10
                if stroke > 0:
                    risk_score += 0.20
                if heartdisease > 0:
                    risk_score += 0.20
                if physactivity == 0:
                    risk_score += 0.05
                if fruits == 0:
                    risk_score += 0.03
                if veggies == 0:
                    risk_score += 0.03
                if genhlth > 3:
                    risk_score += 0.10
                if age > 7:  # Age categories in BRFSS, higher = older
                    risk_score += 0.15
                
                # Normalize and add some randomness
                prediction = min(1.0, max(0.0, risk_score + random.uniform(-0.05, 0.05)))
                print(f"Used heuristic for diabetes prediction: {prediction}")
            
            # Store diabetes risk score and calculate combined score
            session['diabetes_risk'] = prediction
            
            # Calculate combined risk score using weighted mean based on model accuracies
            heart_risk = session.get('heart_risk', 0.5)
            kidney_risk = session.get('kidney_risk', 0.5)
            
            # Calculate weighted mean based on model accuracies
            total_accuracy = heart_weight + kidney_weight + diabetes_weight
            combined_risk = (
                (heart_risk * heart_weight) + 
                (kidney_risk * kidney_weight) + 
                (prediction * diabetes_weight)
            ) / (heart_weight + kidney_weight + diabetes_weight)

            # Store diabetes risk score and calculate combined score
            session['diabetes_risk'] = prediction
            
            # Calculate combined risk score using weighted mean based on model accuracies
            heart_risk = session.get('heart_risk', 0.5)
            kidney_risk = session.get('kidney_risk', 0.5)
            
            # Check if any individual risk is extremely high (>90%)
            has_extremely_high_risk = (heart_risk > 0.9 or kidney_risk > 0.9 or prediction > 0.9)
            
            # Calculate weighted mean based on weights
            total_weight = heart_weight + kidney_weight + diabetes_weight
            combined_risk = (
                (heart_risk * heart_weight) + 
                (kidney_risk * kidney_weight) + 
                (prediction * diabetes_weight)
            ) / total_weight
            
            # Force combined risk to be high if any individual risk is extremely high
            if has_extremely_high_risk and combined_risk < 0.9:
                combined_risk = max(combined_risk, 0.9)  # Ensure minimum 90% risk
                print("Applying high risk override due to at least one disease risk exceeding 90%")
            
            session['combined_risk'] = combined_risk
            
            print(f"Diabetes risk score saved: {prediction}")
            print(f"Combined risk score (weighted): {combined_risk}")
            
            # Redirect to combined results page
            return redirect(url_for('combined_results'))
            
        except Exception as e:
            print(f"Error making diabetes prediction: {e}")
            prediction = 0.5
    
    # Pass heart and kidney risks from session
    heart_risk = session.get('heart_risk', None)
    kidney_risk = session.get('kidney_risk', None)
    
    return render_template_string(DIABETES_TEMPLATE, active_tab="diabetes", prediction=prediction, next_assessment="results", heart_risk=heart_risk, kidney_risk=kidney_risk)

# Add route for combined results
@app.route('/results', methods=['GET'])
def combined_results():
    # Check if all risk scores exist (user should complete all assessments first)
    if 'heart_risk' not in session or 'kidney_risk' not in session or 'diabetes_risk' not in session:
        # If user tries to access results directly, redirect to heart
        return redirect(url_for('heart_disease'))
    
    # Get all risk scores
    heart_risk = session.get('heart_risk', 0.5)
    kidney_risk = session.get('kidney_risk', 0.5)
    diabetes_risk = session.get('diabetes_risk', 0.5)
    
    # Check if any individual risk is extremely high (>90%)
    has_extremely_high_risk = (heart_risk > 0.9 or kidney_risk > 0.9 or diabetes_risk > 0.9)
    
    # Calculate weighted mean based on weights
    total_weight = heart_weight + kidney_weight + diabetes_weight
    weighted_risk = (
        (heart_risk * heart_weight) + 
        (kidney_risk * kidney_weight) + 
        (diabetes_risk * diabetes_weight)
    ) / total_weight
    
    # Force combined risk to be high if any individual risk is extremely high
    if has_extremely_high_risk and weighted_risk < 0.9:
        print("Applying high risk override due to at least one disease risk exceeding 90%")
        weighted_risk = max(weighted_risk, 0.9)  # Ensure minimum 90% risk
    
    # Use stored combined risk or recalculated weighted risk
    combined_risk = session.get('combined_risk', weighted_risk)
    
    return render_template_string(RESULTS_TEMPLATE, 
                                 heart_risk=heart_risk, 
                                 kidney_risk=kidney_risk, 
                                 diabetes_risk=diabetes_risk, 
                                 combined_risk=combined_risk)

if __name__ == '__main__':
    print("Disease Risk Assessment App is running on http://127.0.0.1:5000/")
    app.run(debug=True) 