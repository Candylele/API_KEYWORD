
from common.excel_utils import ExcelUtils

excel_utils = ExcelUtils('test_data.xlsx','Sheet1')

first_row_data = excel_utils.sheet.row_values( 0 ) # 获取首行数据
row_dict = {}
# row_dict[ first_row_data[0] ] = excel_utils.get_merged_cell_value(1,0)
# row_dict[ first_row_data[1] ] = excel_utils.get_merged_cell_value(1,1)
# row_dict[ first_row_data[2] ] = excel_utils.get_merged_cell_value(1,2)
# row_dict[ first_row_data[3] ] = excel_utils.get_merged_cell_value(1,3)

# for i in range(excel_utils.get_column_count()):
#     # row_dict[excel_utils.get_merged_cell_value(0,i)] = excel_utils.get_merged_cell_value(1, i)
#     row_dict[ first_row_data[i] ] = excel_utils.get_merged_cell_value(1, i)
# print( row_dict )

excel_data = []
for row_index in range(1,excel_utils.get_row_count()):
    row_dict = {}
    for col_index in range(excel_utils.get_column_count()):
        row_dict[ first_row_data[col_index] ] = excel_utils.get_merged_cell_value(row_index, col_index)
    excel_data.append( row_dict )

for data in excel_data:
    print( data )

import json
request_info = {"请求头部信息":'{"aaa":1}'}
headers = json.loads(request_info['请求头部信息']) if request_info['请求头部信息'] else None
print( headers )