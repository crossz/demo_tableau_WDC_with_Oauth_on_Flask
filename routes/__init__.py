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

##########################################
# For non-flask usage
##########################################
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

redirect_back = '/'

def create_app():
    if not (env.get("APP_SECRET_KEY") and 
            env.get("AUTH0_CLIENT_ID") and 
            env.get("AUTH0_CLIENT_SECRET") and
            env.get("AUTH0_DOMAIN") and
            env.get("AUTH0_AUDIENCE")
            ):
        raise NameError("The required environment variables are missing. Check .env file.")

    app = Flask(__name__) # Flask(__name__, static_folder='static', template_folder='templates')
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



    #############################
    # Controllers API for WDC
    #############################
    @app.route("/cs_orderByTAT")
    def cs_order_by_tat():
        global redirect_back
        redirect_back = '/cs_orderByTAT'
        resp = render_template(
            "cs_orderByTAT/index.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )
        return resp

    @app.route("/cs_orderByRiskFactor")
    def cs_order_by_riskfactor():
        global redirect_back
        redirect_back = '/cs_orderByRiskFactor'
        resp = render_template(
            "cs_orderByRiskFactor/index.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )
        return resp

    @app.route("/cs_tatAchieveRate")
    def cs_tat_achieve_rate():
        global redirect_back
        redirect_back = '/cs_tatAchieveRate'
        resp = render_template(
            "cs_tatAchieveRate/index.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )
        return resp

    @app.route("/lab_qPCRRepeatCase")
    def lab_qpcr_repeat_case():
        global redirect_back
        redirect_back = '/lab_qPCRRepeatCase'
        resp = render_template(
            "lab_qPCRRepeatCase/index.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )
        return resp

    @app.route("/lab_ngsRepeatCase")
    def lab_ngs_repeat_case():
        global redirect_back
        redirect_back = '/lab_ngsRepeatCase'
        resp = render_template(
            "lab_ngsRepeatCase/index.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )
        return resp

    @app.route("/lab_tatOverview_and_byTAT")
    def lab_tat_overview_and_bytat():
        global redirect_back
        redirect_back = '/lab_tatOverview_and_byTAT'
        resp = render_template(
            "lab_tatOverview_and_byTAT/index.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )
        return resp

    @app.route("/lab_positiveResult")
    def lab_positive_result():
        global redirect_back
        redirect_back = '/lab_positiveResult'
        resp = render_template(
            "lab_positiveResult/index.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )
        return resp


    #############################
    # Controllers API for Auth0
    #############################
    @app.route("/")
    def home():
        resp = render_template(
            "home.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )
        return resp


    @app.route("/callback", methods=["GET", "POST"])
    def callback():
        global redirect_back
        token = oauth.auth0.authorize_access_token()
        session["user"] = token
        accesstoken = token['access_token']
        resp = redirect(redirect_back)
        resp.set_cookie('accessToken', accesstoken, expires=datetime.datetime.now() + datetime.timedelta(days=3))
        return resp

    @app.route("/login")
    def login():
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("callback", _external=True),
            audience=env.get("AUTH0_AUDIENCE")  ## JWT type token for custom API, must-have.
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

    return app

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=env.get("PORT", 3000))
