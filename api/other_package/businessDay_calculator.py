'''
日歷class:主要透過使用"hk_holidays"來計算兩個日期相隔的工作日(business day)
'''


'''
當前程式檔所需的庫
'''
# 自建的hk_holidays類，能爬取節假日資訊，並檢查某個日子是否節假日
from api.other_package.holidays import hk_holidays

# 日期之間的運算
from datetime import datetime, date, timedelta


'''
businessDay_calculator用於計算兩個日期相隔的工作日(business day)
'''
class businessDay_calculator:

    def __init__(self):

        # 建立hk_holidays的物件，並保持節假日資訊的更新
        self._hk_holidays = hk_holidays()
        self._hk_holidays.keep_txt_update()
        self._hk_holidays.keep_list_update()


    # 檢查節假日文檔是否最新的，以及列表是否與文檔保持一致，若不是則再次更新相關資訊
    def keep_calendar_update(self):
        self._hk_holidays.keep_txt_update()
        self._hk_holidays.keep_list_update() 

    
    # 把格式為"2022-01-01 00:00:00"的字串轉化為datetime物件
    def parse_datetime(self, datetime_string):
        if type(datetime_string) == str:
            return datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
        elif type(datetime_string) == datetime:
            return datetime_string


    # 判斷某個datetime物件是否周末或節假日，若是則返回False, 反之返回True
    def is_businessDay(self, date_obj):
        if type(date_obj) == datetime:
            if (date_obj.isoweekday() in [6,7]) or (self._hk_holidays.is_holiday(date_obj)):
                return False
            
            else:
                return True


    # 判斷兩個datetime物件是否同一天
    def is_same_date(self, date_obj_1, date_obj_2):
        return date_obj_1.date() == date_obj_2.date()


    # 取得某個datetime物件的第二天
    def get_next_date(self, date_obj):
        return (datetime(date_obj.year, date_obj.month, date_obj.day, 0, 0, 0)) + timedelta(days=1)


    # 計算兩個給予的日期之間的工作日
    # 需要的參數：startDat = 開始日期
    #            endDate = 結束日期
    # 日期必須是datetime物件，或符合"2022-01-01 00:00:00"的字串
    # 而且開始日期必須早於結束日期，否則會返回-1
    def get_businessDay(self, startDate, endDate):
    
        self.keep_calendar_update()
        startDate_obj = self.parse_datetime(startDate)
        endDate_obj = self.parse_datetime(endDate)

        try: 
            if (type(startDate_obj) == datetime) and (type(endDate_obj) == datetime): 
                if startDate_obj > endDate_obj:
                    return -1.0

                # 計算兩個給予的日期之間的工作日
                else:
                    businessDay = 0.0
                    current_pt = startDate_obj

                    while not self.is_same_date(current_pt, endDate_obj):
                        if self.is_businessDay(current_pt):
                            difference = self.get_next_date(current_pt) - current_pt
                            businessDay += (difference.days + (difference.seconds)/3600.0/24.0)

                        current_pt = self.get_next_date(current_pt)

                    if self.is_businessDay(current_pt):
                        businessDay += (endDate_obj - current_pt).seconds/3600.0/24.0

                    return round(businessDay, 2)
            
        except:
            return -1.0

# 建立calendar物件
calendar = businessDay_calculator()
# print (calendar.get_next_date(calendar.parse_datetime("2022-7-31 17:18:15")))

