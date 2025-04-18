"""
request_by_step(接口信息)-->调用request-->请求__get或__post
"""
import os  #文件操作，用于文件路径操作、环境变量获取等
import json  #数据读取序列化与反序列化，即将python对象转化为JSON格式字符串
import re #正则表达式匹配，在字符串中查找符合正则表达式的子串
import jsonpath  #解析JSON数据，可以按照指定的路径表达式从JSON数据中提取信息
import requests  #接口请求，用于发送HTTP请求，如get、post等
import allure  #用于生成测试报告，记录测试步骤、测试结果  D:\Tools\PyCharm\PythonProject\allure\allure-2.20.1
from common.config import Config  #读取配置信息
from common.check_utils import CheckUtils  #对接口响应结果进行校验
from requests.exceptions import ProxyError #用于处理代理相关异常
from requests.exceptions import ConnectionError  #用于处理连接相关异常
from requests.exceptions import RequestException  #处理通用异常
from common.log_utils import logger #记录日志信息

# 拼接配置文件的路径，从当前文件所在目录的上级目录的conf目录下的config.ini文件中读取配置。
conf_file_path = os.path.join( os.path.abspath(os.path.dirname(__file__)),'..','conf','config.ini' )

#封装HTTP请求的相关操作
class RequestsUtils:
    # 类的初始化方法，创建一个session对象用于发送HTTP请求，读取配置文件中的HOSTS配置，初始化一个临时变量字典。
    def __init__(self):
        self.session = requests.session()
        self.hosts = Config(conf_file_path).HOSTS
        self.tmp_variables = {}

    # # 定义一个request_by_step方法，接收一个测试步骤列表，按照步骤发送HTTP请求。
    # def request_by_step(self,test_steps):
    #     #print("4+++++++++++++开始调用request_by_step方法++++++++++++++++")
    #     for test_step in test_steps:
    #         # 使用allure记录测试步骤的开始，并使用logger记录日志。
    #         with allure.step('测试步骤[%s]开始执行'%test_step['用例步骤']):
    #             logger.info('测试步骤[%s]开始执行'%test_step['用例步骤'])
    #
    #         # 调用request方法发送请求，并获取结果。
    #         result = self.request( test_step )
    #         # 使用allure和logger记录测试步骤的结果。
    #         with allure.step(logger.info('测试步骤[%s]执行结束'%test_step['用例步骤'])):
    #             logger.info('测试步骤[%s]执行结束'%test_step['用例步骤'])
    #
    #         # 如果请求结果中的code不为0，则中断循环
    #         if result['code'] != 0:
    #             break
    #
    #     # 返回最后一个测试步骤的结果。（就是code）
    #     #print("3打印+++++++++++request_by_step方法最后return的result是：%s+++++++++" %result)
    #     return result

    #优化方案
    def request_by_step(self, test_steps):
        for test_step in test_steps:
            step_description = '测试步骤[%s]开始执行' % test_step['用例步骤']
            with allure.step(step_description):
                logger.info(step_description)
                result = self.request(test_step)
            # 将日志记录放在with语句块外部
            logger.info('测试步骤[%s]执行结束' % test_step['用例步骤'])
            if result['code'] != 0:
                break
        return result


    # 定义一个request方法，根据请求方式（get或post）调用对应的方法发送请求。
    def request(self,step_info):
        request_type = step_info['请求方式']
        #print("1打印看看---------------------------请求方式是：%s-------------------------"%request_type)

        if request_type == "get":
            result = self.__get( step_info )
            #print("2打印看看---------------------------request_type==get的result是：%s-------------------------"%result)

        elif request_type == "post":
            result = self.__post( step_info )
        else:
            # 如果请求方式不支持，则返回错误信息。
            result = {'code':1,'message':'%s请求方式不支持'%request_type,'check_result':False}
        return result


    # 定义一个__get私有方法，用于发送GET请求
    def __get(self,request_info):
        # 记录日志，表示接口调用开始
        logger.info( '接口 [%s] 开始调用'%request_info['接口名称'] )
        try:
            # 拼接请求的URL。
            url = 'https://%s%s'%(self.hosts,request_info['请求地址'])

            """
            这段代码的作用是在一个字符串中查找并替换所有形如${变量名}的子串为对应的值
            如果request_info['请求参数(get)']的值为"param1=${value1}&param2=${value2}"，
            且self.tmp_variables的值为{"value1": "123", "value2": "456"}，
            那么经过这段代码处理后，request_info['请求参数(get)']的值将变为"param1=123&param2=456"
            """

            # re.findall('\\${\w+}',{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"})
            #re.findall函数的作用是在输入的字符串中查找所有符合指定正则表达式的子串，并将这些子串作为一个列表返回
            #使用正则表达式查找请求参数中的变量（如${variable}，其中 variable 可以是一个或多个单词字符），并打印变量列表,写成r'\${\w+}'也行。
            variable_list = re.findall('\\${\w+}',request_info['请求参数(get)'])  #在正则表达式中，$ 是一个特殊字符，用于匹配字符串的末尾，使用\\转义$符号，使其变成普通字符
            # 解决一个用例中含有多个接口，然后后面接口的token需要上一个接口获取的值替换问题，替换${token}
            #print("@@@@@@@@@@@@@@@@这是variable_list: %s@@@@@@@@@@@@@@@@@@@"%variable_list)  # \\w+匹配一个或多个单词字符（字母、数字或下划线）
            # 替换请求参数中的变量为对应的值
            for variable in variable_list:
                request_info['请求参数(get)'] = request_info['请求参数(get)'].replace(variable,self.tmp_variables[variable[2:-1]]) #去掉${token}的${和}
            #print("@@@@@@@@@@@@@@@@这是variable: %s@@@@@@@@@@@@@@@@@@@" %request_info['请求参数(get)'])

            response = self.session.get( url = url,
                                         params = json.loads(request_info['请求参数(get)']),  #json.loads作用是将JSON格式的字符串解析为对象(字符串转字典)
                                         headers = json.loads(request_info['请求头部信息']) if request_info['请求头部信息'] else None # 如果有头部信息，则解析为字典传入，否则传入None
                                         )
            # print(response.status_code)
            # print(response.text)
            #print("@@@这是session.get结果: %s@@@"%response)

            # 根据取值方式从响应中提取值，并保存到临时变量字典中
            if request_info['取值方式'] == '正则取值':
                value = re.findall(request_info['取值代码'], response.text)[0]
                self.tmp_variables[request_info['取值变量']] = value
            elif request_info['取值方式'] == 'jsonpath取值':
                value = jsonpath.jsonpath( response.json(), request_info['取值代码'])[0]
                self.tmp_variables[request_info['取值变量']] = value
            #print("@@@这是tmp_variables结果: %s@@@"%self.tmp_variables)

            # 使用CheckUtils对响应结果进行校验。
            result = CheckUtils(response).run_check(request_info['断言类型'],request_info['期望结果'])
            # print("@@@这是get方法CheckUtils校验response_body结果: %s@@@"%result["response_body"])
            # print("@@@这是get方法CheckUtils校验message结果: %s@@@" % result["message"])
            # print("@@@这是get方法CheckUtils校验check_result结果: %s@@@" % result["check_result"])

            # 记录日志，表示接口调用完成
            logger.info( '接口 [%s] 调用完成'%request_info['接口名称'] )

        # 处理代理、连接、通用异常
        except ProxyError as e:
            result = {'code':3,'message':'调用接口 [%s] 时发生代理异常，异常原因：%s'%(request_info['接口名称'],e.__str__()),'check_result':False}
            logger.error( result['message'] )
        except ConnectionError as e:
            result = {'code':3,'message':'调用接口 [%s] 时发生链接异常，异常原因：%s'%(request_info['接口名称'],e.__str__()),'check_result':False}
            logger.error( result['message'] )
        except RequestException as e:
            result = {'code':3,'message':'调用接口 [%s] 时发生请求异常，异常原因：%s'%(request_info['接口名称'],e.__str__()),'check_result':False}
            logger.error( result['message'] )  #e.__str__() 来获取异常的字符串表示,使用 str(e) 会更清晰和简洁
        except Exception as e:
            result = {'code':3,'message':'调用接口 [%s] 时发生系统异常，异常原因：%s'%(request_info['接口名称'],e.__str__()),'check_result':False}
            logger.error( result['message'] )
        return result

    def __post(self,request_info):
        logger.info( '接口 [%s] 开始调用'%request_info['接口名称'] )
        try:
            url = 'https://%s%s'%(self.hosts,request_info['请求地址'])

            get_variable_list = re.findall('\\${\w+}',request_info['请求参数(get)'])
            #  用来处理 '请求参数(get)': '{"access_token":"${token}"}', token替换问题，替换${token}
            for variable in get_variable_list:
                request_info['请求参数(get)'] = request_info['请求参数(get)'].replace(variable,self.tmp_variables[variable[2:-1]])
            #print("~~~这个是request_info['请求参数(get)']：%s~~~"%request_info['请求参数(get)'])

            post_variable_list = re.findall('\\${\w+}',request_info['请求参数(post)'])
            for variable in post_variable_list:
                # new_text = text.replace("old", "new", 次数)
                request_info['请求参数(post)'] = request_info['请求参数(post)'].replace(variable,self.tmp_variables[variable[2:-1]])
            #print("~~~这个是request_info['请求参数(post)']：%s~~~" % request_info['请求参数(post)'])

            response = self.session.post( url = url,
                                         params = json.loads(request_info['请求参数(get)']),
                                         headers = json.loads(request_info['请求头部信息']) if request_info['请求头部信息'] else None,
                                         json = json.loads(request_info['请求参数(post)'])
                                         )
            if request_info['取值方式'] == '正则取值':
                value = re.findall(request_info['取值代码'],response.text)[0]
                self.tmp_variables[request_info['取值变量']] = value
            elif request_info['取值方式'] == 'jsonpath取值':
                value = jsonpath.jsonpath( response.json() , request_info['取值代码'] )[0]
                self.tmp_variables[request_info['取值变量']] = value
            result = CheckUtils(response).run_check(request_info['断言类型'],request_info['期望结果'])
            logger.info( '接口 [%s] 调用完成'%request_info['接口名称'] )

        except ProxyError as e:
            result = {'code':3,'message':'调用接口 [%s] 时发生代理异常，异常原因：%s'%(request_info['接口名称'],e.__str__()),'check_result':False}
            logger.error( result['message'] )
        except ConnectionError as e:
            result = {'code':3,'message':'调用接口 [%s] 时发生链接异常，异常原因：%s'%(request_info['接口名称'],e.__str__()),'check_result':False}
            logger.error( result['message'] )
        except RequestException as e:
            result = {'code':3,'message':'调用接口 [%s] 时发生请求异常，异常原因：%s'%(request_info['接口名称'],e.__str__()),'check_result':False}
            logger.error( result['message'] )
        except Exception as e:
            result = {'code':3,'message':'调用接口 [%s] 时发生系统异常，异常原因：%s'%(request_info['接口名称'],e.__str__()),'check_result':False}
            logger.error( result['message'] )
        return result



if __name__=='__main__':

    request_info = {'测试用例编号': 'api_case_01', '测试用例名称': '获取access_token接口测试', '用例执行': '是', '用例步骤': 'step_01',
                    '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token',
                    '请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}',
                    '请求参数(post)': '',
                    '取值方式': '正则取值', '取值代码': '"access_token":"(.+?)"', '取值变量': '',
                    '断言类型': 'none', '期望结果': '"access_token":"(.+?)"'}
    print(request_info['请求方式'])

    # request_info = {'测试用例编号': 'api_case_01', '测试用例名称': '获取access_token接口测试', '用例执行': '是','用例步骤': 'step_01',
    #                 '接口名称': '获取access_token接口',
    #                 '请求方式': 'get',
    #                 '请求头部信息': '','请求地址': '/cgi-bin/token',
    #                 '请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}',
    #                 '请求参数(post)': '', '取值方式': 'jsonpath取值', '取值代码': '$.access_token','取值变量': 'token_value',
    #                 '断言类型': 'none', '期望结果': '"access_token":"(.+?)"'}
    # r = RequestsUtils()
    # result = r.request(request_info)
    # print( result )

    # request_info = {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_02',
    #                 '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create',
    #                 '请求参数(get)': '{"access_token":"46_Zcj3iwiHHILu8djI7kNG4b-Td8PPZYfCFv43l4ui-EvYdGWZ_SEeetNUvq-Qw1BkJoQs-ggeFKixHLlqFeT3LqHmVq6k76IwVymhYRQiEisiI2MDkAPjXf-dXXpK3QEmUcs0iCpJ1AWTIqguURXeAIAKHN"}',
    #                 '请求参数(post)': '{   "tag" : {     "name" : "P7P8new02" } } ', '取值方式': '无', '取值代码': '', '取值变量': '',
    #                 '断言类型': 'json_key', '期望结果': 'tag'}
    # r = RequestsUtils()
    # result = r.request( request_info  )
    # print( result )

    #俩个步骤的接口用例，先获取access_token再创建标签
    # case_info = [{'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '是', '用例步骤': 'step_01',
    #               '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token',
    #               '请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}',
    #               '请求参数(post)': '',
    #               '取值方式': '正则取值', '取值代码': '"access_token":"(.+?)"', '取值变量': 'token',
    #               '断言类型': 'json_key', '期望结果': ''},
    #              {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_02',
    #               '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create',
    #               '请求参数(get)': '{"access_token":"${token}"}',
    #               '请求参数(post)': '{   "tag" : {     "name" : "P5P6new01" } } ',
    #               '取值方式': '无', '取值代码': '', '取值变量': '',
    #               '断言类型': 'json_key', '期望结果': 'tag'}
    #              ]
    # r = RequestsUtils()
    # result = r.request_by_step( case_info )  #request_by_step-->request-->__get或__post


