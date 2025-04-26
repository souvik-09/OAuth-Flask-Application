import requests

client_id = 'oauth provider client id goes here'
client_secret = 'oauth provider client secret goes here'
token_url = 'https://xxxxxxxx/nidp/oauth/nam/token'
redirect_uri = 'https://xxxxxx/callback'
authorization_base_url = 'https://xxxxxxxxxxx/nidp/oauth/nam/authz'
user_info_url = 'https://xxxxxxxx/nidp/oauth/nam/userinfo'
token_info_url = "https://xxxxxxxxxxx/nidp/oauth/nam/tokeninfo"

def get_access_token(username, password):

    payload = {
        'grant_type': 'password',
        'client_id': client_id,
        'client_secret': client_secret,
        'username': username,
        'password': password
    }
    print(type(payload))
    
    response = requests.post(token_url, data=payload, verify=False)
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None
        
def get_oauth_token_info(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(token_info_url, headers=headers, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the token information as a dictionary
    else:
        # Handle errors (e.g., invalid token, expired token)
        return {"error": f"Failed to retrieve token information, status code: {response.status_code}"} 

        