#nb_log说明文档：https://nb-log-doc.readthedocs.io/
"""
添加同类型handler，不会重复记录
控制台日志变成可点击，精确跳转
自动拦截改变项目中所有地方的print效果
控制台日志根据日志级别自动变色
支持在根目录中nb_log_config.py文件中日志自定义
日志存在D:\pythonlogs
"""

from nb_log import LogManager

# LogManager是一个日志管理类，用于创建logger和添加handler，支持将日志打印到控制台打印和写入日志文件和mongodb和邮件。
logger = LogManager('CandyTest_LOG')\
            .get_logger_and_add_handlers(is_add_stream_handler=True,
                                        log_filename='test.log',
                                         log_level_int=10)
"""
~~~~~~~日志存在D:\pythonlogs~~~~~~~~~可在nb_log_config.py中修改存储位置
is_add_stream_handler: 是否打印日志到控制台
log_filename: 日志文件名字，仅当log_path和log_filename都不为None时候才写入到日志文件。
log_level_int: 日志输出级别，设置为 10 20 30 40 50，分别对应原生logging.DEBUG(10)，logging.INFO(20)，logging.WARNING(30)，logging.ERROR(40),logging.CRITICAL(50)级别，

is_add_mail_handler :是否发邮件
ding_talk_token:钉钉机器人token
"""