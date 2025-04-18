#验证预期结果，响应数据内容
import requests
import json #编码json.dumps()（序列化）转字符串，解码json.loads()（反序列化）转对象
import re  #匹配正则表达式

"""   这段代码定义了一个类的构造函数（也称为初始化方法）
__init__ 是一个特殊方法，用于类的初始化。当创建类的新实例时，这个方法会自动被调用。
self 是对当前对象实例的引用。在类的方法内部，self 代表调用该方法的对象本身。
response_data=None 是该方法的参数，其中 response_data 是一个命名参数，默认值为 None。
这意味着如果在创建类的实例时没有传 response_data 参数时，它将默认为 None
"""
class CheckUtils:
    print("********************调用CheckUtils进行断言***********************")
    def __init__(self,response_data=None):
        self.response_data = response_data
        # 根据用例表格中的“断言类型”赋值
        self.check_types ={
            'none':self.__none_check,  #__用于‌名称改写‌（name mangling）的一种约定
            'json_key':self.__json_key_check,  #改写后的属性名（或方法名）会在原名称前加上类名和一个下划线
            'json_key_value':self.__json_key_value_check,  #从而避免在子类中出现命名冲突
            'body_regexp':self.__body_regexp_check, #regexp正则  #这种改写机制主要用于封装‌：隐藏类的内部实现细节，只暴露给外部必要的接口。
            'response_code':self.__response_code_check,    #避免父类与子类命名冲突时可以使用名称改写。
            'header_key':self.__header_key_check,
            'header_key_value':self.__header_key_value_check
        }
        self.pass_result = {
            'code':0,
            'response_code':self.response_data.status_code,
            'response_reason':self.response_data.reason, #服务器返回的原因短语,如状态码404的reason是"Not Found"
            'response_headers':self.response_data.headers,
            'response_body':self.response_data.text,
            'message':'测试用例执行通过',
            'check_result': True
        }
        self.fail_result = {
            'code':2,
            'response_code':self.response_data.status_code,
            'response_reason':self.response_data.reason,
            'response_headers':self.response_data.headers,
            'response_body':self.response_data.text,
            'message':'测试用例断言失败，执行不通过',
            'check_result': False
        }

    def __none_check(self):  #双下划线前缀 __（名称改写）表示方法是“私有”的，使其在类的外部难以直接访问。
        return self.pass_result

    def __json_key_check(self,check_data):
        ''' 当响应正文为json时，比对是否包含键，支持多个键比较 '''
        key_list = check_data.split(",")  # 同时校验多个key时，用逗号分隔
        tmp_result = []
        for key in key_list:
            if key in self.response_data.json().keys(): #key是否在响应的实际结果中
                tmp_result.append(True)
            else:
                tmp_result.append(False)
        if  False in tmp_result:
            return self.fail_result
        else:
            return self.pass_result

    def __json_key_value_check(self,check_data):
        ''' 当响应正文为json时，比对是否包含键值对，支持多个键值对比较 '''
        check_data_dict = json.loads(check_data)
        tmp_result = []
        for item in check_data_dict.items():
            if item in self.response_data.json().items():
                tmp_result.append(True)
            else:
                tmp_result.append(False)
        if False in tmp_result:
            return self.fail_result
        else:
            return self.pass_result

    def __body_regexp_check(self,check_data): #正则匹配验证
        if re.findall(check_data,self.response_data.text): #re.findall用于在字符串中查找正则表达式匹配项
            return self.pass_result
        else:
            return self.fail_result

    def __response_code_check(self,check_data):
        if self.response_data.status_code == int(check_data):
            return self.pass_result
        else:
            return self.fail_result

    def __header_key_check(self,check_data):
        key_list = check_data.split(",")
        tmp_result = []
        for key in key_list:
            if key in self.response_data.headers.keys():
                tmp_result.append(True)
            else:
                tmp_result.append(False)
        if  False in tmp_result:
            return self.fail_result
        else:
            return self.pass_result

    def __header_key_value_check(self,check_data):
        check_data_dict = json.loads(check_data)
        tmp_result = []
        for item in check_data_dict.items():
            if item in self.response_data.headers.items():
                tmp_result.append(True)
            else:
                tmp_result.append(False)
        if False in tmp_result:
            return self.fail_result
        else:
            return self.pass_result

    def run_check(self,check_type,check_data):
        if check_type=='none' or check_data == '':
            result = self.check_types['none']()
            return result
        elif check_type in self.check_types.keys():   # 判断用例表格中的“验证方式”在不在self.check_types字典的key中
            result = self.check_types[check_type](check_data)  # self.json_key_check()  在的话就根据字典的key获取value，并调用对应方法
            return result
        else:
            return self.fail_result

if __name__=='__main__':
    import requests
    url_params = {"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}
    response = requests.get(url='https://api.weixin.qq.com/cgi-bin/token',
                            params= url_params )
    # result = CheckUtils(response).json_key_check( 'access_token' )
    # print( result )
    # result = CheckUtils(response).json_key_value_check( '{"expires_in":7200}' )
    # print( result )
    # result = CheckUtils(response).body_regexp_check('"access_token":"(.+?)"')
    # print( result )

    result = CheckUtils(response).run_check( 'header_key_value','{"Connection":"keep-alive"}' )
    print( result )

