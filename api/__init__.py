##########################################
# External Modules
##########################################

import os

from flask import Flask, jsonify #把資料轉化成JSON結構
from flask_cors import CORS
from flask_talisman import Talisman
from dotenv import find_dotenv, load_dotenv

from api import exception_views
from api.messages import messages_views
from api.security.auth0_service import auth0_service

from api.database import __get_cursor

from api.api_route.cs_dashboard_p0 import cs_p0_app
from api.api_route.lab_dashboard_p0 import lab_p0_app


##########################################
# For non-flask usage
##########################################
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

def create_app():
    ##########################################
    # Environment Variables
    ##########################################
    client_origin_url = os.environ.get("CLIENT_ORIGIN_URL")
    auth0_audience = os.environ.get("AUTH0_AUDIENCE")
    auth0_domain = os.environ.get("AUTH0_DOMAIN")

    if not (client_origin_url and auth0_audience and auth0_domain):
        raise NameError("The required environment variables are missing. Check .env file.")

    ##########################################
    # Flask App Instance
    ##########################################

    app = Flask(__name__, instance_relative_config=True)


    ##########################################
    # HTTP Security Headers
    ##########################################

    csp = {
        'default-src': ['\'self\''],
        'style-src': ['\'unsafe-inline\''],
        'frame-ancestors': ['\'none\''],
    }

    Talisman(app,
             force_https=False,
             frame_options='DENY',
             content_security_policy=csp,
             referrer_policy='no-referrer'
             )

    auth0_service.initialize(auth0_domain, auth0_audience)

    @app.after_request
    def add_headers(response):
        response.headers['X-XSS-Protection'] = '0'
        response.headers['Cache-Control'] = 'no-store, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    ##########################################
    # CORS
    ##########################################

    CORS(
        app,
        resources={r"/api/*": {"origins": client_origin_url}},
        allow_headers=["Authorization", "Content-Type"],
        methods=["GET"],
        max_age=86400
    )

    ##########################################
    # MYSQL (python_mysqldb, which depends on system-level mysql-devel)
    ##########################################
    # app.config.from_object(mysql_config)
    # mysql = MySQL(app)



    # '''
    # 以下代碼包括首頁和測試用的Api
    # @app.route("/")為api的URL路徑
    # 路徑下方的函式則是該接口將運行的程序
    # '''
    # # 首頁，暫時無用
    # @app.route("/")
    # def home_page():
    #     return "<h1>It's working!!!</h1>"

    # # 測試api，返回qPCR Repeat Case 圖表所需的數據
    # # 代碼拆解如下
    # @app.route("/dataextraction", methods = ['GET'])
    # def data_api():
    #     with app.app_context():
    #         # 呼叫SQL游標物件
    #         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #         # 執行括號內的SQL指令，指令是一個字串
    #         cursor.execute(""" SELECT Operation.master_id AS Master_Lab_ID, \
    #                                 (CASE \
    #                                     WHEN Operation.operation IN (10, 20) \
    #                                     THEN "Yes" \
    #                                     ELSE "No" \
    #                                 END ) AS is_repeat, \
    #                                 (CASE \
    #                                     WHEN Operation.admin_report_type IN ("qPCR Extraction", "qPCR Run", "qPCR  Result Review") \
    #                                     THEN "Yes" \
    #                                     ELSE "No" \
    #                                 END) AS is_qPCR, \
    #                                 DATE_FORMAT(Operation.update_time, '%Y-%m-%d %H:%i:%s') AS approval_time \
    #                         FROM `lims-meinv`.t_batch_specimen_operation AS Operation \
    #                         LEFT JOIN `lims-meinv`.t_specimen AS Specimen ON Operation.master_id = Specimen.marster_id \
    #                         WHERE Operation.specimen_id IS NOT NULL \
    #                                 AND Operation.is_finish = 1 \
    #                                 AND Specimen.specimen_type = "Clinical" \
    #                         GROUP BY master_id; """)
    #         # 將返回所有結果，得到的結果如({"Master_Lab_ID": 21B0027-7, "is_repeat": Yes}, {"Master_Lab_ID": 21E0036-6, "is_repeat": No}.......)
    #         extracted_data = cursor.fetchall()
    #         # 關閉游標物件
    #         cursor.close()
    #     # 把查詢結果轉化成JSON格式並返回到前端
    #     return jsonify({"table": extracted_data})


    ##########################################
    # Blueprint Registration
    ##########################################

    app.register_blueprint(messages_views.bp)
    app.register_blueprint(exception_views.bp)

    
    app.register_blueprint(cs_p0_app)
    app.register_blueprint(lab_p0_app)

    return app

