from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# API Keys
GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"
REALTOR_API_KEY = "YOUR_REALTOR_API_KEY"
REALTOR_API_HOST = "realestate12.p.rapidapi.com"

@app.route('/get_housing', methods=['GET'])
def get_housing():
    # Extract query parameters
    college_name = request.args.get('college')
    max_price = int(request.args.get('max_price', 2000))  # Default: $2000
    radius = float(request.args.get('radius', 1))  # Default: 1 mile

    if not college_name:
        return jsonify({"error": "Please provide a college name"}), 400

    # Step 1: Geocode the college location using Google Maps API
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json"
    geocode_params = {
        "address": college_name,
        "key": GOOGLE_MAPS_API_KEY
    }
    geocode_response = requests.get(geocode_url, params=geocode_params)
    geocode_data = geocode_response.json()

    if geocode_data.get("status") != "OK":
        return jsonify({"error": "Failed to geocode the college name", "details": geocode_data}), 400

    # Extract latitude and longitude of the college
    location = geocode_data['results'][0]['geometry']['location']
    latitude = location['lat']
    longitude = location['lng']

    # Step 2: Query Realtor API for rental properties
    realtor_url = f"https://{REALTOR_API_HOST}/listings/rent"
    realtor_headers = {
        "X-RapidAPI-Key": REALTOR_API_KEY,
        "X-RapidAPI-Host": REALTOR_API_HOST
    }
    realtor_params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,  # Radius in miles
        "min_price": 0,    # Minimum price
        "max_price": max_price,  # Maximum price
        "limit": 50        # Max results per page
    }
    realtor_response = requests.get(realtor_url, headers=realtor_headers, params=realtor_params)
    realtor_data = realtor_response.json()

    if realtor_response.status_code != 200 or not realtor_data.get("data"):
        return jsonify({"error": "Failed to fetch housing data", "details": realtor_data}), 400

    # Step 3: Format and return the results
    housing_options = []
    for listing in realtor_data["data"]["home_search"]["results"]:
        housing_options.append({
            "address": listing.get("location", {}).get("address", {}).get("line"),
            "city": listing.get("location", {}).get("address", {}).get("city"),
            "state": listing.get("location", {}).get("address", {}).get("state"),
            "price": listing.get("list_price"),
            "bedrooms": listing.get("description", {}).get("beds"),
            "bathrooms": listing.get("description", {}).get("baths"),
            "latitude": listing.get("location", {}).get("address", {}).get("lat"),
            "longitude": listing.get("location", {}).get("address", {}).get("lon")
        })

    return jsonify({
        "college": college_name,
        "latitude": latitude,
        "longitude": longitude,
        "housing_options": housing_options
    })

if __name__ == '__main__':
    app.run(debug=True)
