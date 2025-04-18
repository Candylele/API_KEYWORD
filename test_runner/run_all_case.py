# unittest运行完生成HTMLTestReportCN测试报告，在report目录下,测试文件名会以test_开头

import os  #处理文件和目录路径
import unittest #Python内置的单元测试框架，用于编写和运行测试
from common import HTMLTestReportCN #用于生成HTML格式的测试报告
from common.config import Config #读取配置文件
from common.log_utils import logger #用于记录日志

current_path = os.path.dirname( os.path.abspath(__file__) ) #获取当前脚本所在的目录
case_path = os.path.join(current_path,'..','testcases') #构建测试用例所在的目录路径
config_file_path = os.path.join( current_path,'..','conf','config.ini' ) #构建配置文件的路径
local_config = Config(config_file_path) #读取配置文件，并创建一个Config对象
report_dir =  os.path.join( current_path,'..',local_config.REPORT_PATH) #从配置文件中获取报告路径，并构建完整的报告目录路径

logger.info('接口自动化测试开始')
def loading_testcase(): #用于加载测试用例
    logger.info("加载接口测试用例")
    #查找指定目录（case_path）下符合命名模式（test_api_case.py）的测试文件
    discover_obj = unittest.defaultTestLoader.discover(start_dir=case_path,
                                                       pattern='test_api_case.py')
    all_case_suite = unittest.TestSuite() #创建一个空的测试套件（TestSuite）
    all_case_suite.addTest( discover_obj ) #将发现的测试添加到测试套件中
    return all_case_suite

result_path_obj = HTMLTestReportCN.ReportDirectory( report_dir ) #创建HTMLTestReportCN.ReportDirectory对象
result_path_obj.create_dir('接口测试报告_') #创建报告目录

"""
GlobalMsg.get_value()方法的参数是 ‌字符串类型（str）的键（key）‌，用于从全局配置中获取对应键的值
框架默认支持以下键名：
'report_path': 测试报告生成的路径（如 ./report.html）。
'report_title': 测试报告标题（如 "自动化测试报告"）。
'report_description': 测试报告描述（如测试环境、版本等）。
'theme': 报告主题（默认为 'default'）
"""
result_html_path = HTMLTestReportCN.GlobalMsg.get_value( 'report_path' ) #获取报告路径
result_html_obj = open( result_html_path,'wb' ) #打开报告文件，准备写入
#创建HTMLTestRunner对象，设置报告的输出流、标题、描述和测试人员
html_runner = HTMLTestReportCN.HTMLTestRunner(stream=result_html_obj,
                                              title="测试报告",
                                              description="关键字驱动框架",
                                              tester="tester")

html_runner.run( loading_testcase() ) #运行测试套件，并生成HTML格式的测试报告
logger.info('接口自动化测试结束')






