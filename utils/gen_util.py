#!/usr/bin/env python
# coding=UTF-8
'''
 # Desc：生成测试数据。
 # Author：TavisD 
 # Time：2016-10-13 17:42
 # Ver：V1.0
'''

import string
import random
import time


class GenUtil:
    """
    生成测试数据。
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
            cls.__instance = super( GenUtil, cls ).__new__( cls, *args )
        return cls.__instance

    def gen_phones( self, count = 1 ):
        '''
        生成手机号 1[3,4,5,7,8][1~9]
        :param count: 生成数量
        :return:list
        '''
        try:
            list = [ ]
            for i in range( count ):
                list.append(
                        '1' + ''.join( random.choice( "34578" ) ) + ''.join( random.choice( "123456789" ) ) + ''.join(
                                random.sample( string.digits, 9 ) ) )
            if count == 1:
                return list[ 0 ]
            else:
                return list
        except Exception as e:
            print( "生成手机号出错！----" + str( e ) )

    def gen_digits( self, length = 5, count = 1 ):
        '''
        生成正整数
        :param length:正整数的位数
        :param count:生成数量
        :return:list
        '''
        try:
            list = [ ]
            if length <= 10:
                for i in range( count ):
                    list.append( ''.join( random.sample( string.digits, length ) ) )
            elif length > 10:
                for i in range( count ):
                    list.append( ''.join( [ random.choice( string.digits ) for _ in range( length ) ] ) )
            if count == 1:
                return list[ 0 ]
            else:
                return list
        except Exception as e:
            print( "生成正整数出错！----" + str( e ) )

    def gen_chinese_name( self, count = 1 ):
        '''
        生成中文+时间（年月日时分秒）
        :param count:生成姓名的个数
        :return:
        '''
        try:
            list = [ ]
            for i in range( count ):
                list.append( '测试' + ''.join( time.strftime( '%Y%m%d%H%M%S', time.localtime( ) ) ) )
            if count == 1:
                return list[ 0 ]
            else:
                return list
        except Exception as e:
            print( "生成中文+4位随机数出错！----" + str( e ) )

    def gen_characters( self, length = 10, count = 1 ):
        '''
        生成随机字符（字母+数字）
        :param length:单个字符串的长度
        :param count:生成字符串的个数
        :return:
        '''
        try:
            chars = string.ascii_letters + string.digits
            list = [ ]
            if length <= 62:
                for i in range( count ):
                    list.append( ''.join( random.sample( chars, length ) ) )
                if count == 1:
                    return list[ 0 ]
                else:
                    return list
            else:
                for i in range( count ):
                    list.append( ''.join( [ random.choice( chars ) for i in range( length ) ] ) )
                if count == 1:
                    return list[ 0 ]
                else:
                    return list
        except Exception as e:
            print( "生成随机字符（字母+数字）出错！----" + str( e ) )

    def gen_telephones( self, count = 1 ):
        '''
        生成固定电话
        :param count: 生成数量
        :return:
        '''
        try:
            list = [ ]
            for i in range( count ):
                if random.randint( 1, 100 ) < 10:
                    prefix = [ '010', '020', '021', '022', '023', '025', '027', '028' ]
                else:
                    prefix = [ '0' + random.choice( "3456789" ) + random.choice( "0123456789" ) + random.choice(
                            "0123456789" ) ]
                list.append( random.choice( prefix ) + '-' + ''.join( random.sample( string.digits, 8 ) ) )
            if count == 1:
                return list[ 0 ]
            else:
                return list
        except Exception as e:
            print( "生成固定电话出错！----" + str( e ) )

    def gen_emails( self, count = 1 ):
        '''
        生成邮箱地址
        :param count:生成数量
        :return:
        '''
        try:
            chars = string.ascii_letters + string.digits + "."
            list = [ ]
            for i in range( count ):
                list.append( ''.join( random.sample( chars, 8 ) ) + '@' + ''.join(
                        random.sample( string.ascii_lowercase, 5 ) ) + '.com' )
            if count == 1:
                return list[ 0 ]
            else:
                return list
        except Exception as e:
            print( "生成邮箱地址出错！----" + str( e ) )

# # Demo
# gen_util = GenUtil( )
# print( gen_util.gen_emails( 222 ) )
