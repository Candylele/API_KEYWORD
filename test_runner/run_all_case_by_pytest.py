# pytest运行完生成allure测试报告，在pytest_report目录下,测试文件的命名以test_或_test作为前缀或后缀

import os #文件路径操作、目录管理
import shutil #文件操作，如复制、删除目录树
import pytest #Python测试框架，用于编写和执行测试用例

current_path = os.path.dirname( os.path.abspath(__file__) ) #获取当前脚本的绝对路径
case_path = os.path.join( current_path , '..','testcases' ) #构造测试用例的路径
json_report_path = os.path.join( current_path,'..','pytest_report','json_report' ) #构造JSON格式测试报告的存储路径
html_report_path = os.path.join( current_path,'..','pytest_report','html_report' ) #构造HTML格式测试报告的存储路径

if os.path.isdir( json_report_path ): #检查JSON报告目录是否存在
    shutil.rmtree( json_report_path ) #如果存在，则删除该目录及其所有内容
os.mkdir( json_report_path ) #创建JSON报告目录

"""
使用pytest运行测试用例。这里指定了测试用例的路径（case_path）和Allure报告的输出目录（--alluredir）。
Allure是一个灵活的轻量级多语言测试报告工具，它可以将测试结果以JSON格式输出，并可以进一步生成HTML格式的报告
"""
pytest.main([case_path,'--alluredir=%s'%json_report_path]) #运行测试用例
os.system( 'allure generate %s -o %s --clean'%(json_report_path,html_report_path) ) #生成测试报告


