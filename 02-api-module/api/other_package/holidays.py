# -*- coding: UTF-8 -*-
'''
說明：
當前程式檔主要建立用於爬取節假日資訊的Class, 以便計算工作日(business day)
'''

'''
當前程式檔所需的庫
'''
# Get方式獲取網頁數據
import requests
# 解構requests返回的網頁數據
from bs4 import BeautifulSoup
# 日期之間的運算
from datetime import datetime, date


'''
節假日class:從香港政府的網站爬取香港節假日
'''
class hk_holidays:

    # holidays類的建構器
    def __init__(self, start_year= "2020"):
        self._start_year = start_year # 爬取節假日的起始年份
        self._holiday_doc = 'api/other_package/hongKong_holidays.txt' # 節假日文檔
        self._list_last_update = "" # 最後讀取文檔的年份
        self._holiday_list = [] # 存放爬取的節假日（日期以datatime物件存放在list中） 


    def __str__(self):
        return "截至" + self._list_last_update +", 目前爬取了的節假日: \n" + str(self._holiday_list)
    

    # 保持更新，並返回所有節假日的時間日期
    def get_holidays(self):
        return self._holiday_list
    

    # 把節假日加入到列表中
    def add_holiday(self, date_obj):
        if type(date_obj) == datetime:
            self._holiday_list.append(date_obj) 
    

    # 清空節假日列表和最後讀取文檔年份
    def clear_holidays(self):
        self._last_update = ""
        self._holiday_list.clear()
    

    # 檢查特定的日期時間是否在節假日列表中
    def is_holiday(self, date_obj):
        return (datetime(date_obj.year, date_obj.month, date_obj.day)) in self._holiday_list


    # 透過讀取節假日文檔首句，取得最後更新年份
    def txt_last_update(self):
        try:
            with open(self._holiday_doc, mode ="r", encoding="utf-8" ) as doc :
                return doc.readline()[-5:-1]

        except:
            return "" 


    # 保持節假日文檔的更新，若不是最新的便會重新爬取，並返回True，否則返回False(代表無須更新)
    def keep_txt_update(self):
        current_year = str(datetime.today().year) # 今年
        if self.txt_last_update() != current_year:
            self.write_holidays_from_web(current_year) 
            self.read_holidays_from_txt()
            return True
        
        else:
            return False
        


    # 保持列表與節假日文檔一致，若不是一致的便會重新讀取文檔，並返回True，否則返回False(代表無須更新)
    def keep_list_update(self):
        if self._list_last_update != self.txt_last_update():
            self.read_holidays_from_txt()
            return True
        
        else:
            return False


    # 從香港政府的網站爬取香港節假日，並存放在"hongKong_holidays.txt"文檔中，共分成三步
    def write_holidays_from_web(self, end_year):
        try:
            with open(self._holiday_doc, mode ="w", encoding="utf-8") as doc :
                doc.write("Last update: " + str(end_year) + "\n") # 首句是文檔的最後更新年份

                for year in range(int(self._start_year), int(end_year)+1):
                    # 1. 用request庫以Get方式獲取網頁數據
                    url = "https://www.gov.hk/tc/about/abouthk/holiday/" + str(year) + ".htm"
                    strhtml = requests.get(url)

                    # 2. 用beautifulsoup解構requests返回的網頁數據
                    soup = BeautifulSoup(strhtml.text,'html.parser')
                         # 取得tag為"td"和class為"date"的所有元素，如"<td align="center" class="date"....>1月1日</td>""
                    html_tags = soup.find_all("td", class_ = "date") 

                    # 3. 把爬取的資訊放在txt文檔中 (從列表第2個元素開始)
                    for index in range(1, len(html_tags)):
                        doc.write("{year}年{date}\n".format(year = str(year),
                                                            date = html_tags[index].getText())) # 取得每個元表的文字內容，即1月1日
                        print (html_tags[index].getText())
            return "Update success"   
        
        except:
            return "Update Failed"
            

    # 讀取文檔中的節假日，並放到列表之中    
    def read_holidays_from_txt(self):
        self.clear_holidays()
        try:
            with open(self._holiday_doc, mode ="r", encoding="utf-8" ) as doc:
                lines = self._list_last_update = doc.readlines() 
                self._list_last_update = lines[0][-5:-1] 
                for index in range(1, len(lines)): 
                    self.add_holiday(datetime.strptime(lines[index][:-1], "%Y年%m月%d日"))
            return "Read success"

        except:
            return "Read failed"







    




