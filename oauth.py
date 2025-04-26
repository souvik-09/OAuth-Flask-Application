from flask import Flask, session, redirect, url_for, request, render_template, jsonify
from services import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(15)


@app.route('/')
def index():
    if 'access_token' in session:
        return redirect(url_for('success'))
    return 'You are not logged in. <a href="/login">Login</a>'

@app.route('/login')
def login():
    # Redirect the user to Access Manager's login page
    authorization_url = f"{authorization_base_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    
    if code:
        # Exchange the authorization code for an access token
        token_response = requests.post(token_url, data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }, verify=False)
        
        if token_response.status_code == 200:
            access_token = token_response.json().get('access_token')
            session['access_token'] = access_token

            # Retrieve user info using the access token
            user_info = get_oauth_token_info(access_token)
            print(user_info)
            
            # Store user info in session
            session['username'] = user_info.get('user_id')
            #session['email'] = user_info.get('email')
            #session['profile'] = user_info
            
            return redirect(url_for('success'))
        else:
            return 'Failed to retrieve access token.'
    
    return 'Authorization failed.'

@app.route('/success')
def success():
    if 'username' not in session:
        return redirect(url_for('index'))

    return f"Success! You are now authorized as: {session.get('username')}"
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
