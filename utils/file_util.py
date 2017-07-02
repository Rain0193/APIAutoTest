#!/usr/bin/env python
# coding=UTF-8
'''
 # Desc：文件处理类
 # Author：TavisD 
 # Time：2016-12-5 9:02
 # Ver：V1.0
'''

import os
import yaml


class FileUtil:
    '''
    文件处理类
    '''

    __instance = None  # 实例

    def __new__( cls, *args, **kwargs ):
        '''
        单实例
        :param args:
        :param kwargs:
        :return:
        '''
        if not cls.__instance:
            cls.__instance = super( FileUtil, cls ).__new__( cls, *args )
        return cls.__instance

    def get_file_path( self, file_name ):
        file_path = None
        try:
            project_name = ""
            # windows系统下获取工程名
            if os.name == "nt":
                file_dirs = os.path.split( file_name )[ 0 ]
                # 处理“D:/Software/WorkSpace/Python/”这种格式的路径
                if file_dirs.find( "/" ) != -1:
                    project_name = file_dirs.split( "/" )[ len( file_dirs.split( "/" ) ) - 1 ]  # 倒数第一个目录
                # 处理“D:\Software\WorkSpace\Python\”这种格式的路径
                elif file_dirs.find( "\\" ) != -1:
                    project_name = file_dirs.split( "\\" )[ len( file_dirs.split( "\\" ) ) - 1 ]  # 倒数第一个目录
            # Linux系统下获取工程名
            elif os.name == "posix":
                file_dirs = os.path.split( file_name )[ 0 ]
                # 处理“/usr/local/HTAPTTest/testdata/”这种格式的路径
                if file_dirs.find( "/" ) != -1:
                    project_name = file_dirs.split( "/" )[ len( file_dirs.split( "/" ) ) - 1 ]  # 倒数第一个目录
            # 拼接出yml测试数据文件的绝对路径
            file_path = os.path.join(
                    os.path.realpath( os.path.dirname( os.path.dirname( os.path.dirname( file_name ) ) ) ),
                    "testdata", project_name,
                    os.path.basename( file_name )[ 5:-3 ] ) + ".yml"
            self.file_path = file_path
        except Exception as e:
            print( "yml测试数据文件路径有误！" + str( e ) )
        return file_path

    def get_test_data_by_name( self, file_name ):
        '''
        根据test case的名字自动获取对应的yml格式测试数据
        :param file_name: test case的名字  os.path.abspath( __file__ )
        :return:
        '''

        return self.connect_to( self.get_file_path( file_name ) ).parsed_data, self.file_path

    def save_test_data_by_name( self, file_path, test_data ):
        '''
        根据test case名字自动保存对应的yml格式测试数据
        :param file_path:
        :param test_data:
        :return:
        '''
        with open( file_path, "w", encoding = "utf-8" ) as f:
            yaml.dump( test_data, f, default_flow_style = False, allow_unicode = True )

    ##使用工厂方法处理文件，以便后面扩展
    class YAMLConnector:
        def __init__( self, file_path ):
            with open( file_path, "rb" )as f:
                self.data = yaml.load( f )

        @property
        def parsed_data( self ):
            return self.data

    def connection_factory( self, file_path ):
        if file_path.endswith( "yml" ):
            connector = self.YAMLConnector
        else:
            raise ValueError( "文件格式错误，Can't connect to {}".format( file_path ) )
        return connector( file_path )

    def connect_to( self, file_path ):
        factory = None
        try:
            factory = self.connection_factory( file_path )
        except ValueError as ve:
            print( ve )
        return factory
