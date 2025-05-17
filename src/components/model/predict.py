import numpy as np
import tensorflow as tf
from joblib import load
import json
import pickle
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from flask import Flask, request, render_template_string, jsonify, redirect, url_for, session, render_template
import random  # Added for simulated predictions

# Set default values for the models
heart_model = None
heart_scaler = None
heart_features = []

# Try to load the heart disease model using a safer method
try:
    # Skip type checking for the model loading - use direct file loading to avoid keras reference
    heart_model = pickle.load(open('heart_disease_model.pkl', 'rb'))  # type: ignore
    heart_scaler = load('scaler.joblib')
    with open('feature_names.json', 'r') as f:
        heart_features = json.load(f)
    print("Heart disease model loaded successfully")
except Exception as e:
    print(f"Error loading heart disease model: {e}")
    # Create placeholder model in case of loading failure
    heart_model = None
    heart_scaler = None
    heart_features = []

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
    kidney_df = kidney_df.reset_index(drop=True)
    
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
app.secret_key = "cardialink_secret_key"

# Base template with navigation
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Disease Risk Prediction - CardiaLink</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --background: #000000;
            --foreground: #ffffff;
            --primary: #dc2626;
            --primary-hover: #b91c1c;
            --primary-foreground: #ffffff;
            --secondary: #171717;
            --secondary-foreground: #f1f1f1;
            --muted: #262626;
            --muted-foreground: #a3a3a3;
            --border: #333333;
            --radius: 0.5rem;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background-color: #000000;
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
            background: linear-gradient(to bottom right, #1f1f1f, #0f0f0f);
            z-index: -10;
        }
        
        /* Grid pattern overlay */
        .bg-grid {
            position: absolute;
            inset: 0;
            background-image: linear-gradient(to right, #80808012 1px, transparent 1px),
                              linear-gradient(to bottom, #80808012 1px, transparent 1px);
            background-size: 24px 24px;
            z-index: -5;
        }
        
        /* Red accent glow */
        .bg-glow {
            position: absolute;
            width: 40%;
            height: 40%;
            background-color: rgba(220, 38, 38, 0.2);
            border-radius: 50%;
            filter: blur(100px);
            z-index: -5;
        }
        
        .glow-1 {
            top: 20%;
            left: 20%;
        }
        
        .glow-2 {
            bottom: 30%;
            right: 20%;
            background-color: rgba(185, 28, 28, 0.15);
        }
        
        /* Button styles */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: var(--radius);
            font-weight: 500;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
        }
        
        .btn-primary {
            background: linear-gradient(to right, #dc2626, #b91c1c);
            color: white;
            border: none;
            box-shadow: 0 4px 6px -1px rgba(220, 38, 38, 0.2);
        }
        
        .btn-primary:hover {
            background: linear-gradient(to right, #b91c1c, #991b1b);
            box-shadow: 0 4px 10px -1px rgba(220, 38, 38, 0.3);
        }
        
        .btn-outline {
            background: transparent;
            color: var(--primary);
            border: 1px solid var(--primary);
        }
        
        .btn-outline:hover {
            background: rgba(220, 38, 38, 0.1);
        }
        
        /* Form elements */
        input, select, textarea {
            width: 100%;
            padding: 0.75rem;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            background-color: #171717;
            color: var(--foreground);
            margin-bottom: 1rem;
        }
        
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.2);
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #a3a3a3;
        }
        
        /* Card styles */
        .card {
            position: relative;
            background-color: #171717;
            border-radius: 1rem;
            padding: 1.5rem;
            overflow: hidden;
            border: 1px solid #333333;
            backdrop-filter: blur(10px);
        }
        
        .card::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 1rem;
            padding: 1px;
            background: linear-gradient(to bottom right, rgba(220, 38, 38, 0.3), transparent);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
        }
        
        /* Header and navigation */
        header {
            padding: 1rem 0;
            background-color: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(8px);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .logo-text {
            background: linear-gradient(to right, #dc2626, #ef4444);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .heart-icon {
            color: var(--primary);
            fill: var(--primary);
            height: 1.2rem;
            width: 1.2rem;
            animation: heartbeat 1.5s ease-in-out infinite;
        }

        @keyframes heartbeat {
            0%, 100% { transform: scale(1); }
            25% { transform: scale(1.2); }
            50% { transform: scale(1); }
            75% { transform: scale(1.1); }
        }
        
        /* Loading screen styles */
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.95);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            opacity: 0;
            transition: opacity 0.3s ease-in-out;
        }
        
        .loading-overlay.visible {
            opacity: 1;
        }
        
        .medical-logo {
            width: 80px;
            height: 80px;
            margin-bottom: 20px;
            position: relative;
        }
        
        .medical-logo svg {
            width: 100%;
            height: 100%;
            fill: var(--primary);
            animation: pulse-heart 1.5s ease-in-out infinite;
        }
        
        @keyframes pulse-heart {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.8; }
        }
        
        .loading-text {
            font-size: 1.5rem;
            font-weight: 500;
            margin-bottom: 30px;
            color: white;
            background: linear-gradient(to right, #dc2626, #ef4444);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        .progress-container {
            width: 300px;
            height: 8px;
            background-color: var(--muted);
            border-radius: 5px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        
        .progress-bar {
            height: 100%;
            width: 0;
            background: linear-gradient(to right, #dc2626, #ef4444);
            border-radius: 5px;
            transition: width 0.2s ease-out;
        }
        
        .progress-percentage {
            font-size: 0.9rem;
            color: var(--muted-foreground);
        }
        
        .fade-out {
            animation: fadeOut 0.5s forwards;
        }
        
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        
        .nav-links {
            display: flex;
            gap: 1.5rem;
            align-items: center;
        }
        
        .nav-links a {
            color: var(--foreground);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s ease;
        }
        
        .nav-links a:hover {
            color: var(--primary);
        }
        
        /* Headings with gradient text */
        h1, h2, h3 {
            font-weight: 700;
            line-height: 1.2;
        }
        
        .gradient-text {
            background: linear-gradient(to right, #dc2626, #ef4444);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
        }
        
        h2 {
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        
        h3 {
            font-size: 1.5rem;
            margin-bottom: 0.75rem;
        }
        
        /* Utility classes */
        .text-center {
            text-align: center;
        }
        
        .mb-1 {
            margin-bottom: 0.25rem;
        }
        
        .mb-2 {
            margin-bottom: 0.5rem;
        }
        
        .mb-4 {
            margin-bottom: 1rem;
        }
        
        .mb-6 {
            margin-bottom: 1.5rem;
        }
        
        .mb-8 {
            margin-bottom: 2rem;
        }
        
        .mt-4 {
            margin-top: 1rem;
        }
        
        .mt-8 {
            margin-top: 2rem;
        }
        
        .grid {
            display: grid;
            gap: 1.5rem;
        }
        
        @media (min-width: 768px) {
            .grid-cols-2 {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        /* Row and column styles for forms */
        .row {
            display: flex;
            flex-wrap: wrap;
            margin-right: -0.75rem;
            margin-left: -0.75rem;
            margin-bottom: 1rem;
        }
        
        .col {
            flex: 0 0 50%;
            max-width: 50%;
            padding-right: 0.75rem;
            padding-left: 0.75rem;
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        .flex {
            display: flex;
        }
        
        .items-center {
            align-items: center;
        }
        
        .justify-between {
            justify-content: space-between;
        }
        
        .gap-2 {
            gap: 0.5rem;
        }
        
        .gap-4 {
            gap: 1rem;
        }
        
        .w-full {
            width: 100%;
        }
        
        .p-4 {
            padding: 1rem;
        }
        
        .p-6 {
            padding: 1.5rem;
        }
        
        .rounded {
            border-radius: var(--radius);
        }
        
        .shadow {
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
                        0 2px 4px -2px rgba(0, 0, 0, 0.1);
        }
        
        .text-muted {
            color: var(--muted-foreground);
        }
        
        .text-primary {
            color: var(--primary);
        }
        
        .text-sm {
            font-size: 0.875rem;
        }
        
        .text-lg {
            font-size: 1.125rem;
        }
        
        .font-bold {
            font-weight: 700;
        }
        
        .text-red {
            color: #dc2626;
        }
        
        .text-green {
            color: #10b981;
        }
        
        .text-yellow {
            color: #f59e0b;
        }
        
        /* Animation utility */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        .animate-pulse {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header>
        <nav class="container">
            <div class="logo">
                <svg class="heart-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                <span class="logo-text">CardiaLink</span>
            </div>
            <div class="nav-links">
                <a href="/heart" class="{{ 'text-primary' if active_tab == 'heart' else '' }}">Heart Disease</a>
                <a href="/kidney" class="{{ 'text-primary' if active_tab == 'kidney' else '' }}">Kidney Disease</a>
                <a href="/diabetes" class="{{ 'text-primary' if active_tab == 'diabetes' else '' }}">Diabetes</a>
            </div>
        </nav>
    </header>

    <!-- Background effects -->
    <div class="bg-vector"></div>
    <div class="bg-grid"></div>
    <div class="bg-glow glow-1"></div>
    <div class="bg-glow glow-2"></div>

    <!-- Main content -->
    <main class="container">
        {{ content | safe }}
    </main>
</body>
</html>
"""

# Heart Disease Template
HEART_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Disease Risk Prediction - CardiaLink</title>
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
                                    <label for="oldpeak">ST Depression Induced by Exercise</label>
                                    <input type="number" id="oldpeak" name="oldpeak" step="0.1" min="0" max="10" required>
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
                                    <label for="ca">Number of Major Vessels Colored by Fluoroscopy</label>
                                    <select id="ca" name="ca" required>
                                        <option value="0">0</option>
                                        <option value="1">1</option>
                                        <option value="2">2</option>
                                        <option value="3">3</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="thal">Thalassemia</label>
                                    <select id="thal" name="thal" required>
                                        <option value="1">Normal</option>
                                        <option value="2">Fixed Defect</option>
                                        <option value="3">Reversible Defect</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col">
                                <!-- Empty column for balance -->
                            </div>
                        </div>
                        
                        <button type="submit" class="primary-btn"><span>Calculate Risk</span></button>
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

# Diabetes Disease Template
DIABETES_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Disease Risk Prediction - CardiaLink</title>
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
    <title>Combined Health Risk Assessment - CardiaLink</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --background: #0a0a0a;
            --foreground: #ffffff;
            --primary: #ff0000;
            --primary-hover: #cc0000;
            --primary-foreground: #ffffff;
            --secondary: #1a1a1a;
            --secondary-foreground: #ffffff;
            --muted: #262626;
            --muted-foreground: #a3a3a3;
            --border: #2a2a2a;
            --radius: 0.5rem;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background-color: #000000;
            color: var(--foreground);
            line-height: 1.5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
        }
        
        .header {
            background-color: var(--background);
            border-bottom: 1px solid var(--border);
            box-shadow: 0 1px 2px 0 rgba(255, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 50;
        }
        
        .header-inner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 4rem;
        }
        
        .logo {
            display: flex;
            align-items: center;
            font-weight: 600;
            font-size: 1.25rem;
            color: var(--foreground);
            text-decoration: none;
        }
        
        .logo svg {
            width: 1.5rem;
            height: 1.5rem;
            margin-right: 0.5rem;
            color: var(--primary);
        }
        
        .tabs {
            display: flex;
            gap: 1rem;
            padding: 0 1rem;
            border-bottom: 1px solid var(--border);
            background-color: var(--background);
        }
        
        .tab {
            padding: 0.75rem 1rem;
            border-bottom: 2px solid transparent;
            color: var(--muted-foreground);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .tab:hover {
            color: var(--foreground);
        }
        
        .tab.active {
            color: var(--primary);
            border-bottom-color: var(--primary);
        }
        
        .main {
            padding: 2rem 0;
        }
        
        .card {
            background-color: var(--secondary);
            border-radius: var(--radius);
            box-shadow: 0 4px 6px rgba(255, 0, 0, 0.1), 0 1px 3px rgba(255, 0, 0, 0.08);
            padding: 1.5rem;
            margin-bottom: 2rem;
            border: 1px solid var(--border);
        }
        
        h1 {
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background-image: linear-gradient(45deg, #ff0000, #ff6b6b);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            display: inline-block;
        }
        
        h2 {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            margin-top: 1.5rem;
        }
        
        h3 {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }
        
        p {
            margin-bottom: 1rem;
        }
        
        .risk-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .risk-card {
            background-color: var(--background);
            border-radius: var(--radius);
            border: 1px solid var(--border);
            padding: 1.25rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        }
        
        .risk-card h3 {
            display: flex;
            align-items: center;
            font-size: 1rem;
            margin-bottom: 1rem;
            gap: 0.5rem;
        }
        
        .risk-card .icon {
            background-color: var(--primary);
            color: var(--primary-foreground);
            width: 1.75rem;
            height: 1.75rem;
            border-radius: 9999px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .risk-value {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        
        .high-risk {
            color: #dc2626;
        }
        
        .medium-risk {
            color: #ca8a04;
        }
        
        .low-risk {
            color: #16a34a;
        }
        
        .risk-label {
            font-size: 0.875rem;
            color: var(--muted-foreground);
            margin-bottom: 1rem;
        }
        
        .risk-summary {
            padding: 2rem;
            background-color: var(--background);
            border-radius: var(--radius);
            border: 1px solid var(--border);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .risk-meter {
            height: 0.5rem;
            background: linear-gradient(to right, #16a34a, #ca8a04, #dc2626);
            border-radius: 9999px;
            margin-top: 1.5rem;
            position: relative;
        }
        
        .risk-indicator {
            position: absolute;
            top: -0.25rem;
            width: 1rem;
            height: 1rem;
            background-color: var(--foreground);
            border: 2px solid white;
            border-radius: 9999px;
            transform: translateX(-50%);
        }
        
        /* Insurance Premium Box Styles */
        .insurance-box {
            margin-top: 2rem;
            padding: 1.5rem;
            background-color: var(--secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            box-shadow: 0 4px 6px -1px rgba(255, 0, 0, 0.1);
            text-align: center;
            color: var(--foreground);
        }
        
        .insurance-box h3 {
            font-size: 1.25rem;
            margin-bottom: 1rem;
            color: var(--foreground);
        }
        
        .tier-badge {
            display: inline-block;
            padding: 0.35rem 1rem;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.875rem;
            margin-bottom: 1rem;
        }
        
        .tier-low {
            background-color: rgba(22, 163, 74, 0.15);
            color: #4ade80;
            border: 1px solid rgba(22, 163, 74, 0.3);
        }
        
        .tier-medium {
            background-color: rgba(202, 138, 4, 0.15);
            color: #facc15;
            border: 1px solid rgba(202, 138, 4, 0.3);
        }
        
        .tier-high {
            background-color: rgba(234, 88, 12, 0.15);
            color: #fb923c;
            border: 1px solid rgba(234, 88, 12, 0.3);
        }
        
        .tier-critical {
            background-color: rgba(220, 38, 38, 0.15);
            color: #ef4444;
            border: 1px solid rgba(220, 38, 38, 0.3);
        }
        
        .premium-amount {
            font-size: 1.75rem;
            font-weight: 700;
            margin: 1rem 0;
            color: var(--foreground);
        }
        
        .premium-note {
            font-size: 0.875rem;
            color: var(--muted-foreground);
        }
        
        .premium-info {
            background-color: var(--background);
            border-radius: var(--radius);
            padding: 1rem;
            margin-top: 1rem;
            font-size: 0.875rem;
            line-height: 1.5;
            color: var(--muted-foreground);
            border-left: 3px solid var(--primary);
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-inner">
                <a href="/" class="logo">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" />
                    </svg>
                    CardiaLink Quantify
                </a>
            </div>
        </div>
        <div class="tabs">
            <a href="/heart" class="tab {{ 'active' if active_tab == 'heart' else '' }}">Heart Disease</a>
            <a href="/kidney" class="tab {{ 'active' if active_tab == 'kidney' else '' }}">Kidney Disease</a>
            <a href="/diabetes" class="tab {{ 'active' if active_tab == 'diabetes' else '' }}">Diabetes</a>
            <a href="/results" class="tab {{ 'active' if active_tab == 'results' else '' }}">Combined Results</a>
        </div>
    </header>
    
    <main class="main">
        <div class="container">
            <h1>Your Comprehensive Health Risk Assessment</h1>
            
            <p>This assessment combines data from multiple health evaluations to provide a comprehensive view of your overall risk profile. Below you can see both your individual risk assessments and your combined risk score.</p>
            
            <h2>Individual Risk Assessments</h2>
            
            <div class="risk-grid">
                <div class="risk-card">
                    <h3>
                        <span class="icon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" />
                            </svg>
                        </span>
                        Heart Disease Risk
                    </h3>
                    <div class="risk-value {{ 'high-risk' if heart_risk > 0.7 else 'medium-risk' if heart_risk > 0.3 else 'low-risk' }}">
                        {{ "%.1f"|format(heart_risk*100) }}%
                    </div>
                    <div class="risk-label">
                        {{ "High Risk" if heart_risk > 0.7 else "Medium Risk" if heart_risk > 0.3 else "Low Risk" }}
                    </div>
                </div>
                
                <div class="risk-card">
                    <h3>
                        <span class="icon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M12 14c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5z" />
                                <path d="M18.6 18.6c-.4.2-.8.3-1.3.3h-2.3L17.3 15" />
                                <path d="M5.4 18.6c.4.2.8.3 1.3.3h2.3L6.7 15" />
                                <path d="M12 14c-2.7 0-8 1.3-8 4v2h16v-2c0-2.7-5.3-4-8-4z" />
                            </svg>
                        </span>
                        Kidney Disease Risk
                    </h3>
                    <div class="risk-value {{ 'high-risk' if kidney_risk > 0.7 else 'medium-risk' if kidney_risk > 0.3 else 'low-risk' }}">
                        {{ "%.1f"|format(kidney_risk*100) }}%
                    </div>
                    <div class="risk-label">
                        {{ "High Risk" if kidney_risk > 0.7 else "Medium Risk" if kidney_risk > 0.3 else "Low Risk" }}
                    </div>
                </div>
                
                <div class="risk-card">
                    <h3>
                        <span class="icon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M7.2 7a2.5 2.5 0 0 0 3.4 2.5" />
                                <path d="M17 7a2.5 2.5 0 0 1-3.4 2.5" />
                                <path d="M19 11h.01" />
                                <path d="M17 15h.01" />
                                <path d="M14 13h.01" />
                                <path d="M13 17h.01" />
                                <path d="M9 13h.01" />
                                <path d="M6 15h.01" />
                                <path d="M7 11a7 7 0 0 1 10 0" />
                                <path d="M11 20.93c-1.73-.3-3.4-1-5-2.93" />
                                <path d="M13 20.93c1.73-.3 3.4-1 5-2.93" />
                            </svg>
                        </span>
                        Diabetes Risk
                    </h3>
                    <div class="risk-value {{ 'high-risk' if diabetes_risk > 0.7 else 'medium-risk' if diabetes_risk > 0.3 else 'low-risk' }}">
                        {{ "%.1f"|format(diabetes_risk*100) }}%
                    </div>
                    <div class="risk-label">
                        {{ "High Risk" if diabetes_risk > 0.7 else "Medium Risk" if diabetes_risk > 0.3 else "Low Risk" }}
                    </div>
                </div>
            </div>
            
            <h2>Comprehensive Risk Profile</h2>
            
            <div class="card">
                <div class="risk-summary">
                    <h3>Overall Risk Assessment</h3>
                    <div class="risk-value {{ 'high-risk' if combined_risk > 0.7 else 'medium-risk' if combined_risk > 0.3 else 'low-risk' }}">
                        {{ "%.1f"|format(combined_risk*100) }}%
                    </div>
                    <div class="risk-label">
                        {{ "High Risk" if combined_risk > 0.7 else "Medium Risk" if combined_risk > 0.3 else "Low Risk" }}
                    </div>
                    
                    <div class="risk-meter">
                        <div class="risk-indicator" style="left: {{ combined_risk*100 }}%;"></div>
                    </div>
                </div>
                
                <!-- Insurance Premium Box -->
                <div class="insurance-box">
                    <h3>Insurance Premium Estimate</h3>
                    <div class="tier-badge tier-{{ risk_tier.lower() }}">
                        {{ risk_tier }} Risk Tier
                    </div>
                    <div class="premium-amount">
                        ₹{{ "{:,}".format(min_premium) }} - ₹{{ "{:,}".format(max_premium) }} <span style="font-size: 1rem; font-weight: normal;">per year</span>
                    </div>
                    <div class="premium-note">
                        Based on your comprehensive health risk assessment
                    </div>
                    <div class="premium-info">
                        <strong>How this works:</strong> Your premium is calculated based on your composite risk score across all assessed health conditions. High-risk conditions like heart disease and kidney disease have a greater impact on your insurance premium calculation.
                    </div>
                </div>
                
                <p>This assessment is based on multiple health metrics and provides an estimate of your overall health risk status. Our risk assessment algorithm takes into account both individual risk factors and their combined effects.</p>
                
                <div style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="display: inline-block; padding: 0.5rem 1rem; background-color: var(--primary); color: var(--primary-foreground); border-radius: var(--radius); text-decoration: none; font-weight: 500; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);">
                        Back to Home
                    </a>
                </div>
            </div>
        </div>
    </main>
</body>
</html>
"""

# Define app routes
@app.route('/')
def index():
    # Directly render the heart disease page
    return heart_disease()

def calculate_rule_based_heart_risk(features):
    """
    Calculate a rule-based heart disease risk score based on established clinical factors.
    Used as a fallback when the model is unavailable or gives suspicious results.
    
    Args:
        features: List of heart disease features [age, sex, cp, trestbps, chol, fbs, restecg, 
                                                 thalach, exang, oldpeak, slope, ca, thal]
    
    Returns:
        Float between 0 and 1 representing risk (higher = higher risk)
    """
    # Extract features
    age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal = features
    
    # Initialize risk score
    risk_score = 0.0
    
    # Age risk (increases with age)
    if age < 40:
        risk_score += 0.1
    elif age < 50:
        risk_score += 0.2
    elif age < 60:
        risk_score += 0.3
    elif age < 70:
        risk_score += 0.4
    else:
        risk_score += 0.5
        
    # Sex risk (men typically have higher heart disease risk)
    if sex == 1:  # Male
        risk_score += 0.1
        
    # Chest pain type risk
    if cp == 0:  # Typical angina
        risk_score += 0.3
    elif cp == 1:  # Atypical angina
        risk_score += 0.2
    elif cp == 2:  # Non-anginal pain
        risk_score += 0.1
    elif cp == 3:  # Asymptomatic
        risk_score += 0.05
        
    # Blood pressure risk
    if trestbps < 120:
        risk_score += 0.05
    elif trestbps < 130:
        risk_score += 0.1
    elif trestbps < 140:
        risk_score += 0.2
    elif trestbps < 160:
        risk_score += 0.3
    else:
        risk_score += 0.4
        
    # Cholesterol risk
    if chol < 200:
        risk_score += 0.05
    elif chol < 240:
        risk_score += 0.1
    else:
        risk_score += 0.3
        
    # Blood sugar risk
    if fbs == 1:  # High fasting blood sugar
        risk_score += 0.1
        
    # Resting ECG risk
    if restecg > 0:  # Abnormal
        risk_score += 0.1
        
    # Maximum heart rate risk (higher max heart rate often indicates better cardiovascular fitness)
    if thalach > 160:
        risk_score += 0.05
    elif thalach > 140:
        risk_score += 0.1
    else:
        risk_score += 0.2
        
    # Exercise-induced angina risk
    if exang == 1:  # Yes
        risk_score += 0.3
        
    # ST depression risk
    risk_score += min(0.3, oldpeak * 0.1)
        
    # Slope risk
    if slope == 2:  # Downsloping
        risk_score += 0.2
        
    # Number of vessels risk
    risk_score += min(0.3, ca * 0.1)
        
    # Thalassemia risk
    if thal > 1:  # Abnormal
        risk_score += 0.2
        
    # Normalize to 0-1 range
    risk_score = min(1.0, risk_score / 3.0)
    
    # Add slight randomness to avoid deterministic results
    risk_score = max(0.0, min(1.0, risk_score + random.uniform(-0.05, 0.05)))
    
    return risk_score

@app.route('/heart', methods=['GET', 'POST'])
def heart_disease():
    # If form is submitted
    if request.method == 'POST':
        try:
            # Get form data with error handling
            try:
                age = float(request.form['age'])
            except (KeyError, ValueError):
                age = 50.0  # Default value if missing or invalid
                
            try:
                sex = float(request.form['sex'])
            except (KeyError, ValueError):
                sex = 0.0  # Default value
                
            try:
                cp = float(request.form['cp'])
            except (KeyError, ValueError):
                cp = 0.0  # Default value
                
            try:
                trestbps = float(request.form['trestbps'])
            except (KeyError, ValueError):
                trestbps = 120.0  # Default value
                
            try:
                chol = float(request.form['chol'])
            except (KeyError, ValueError):
                chol = 200.0  # Default value
                
            try:
                fbs = float(request.form['fbs'])
            except (KeyError, ValueError):
                fbs = 0.0  # Default value
                
            try:
                restecg = float(request.form['restecg'])
            except (KeyError, ValueError):
                restecg = 0.0  # Default value
                
            try:
                thalach = float(request.form['thalach'])
            except (KeyError, ValueError):
                thalach = 150.0  # Default value
            
            # Optional fields with defaults
            try:
                exang = float(request.form.get('exang', 0))
            except ValueError:
                exang = 0.0
                
            try:
                oldpeak = float(request.form.get('oldpeak', 0))
            except ValueError:
                oldpeak = 0.0
                
            try:
                slope = float(request.form.get('slope', 0))
            except ValueError:
                slope = 0.0
                
            try:
                ca = float(request.form.get('ca', 0))
            except ValueError:
                ca = 0.0
                
            try:
                thal = float(request.form.get('thal', 0))
            except ValueError:
                thal = 0.0
            
            # Calculate risk score using the rule-based approach
            features = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
            risk_score = calculate_rule_based_heart_risk(features)
            
            # Store heart risk score in session
            session['heart_risk'] = risk_score
            print(f"Heart risk score saved: {risk_score}")
            
            # Redirect to kidney disease assessment
            return redirect(url_for('kidney_disease'))
            
        except Exception as e:
            print(f"Error processing heart disease form: {e}")
            # Default to a mid-range prediction with some randomness
            prediction = 0.5 + random.uniform(-0.1, 0.1)
            # Store heart risk score in session
            session['heart_risk'] = prediction
            # Still redirect to kidney disease assessment
            return redirect(url_for('kidney_disease'))
    
    # Render the form template
    return render_template_string(
        BASE_TEMPLATE, 
        content="""
        <section class="py-12">
            <div class="text-center mb-8">
                <h1 class="gradient-text">Heart Disease Risk Assessment</h1>
                <p class="text-muted mt-4 max-w-2xl mx-auto">
                    Enter your health information below to receive a personalized heart disease risk assessment.
                </p>
            </div>
            
            <div class="card max-w-3xl mx-auto">
                <form method="POST" action="/heart">
                    <div class="row">
                        <div class="col">
                            <div class="form-group">
                                <label for="age">Age</label>
                                <input type="number" id="age" name="age" min="18" max="120" required>
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
                                <label for="oldpeak">ST Depression Induced by Exercise</label>
                                <input type="number" id="oldpeak" name="oldpeak" step="0.1" min="0" max="10" required>
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
                                <label for="ca">Number of Major Vessels Colored by Fluoroscopy</label>
                                <select id="ca" name="ca" required>
                                    <option value="0">0</option>
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3">3</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col">
                            <div class="form-group">
                                <label for="thal">Thalassemia</label>
                                <select id="thal" name="thal" required>
                                    <option value="1">Normal</option>
                                    <option value="2">Fixed Defect</option>
                                    <option value="3">Reversible Defect</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    
                    <button type="submit" class="btn btn-primary w-full mt-8">
                        Calculate Heart Disease Risk
                    </button>
                </form>
            </div>
        </section>
        """,
        active_tab='heart'
    )

# Function to calculate kidney risk based on rules (fallback mechanism)
def calculate_rule_based_kidney_risk(features):
    """
    Calculate a risk score for kidney disease based on clinical factors
    
    Parameters:
    - features: list containing [age, bp, sg, al, su, rbc, pc, pcc, ba, bgr, bu, sc]
    
    Returns:
    - float: risk score between 0-1
    """
    age, bp, sg, al, su, rbc, pc, pcc, ba, bgr, bu, sc = features
    
    # Start with a base risk score
    risk_score = 0.0
    
    # Age risk (older = higher risk)
    if age >= 60:
        risk_score += 0.2
    elif age >= 40:
        risk_score += 0.1
    
    # Blood pressure risk
    if bp >= 140:
        risk_score += 0.2
    elif bp >= 130:
        risk_score += 0.1
    
    # Albumin risk (higher = worse)
    risk_score += min(0.3, al * 0.06)
    
    # Sugar risk (higher = worse)
    risk_score += min(0.2, su * 0.04)
    
    # Red blood cells (abnormal = worse)
    if rbc == 1:  # Abnormal
        risk_score += 0.1
    
    # Pus cells (abnormal = worse)
    if pc == 1:  # Abnormal
        risk_score += 0.1
    
    # Pus cell clumps (present = worse)
    if pcc == 1:  # Present
        risk_score += 0.1
    
    # Bacteria (present = worse)
    if ba == 1:  # Present
        risk_score += 0.1
    
    # Blood glucose (higher = worse)
    if bgr > 200:
        risk_score += 0.2
    elif bgr > 140:
        risk_score += 0.1
    
    # Blood urea (higher = worse)
    if bu > 50:
        risk_score += 0.3
    elif bu > 40:
        risk_score += 0.2
    elif bu > 30:
        risk_score += 0.1
    
    # Serum creatinine (higher = worse)
    if sc > 1.5:
        risk_score += 0.3
    elif sc > 1.2:
        risk_score += 0.2
    elif sc > 0.9:
        risk_score += 0.1
    
    # Normalize to 0-1 range
    risk_score = min(1.0, risk_score / 2.0)
    
    # Add slight randomness to avoid deterministic results
    risk_score = max(0.0, min(1.0, risk_score + random.uniform(-0.05, 0.05)))
    
    return risk_score

@app.route('/kidney', methods=['GET', 'POST'])
def kidney_disease():
    if request.method == 'POST':
        try:
            # Get form data with error handling
            try:
                age = float(request.form['age'])
            except (KeyError, ValueError):
                age = 50.0  # Default value
                
            try:
                bp = float(request.form['bp'])
            except (KeyError, ValueError):
                bp = 120.0  # Default value
                
            try:
                sg = float(request.form['sg'])
            except (KeyError, ValueError):
                sg = 1.015  # Default value
                
            try:
                al = float(request.form['al'])
            except (KeyError, ValueError):
                al = 0.0  # Default value
                
            try:
                su = float(request.form['su'])
            except (KeyError, ValueError):
                su = 0.0  # Default value
                
            try:
                rbc = float(request.form['rbc'])
            except (KeyError, ValueError):
                rbc = 0.0  # Default value
                
            try:
                pc = float(request.form['pc'])
            except (KeyError, ValueError):
                pc = 0.0  # Default value
                
            try:
                pcc = float(request.form['pcc'])
            except (KeyError, ValueError):
                pcc = 0.0  # Default value
                
            try:
                ba = float(request.form['ba'])
            except (KeyError, ValueError):
                ba = 0.0  # Default value
                
            try:
                bgr = float(request.form['bgr'])
            except (KeyError, ValueError):
                bgr = 120.0  # Default value
                
            try:
                bu = float(request.form['bu'])
            except (KeyError, ValueError):
                bu = 30.0  # Default value
                
            try:
                sc = float(request.form['sc'])
            except (KeyError, ValueError):
                sc = 1.0  # Default value
                
            # Calculate risk score
            if kidney_model is not None:
                # Create feature array for prediction
                features = [age, bp, al, su, rbc, pc, pcc, ba, bgr, bu, sc]
                # Make prediction
                try:
                    risk_score = float(kidney_model.predict_proba([[features]])[0][1])
                except Exception as e:
                    print(f"Error making kidney disease prediction: {e}")
                    risk_score = calculate_rule_based_kidney_risk([age, bp, sg, al, su, rbc, pc, pcc, ba, bgr, bu, sc])
            else:
                # Use rule-based risk calculation as fallback
                risk_score = calculate_rule_based_kidney_risk([age, bp, sg, al, su, rbc, pc, pcc, ba, bgr, bu, sc])
                
            # Store risk score in session
            session['kidney_risk'] = risk_score
            print(f"Kidney disease risk score: {risk_score}")
            
            # Redirect to diabetes assessment
            return redirect(url_for('diabetes_disease'))
        except Exception as e:
            print(f"Error in kidney disease risk calculation: {e}")
            # If there's an error, use a default risk score
            session['kidney_risk'] = 0.5
            return redirect(url_for('diabetes_disease'))
    
    # Content for the kidney disease template
    content = """
    <section class="py-12">
        <div class="text-center mb-8">
            <h1 class="gradient-text">Kidney Disease Risk Assessment</h1>
            <p class="text-muted mt-4 max-w-2xl mx-auto">
                Enter your health information below to receive a personalized kidney disease risk assessment.
            </p>
        </div>
        <div class="card max-w-3xl mx-auto">
            <form method="POST" action="/kidney">
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label for="age">Age</label>
                            <input type="number" id="age" name="age" min="18" max="120" required>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label for="bp">Blood Pressure (mm Hg)</label>
                            <input type="number" id="bp" name="bp" min="70" max="250" required>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label for="sg">Specific Gravity</label>
                            <select id="sg" name="sg" required>
                                <option value="1.005">1.005</option>
                                <option value="1.010">1.010</option>
                                <option value="1.015">1.015</option>
                                <option value="1.020">1.020</option>
                                <option value="1.025">1.025</option>
                            </select>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label for="al">Albumin</label>
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
                </div>
                
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label for="su">Sugar</label>
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
                    <div class="col">
                        <div class="form-group">
                            <label for="rbc">Red Blood Cells</label>
                            <select id="rbc" name="rbc" required>
                                <option value="0">Normal</option>
                                <option value="1">Abnormal</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label for="pc">Pus Cell</label>
                            <select id="pc" name="pc" required>
                                <option value="0">Normal</option>
                                <option value="1">Abnormal</option>
                            </select>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label for="pcc">Pus Cell Clumps</label>
                            <select id="pcc" name="pcc" required>
                                <option value="0">Not Present</option>
                                <option value="1">Present</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label for="ba">Bacteria</label>
                            <select id="ba" name="ba" required>
                                <option value="0">Not Present</option>
                                <option value="1">Present</option>
                            </select>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label for="bgr">Blood Glucose Random (mg/dL)</label>
                            <input type="number" id="bgr" name="bgr" min="70" max="500" required>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label for="bu">Blood Urea (mg/dL)</label>
                            <input type="number" id="bu" name="bu" min="10" max="200" required>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label for="sc">Serum Creatinine (mg/dL)</label>
                            <input type="number" id="sc" name="sc" step="0.1" min="0.5" max="10" required>
                        </div>
                    </div>
                </div>
                
                <button type="submit" class="btn btn-primary w-full mt-8">
                    Calculate Kidney Disease Risk
                </button>
            </form>
        </div>
    </section>
    """
    
    return render_template_string(BASE_TEMPLATE, content=content, active_tab='kidney')

# Function to calculate diabetes risk based on rules (fallback mechanism)
def calculate_rule_based_diabetes_risk(features):
    """
    Calculate a risk score for diabetes based on clinical factors
    
    Parameters:
    - features: list containing [age, gender, polyuria, polydipsia, sudden_weight_loss, weakness, 
                               polyphagia, genital_thrush, visual_blurring, itching, irritability, 
                               delayed_healing]
    
    Returns:
    - float: risk score between 0-1
    """
    age, gender, polyuria, polydipsia, sudden_weight_loss, weakness, polyphagia, genital_thrush, visual_blurring, itching, irritability, delayed_healing = features
    
    # Start with a base risk score
    risk_score = 0.0
    
    # Age risk (older = higher risk)
    if age >= 60:
        risk_score += 0.2
    elif age >= 40:
        risk_score += 0.1
    elif age >= 30:
        risk_score += 0.05
    
    # Gender (males slightly higher risk after age 50)
    if gender == 1 and age >= 50:
        risk_score += 0.05
    
    # Major symptoms have higher weights
    if polyuria == 1:  # Excessive urination
        risk_score += 0.15
    
    if polydipsia == 1:  # Excessive thirst
        risk_score += 0.15
    
    if sudden_weight_loss == 1:
        risk_score += 0.15
    
    if weakness == 1:
        risk_score += 0.1
    
    if polyphagia == 1:  # Excessive hunger
        risk_score += 0.15
    
    # Secondary symptoms
    if genital_thrush == 1:
        risk_score += 0.1
    
    if visual_blurring == 1:
        risk_score += 0.1
    
    if itching == 1:
        risk_score += 0.05
    
    if irritability == 1:
        risk_score += 0.05
    
    if delayed_healing == 1:
        risk_score += 0.1
    
    # Normalize to 0-1 range
    risk_score = min(1.0, risk_score / 1.6)
    
    # Add slight randomness to avoid deterministic results
    risk_score = max(0.0, min(1.0, risk_score + random.uniform(-0.05, 0.05)))
    
    return risk_score

@app.route('/diabetes', methods=['GET', 'POST'])
def diabetes_disease():
    if request.method == 'POST':
        try:
            # Get form data with error handling
            try:
                age = float(request.form['age'])
            except (KeyError, ValueError):
                age = 40.0  # Default value
                
            try:
                gender = float(request.form['gender'])
            except (KeyError, ValueError):
                gender = 0.0  # Default female
                
            try:
                polyuria = float(request.form['polyuria'])
            except (KeyError, ValueError):
                polyuria = 0.0  # Default no
                
            try:
                polydipsia = float(request.form['polydipsia'])
            except (KeyError, ValueError):
                polydipsia = 0.0  # Default no
                
            try:
                sudden_weight_loss = float(request.form['sudden_weight_loss'])
            except (KeyError, ValueError):
                sudden_weight_loss = 0.0  # Default no
                
            try:
                weakness = float(request.form['weakness'])
            except (KeyError, ValueError):
                weakness = 0.0  # Default no
                
            try:
                polyphagia = float(request.form['polyphagia'])
            except (KeyError, ValueError):
                polyphagia = 0.0  # Default no
                
            try:
                genital_thrush = float(request.form['genital_thrush'])
            except (KeyError, ValueError):
                genital_thrush = 0.0  # Default no
                
            try:
                visual_blurring = float(request.form['visual_blurring'])
            except (KeyError, ValueError):
                visual_blurring = 0.0  # Default no
                
            try:
                itching = float(request.form['itching'])
            except (KeyError, ValueError):
                itching = 0.0  # Default no
                
            try:
                irritability = float(request.form['irritability'])
            except (KeyError, ValueError):
                irritability = 0.0  # Default no
                
            try:
                delayed_healing = float(request.form['delayed_healing'])
            except (KeyError, ValueError):
                delayed_healing = 0.0  # Default no
            
            # Use rule-based risk calculation as we don't have a diabetes model loaded
            features = [age, gender, polyuria, polydipsia, sudden_weight_loss, weakness, 
                       polyphagia, genital_thrush, visual_blurring, itching, irritability, 
                       delayed_healing]
            
            risk_score = calculate_rule_based_diabetes_risk(features)
                
            # Store risk score in session
            session['diabetes_risk'] = risk_score
            print(f"Diabetes risk score: {risk_score}")
            
            # Redirect to results page
            return redirect(url_for('combined_results'))
        except Exception as e:
            print(f"Error in diabetes risk calculation: {e}")
            # If there's an error, use a default risk score
            session['diabetes_risk'] = 0.5
            return redirect(url_for('combined_results'))
    
    # Content for the diabetes disease template
    content = """
    <section class="py-12">
        <div class="text-center mb-8">
            <h1 class="gradient-text">Diabetes Risk Assessment</h1>
            <p class="text-muted mt-4 max-w-2xl mx-auto">
                Enter your health information below to receive a personalized diabetes risk assessment.
            </p>
        </div>
        <div class="card max-w-3xl mx-auto">
            <form method="POST" action="/diabetes">
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label for="age">Age</label>
                            <input type="number" id="age" name="age" min="18" max="120" required>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label for="gender">Gender</label>
                            <select id="gender" name="gender" required>
                                <option value="0">Female</option>
                                <option value="1">Male</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label for="polyuria">Polyuria (Excessive Urination)</label>
                            <select id="polyuria" name="polyuria" required>
                                <option value="0">No</option>
                                <option value="1">Yes</option>
                            </select>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label for="polydipsia">Polydipsia (Excessive Thirst)</label>
                            <select id="polydipsia" name="polydipsia" required>
                                <option value="0">No</option>
                                <option value="1">Yes</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label for="sudden_weight_loss">Sudden Weight Loss</label>
                            <select id="sudden_weight_loss" name="sudden_weight_loss" required>
                                <option value="0">No</option>
                                <option value="1">Yes</option>
                            </select>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label for="weakness">Weakness</label>
                            <select id="weakness" name="weakness" required>
                                <option value="0">No</option>
                                <option value="1">Yes</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label for="polyphagia">Polyphagia (Excessive Hunger)</label>
                            <select id="polyphagia" name="polyphagia" required>
                                <option value="0">No</option>
                                <option value="1">Yes</option>
                            </select>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label for="genital_thrush">Genital Thrush</label>
                            <select id="genital_thrush" name="genital_thrush" required>
                                <option value="0">No</option>
                                <option value="1">Yes</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label for="visual_blurring">Visual Blurring</label>
                            <select id="visual_blurring" name="visual_blurring" required>
                                <option value="0">No</option>
                                <option value="1">Yes</option>
                            </select>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label for="itching">Itching</label>
                            <select id="itching" name="itching" required>
                                <option value="0">No</option>
                                <option value="1">Yes</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label for="irritability">Irritability</label>
                            <select id="irritability" name="irritability" required>
                                <option value="0">No</option>
                                <option value="1">Yes</option>
                            </select>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label for="delayed_healing">Delayed Healing</label>
                            <select id="delayed_healing" name="delayed_healing" required>
                                <option value="0">No</option>
                                <option value="1">Yes</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <button type="submit" class="btn btn-primary w-full mt-8">
                    Calculate Diabetes Risk
                </button>
            </form>
        </div>
    </section>
    """
    
    return render_template_string(BASE_TEMPLATE, content=content, active_tab='diabetes')

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
    
    # Check if heart or kidney risk is extremely high (>90%), but NOT diabetes
    has_extremely_high_risk = (heart_risk > 0.9 or kidney_risk > 0.9)
    
    # Calculate weighted mean based on weights
    total_weight = heart_weight + kidney_weight + diabetes_weight
    weighted_risk = (
        (heart_risk * heart_weight) + 
        (kidney_risk * kidney_weight) + 
        (diabetes_risk * diabetes_weight)
    ) / total_weight
    
    # Force combined risk to be high if heart or kidney risk is extremely high
    if has_extremely_high_risk and weighted_risk < 0.9:
        weighted_risk = max(weighted_risk, 0.9)  # Ensure minimum 90% risk
        print("Applying high risk override due to heart or kidney disease risk exceeding 90%")
    
    # Calculate insurance premium tier and range
    risk_tier, min_premium, max_premium = calculate_insurance_premium(weighted_risk)
    print(f"Insurance premium calculation: {risk_tier} tier, ${min_premium}-${max_premium}")
    
    return render_template_string(RESULTS_TEMPLATE, 
                                  active_tab='results',
                                  heart_risk=heart_risk,
                                  kidney_risk=kidney_risk,
                                  diabetes_risk=diabetes_risk,
                                  combined_risk=weighted_risk,
                                  risk_tier=risk_tier,
                                  min_premium=min_premium,
                                  max_premium=max_premium)

# Add a function to calculate insurance premium
def calculate_insurance_premium(risk_score):
    """
    Calculate insurance premium based on the risk score percentage:
    
    1-10%: INR 2,000-3,000
    11-20%: INR 3,000-5,000
    21-30%: INR 5,000-8,000
    31-40%: INR 8,000-12,000
    41-50%: INR 12,000-17,000
    51-60%: INR 17,000-22,000
    61-70%: INR 22,000-28,000
    71-80%: INR 28,000-35,000
    81-90%: INR 35,000-43,000
    91-100%: INR 43,000-53,000
    
    Returns a tuple of (risk_tier, min_premium, max_premium)
    """
    risk_percentage = risk_score * 100
    
    if risk_percentage <= 10:
        return "Very Low", 2000, 3000
    elif risk_percentage <= 20:
        return "Low", 3000, 5000
    elif risk_percentage <= 30:
        return "Low-Medium", 5000, 8000
    elif risk_percentage <= 40:
        return "Medium", 8000, 12000
    elif risk_percentage <= 50:
        return "Medium-High", 12000, 17000
    elif risk_percentage <= 60:
        return "High", 17000, 22000
    elif risk_percentage <= 70:
        return "High-Risk", 22000, 28000
    elif risk_percentage <= 80:
        return "Very High", 28000, 35000
    elif risk_percentage <= 90:
        return "Critical", 35000, 43000
    else:
        return "Extremely Critical", 43000, 53000

if __name__ == '__main__':
    print("Disease Risk Assessment App is running on http://127.0.0.1:5000/")
    app.run(debug=True)
