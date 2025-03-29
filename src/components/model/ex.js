const express = require('express');
const path = require('path');
const fs = require('fs');
const bodyParser = require('body-parser');
const tf = require('@tensorflow/tfjs-node');  // Make sure to install @tensorflow/tfjs-node

const app = express();
const SECRET_KEY = process.env.SECRET_KEY || 'your-default-secret';

// Set up view engine (using EJS as an example)
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Parse URL-encoded bodies (for form submissions)
app.use(bodyParser.urlencoded({ extended: true }));

// Define file paths (adjust paths as needed)
// Note: You must convert your model to TensorFlow.js format and export the scaler as JSON.
const MODEL_PATH = path.join(__dirname, 'model', 'heart');
const SCALER_PATH = path.join(__dirname, 'scaler.json');
const FEATURE_NAMES_PATH = path.join(__dirname, 'feature_names.json');

// Load assets
let model;
let scaler;
let FEATURE_NAMES;

async function loadAssets() {
  try {
    // Load the TensorFlow.js model from file system
    model = await tf.loadLayersModel(`file://${MODEL_PATH}`);
    console.log('Model loaded successfully.');

    // Load scaler parameters (assumed to be saved as JSON with keys "mean" and "scale")
    scaler = JSON.parse(fs.readFileSync(SCALER_PATH, 'utf8'));

    // Load feature names from JSON
    FEATURE_NAMES = JSON.parse(fs.readFileSync(FEATURE_NAMES_PATH, 'utf8'));
  } catch (err) {
    console.error('Error loading assets:', err);
    process.exit(1);
  }
}

loadAssets();

// Define optional constraints for some fields
const MEDICAL_CONSTRAINTS = {
  age: [0, 120],
  trestbps: [50, 250],
  chol: [100, 600],
  thalach: [60, 220],
  oldpeak: [0, 10]
};

// A helper function to scale the input values using the loaded scaler parameters.
// This example assumes that "scaler" has "mean" and "scale" arrays corresponding to the order of features.
function scaleInput(input) {
  if (!scaler.mean || !scaler.scale) {
    throw new Error('Scaler parameters not found');
  }
  return input.map((val, idx) => (val - scaler.mean[idx]) / scaler.scale[idx]);
}

// Home route – renders the form
app.get('/', (req, res) => {
  // Exclude "target" (the label) from features
  const formFeatures = FEATURE_NAMES.filter(feat => feat !== 'target');
  res.render('index', {
    features: formFeatures,
    constraints: MEDICAL_CONSTRAINTS,
    previous_values: {}
  });
});

// Prediction route – processes form input, validates data, scales the input, and makes a prediction
app.post('/predict', async (req, res) => {
  try {
    const features = [];
    const formFeatures = FEATURE_NAMES.filter(feat => feat !== 'target');
    
    // Extract and validate features from the form
    for (const field of formFeatures) {
      let value = req.body[field];
      if (!value || value.trim() === '') {
        throw new Error(`Field '${field}' is required.`);
      }
      if (field === 'sex') {
        // Convert gender to binary: "male" is 1; otherwise 0
        features.push(value.toLowerCase() === 'male' ? 1 : 0);
      } else {
        const num_value = parseFloat(value);
        if (isNaN(num_value)) {
          throw new Error(`Field '${field}' must be numeric.`);
        }
        if (MEDICAL_CONSTRAINTS[field]) {
          const [min_val, max_val] = MEDICAL_CONSTRAINTS[field];
          if (num_value < min_val || num_value > max_val) {
            throw new Error(`'${field}' must be between ${min_val} and ${max_val}.`);
          }
        }
        features.push(num_value);
      }
    }

    // Scale the input and prepare it as a tensor
    const scaledFeatures = scaleInput(features);
    const inputTensor = tf.tensor2d([scaledFeatures]);

    // Run prediction
    const predictionTensor = model.predict(inputTensor);
    const predictionData = await predictionTensor.data();
    const probability = predictionData[0];

    // Determine result based on threshold 0.5
    const result = probability > 0.5 ? 'Positive' : 'Negative';
    const resultClass = result === 'Positive' ? 'danger' : 'success';

    res.render('index', {
      prediction_text: result,
      result_class: resultClass,
      features: formFeatures,
      constraints: MEDICAL_CONSTRAINTS,
      previous_values: req.body
    });
  } catch (e) {
    console.error('Prediction error:', e);
    const formFeatures = FEATURE_NAMES.filter(feat => feat !== 'target');
    res.render('index', {
      error_text: e.message,
      features: formFeatures,
      constraints: MEDICAL_CONSTRAINTS,
      previous_values: req.body
    });
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server started on port ${PORT}`);
});
