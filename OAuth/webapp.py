from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import json
import os

app = Flask(__name__)

# Read in credentials from creds.json
fileObject = open("creds.json", "r")
jsoncontent = fileObject.read()
creds = json.loads(jsoncontent)

# Updated variables with values from the json file
client_id = creds['client_id']
client_secret = creds['client_secret']
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

@app.route("/")
def demo():
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route("/callback", methods=["GET"])
def callback():
    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    session['oauth_token'] = token
    return redirect(url_for('.profile'))

@app.route("/profile", methods=["GET"])
def profile():
    github = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(github.get('https://api.github.com/user').json())

if __name__ == "__main__":
    # Enable SSL for enhanced security
    app.secret_key = os.urandom(24)
    app.run(ssl_context="adhoc")
