#调用 ConfigUtils中读写config.ini配置数据的方法 读取数据

import os
from common.config_utils import ConfigUtils

class Config:
    def __init__(self,config_file_path):
        self.cfg_obj = ConfigUtils( config_file_path ) #调用读取配置文件类
    """
    @property是内置装饰器，将这个方法转换为一个属性。
    可以像访问普通属性一样访问这个属性，而不需要在属性名后加上括号。
    """
    @property
    def HOSTS(self):
        hosts_value = self.cfg_obj.read_value( 'default','HOSTS' )  #使用类中的方法读取配置文件
        return hosts_value
    @property
    def TOKEN_VALUE(self):
        toekn_value = self.cfg_obj.read_value( 'default','TOKEN_VALUE' ) # 读取时不区分大小写token_value
        return toekn_value
    @property
    def REPORT_PATH(self):
        report_path_value = self.cfg_obj.read_value('default','report_path')
        return report_path_value

if __name__=='__main__':
    current_path = os.path.dirname(os.path.abspath(__file__))
    print(current_path)
    config_file_dir = os.path.join(current_path, '..', 'conf', 'config.ini') #拼接配置文件路径
    print(config_file_dir)
    local_config = Config(config_file_dir)
    print(local_config.HOSTS)  #读取配置文件中的hosts
    print(local_config.TOKEN_VALUE)  # 不区分大小写
    print(local_config.REPORT_PATH)