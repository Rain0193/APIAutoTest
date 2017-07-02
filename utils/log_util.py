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


class LogUtil( ):
    """
    日志处理类
    """
    __default_level = logging.DEBUG  # 日志默认开启级别
    __levels = { "debug": logging.DEBUG, "info": logging.INFO, "warning": logging.WARNING, "error": logging.ERROR,
                 "critical": logging.CRITICAL }

    def __gen_log_name( self, level ):
        '''
        log文件的绝对路径，log文件以年月日格式命名，如log-error.2017-03-09.log。建立一个父级目录的同级目录log。
        :param level:根据日志等级命名不同日志
        :return:
        '''
        parent_dir = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )
        name = "log-{}.".format( level ) + time.strftime( '%Y-%m-%d', time.localtime( ) ) + '.log'
        log_name = os.path.join( os.path.abspath( parent_dir ), "log" )
        log_final_name = os.path.join( os.path.abspath( log_name ), name )
        return log_final_name

    def __create_handler( self, log_name ):
        '''
        根据日志文件名创建不同的日志类FileHandler
        :param log_name: 日志名
        :return:
        '''
        if (not (os.path.isfile( log_name ))):  # 若文件不存在
            parent_dir = os.path.dirname( os.path.abspath( log_name ) )  # 日志文件的父级目录
            if (not os.path.exists( parent_dir )):  # 若父级目录不存在，则需要先创建目录，否则报错
                os.mkdir( parent_dir )
        return logging.FileHandler( log_name )

    def __log_config( self, level ):
        '''
        配置日志类
        :param level:日志等级
        :return:
        '''
        logger = logging.getLogger( str( level ) )
        # 设置日志默认等级。只有大于或等于默认等级时，才创建FileHandler
        logger.setLevel( self.__default_level )
        if self.__levels[
            level ] >= self.__default_level:  # logging级别代表的数字。NOTSET:0 DEBUG:10 INFO:10 WARNING:10 ERROR:10 CRITICAL:10
            if not logger.handlers:  # 若在该logger里已经有handler里则不添加，否则会出现重复写日志问题
                logger.addHandler( self.__create_handler( self.__gen_log_name( level ) ) )
        return logger

    def __format_message( self, level, message ):
        '''
        格式化日志信息
        :param level:
        :param message:
        :return:
        '''
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack( )[ 2 ]  # 利用反射得到调用函数信息
        return "[%s][%s] %s" % (
            time.strftime( '%Y-%m-%d %H:%M:%S', time.localtime( ) ), level,  message)

    def debug( self, message, print_flag = True ):
        '''
        记录DEBUG日志
        :param message:
        :param print_flag:是否输出到控制台
        :return:
        '''
        msg = self.__format_message( "debug", message )
        self.__log_config( "debug" ).debug( msg )
        if (print_flag):
            print( msg )

    def info( self, message, print_flag = True ):
        '''
        记录DEBUG日志
        :param message:
        :param print_flag:是否输出到控制台
        :return:
        '''
        msg = self.__format_message( "info", message )
        self.__log_config( "info" ).info( msg )
        if (print_flag):
            print( msg )

    def warning( self, message, print_flag = True ):
        '''
        记录WARNING日志
        :param message:
        :param print_flag:是否输出到控制台
        :return:
        '''
        msg = self.__format_message( "warning", message )
        self.__log_config( "warning" ).warning( msg )
        if (print_flag):
            print( msg )

    def error( self, message, print_flag = True ):
        '''
        记录ERROR日志
        :param message:
        :param print_flag:是否输出到控制台
        :return:
        '''
        msg = self.__format_message( "error", message )
        self.__log_config( "error" ).error( msg )
        if (print_flag):
            print( msg )

    def critical( self, message, print_flag = True ):
        '''
        记录CRITICAL日志
        :param message:
        :param print_flag:是否输出到控制台
        :return:
        '''
        msg = self.__format_message( "critical", message )
        self.__log_config( "critical" ).critical( msg )
        if (print_flag):
            print( msg )

# log = LogUtil( )
# log.debug( "debug test" )
