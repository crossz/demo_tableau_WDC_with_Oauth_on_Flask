from os import environ as env
from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix
from werkzeug.serving import run_simple
import api
import routes

flask_app_1 = routes.create_app()
flask_app_2 = api.create_app()

app = DispatcherMiddleware(flask_app_1, {
    '/api/v2': flask_app_2
})

port = int(env.get("PORT", 5000))

if __name__ == '__main__':
    run_simple('0.0.0.0', port, app, use_reloader=True, use_debugger=True, use_evalex=True)
