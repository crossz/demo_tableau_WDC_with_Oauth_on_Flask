"""Python Flask WebApp Auth0 integration example
"""

import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

import datetime
from authlib.integrations.flask_client import OAuth
from authlib.integrations.requests_client import OAuth2Session
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request, make_response

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")



oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


fs_oauth = OAuth(app)
fs_oauth.register(
    "foursquare",
    client_id=env.get("FOURSQUARE_CLIENT_ID"),
    client_secret=env.get("FOURSQUARE_CLIENT_SECRET"),
    authorize_url=env.get("FOURSQUARE_AUTHORIZE_URL"),
    access_token_url=env.get("FOURSQUARE_ACCESSTOKEN_URL"),
    client_kwargs={
        'response_type':'code',
        # 'grant_type':'authorization_code',
    }
    
)

###################################
## Controllers API for FourSquare
###################################
@app.route("/foursquare")
# @csrf.exempt
def foursquare():
    print(session)
    return render_template(
        "foursquare.html"
    )

@app.route("/signin")
def signin():
    return fs_oauth.foursquare.authorize_redirect(
        redirect_uri=url_for("fs_redirect", _external=True)
    )

@app.route("/redirect", methods=["GET", "POST"])
# @csrf.exempt
def fs_redirect():
    print(request.args)
    print(session)
    token = fs_oauth.foursquare.authorize_access_token()
    print(token['access_token'])
    print(session)

    session['app'] = 'foursquare'

    # resp = make_response(url_for('foursquare'))
    # resp = make_response(render_template('index.html'))
    resp = redirect("/foursquare")
    resp.set_cookie('accessToken', token['access_token'], expires=datetime.datetime.now() + datetime.timedelta(days=30))
    return resp
    # return redirect("/four")


#############################
## Controllers API for Auth0
#############################
@app.route("/")
def home():
    # print(session)
    # if session:
        # print(session['user']['access_token'])
    resp = render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )
    return resp


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    accessToken = token['access_token']
    resp = redirect("/")
    resp.set_cookie('accessToken', accessToken, expires=datetime.datetime.now() + datetime.timedelta(days=3))
    return resp

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    resp = redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )
    resp.set_cookie('accessToken', '', expires=0)
    return resp



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))
