'''
split_commaSeparatedValues的函式說明：
把內含多個選項的字段(datatype為逗點分隔值)拆分，並把每一個選項作為新的字段新增到查詢結果中
'''

# 所需的參數:
#            result = 某一條SQL查詢結果，而資料類型為python字典，如{列名_1: 值_1, 列名_2: 值_2}
#            dataField_name = 要拆分的字段名字，必須列名一樣
#            num_of_choices = 字段有多少選項                

# 結果：
#      以current_symptoms的字段為例，一共有22個選項，假設在某一條SQL查詢結果在這個字段的值為"1,2" 
#      那麼接下來的程序就會新増22個鍵/值，然後在代表選項1和2的值中，分別改成"1"和"2"，其他20個鍵的值則為None
#      
def split_commaSeparatedValues(result, dataField_name, num_of_choices):
    if result[dataField_name] != None:
        list_of_userChoice = result[dataField_name].split(",")

    else:
        list_of_userChoice = []

    for choice_num in range(0, num_of_choices):
        matched_result = None
        if str(choice_num) in list_of_userChoice:
            matched_result = str(choice_num)

        result[dataField_name + "_opt_" + str(choice_num)] = matched_result
            