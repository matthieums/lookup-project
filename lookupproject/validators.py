import requests
from django.core.exceptions import ValidationError


def validate_location(location):
    print('validating......')
    # If I change the API key, make sure to change it in main JS globals too
    api_key = "931a2f65384241b19147a6b601733f10"
    url = f"https://api.geoapify.com/v1/geocode/search?text={location}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if 'features' not in data or len(data['features']) == 0:
        raise ValidationError("The address is not valid. Please provide a valid address.")