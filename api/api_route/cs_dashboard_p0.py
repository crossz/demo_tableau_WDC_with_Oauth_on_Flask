'''
說明：
當前程式檔主要存放CS界面在P0階段所需的api, 並在app.py導入 (方便管理)
由於每個api的代碼結構都很相似, 所以api代碼解析只放在init.py的例子
'''


'''
Api 所需的庫
'''
# 導入已初始化的Flask應用程序和mysql資料庫物件
from api.database import __get_cursor
# from flask_mysqldb import MySQLdb # 向MySQL進行CRUD操作


# Flask的衍生套件和函式：
from flask import Blueprint, jsonify, current_app
# from flask_mysqldb import MySQL, MySQLdb

# 自建的類和函式
from api.other_package.businessDay_calculator import calendar # 可計算兩個日子相隔的工作日               
from api.other_package.split_commaSeparatedValues import split_commaSeparatedValues 
                             # 把內含多個選項的字段(datatype為逗點分隔值)拆分，並把每一個選項作為新的字段新增到樣本記錄中

from api.security.guards import (
    authorization_guard,
)

# 建立Flask 的藍圖 (會在app.py裏註冊到主應用程序中)
# cs_p0_app = Blueprint('cs_p0_app', __name__)
bp_name = 'cs_p0_app'
bp_url_prefix = '/csP0Dashboard'
cs_p0_app = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix)

'''
頁面說明：測試用途
'''
@cs_p0_app.route("/")
def cs_p0_dashboard_testing():
    return "<h1>CS P0 Dashboard, It's working!!!</h1>"

'''
頁面說明：(Order) by TAT 圖表所需的data
'''
@cs_p0_app.route("/orderByTAT")
@authorization_guard
def order_bytat_data():
    cursor = __get_cursor()
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT
            marster_id AS Master_Lab_ID,
            DATE_FORMAT(printxitattime, '%Y-%m-%d %H:%i:%s') AS report_delivery_time,
            DATE_FORMAT( create_time, '%Y-%m-%d %H:%i:%s' ) AS specimen_accessioning_time,
            internaltat 
        FROM
            t_specimen 
        WHERE
            specimen_type = 'Clinical' 
        ORDER BY
            id DESC""")
    extracted_data = cursor.fetchall()

    # 計算每個樣本的TAT
    # 使用calendar物件的get_businessDay，順序輸入開始和結束的時間，便可得到TAT(浮點數)
    for each_record in list(extracted_data):
        each_record['internal_TAT'] = calendar.get_businessDay(each_record['specimen_accessioning_time'],
                                                                        each_record['report_delivery_time'])
    cursor.close()
    return jsonify({"table": extracted_data})

'''
頁面說明：(Order) by Risk Factor圖表所需的data
'''
@cs_p0_app.route("/orderByRiskFactor")
@authorization_guard
def order_byriskfactor_data():
    cursor = __get_cursor()
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT Specimen.marster_id AS Master_Lab_ID,
        DATE_FORMAT(Specimen.create_time, '%Y-%m-%d %H:%i:%s') AS specimen_accessioning_time,
        DATE_FORMAT(DATE_ADD(Specimen.create_time, INTERVAL ABS(Specimen.trfentrytat) DAY ), '%Y-%m-%d %H:%i:%s') AS trf_verification_time,
        is_aproval,
        Specimen.trfentrytat,
        Detail.current_smoker,
        Detail.current_symptoms,
        Detail.family_historyofnpc AS family_history_of_npc,
        Detail.previousnpcscreen AS previous_npc_screen
        FROM t_specimen AS Specimen
        LEFT Join t_spencimen_detail AS Detail ON Specimen.id= Detail.specimen_id
        WHERE specimen_type = 'Clinical'
        order by specimen_accessioning_time desc;""")
    extracted_data = cursor.fetchall()

    # 把內含多個選項的字段(datatype為逗點分隔值)拆分，並把每一個選項作為新的字段新增到樣本記錄中
    risk_factors = [["current_symptoms", 22],
                    ["family_history_of_npc", 10],
                    ["previous_npc_screen", 12]]
    for each_record in list(extracted_data):
        for risk_factor in risk_factors:
            split_commaSeparatedValues(each_record, risk_factor[0], risk_factor[1]) 

    cursor.close()
    return jsonify({"table": extracted_data})


'''
頁面說明: TAT Achieve Rate圖表所需的data
'''
@cs_p0_app.route("/tatAchieveRate")
@authorization_guard
def tatachieverate_data():
    cursor = __get_cursor()
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT
            DATE_FORMAT( Detail.courier_dispatch_time, '%Y-%m-%d %H:%i:%s' ) AS courier_dispatch_time,
            Specimen.marster_id AS Master_Lab_ID,
            DATE_FORMAT( Specimen.printxitattime, '%Y-%m-%d %H:%i:%s' ) AS report_delivery_time,
            DATE_FORMAT( Specimen.create_time, '%Y-%m-%d %H:%i:%s' ) AS specimen_accessioning_time,
            DATE_FORMAT( Specimen.trf_scanning_time, '%Y-%m-%d %H:%i:%s' ) AS trf_scanning_time,
            DATE_FORMAT( DATE_ADD( Specimen.create_time, INTERVAL ABS( Specimen.trfentrytat ) DAY ), '%Y-%m-%d %H:%i:%s' ) AS trf_verification_time,internaltat,
            partnertat,
            porter_servicetat,
            Specimen.trfentrytat
        FROM
            t_specimen AS Specimen
            LEFT JOIN t_spencimen_detail AS Detail ON Specimen.id=Detail.specimen_id 
        WHERE
            specimen_type='Clinical' 
        ORDER BY
            Specimen.id DESC;""")
    extracted_data = cursor.fetchall()

    # 計算每個樣本的TAT
    for each_record in list(extracted_data):
        each_record['porter_Service_TAT'] = calendar.get_businessDay(each_record['courier_dispatch_time'],
                                                                        each_record['specimen_accessioning_time'])
        each_record['internal_TAT'] = calendar.get_businessDay(each_record['specimen_accessioning_time'],
                                                                        each_record['report_delivery_time'])    
        each_record['partner_TAT'] =  calendar.get_businessDay(each_record['courier_dispatch_time'],
                                                                        each_record['report_delivery_time'])
        each_record['trf_Entry_TAT'] = calendar.get_businessDay(each_record['trf_scanning_time'],
                                                                each_record['trf_verification_time'])
    
    cursor.close()
    return jsonify({"table": extracted_data})