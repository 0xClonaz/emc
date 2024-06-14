from flask import Flask, request, jsonify
from flask_cors import CORS
import pwnedpasswords
import requests
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/api/v1/check_if_pw_leaked', methods=['GET'])
def check_password():
    password = request.args.get('password')
    if not password:
        return jsonify({'error': 'No password provided'}), 400

    pw2 = pwnedpasswords.check(password)
    if pw2 > 0:
        return jsonify({'found_in_leaked_databases': str(pw2), 'leaked': True})
    else:
        return jsonify({'leaked': False})

@app.route('/api/v1/search_email', methods=['GET'])
def search_email():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'No email provided'}), 400

    url = "https://api-experimental.snusbase.com/data/search"
    headers = {
        "Auth": "sbx39mh542d0oshydtx3oes9whn1ay",
        "Content-Type": "application/json"
    }
    data = {
        "terms": [email],
        "types": ["email"],
        "wildcard": False
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise HTTPError for bad responses
        app.logger.debug(f"Snusbase response: {response.json()}")
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching data from Snusbase: {e}")
        return jsonify({'error': 'Failed to fetch data from Snusbase'}), 500

if __name__ == '__main__':
    app.run(debug=True)
