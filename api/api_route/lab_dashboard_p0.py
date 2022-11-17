'''
說明: 
當前程式檔主要存放實驗室P0階段所需的api, 並在app.py導入 (方便管理)
由於每個api的代碼結構都很相似, 所以api代碼解析只放在init.py的例子
'''


'''
Api 所需的庫
'''
# 導入已初始化的Flask應用程序和mysql資料庫物件
from api.database import __get_cursor
# from flask_mysqldb import MySQLdb 
from flask import jsonify
from flask import Blueprint # 連接當前程式檔的api與Flask應用程序, 進行應用模塊化

# 自建的calendar類, 可計算兩個日子相隔的工作日
from api.other_package.businessDay_calculator import calendar

from api.security.guards import (
    authorization_guard,
)

# 建立Flask的藍圖 (會在app.py裏註冊到主應用程序中)
# lab_p0_app = Blueprint('lab_p0_app', __name__)
bp_name = 'lab_p0_app'
bp_url_prefix = '/labP0Dashboard'
lab_p0_app = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix)



'''
頁面說明: 只是測試用途
'''
@lab_p0_app.route("/")
def lab_p0_dashboard_testing():
    return "<h1>Lab P0 Dashboard, It's working!!!</h1>"


'''
頁面說明: qPCR Repeat Case圖表所需的data
'''
@lab_p0_app.route("/qPCRRepeatCase", methods=['GET'])
@authorization_guard
def qpcrrepeatcase_data():
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor = __get_cursor()
    cursor.execute("""select Specimen.marster_id AS Master_Lab_ID,
        DATE_FORMAT(Specimen.create_time, '%Y-%m-%d %H:%i:%s') AS specimen_accessioning_time,
        (CASE
        WHEN Operation.operation IN (10, 20)
        THEN "Yes"
        ELSE "No"
        END ) AS is_repeat,
        (CASE
        WHEN Specimen.lab_process IN ("qPCR Extraction", "qPCR Run", "qPCR Results Review")
        THEN "Yes"
        ELSE "No"
        END) AS is_qPCR,
        Specimen.lab_process
        from t_specimen Specimen left join t_batch_specimen_operation Operation on Specimen.marster_id = Operation.master_id
        where Specimen.create_time between '2022-10-1' and '2022-11-01 00:00' and Specimen.specimen_type = 'Clinical' group by Specimen.marster_id;""")
    extracted_data = cursor.fetchall()
    cursor.close()
    return jsonify({"table": extracted_data})


'''
頁面說明: NGS Repeat Case圖表所需的data
'''
@lab_p0_app.route("/ngsRepeatCase", methods=['GET'])
@authorization_guard
def ngsrepeatcase_data():
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor = __get_cursor()
    cursor.execute("""select Specimen.marster_id AS Master_Lab_ID,
        DATE_FORMAT(Specimen.create_time, '%Y-%m-%d %H:%i:%s') AS specimen_accessioning_time,
        (CASE
        WHEN Operation.operation IN (10, 20)
        THEN "Yes"
        ELSE "No"
        END ) AS is_repeat,
        (CASE
        WHEN Specimen.lab_process IN ('NGS Extraction', 'NGS Extraction QC', 'Library Prep', 'Library Prep QC',
        'Target Capture', 'Target Capture QC', 'Sequencing', 'Pipeline Results Review')
        THEN "Yes"
        ELSE "No"
        END) AS is_NGS,
        Specimen.lab_process
        from t_specimen Specimen left join t_batch_specimen_operation Operation on Specimen.marster_id = Operation.master_id
        where Specimen.create_time between '2022-10-1' and '2022-11-01 00:00' and Specimen.specimen_type = 'Clinical' group by Specimen.marster_id;""")
    extracted_data = cursor.fetchall()
    cursor.close()
    return jsonify({"table": extracted_data})


'''
頁面說明: TAT Overview 和 By TAT圖表所需的data
'''
@lab_p0_app.route("/tatOverview_and_byTAT", methods=['GET'])
@authorization_guard
def tat_data():
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor = __get_cursor()
    cursor.execute("""SELECT
            DATE_FORMAT( Details.specimen_pickup_time, '%Y-%m-%d %H:%i:%s' ) AS clinic_call_time,
            Specimen.lab_process AS end_process,
            Specimen.marster_id AS Master_Lab_ID,
            DATE_FORMAT( Specimen.printxitattime, '%Y-%m-%d %H:%i:%s' ) AS report_delivery_time,
            DATE_FORMAT( Specimen.create_time, '%Y-%m-%d %H:%i:%s' ) AS specimen_accessioning_time,
            DATE_FORMAT( Specimen.report_time, '%Y-%m-%d %H:%i:%s' ) AS v01_report_signoff_time,
            DATEDIFF( printxtattime, specimen_pickup_time ) AS doctor_percived_tat,
            internaltat,
            DATEDIFF( printxtattime, blood_draw_data ) AS patient_percived_tat 
        FROM
            t_specimen AS Specimen
            INNER JOIN t_spencimen_detail AS Details ON Specimen.id = Details.specimen_id 
        WHERE
            Specimen.specimen_type = 'Clinical' 
        ORDER BY
            Specimen.create_time DESC;""")
    extracted_data = cursor.fetchall()

    # 計算每個樣本的TAT
    # 使用calendar物件的get_businessDay, 順序輸入開始和結束的時間, 便可得到TAT(浮點數)
    for each_record in list(extracted_data):
        each_record['doctor_perceived_TAT'] = calendar.get_businessDay(each_record['clinic_call_time'],
                                                                        each_record['report_delivery_time'])
        each_record['patient_perceived_TAT'] = calendar.get_businessDay(each_record['blood_draw_time'],
                                                                        each_record['report_delivery_time'])    
        each_record['internal_TAT'] = calendar.get_businessDay(each_record['specimen_accessioning_time'],
                                                                each_record['v01_report_signoff_time'])
        
    cursor.close()

    return jsonify({"table": extracted_data})
   

'''
頁面說明: qPCR Positive 和 NGS Positive 圖表所需的data
'''
@lab_p0_app.route("/positiveResult", methods=['GET'])
@authorization_guard
def positiveresult_data():
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor = __get_cursor()
    cursor.execute("""SELECT DISTINCT Specimen.marster_id AS Master_Lab_ID,
        DATE_FORMAT(Specimen.create_time, '%Y-%m-%d %H:%i:%s') AS specimen_accessioning_time,
        DATE_FORMAT(Specimen.report_time, '%Y-%m-%d %H:%i:%s') AS v01_report_sign_off_time,
        CASE
        WHEN Specimen.status = 50
        THEN 'Yes'
        ELSE 'No'
        END AS is_v01_report_result_authorized,
        Specimen.test_result AS v01_report_result,
        Specimen.lab_process AS v01_end_process,
        CASE
        WHEN Report.status = 50
        THEN 'Yes'
        WHEN Report.status IS NULL
        THEN NULL
        ELSE 'No'
        END AS is_v02_report_result_authorized,
        Report.test_result AS v02_test_result,
        Report.lab_process AS v02_end_process
        FROM t_specimen AS Specimen LEFT Join t_specimen_report AS Report ON Specimen.id= Report.specimen_id
        Where Specimen.specimen_type = 'Clinical'
        order by Specimen.create_time desc""") 
                        
    extracted_data = cursor.fetchall()
    cursor.close()
    return jsonify({"table": extracted_data})