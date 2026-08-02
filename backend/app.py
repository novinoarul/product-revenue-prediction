# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
product_revenue_predictor_api = Flask("SuperKart Revenue Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_revenue_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@product_revenue_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Revenue Prediction API!"

# Define an endpoint for single product prediction (POST request)
@product_revenue_predictor_api.post('/v1/revenue')
def predict_revenue():
    """
    This function handles POST requests to the '/v1/revenue' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    property_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Id_Char': property_data['Product_Id_Char'],
        'Product_Weight': property_data['Product_Weight'],
        'Product_Sugar_Content': property_data['Product_Sugar_Content'],
        'Product_Allocated_Area': property_data['Product_Allocated_Area'],
        'Product_MRP': property_data['Product_MRP'],
        'Store_Size': property_data['Store_Size'],
        'Store_Location_City_Type': property_data['Store_Location_City_Type'],
        'Store_Type': property_data['Store_Type'],
        'Store_Age_Years': property_data['Store_Age_Years'],
        'Product_Type_Category': property_data['Product_Type_Category']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    predicted_sales = model.predict(input_data)[0]

    # Convert predicted_sales to Python float
    predicted_sales = round(float(predicted_sales), 2)

    # Return the actual price
    return jsonify({'Predicted Sales (in dollars)': predicted_sales})


# Define an endpoint for batch prediction (POST request)
@product_revenue_predictor_api.post('/v1/revenuebatch')
def predict_revenue_batch():
    """
    This function handles POST requests to the '/v1/revenuebatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_sales = model.predict(input_data).tolist()

    # Calculate actual prices
    predicted_sales = [round(sale, 2) for sale in predicted_sales]

    # Return the predictions dictionary as a JSON response
    return {'predicted_sales': predicted_sales}

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    product_revenue_predictor_api.run(debug=True)
