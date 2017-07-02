#!/usr/bin/env python
# coding=UTF-8
'''
 # Desc：时间处理类
 # Author：TavisD 
 # Time：2016/10/23 16:12
 # Ver：V1.0
'''

import datetime


class TimeUtil( ):
    """
    时间处理类
    """

    __instance = None  # 实例

    def __new__( cls, *args, **kwargs ):
        '''
        单实例
        :param args:
        :param kwargs:
        :return:
        '''
        if not cls.__instance:
            cls.__instance = super( TimeUtil, cls ).__new__( cls, *args )
        return cls.__instance

    def get_second_str( self ):
        '''
        获取"20170316162233" 年月日时分秒的字符串
        :return:
        '''
        return datetime.datetime.now( ).strftime( "Y%%m%d%H%M%S" )

    def get_micro_str( self ):
        '''
        获取"1023165507875" 月日时分秒毫秒的字符串
        :return: str
        '''
        return datetime.datetime.now( ).strftime( "%m%d%H%M%S%f" )[ :-3 ]

    def get_common_str( self ):
        '''
        获取"2016-10-23 16:55:43"字符串
        :return: str
        '''
        return datetime.datetime.now( ).strftime( "%Y-%m-%d %H:%M:%S" )

    def get_stamp( self ):
        '''
        获取13位时间戳1477214391116
        :return: str
        '''
        return str( int( datetime.datetime.now( ).timestamp( ) * 1000 ) )

    def str_to_time( self, str_time ):
        '''
        2016-10-23 17:25:44转换成date对象
        :param str_time:  2016-10-23 17:25:44格式的字符串
        :return: date对象
        '''
        try:
            return datetime.datetime.strptime( str_time, '%Y-%m-%d %H:%M:%S' )
        except Exception as e:
            print( "转换时间出错!----" + str( e ) )

# # Demo
# time_util = TimeUtil( )
# common_time = time_util.get_common_str( )
# print( time_util.str_to_time( common_time ) )
