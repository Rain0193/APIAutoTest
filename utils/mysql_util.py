#!/usr/bin/env python
# coding=UTF-8
'''
 # 说明：封装MySQL的CURD
 # 创建人：TavisD
 # 创建时间：16-1-16 下午7:19
'''

import pymysql
import os
import sys

sys.path.append( os.path.dirname( os.path.abspath( __file__ ) ) )
from file_util import FileUtil
from  utils.base import ENV,DB

class MysqlUtil:
    __conn = None
    __cur = None
    __instance = None

    def __new__( cls, *args, **kwargs ):
        if not cls.__instance:
            cls.__instance = super( MysqlUtil, cls ).__new__( cls, *args )
        return cls.__instance

    def __init__( self ):
        db = DB[ENV]
        if db is not None:
            self.__connect( db[ "host" ], db[ "port" ], db[ "user_name" ], db[ "password" ] )

    def __del__( self ):
        '''
        释放资源（系统GC自动调用）
        :return:
        '''
        try:
            self.__cur.close( )
            self.__conn.close( )
        except:
            print( "释放MySQL资源出错！" )

    # def __get_db_from_config( self, env = "beta" ):
    #     '''
    #     从配置获取DB信息
    #     :param env:
    #     :return:
    #     '''
    #     base_dir = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )
    #     file = os.path.join( os.path.join( os.path.realpath( base_dir ), "config" ), "db.yml" )  # DB配置文件的绝对路径
    #     db = FileUtil( ).connect_to( file ).parsed_data[ env ]
    #     return db

    def __connect( self, host, port, user, password, charset = 'utf8' ):
        '''
        根据连接参数，创建MySQL连接
        :param host:数据库IP
        :param port:端口
        :param user:用户名
        :param password:密码
        :param db:数据库
        :param charset:字符集
        :return:
        '''
        try:
            self.__conn = pymysql.connect( host = host, port = port, user = user, password = password,
                                          charset = charset )
        except pymysql.Error as e:
            print( 'MySQL连接出错！%d：%s' % (e.args[ 0 ], e.args[ 1 ]) )
        self.__cur = self.__conn.cursor( )

    def query( self, sql, args = None ):
        '''
        执行 select 语句
        :param sql:查询SQL
        :return:
        '''
        try:
            result = self.__cur.execute( sql, args )
        except pymysql.Error as e:
            print( "select出错！%d：%s" % (e.args[ 0 ], e.args[ 1 ]) )
            result = False
        return result

    def queryOutputDict( self, sql, args = None ):
        '''
        执行以字典Cursor返回方式的Select查询语句
        :param sql:查询SQL
        :return:
        '''
        self.__cur = self.__conn.cursor( pymysql.cursors.DictCursor )
        try:
            result = self.__cur.execute( sql, args )
        except pymysql.Error as e:
            print( "字典Cursor方式select出错！%d：%s" % (e.args[ 0 ], e.args[ 1 ]) )
            result = False
        return result

    def update( self, sql, args = None ):
        '''
        执行update或delete语句
        :param sql:
        :return:
        '''
        try:
            self.__cur.execute( sql, args )
            affectedRows = self.__conn._affected_rows
            self.__commit( )
        except pymysql.Error as e:
            print( "update或delete出错！%d：%s" % (e.args[ 0 ], e.args[ 1 ]) )
            affectedRows = False
        return affectedRows

    def insert( self, sql, args = None ):
        '''
        执行insert语句，若主键是自增ID，则返回新生成的ID
        :param sql:
        :return:
        '''
        try:
            self.__cur.execute( sql, args )
            insertId = self.__conn.insert_id( )
            self.__commit( )
            return insertId
        except pymysql.Error as e:
            print( "insert出错！%d：%s" % (e.args[ 0 ], e.args[ 1 ]) )
            return False

    def getColumnNames( self ):
        '''
        获取表的列名
        :return: List
        '''
        desc = self.__cur.description
        columnNames = [ ]
        for i in range( len( desc ) ):
            columnNames.append( desc[ i ][ 0 ] )
        return columnNames

    def fetchOneRow( self ):
        '''
        返回一行结果，然后游标指向下一行。到达最后一行以后，返回None
        :return:
        '''
        return self.__cur.fetchone( )

    def fetchAllRows( self ):
        '''
        返回所有结果
        :return:
        '''
        return self.__cur.fetchall( )

    def getRowCount( self ):
        '''
        获取结果行数
        :return:
        '''
        return self.__cur.rowcount

    def __commit( self ):
        '''
        数据库commit操作
        :return:
        '''
        self.__conn.commit( )

    def __rollback( self ):
        '''
        数据库回滚操作
        :return:
        '''
        self.__conn.rollback( )

    def __close( self ):
        '''
        关闭数据库连接
        :return:
        '''
        self.__del__( )


# mysql_util = MysqlUtil( )
# mysql_util.query( "select * from orderdb.t_ecomm_order limit 10" )
# if __name__ == '__main__':
#     '''使用范例'''
#     mysql_util = MysqlUtil( )  # 创建MYSQL实例
#
#     ##====Select操作====##
#     # 无参数查询
#     mysql_util.query( "select * from FANS" )  # 执行查询语句
#     oneRow = mysql_util.fetchOneRow( )  # 取得一行结果
#     allRows = mysql_util.fetchAllRows( )  # 取得所有结果集
#     rowCount = mysql_util.getRowCount( )  # 取得结果行数
#     columnNames = mysql_util.getColumnNames( )  # 获取表的列名
#
#     # 有参数查询
#     mysql_util.query( "select * from FANS WHERE id=%s OR NAME=%s", (2, "测试1") )
#
#     # 以字典Cursor方式返回进行查询
#     mysql_util.queryOutputDict( "select * from FANS" )
#
#     ##====Insert操作====##
#     insertId = mysql_util.insert( "insert INTO FANS ( NAME, PHONE, OPEN_ID, IMG_URL) VALUES (%s,%s,%s,%s)",
#                           ("ddd", "18899990000", "dkklkll", "cc") )
#
#     ##====Update或Delete操作====##
#     mysql_util.update( "update FANS SET NAME=%s WHERE PHONE=%s", ("TavisD", 18899990000) )
#     print( mysql_util.update( "delete FROM FANS where PHONE=%s ", (4) ) )
# #
