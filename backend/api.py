# Get model from JSON file stored in S3 - keep access details in an ENV variable
# Take input from API call and run through the model
# Return result of API call to caller
# Save to CSV stored in S3
import json
import xgboost as xgb

# PUT IN ENV
MODEL_PATH = 
DB_PATH = 

def load_model():
    # Get JSON config from S3
    
    # Load model
    model = xgb.Booster()
    model.load_model("model.json")

    return model

def run_model(model, data):
    model.predict(data)

def save_result(result):
    # Get CSV file from S3
    
    # Append result to CSV
     
    # Save CSV file back to S3
    

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))

    # Extract parameters
    try:
        name = body.get("name")
        email = body.get("email")
        address = body.get("address")
        zipcode = body.get("zipcode")
        hvac_age = body.get("hvac_age")
        water_heater_age = body.get("water_heater_age")
        washer_dryer_age = body.get("washer_dryer_age")
        percent_older_bulbs = body.get("percent_older_bulbs")
        kitchen_appliances_age = body.get("kitchen_appliances_age")
        identifiers = [name, email, address, zipcode]
        data = [zipcode, hvac_age, water_heater_age, washer_dryer_age, percent_older_bulbs, kitchen_appliances_age]
    except: # TODO error handling for unknown zip!
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing parameters"}),
        }
    
    model = load_model()
    result = run_model(model, data)
    
    save_result(result)
    
    response = {
        "statusCode": 200,
        "body": json.dumps(result),
    }
    
    return response
