# 读写config.ini配置数据的类与方法

import os
import configparser  # 读取与写入配置文件，文件内容为 节和参数(键=值对)组成的ini文件

class ConfigUtils:
    def __init__(self,config_file_path ):
        self.cfg_path = config_file_path
        """
        configparser.ConfigParser() 是 Python 标准库中的一个类，不用单独安装。
        用于读取和写入，修改配置文件。配置文件通常是以 .ini 结尾的文件，里面包含了键值对形式的配置信息。
        """
        self.cfg = configparser.ConfigParser()  #创建对象，用于读取和写入配置文件
        self.cfg.read( self.cfg_path )  #根据文件路径读取配置文件

    def read_value(self,section,key): # 定义一个方法，用于读取配置文件中的值
        value = self.cfg.get(section,key)  # 从配置文件的指定节(section)和键(key)中读取值
        return value  # get方法来读取配置文件中的数据不区分大小写

    def write_value(self,section,key,value): # 定义一个方法，用于向配置文件中写入值
        self.cfg.set(section,key,value) # 在配置文件的指定节(section)和键(key)中设置值
        config_file_obj = open( self.cfg_path ,'w') # 以写入模式打开配置文件，文件路径由实例变量cfg_path提供
        self.cfg.write( config_file_obj ) # 将修改后的配置内容写入到打开的文件对象中
        config_file_obj.flush() # 刷新文件对象的缓冲区，确保所有内容都被写入到文件中
        config_file_obj.close() # 关闭文件对象，释放资源

if __name__=='__main__':
    config_utils = ConfigUtils("../conf/config.ini")
    print( config_utils.read_value( 'default','HOSTS' ) )  #读取配置文件数据
    config_utils.write_value('default','token_value','6666')  #给配置文件写数据

