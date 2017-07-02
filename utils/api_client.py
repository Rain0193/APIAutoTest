#!/usr/bin/env python
# coding=UTF-8
'''
# Desc：调用Http Json协议的接口。主要封装请求及处理响应。根据自己公司情况修改。
# Author：TavisD
# Time：2016-9-4 16:58
# Ver：V1.1
#
'''

import hashlib
import json
from Crypto.Cipher import AES
from Crypto.Cipher import DES3
import base64
import requests
import re
import os
import sys
import traceback

sys.path.append( os.path.dirname( os.path.abspath( __file__ ) ) )
from file_util import FileUtil
from log_util import LogUtil


class APIClient:
    """
    HTTP Json协议接口的调用，token、签名、加密、解密。
    """
    __instance = None  # 实例
    # 登录的类型，直接定义成类变量，方便引用
    LOGIN_TYPE_NORMAL = "NORMAL"  # 业主端
    LOGIN_TYPE_SUPPLIER = "SUPPLIER"  # 电商商家端
    LOGIN_TYPE_MANAGER = "MANAGER"  # 运营后台
    LOGIN_TYPE_PMMANAGER = "PMMANAGER"  # 物业后台
    LOGIN_TYPE_STAFF = "STAFF"  # 员工端

    def __new__( cls, *args, **kwargs ):
        '''
        单实例
        :param args:
        :param kwargs:
        :return:
        '''
        if not cls.__instance:
            cls.__instance = super( APIClient, cls ).__new__( cls, *args )
        return cls.__instance

    def __init__( self ):
        '''
        构造函数
        :return: 
        '''
        ##加密、解密属性。
        self.__AES_BASE_KEY = "XXXXX"
        self.__APP_ID = "XXXXX"
        self.__APP_SECURITY = "XXXXX"
        self.__DEFAULT_TOKEN = "XXXXX"

        ##各端的token
        self.__NORMAL_TOKEN = None  # 业主端，默认账号
        self.__NORMAL_TOKEN_XIAOMEI = None  # 业主端，小梅。
        self.__NORMAL_TOKEN_YAOYAO = None  # 业主端，瑶瑶
        self.__NORMAL_TOKEN_LILI = None  # 业主端，丽丽姐
        self.__SUPPLIER_TOKEN = None  # 供应商，默认账号
        self.__MANAGER_TOKEN = None  # 运营后台，默认账号
        self.__PMMANAGER_TOKEN = None  # 物业后台，默认账号
        self.__STAFF_TOKEN = None  # 员工端，默认账号

    def __cal_different_account( self, env = "beta", login_type = LOGIN_TYPE_NORMAL, tester_account = "default" ):
        '''
        动态变量名、动态login_type、动态环境生成不同账号
        :param env: 
        :param login_type: 
        :param tester_account: 
        :return: 
        '''
        accounts = self.__read_accounts( env )
        if accounts:
            if tester_account == "default":  # 默认账号
                if login_type == self.LOGIN_TYPE_NORMAL:  # 业主端
                    self.__NORMAL_TOKEN = self.cal_token(
                            accounts[ env ][ self.LOGIN_TYPE_NORMAL ][ "user_name" ],
                            accounts[ env ][ self.LOGIN_TYPE_NORMAL ][ "password" ],
                            self.LOGIN_TYPE_NORMAL,
                            env )
                elif login_type == self.LOGIN_TYPE_SUPPLIER:  # 供应商
                    self.__SUPPLIER_TOKEN = self.cal_token(
                            accounts[ env ][ self.LOGIN_TYPE_SUPPLIER ][ "user_name" ],
                            accounts[ env ][ self.LOGIN_TYPE_SUPPLIER ][ "password" ],
                            self.LOGIN_TYPE_SUPPLIER,
                            env )
                elif login_type == self.LOGIN_TYPE_MANAGER:  # 运营后台
                    self.__MANAGER_TOKEN = self.cal_token(
                            accounts[ env ][ self.LOGIN_TYPE_MANAGER ][ "user_name" ],
                            accounts[ env ][ self.LOGIN_TYPE_MANAGER ][ "password" ],
                            self.LOGIN_TYPE_MANAGER,
                            env )
                elif login_type == self.LOGIN_TYPE_PMMANAGER:  # 物业后台
                    self.__PMMANAGER_TOKEN = self.cal_token(
                            accounts[ env ][ self.LOGIN_TYPE_PMMANAGER ][ "user_name" ],
                            accounts[ env ][ self.LOGIN_TYPE_PMMANAGER ][ "password" ],
                            self.LOGIN_TYPE_PMMANAGER,
                            env )
                elif login_type == self.LOGIN_TYPE_STAFF:  # 员工端
                    self.__STAFF_TOKEN = self.cal_token(
                            accounts[ env ][ self.LOGIN_TYPE_STAFF ][ "user_name" ],
                            accounts[ env ][ self.LOGIN_TYPE_STAFF ][ "password" ],
                            self.LOGIN_TYPE_STAFF,
                            env )

            else:  # tester自己的账号，自己写的用例，用自己的token，例子 ：api_client.NORMAL_TOKEN_YAOYAO
                if login_type == self.LOGIN_TYPE_NORMAL:  # 业主端
                    self.__dict__[ "_APIClient__NORMAL_TOKEN_{}".format( tester_account ) ] = self.cal_token(
                            accounts[ env ][ self.LOGIN_TYPE_NORMAL + "_{}".format( tester_account ) ][ "user_name" ],
                            accounts[ env ][ self.LOGIN_TYPE_NORMAL + "_{}".format( tester_account ) ][ "password" ],
                            self.LOGIN_TYPE_NORMAL,
                            env )
                else:  # 其他端，暂没必要，若有必要再补充
                    pass

    @property
    def NORMAL_TOKEN( self, env = "beta" ):
        '''
        通过get属性方式来访问私有变量__NORMAL_TOKEN   #默认业主端账号
        :param env:
        :return:
        '''
        if self.__NORMAL_TOKEN == None:
            self.__cal_different_account( env = env, login_type = self.LOGIN_TYPE_NORMAL )
        return self.__NORMAL_TOKEN

    @property
    def NORMAL_TOKEN_XIAOMEI( self, env = "beta" ):
        '''
        通过get属性方式来访问私有变量__NORMAL_TOKEN_XIAOMEI  #小梅的业主端账号
        :param env:
        :return:
        '''
        if self.__NORMAL_TOKEN_YAOYAO == None:
            self.__cal_different_account( env = env, login_type = self.LOGIN_TYPE_NORMAL, tester_account = "XIAOMEI" )
        return self.__NORMAL_TOKEN_XIAOMEI

    @property
    def NORMAL_TOKEN_YAOYAO( self, env = "beta" ):
        '''
        通过get属性方式来访问私有变量__NORMAL_TOKEN_YAOYAO  #瑶瑶的业主端账号
        :param env:
        :return:
        '''
        if self.__NORMAL_TOKEN_YAOYAO == None:
            self.__cal_different_account( env = env, login_type = self.LOGIN_TYPE_NORMAL, tester_account = "YAOYAO" )
        return self.__NORMAL_TOKEN_YAOYAO

    @property
    def NORMAL_TOKEN_LILI( self, env = "beta" ):
        '''
        通过get属性方式来访问私有变量__NORMAL_TOKEN_LILI  #丽丽姐的业主端账号
        :param env:
        :return:
        '''
        if self.__NORMAL_TOKEN_LILI == None:
            self.__cal_different_account( env = env, login_type = self.LOGIN_TYPE_NORMAL, tester_account = "LILI" )
        return self.__NORMAL_TOKEN_LILI

    @property
    def SUPPLIER_TOKEN( self, env = "beta" ):
        '''
        通过get属性方式来访问私有变量__SUPPLIER_TOKEN  #默认供应商账号
        :param env:
        :return:
        '''
        if self.__SUPPLIER_TOKEN == None:
            self.__cal_different_account( env = env, login_type = self.LOGIN_TYPE_SUPPLIER )
        return self.__SUPPLIER_TOKEN

    @property
    def MANAGER_TOKEN( self, env = "beta" ):
        '''
        通过get属性方式来访问私有变量__MANAGER_TOKEN  #默认运营后台账号
        :param env:
        :return:
        '''
        if self.__MANAGER_TOKEN == None:
            self.__cal_different_account( env = env, login_type = self.LOGIN_TYPE_MANAGER )
        return self.__MANAGER_TOKEN

    @property
    def PMMANAGER_TOKEN( self, env = "beta" ):
        '''
        通过get属性方式来访问私有变量__PMMANAGER_TOKEN   #默认物业后台账号
        :param env:
        :return:
        '''
        if self.__PMMANAGER_TOKEN == None:
            self.__cal_different_account( env = env, login_type = self.LOGIN_TYPE_PMMANAGER )
        return self.__PMMANAGER_TOKEN

    @property
    def STAFF_TOKEN( self, env = "beta" ):
        '''
        通过get属性方式来访问私有变量__PMMANAGER_TOKEN   #默认员工端账号
        :param env:
        :return:
        '''
        if self.__STAFF_TOKEN == None:
            self.__cal_different_account( env = env, login_type = self.LOGIN_TYPE_STAFF )
        return self.__STAFF_TOKEN

    def cal_url( self, project_name, api_name, env = "beta" ):
        '''
        生成最终请求的url，根据自己公司需要修改。
        :param env: 环境，beta、fix
        :param project_name:工程名称
        :param api_name:接口名
        :return:
        '''
        env_url = { "beta": "test", "fix": "fix", "stress": "stress" }
        if api_name.startswith( "/" ):
            api_name = api_name[ 1: ]
        return "http://" + env_url[ env ] + "." + project_name + "-api.hd/" + api_name

    def cal_token( self, username, password, login_type = LOGIN_TYPE_NORMAL, env = "beta" ):
        '''
        生成token
        :param username: 用户名
        :param password: 密码
        :param login_type: 业主端：NORMAL，供应商：SUPPLIER，运营后台：MANAGER。物业后台：PMMANAGER。默认生成业主端的token。
        :param env:环境。beta、Fix。
        :return:
        '''
        # 业主端：NORMAL
        if login_type == self.LOGIN_TYPE_NORMAL:
            params = { "loginName": username, "password": password }
            url = self.cal_url( "sso", "sso/login", env )
            try:
                result = self.http_post( url, params, None )
                if result is not None:
                    return result[ "result" ]
            except:
                LogUtil( ).error( "生成NORMAL token出错！----" + traceback.format_exc( ) )
        # 供应商：SUPPLIER
        elif login_type == self.LOGIN_TYPE_SUPPLIER:
            params = { "username": username, "password": password }
            url = self.cal_url( "supplier", "supplierSso/login", env )
            try:
                result = self.http_post( url, params, None, login_type = login_type )
                if result is not None:
                    token_result = json.loads( result[ "result" ] )
                    return token_result[ "token" ]
            except:
                LogUtil( ).error( "生成SUPPLIER token出错！----" + traceback.format_exc( ) )
        # 运营后台：MANAGER
        elif login_type == self.LOGIN_TYPE_MANAGER:
            params = { "username": username, "password": password, "systemType": 2 }
            url = self.cal_url( "sys-sso", "systemSso/loginSys", env )
            try:
                result = self.http_post( url, params, None, login_type = login_type )
                if result is not None:
                    return result[ "result" ]
            except:
                LogUtil( ).error( "生成MANAGER token出错！----" + traceback.format_exc( ) )
        # 物业后台：PMMANAGER
        elif login_type == self.LOGIN_TYPE_PMMANAGER:
            params = { "username": str( username ), "password": str( password ), "systemType": 1 }
            url = self.cal_url( "sys-sso", "systemSso/loginSys", env )
            try:
                result = self.http_post( url, params, None, login_type = login_type )
                if result is not None:
                    return result[ "result" ]
            except:
                LogUtil( ).error( "生成PMMANAGER token出错！----" + traceback.format_exc( ) )
        # 员工端：STAFF
        elif login_type == self.LOGIN_TYPE_STAFF:
            params = { "username": str( username ), "password": str( password ) }
            url = self.cal_url( "sys-sso", "systemSso/login", env )
            try:
                result = self.http_post( url, params, None, login_type = self.LOGIN_TYPE_NORMAL )
                if result is not None:
                    return result[ "result" ]
            except:
                LogUtil( ).error( "生成STAFF token出错！----" + traceback.format_exc( ) )

    def __read_accounts( self, env = "beta" ):
        '''
        读取全局账号
        :param env: 默认Beta环境
        :return:
        '''
        base_dir = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )
        file = os.path.join( os.path.join( os.path.realpath( base_dir ), "config" ), "account.yml" )  # 全局账号文件的绝对路径
        accounts = FileUtil( ).connect_to( file ).parsed_data
        return accounts

    def cal_signature( self, params ):
        '''
        生成MD5加密过的签名
        :param params: Dict格式
        :return:
        '''
        # 1.使用json解决传递的参数双引号会变成单引号问题。
        # 2.使用separators参数解决字典转json后有空白字符的问题。
        # 3.使用ensure_ascii=False解决中文会转成unicode的问题。
        try:
            if params == None:
                params = { }
            if (isinstance( params, dict )):
                params = json.dumps( params, ensure_ascii = False, separators = (',', ':') )
                content = str( params ) + self.__APP_ID + self.__APP_SECURITY
                m = hashlib.md5( )
                if (isinstance( content, str )):
                    m.update( content.encode( 'utf-8' ) )
                    return (m.hexdigest( )).upper( )
        except:
            LogUtil( ).error( "生成签名失败！----" + traceback.format_exc( ) )

    def cal_secret( self, token, crypto_type ):
        '''
        生成密钥
        :param token: token凭证
        :param crypto_type: 加密的类型
        :return:
        '''
        try:
            if (token == None or token == ""):
                token = self.__DEFAULT_TOKEN
            source_content = (token + self.__AES_BASE_KEY).encode( "utf-8" )
            sha_result = hashlib.sha256( source_content ).hexdigest( )
            if "AES" == crypto_type:
                key_length = 16
            elif "3DES" == crypto_type:
                key_length = 24
            else:
                return None
            return sha_result[ 0:key_length ]
        except:
            LogUtil( ).error( "生成密钥失败！----" + traceback.format_exc( ) )

    def AES_encrypt( self, content, secret ):
        '''
        使用AES-128算法加密
        :param content: 待加密内容
        :param secret:  密钥
        :return:
        '''
        BLOCK_SIZE = 16  # must be 16, 24, or 32 for AES。16（AES-128）、24（AES-192）、或32（AES-256）
        pad = lambda s: s + (BLOCK_SIZE - len( s ) % BLOCK_SIZE) * chr(
                BLOCK_SIZE - len( s ) % BLOCK_SIZE )  # 填充位数函数，填充成16位的倍数
        try:
            obj = AES.new( secret, AES.MODE_ECB )  # 使用密钥生成一个加密对象。
            crypt = obj.encrypt( pad( content ) )  # 加密
            return base64.b64encode( crypt ).decode( 'utf-8' )  # 最终生成base64编码的加密内容，并从byte类型decode回str
        except:
            LogUtil( ).error( "AES加密失败！----" + traceback.format_exc( ) )

    def AES_decrypt( self, content, secret ):
        '''
        使用AES-128算法解密
        :param content: 待解密内容，base64编码
        :param secret: 密钥
        :return:
        '''
        try:
            content = base64.b64decode( content )  # 先把base64编码内容转换成字节码
            obj = AES.new( secret, AES.MODE_ECB )  # 使用密钥生成一个加密对象。
            return obj.decrypt( content ).decode( 'utf-8' )  # 解密，并从byte类型decode回str
        except:
            LogUtil( ).error( "AES解密失败！----" + traceback.format_exc( ) )

    def DES3_encrypt( self, content, secret ):
        '''
        使用3DES算法加密
        :param content: 待加密内容
        :param secret: 密钥
        :return:
        '''

        BLOCK_SIZE = 8  # 3DES用8位填充
        pad = lambda s: s + (BLOCK_SIZE - len( s ) % BLOCK_SIZE) * chr(
                BLOCK_SIZE - len( s ) % BLOCK_SIZE )  # 填充函数

        try:
            encryptor = DES3.new( secret, DES3.MODE_ECB )  # 使用密钥生成一个加密对象
            crypt = encryptor.encrypt( pad( content ) )  # 加密
            return base64.b64encode( crypt ).decode( 'utf-8' )  # 最终生成base64编码的加密内容，并从byte类型decode回str
        except:
            LogUtil( ).error( "3DES加密失败！----" + traceback.format_exc( ) )

    def DES3_decrypt( self, content, secret ):
        '''
        使用3DES算法解密
        :param content: 待解密内容，base64编码
        :param secret: 密钥
        :return:
        '''
        try:
            content = base64.b64decode( content )  # 先把base64编码内容转换成字节码
            obj = DES3.new( secret, DES3.MODE_ECB )  # 使用密钥生成一个加密对象。
            return obj.decrypt( content ).decode( 'utf-8' )  # 解密，并从byte类型decode回str
        except:
            LogUtil( ).error( "3DES解密失败！----" + traceback.format_exc( ) )

    def http_post( self, url, params, token, login_type = LOGIN_TYPE_NORMAL, crypto_type = "3DES" ):
        '''
        http Post请求
        :param url: 请求url
        :param params: 请求参数，Dict类型
        :param login_type: token类型
        :param token: 登录的token
        :param crypto_type: 加密方式，AES、3DES。默认为3DES。
        :return: 返回解密后的response
        '''
        # 设置headers
        headers = { "content-type": "application/x-json", "x-client-appId": self.__APP_ID, "x-security-version": "2.0" }
        if crypto_type == "3DES":
            headers[ "x-client-fruit" ] = "mango"
        elif crypto_type == "AES":
            headers[ "x-client-fruit" ] = "watermelon"
        if login_type == self.LOGIN_TYPE_NORMAL:
            headers[ "x-client-type" ] = "app"
            headers[ "x-client-os" ] = "ios"
            headers[ "x-security-token" ] = token
        elif login_type == self.LOGIN_TYPE_SUPPLIER:
            headers[ "x-client-type" ] = "pc"
            headers[ "x-client-os" ] = "web"
            headers[ "x-supplier-token" ] = token
        elif login_type == self.LOGIN_TYPE_PMMANAGER or login_type == self.LOGIN_TYPE_MANAGER:
            headers[ "x-client-type" ] = "pc"
            headers[ "x-client-os" ] = "web"
            headers[ "x-manager-token" ] = token
        elif login_type == self.LOGIN_TYPE_STAFF:
            headers[ "x-client-type" ] = "app"
            headers[ "x-client-os" ] = "ios"
            headers[ "x-manager-token" ] = token

        # 设置请求内容
        if params == None:  # 没有入参时，重置为空字典
            params = { }
        LogUtil( ).info(
                "请求入参：====>" + json.dumps( params, ensure_ascii = False, separators = (',', ':') ) )
        signature = self.cal_signature( params )
        post_content = { "signature": signature, "params": params }
        if (isinstance( post_content, dict )):
            post_content = json.dumps( post_content, separators = (',', ':') )

            if (crypto_type == "AES"):
                # AES加密后的请求内容
                secret = self.cal_secret( token, "AES" )
                payload = self.AES_encrypt( post_content, secret )

                result = None
                # 发送HTTP Post请求
                try:
                    response = requests.post( url, data = payload, headers = headers )
                    # 解析HTTP响应
                    try:
                        if (response.status_code == 200):
                            json_temp = json.loads( response.text )
                            if (json_temp[ "msgCode" ] == 200):
                                decrypt_result = self.AES_decrypt( str( json_temp[ "data" ] ), secret )
                                s = re.compile( '[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]' ).sub( '', decrypt_result )
                                result = json.loads( s )
                                LogUtil( ).info( "解密结果：====>\n" + json.dumps( result, sort_keys = True,
                                                                              ensure_ascii = False,
                                                                              separators = (',', ':') ) )
                            else:
                                LogUtil( ).warning(
                                        "warning的请求入参：====>\n" + url + "  " + json.dumps( params, sort_keys = True,
                                                                                          ensure_ascii = False,
                                                                                          separators = (',', ':') ) )
                                LogUtil( ).warning( "msgCode不等于200：====>" + str( json_temp ) )
                                return json_temp
                        else:
                            LogUtil( ).error(
                                    "error的请求入参：====>\n" + url + "  " + json.dumps( params, sort_keys = True,
                                                                                    ensure_ascii = False,
                                                                                    separators = (',', ':') ) )
                            LogUtil( ).error( 'HTTP返回结果：=====>' + response.text )
                    except:
                        LogUtil( ).error(
                                "error的请求入参：====>\n" + url + "  " + json.dumps( params, sort_keys = True,
                                                                                ensure_ascii = False,
                                                                                separators = (',', ':') ) )
                        LogUtil( ).error( "解析AES响应失败!----" + traceback.format_exc( ) )
                except:
                    LogUtil( ).error(
                            "error的请求入参：====>\n" + url + "  " + json.dumps( params, sort_keys = True,
                                                                            ensure_ascii = False,
                                                                            separators = (',', ':') ) )
                    LogUtil( ).error( "http请求失败！----" + traceback.format_exc( ) )
                return result

            elif (crypto_type == "3DES"):
                # 3DES加密后的请求内容
                secret = self.cal_secret( token, "3DES" )
                payload = self.DES3_encrypt( post_content, secret )

                # 发送HTTP Post请求
                try:
                    response = requests.post( url, data = payload, headers = headers )
                    # 解析HTTP响应
                    result = None
                    try:
                        if (response.status_code == 200):
                            json_temp = json.loads( response.text )
                            if (json_temp[ "msgCode" ] == 200):
                                decrypt_result = self.DES3_decrypt( str( json_temp[ "data" ] ), secret )
                                s = re.compile( '[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]' ).sub( '',
                                                                                             decrypt_result )  # 过滤返回结果的转义字符
                                result = json.loads( s )
                                LogUtil( ).info(
                                        "解密结果：====>\n" + json.dumps( result, sort_keys = True, ensure_ascii = False,
                                                                     separators = (',', ':') ) )
                            else:
                                LogUtil( ).warning(
                                        "warning的请求入参：====>\n" + url + "  " + json.dumps( params, sort_keys = True,
                                                                                          ensure_ascii = False,
                                                                                          separators = (',', ':') ) )
                                LogUtil( ).warning( "msgCode不等于200：====>" + str( json_temp ) )
                                return json_temp
                        else:
                            LogUtil( ).error(
                                    "error的请求入参：====>\n" + url + "  " + json.dumps( params, sort_keys = True,
                                                                                    ensure_ascii = False,
                                                                                    separators = (',', ':') ) )
                            LogUtil( ).error( 'HTTP返回结果：=====>' + response.text )
                    except:
                        LogUtil( ).error(
                                "error的请求入参：====>\n" + url + "  " + json.dumps( params, sort_keys = True,
                                                                                ensure_ascii = False,
                                                                                separators = (',', ':') ) )
                        LogUtil( ).error( "解析3DES响应失败!----" + traceback.format_exc( ) )
                    return result
                except:
                    LogUtil( ).error(
                            "error的请求入参：====>\n" + url + "  " + json.dumps( params, sort_keys = True,
                                                                            ensure_ascii = False,
                                                                            separators = (',', ':') ) )
                    LogUtil( ).error( "http请求失败！----" + traceback.format_exc( ) )
        else:
            return "请求参数必须是Dict类型!"
