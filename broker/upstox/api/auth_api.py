import json
import os
import httpx
from utils.httpx_client import get_httpx_client



def authenticate_broker(code):
    try:
        BROKER_API_KEY = os.getenv('BROKER_API_KEY')
        BROKER_API_SECRET = os.getenv('BROKER_API_SECRET')
        REDIRECT_URL = os.getenv('REDIRECT_URL')
        url = 'https://api.upstox.com/v2/login/authorization/token'
        data = {
            'code': code,
            'client_id': BROKER_API_KEY,
            'client_secret': BROKER_API_SECRET,
            'redirect_uri': REDIRECT_URL,
            'grant_type': 'authorization_code',
        }
        # Get the shared httpx client
        client = get_httpx_client()
        response = client.post(url, data=data)

        if response.status_code == 200:
            response_data = response.json()
            if 'access_token' in response_data:
                return response_data['access_token'], None
            else:
                return None, "Authentication succeeded but no access token was returned. Please check the response."
        else:
            # Parsing the error message from the API response
            error_detail = response.json()  # Assuming the error is in JSON format
            error_messages = error_detail.get('errors', [])
            detailed_error_message = "; ".join([error['message'] for error in error_messages])
            return None, f"API error: {error_messages}" if detailed_error_message else "Authentication failed. Please try again."
    except Exception as e:
        return None, f"An exception occurred: {str(e)}"

