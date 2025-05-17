# Import the Flask app from the main application file
from src.components.model.predict import app

# Run the Flask app if this file is executed directly
if __name__ == '__main__':
    print("Disease Risk Assessment App is running on http://127.0.0.1:5000/")
    app.run(debug=True) 