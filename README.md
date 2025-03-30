# CardiaLink Quantify

A comprehensive health risk assessment application that evaluates heart disease, kidney disease, and diabetes risk factors to provide personalized health risk predictions.

## Features

- **Multi-disease Risk Assessment**: Analyzes risk factors for heart disease, kidney disease, and diabetes
- **Weighted Prediction Model**: Combines multiple disease risks into a single comprehensive health score
- **Priority-based Weighting**: Heart disease (50%), kidney disease (30%), and diabetes (20%)
- **High-Risk Detection**: Automatically elevates overall risk assessment when any individual disease risk exceeds 90%
- **Interactive User Interface**: Clean, responsive design with intuitive forms and visual risk indicators
- **Sequential Assessment Process**: Guides users through a step-by-step assessment of each disease

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Machine Learning**: TensorFlow, scikit-learn, joblib
- **Data Processing**: pandas, NumPy

## How It Works

1. Users are first assessed for heart disease risk based on key cardiovascular indicators
2. The assessment continues with kidney disease evaluation
3. Diabetes risk factors are then analyzed
4. A comprehensive health risk score is calculated using a weighted mean of all three assessments
5. Results are presented in an easy-to-understand format with visual indicators and risk levels

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Required Python packages (see requirements.txt)

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cardialink-quantify.git
   cd cardialink-quantify
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   cd src/components/model
   python predict.py
   ```

5. Open a web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Web Application

The main application consists of:
- A responsive health assessment interface
- Step-by-step disease risk evaluation
- Visual risk indicators and comprehensive results dashboard
- Personalized recommendations based on risk assessment

## Future Enhancements

- User accounts and saved assessments
- Detailed health recommendation engine
- Integration with health tracking devices
- Expanded disease risk models

## Contributors

- HIMANSHU SINGH
- AYAN DAFADAR
- SHIVAM KUMAR
