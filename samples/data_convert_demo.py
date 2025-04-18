
a = {'one':1,'two':2,'three':3}
a.setdefault( 'four' , 4 )  # 设置默认值 ，key不存在新增键值对
print( a )
a.setdefault( 'three',5 )  #  key存在,不修改内容
print( a )

# setdefault 和 list结合使用
data_list = [
    {'学习课程': 'PYTHON课程', '步骤序号': 'step_01', '步骤操作': '观看学习视频', '完成情况': 100.0},
    {'学习课程': 'PYTHON课程', '步骤序号': 'step_02', '步骤操作': '搭建环境', '完成情况': 100.0},
    {'学习课程': 'PYTHON课程', '步骤序号': 'step_03', '步骤操作': '操作以及做笔记', '完成情况': 100.0},
    {'学习课程': 'PYTHON课程', '步骤序号': 'step_04', '步骤操作': '应用到企业', '完成情况': 100.0},
    {'学习课程': 'JAVA课程', '步骤序号': 'step_01', '步骤操作': '观看学习视频', '完成情况': 100.0},
    {'学习课程': 'JAVA课程', '步骤序号': 'step_02', '步骤操作': '搭建环境', '完成情况': 100.0},
    {'学习课程': 'JAVA课程', '步骤序号': 'step_03', '步骤操作': '操作以及做笔记', '完成情况': 100.0},
    {'学习课程': 'JAVA课程', '步骤序号': 'step_04', '步骤操作': '应用到企业', '完成情况': 100.0}
]
data_dict = {}
# data_dict.setdefault( data_list[0]['学习课程'], [] ).append( data_list[0] )
# print( data_dict )
# data_dict.setdefault( data_list[1]['学习课程'], [] ).append( data_list[1] )
# print( data_dict )

for data in data_list:
    data_dict.setdefault( data['学习课程'],[] ).append( data )

print( data_dict )

import os
from common.excel_utils import ExcelUtils
excel_path = os.path.join( os.path.dirname(os.path.abspath(__file__)),'..','test_data','testcase_infos.xlsx' )
excel_data = ExcelUtils(excel_path,'Sheet1').get_excel_data_by_list()
# print( excel_data )
data_dict = {}
for data in excel_data:
    data_dict.setdefault( data['测试用例编号'],[] ).append( data )
print( data_dict )


dicta = {'api_case_01':[{'book1':"书1"},{'book2':"书2"}],
         'api_case_02':[{'book1':"书11"},{'book2':"书12"}]
         }
data_list = []
for key,value in dicta.items():
    temp_dict = {}
    temp_dict['case_id'] = key
    temp_dict['case_step'] = value
    data_list.append( temp_dict )
print( data_list )




