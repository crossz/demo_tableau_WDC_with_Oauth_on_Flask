Auth0 Protected API for Tableau WDC
====

**02-api-module**

1. Prepare .env file.
```
AUTH0_CLIENT_ID=
AUTH0_CLIENT_SECRET=
AUTH0_DOMAIN=
AUTH0_AUDIENCE=
APP_SECRET_KEY=
CLIENT_ORIGIN_URL=http://localhost:3000
```

2. Create venv environment and install from requirement.txt

3. run

2 separate flask apps:

auth0.js should adjust the api url to work on port 6060. The API protected with auth0 refers to https://auth0.com/developers/hub/code-samples/api/flask-python/basic-authorization

```
# start home and login web app
gunicorn 'routes:create_app()' -b 0.0.0.0:3000

# start api service
gunicorn 'api:create_app()' -b 0.0.0.0:6060
## or
flask run ## alternative method, configured in .flaskenv
```

1 wsgi app combined with above 2 flask apps together:

auth0.js should adjust the api url to work on port 3000

```
gunicorn server:application -b 0.0.0.0:3000
## or
python server.py ## alternative way, with debugger
```

4. run Tableau WDC Simulator

5. Connector URL: `http://localhost:3000`

6. Get the Table data

| Name | Message |
|:--|:--|
| text | The API successfully validated your access token.
 |


-------


Reference: Tableau Official Example with Oauth
====

This is the demo, which uses Flask to replace the used express.jd in examples coming along with Tableau WDC v2.0.

So that data analysis job can easily be carried out with Python only, no Express.js and corresponding node.js hosting tricks needed.

## Run It

**Start Page**

Commands, 3 ways:
```
# python: raw
python server.py

# flask: with .flaskenv file
flask run

# gunicorn: raw
gunicorn server:app -b 0.0.0.0:3000
```

For FourSquare Oauth example:

http://localhost:3000/foursquare


## Original Repo of Tableau WDC v2.0 Examples

https://github.com/tableau/webdataconnector

----
Original Repo of Flask w/ Auth0
====

This sample demonstrates how to add authentication to a Python web app using Auth0.

# Running the App

To run the sample, make sure you have `python3` and `pip` installed.

Rename `.env.example` to `.env` and populate it with the client ID, domain, secret, callback URL and audience for your
Auth0 app. If you are not implementing any API you can use `https://YOUR_DOMAIN.auth0.com/userinfo` as the audience.
Also, add the callback URL to the settings section of your Auth0 client.

Register `http://localhost:3000/callback` as `Allowed Callback URLs` and `http://localhost:3000`
as `Allowed Logout URLs` in your client settings.

Run `pip install -r requirements.txt` to install the dependencies and run `python server.py`.
The app will be served at [http://localhost:3000/](http://localhost:3000/).

# Running the App with Docker

To run the sample, make sure you have `docker` installed.

To run the sample with [Docker](https://www.docker.com/), make sure you have `docker` installed.

Rename the .env.example file to .env, change the environment variables, and register the URLs as explained [previously](#running-the-app).

Run `sh exec.sh` to build and run the docker image in Linux or run `.\exec.ps1` to build
and run the docker image on Windows.

## What is Auth0?

Auth0 helps you to:

* Add authentication with [multiple authentication sources](https://auth0.com/docs/identityproviders),
either social like **Google, Facebook, Microsoft Account, LinkedIn, GitHub, Twitter, Box, Salesforce, among others**,or
enterprise identity systems like **Windows Azure AD, Google Apps, Active Directory, ADFS or any SAML Identity Provider**.
* Add authentication through more traditional **[username/password databases](https://docs.auth0.com/mysql-connection-tutorial)**.
* Add support for **[linking different user accounts](https://auth0.com/docs/link-accounts)** with the same user.
* Support for generating signed [JSON Web Tokens](https://auth0.com/docs/jwt) to call your APIs and
**flow the user identity** securely.
* Analytics of how, when and where users are logging in.
* Pull data from other sources and add it to the user profile, through [JavaScript rules](https://auth0.com/docs/rules).

## Create a free account in Auth0

1. Go to [Auth0](https://auth0.com) and click Sign Up.
2. Use Google, GitHub or Microsoft Account to login.

## Issue Reporting

If you have found a bug or if you have a feature request, please report them at this repository issues section.
Please do not report security vulnerabilities on the public GitHub issue tracker.
The [Responsible Disclosure Program](https://auth0.com/whitehat) details the procedure for disclosing security issues.

## Author

[Auth0](https://auth0.com)

## License

This project is licensed under the MIT license. See the [LICENSE](../LICENSE) file for more info.
