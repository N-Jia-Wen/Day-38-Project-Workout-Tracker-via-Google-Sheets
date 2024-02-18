import requests
from datetime import datetime
import os

NUTRITIONIX_APP_ID = os.environ["NUTRITIONIX_APP_ID"]
NUTRITIONIX_APP_KEY = os.environ["NUTRITIONIX_APP_KEY"]
SHEETY_AUTH = os.environ["SHEETY_AUTH"]
GENDER = os.environ["GENDER"]
WEIGHT_KG = float(os.environ["WEIGHT_KG"])
HEIGHT_CM = int(os.environ["HEIGHT_CM"])
AGE = int(os.environ["AGE"])
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]

NUTRITIONIX_HEADERS = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_APP_KEY
}

user_input = input("Tell me which exercises you did: ")
nutritionix_parameters = {
    "query": user_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
sheety_headers = {
    "Authorization": SHEETY_AUTH
}

exercise_response = requests.post(url=NUTRITIONIX_ENDPOINT, json=nutritionix_parameters, headers=NUTRITIONIX_HEADERS)
exercise_response.raise_for_status()
exercise_data = exercise_response.json()["exercises"]
date = datetime.now()


for exercise in exercise_data:
    # For Sheety, keys must be in lowercase, while values are in camelCase:
    sheety_config = {
        "workout": {
            "date": date.strftime("%d/%m/%Y").title(),
            "time": date.strftime("%X").title(),
            "exercise": exercise["name"].title(),
            "duration": str(exercise["duration_min"]).title(),
            "calories": str(exercise["nf_calories"]).title()
        }
    }

    sheety_post_response = requests.post(url=SHEETY_ENDPOINT, json=sheety_config, headers=sheety_headers)
    sheety_post_response.raise_for_status()
    print(sheety_post_response.status_code)
