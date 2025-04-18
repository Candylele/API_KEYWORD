# pytest代码

import pytest
import warnings
import allure
from _pytest.warning_types import PytestCollectionWarning
from common.requests_utils import RequestsUtils
from common.testdata_utils import TestdataUtils
from common.log_utils import logger

# 调用TestdataUtils类的实例方法，将测试数据转换为列表格式，并赋值给test_case_lists变量。这个列表可能包含了多个字典，每个字典代表一个测试用例的数据。
test_case_lists = TestdataUtils().convert_testdata_to_list()
#获取test_case_lists中第一个字典的键，并用逗号连接它们，生成一个字符串。这个字符串表示测试用例的字段名
case_name_str = ','.join( test_case_lists[0].keys() ) # 'case_id,case_step'
print(case_name_str)

case_step_infos = [] #存储处理后的测试用例数据
for test_case in test_case_lists:
    case_step_infos.append( tuple(test_case.values()) ) #将每个字典的值转换为元组

@allure.epic('微信公众平台接口测试项目')  #设置测试用例的史诗标题,装饰器来设置测试用例的标题和测试用例的标题
@allure.title("{case_id}") # 设置测试用例的标题，这里使用了占位符{case_id}，不支持动态参数替换。

# @pytest.mark.parametrize(case_name_str,case_step_infos)  #装饰器来参数化测试函数test_api_case
# def test_api_case(case_id,case_step):

@pytest.mark.parametrize("case_id, case_step", case_step_infos) #参数化测试函数,俩个参数，传参值
def test_api_case(case_id, case_step):
    logger.info('测试用例 [%s--%s] 开始执行'%(case_step[0]['测试用例编号'],case_step[0]['测试用例名称']))
    actual_result = RequestsUtils().request_by_step( case_step ) #发送HTTP请求并执行测试用例步骤
    logger.info('测试用例 [%s--%s] 执行结束'%(case_step[0]['测试用例编号'],case_step[0]['测试用例名称']))
    assert actual_result['check_result']

if __name__=="__main__":
    pytest.main()

"""
@pytest.mark.parametrize装饰器在pytest测试框架中用于参数化测试函数。它允许你定义一个测试函数，并为该函数提供多个参数集，每个参数集都会导致测试函数被独立执行一次
"""