# unittest框架

import unittest  #单元测试控件
import warnings  #警告单元
import paramunittest  #参数化测试的扩展库
from common.requests_utils import RequestsUtils
from common.testdata_utils import TestdataUtils
from common.log_utils import logger

# 调用TestdataUtils类的实例方法，将测试数据转换为列表格式，并赋值给test_case_lists变量。这个列表可能包含了多个字典，每个字典代表一个测试用例的数据。
test_case_lists = TestdataUtils().convert_testdata_to_list()

# 装饰器来参数化测试类TestApiCase，每个测试用例的数据都会作为一个参数传递给测试类的方法
@paramunittest.parametrized(*test_case_lists  ) # [ {'case_id':'','case_step':[....]} ,{'case_id':'','case_step':[....]}]
class TestApiCase(paramunittest.ParametrizedTestCase):
    def setUp(self) -> None: # 在每个测试用例前调用，前置操作，用于设置测试环境
        warnings.simplefilter('ignore',ResourceWarning) #忽略ResourceWarning警告
    def setParameters(self, case_id, case_step): #设置参数，用于设置测试用例的ID和步骤
        self.case_id = case_id
        self.case_step = case_step
    def test_api_case(self):
        logger.info('测试用例 [%s--%s] 开始执行'%(self.case_step[0]['测试用例编号'],self.case_step[0]['测试用例名称']))
        self._testMethodName = self.case_step[0]['测试用例编号']  #在unittest框架中，self._testMethodName和self._testMethodDoc属性，用于存储测试用例的名称和描述
        self._testMethodDoc = self.case_step[0]['测试用例名称']
        test_result = RequestsUtils().request_by_step( self.case_step )
        logger.info('测试用例 [%s--%s] 执行结束'%(self.case_step[0]['测试用例编号'],self.case_step[0]['测试用例名称']))
        self.assertTrue( test_result['check_result'],test_result['message'] )

if  __name__=='__main__':
    unittest.main(verbosity=2)


