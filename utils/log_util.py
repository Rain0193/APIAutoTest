#!/usr/bin/env python
# coding=UTF-8
'''
 # Desc：日志处理类。
 # Author：TavisD 
 # Time：2017-3-9 8:54
 # Ver：V1.0
'''

import time
import logging
import os
import inspect
from  utils.base import LOG_SWITCH, LOG_LEVEL, PRINT_SWITCH


class LogUtil( ):
    """
    日志处理类
    """
    __default_level = logging.DEBUG
    __levels = { "DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR,
                 "CRITICAL": logging.CRITICAL }
    __logger = None
    __handler = None

    def __gen_log_name( self, level ):
        '''
        log文件的绝对路径，log文件以年月日格式命名，如log-error.2017-03-09.log。建立一个父级目录的同级目录log。
        :param level:根据日志等级命名不同日志
        :return:
        '''
        parent_dir = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )
        name = "log-{}.".format( level.lower( ) ) + time.strftime( '%Y-%m-%d', time.localtime( ) ) + '.log'
        log_name = os.path.join( os.path.abspath( parent_dir ), "log" )
        log_final_name = os.path.join( os.path.abspath( log_name ), name )
        return log_final_name

    def __create_handler( self, log_name ):
        '''
        根据日志文件名创建不同的日志类FileHandler
        :param log_name: 日志名
        :return:
        '''
        if (not (os.path.isfile( log_name ))):
            parent_dir = os.path.dirname( os.path.abspath( log_name ) )
            if (not os.path.exists( parent_dir )):
                os.mkdir( parent_dir )
        return logging.FileHandler( log_name, encoding = "utf-8" )

    def __log_config( self, LOG_LEVEL, log_name_level ):
        '''
        配置日志类
        :param LOG_LEVEL:总开关的日志等级
        :param log_name_level: 日志名的等级
        :return:
        '''
        if LOG_SWITCH:
            self.__logger = logging.getLogger( str( self.__levels[ log_name_level ] ) )
            self.__logger.setLevel( self.__levels[ LOG_LEVEL ] )
            # 若总开关等级小于等于日志名等级，才创建日志文件.DEBUG:10  INFO:20 WARNING:30 ERROR:40 CRITICAL:50
            if self.__levels[ LOG_LEVEL ] <= self.__levels[ log_name_level ]:
                if not self.__logger.handlers:
                    self.__handler = self.__create_handler( self.__gen_log_name( log_name_level ) )
                    self.__logger.addHandler( self.__handler )
            return self.__logger

    def __format_message( self, level, message ):
        '''
        格式化日志信息
        :param level:
        :param message:
        :return:
        '''
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack( )[ 2 ]
        return "[%s][%s] %s" % (
            time.strftime( '%Y-%m-%d %H:%M:%S', time.localtime( ) ), level, message)

    def __recording( self, message, print_flag, level ):
        msg = self.__format_message( level, message )
        if (print_flag):
            print( msg )
        return msg

    def debug( self, message, print_flag = PRINT_SWITCH, level = "DEBUG" ):
        msg = self.__recording( message, print_flag, level )
        logger = self.__log_config( LOG_LEVEL, level )
        if logger:
            logger.debug( msg )

    def info( self, message, print_flag = PRINT_SWITCH, level = "INFO" ):
        msg = self.__recording( message, print_flag, level )
        logger = self.__log_config( LOG_LEVEL, level )
        if logger:
            logger.info( msg )

    def warning( self, message, print_flag = PRINT_SWITCH, level = "WARNING" ):
        msg = self.__recording( message, print_flag, level )
        logger = self.__log_config( LOG_LEVEL, level )
        if logger:
            logger.warning( msg )

    def error( self, message, print_flag = PRINT_SWITCH, level = "ERROR" ):
        msg = self.__recording( message, print_flag, level )
        logger = self.__log_config( LOG_LEVEL, level )
        if logger:
            logger.error( msg )

    def critical( self, message, print_flag = PRINT_SWITCH, level = "CRITICAL" ):
        msg = self.__recording( message, print_flag, level )
        logger = self.__log_config( LOG_LEVEL, level )
        if logger:
            logger.critical( msg )

# log = LogUtil( )
# print( logging.DEBUG )
# print( logging.INFO )
# print( logging.WARNING )
# print( logging.ERROR )
# print( logging.CRITICAL )
# DEBUG:10  INFO:20 WARNING:30 ERROR:40 CRITICAL:50
