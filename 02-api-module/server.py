from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix
from werkzeug.serving import run_simple
import api
import routes

flask_app_1 = routes.create_app()
flask_app_2 = api.create_app()

application = DispatcherMiddleware(flask_app_1, {
    '/v2': flask_app_2
})

if __name__ == '__main__':
    run_simple('localhost', 3000, application, use_reloader=True, use_debugger=True, use_evalex=True)