

import os
from common.excel_utils import ExcelUtils

excel_path = os.path.join( os.path.dirname(os.path.abspath(__file__)),'..','test_data','testcase_infos.xlsx' )

class TestdataUtils():
    def __init__(self):
        self.excel_utlis = ExcelUtils(excel_path,'Sheet1')

    def convert_testdata_to_dict(self):
        # 判断是否执行，再将[{第一行数据},{第二行数据}...]转为{"用例编号1":[{}],"用例编号2":[{}，{}],...}
        testdata_dict = {}
        for row_data in self.excel_utlis.get_excel_data_by_list():  #遍历转化为集合套字典[{},{},...,{}]的每一行测试数据
            if row_data['用例执行'] == '是':
                testdata_dict.setdefault(row_data['测试用例编号'], []).append(row_data)
        return testdata_dict

    def convert_testdata_to_list(self):  #转列表
        testcase_data = []
        for key, value in self.convert_testdata_to_dict().items():
            temp_dict = {}
            temp_dict['case_id'] = key   #{'case_id': 'api_case_01','case_step': []  }
            temp_dict['case_step'] = value
            testcase_data.append(temp_dict)
        return testcase_data

if __name__=='__main__':
    print( TestdataUtils().convert_testdata_to_dict() )
    print( TestdataUtils().convert_testdata_to_list() )
