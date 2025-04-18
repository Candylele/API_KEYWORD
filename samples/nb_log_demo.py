
from nb_log import LogManager

logger = LogManager('P7P8').get_logger_and_add_handlers(is_add_stream_handler=True,
                                                        log_filename='test.log')
logger.info( 'info级别的日志' )
logger.warning(  'warn --++++' )
logger.error(  'error --++++' )
logger.fatal(  'fatal --++++' )


