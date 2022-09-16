"""Python Flask WebApp Auth0 integration example
"""

from flask import (
    Blueprint
)

import json
from urllib.parse import quote_plus, urlencode

import datetime
from flask import Flask, redirect, render_template, session, url_for, request, make_response

from routes.messages.messages_service import (
    get_public_message
)

bp_name = 'routes'
bp_url_prefix = '/'
bp = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix)

@bp.route("/public")
def public():
    return {
        "text": get_public_message().text
    }

