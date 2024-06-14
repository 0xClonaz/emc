from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/v1/search_email', methods=['GET'])
def search_email():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'No email provided'}), 400

    url = "https://demo.leakedapi.com"  # Replace with correct endpoint
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",  # Replace with actual authorization header if needed
        "Content-Type": "application/json"
    }
    params = {
        "email": email
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching data from LeakedAPI: {e}")
        return jsonify({'error': 'Failed to fetch data from LeakedAPI'}), 500

if __name__ == '__main__':
    app.run(debug=True)
