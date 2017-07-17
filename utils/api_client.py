#!/usr/bin/env python
# coding=UTF-8
'''
# Desc：调用Http Json协议的接口。根据自己公司情况修改http_post方法。
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
from  utils.base import ENV, ACCOUNTS


class APIClient:
    """
    HTTP Json协议接口的调用，token、签名、加密、解密。
    """
    __instance = None
    NORMAL_TOKEN = None  # 业主端，默认账号
    NORMAL_TOKEN_XIAOMEI = None  # 业主端，小梅。
    NORMAL_TOKEN_YAOYAO = None  # 业主端，瑶瑶
    NORMAL_TOKEN_XIAOAI = None  # 业主端，小爱
    SUPPLIER_TOKEN = None  # 供应商，默认账号
    MANAGER_TOKEN = None  # 运营后台，默认账号
    PMMANAGER_TOKEN = None  # 物业后台，默认账号
    STAFF_TOKEN = None  # 员工端，默认账号

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
        self.__AES_BASE_KEY = "XXXX"
        self.__APP_ID = "XXXX"
        self.__APP_SECURITY = "XXXX"
        self.__DEFAULT_TOKEN = "XXXX"

        self.__LOGIN_TYPE_NORMAL = "NORMAL"  # 业主端
        self.__LOGIN_TYPE_SUPPLIER = "SUPPLIER"  # 电商商家端
        self.__LOGIN_TYPE_MANAGER = "MANAGER"  # 运营后台
        self.__LOGIN_TYPE_PMMANAGER = "PMMANAGER"  # 物业后台
        self.__LOGIN_TYPE_STAFF = "STAFF"  # 员工端

        self.NORMAL_TOKEN = self.__cal_different_account( ENV, self.LOGIN_TYPE_NORMAL )
        # self.NORMAL_TOKEN_XIAOMEI = self.__cal_different_account( ENV, self.LOGIN_TYPE_NORMAL,
        #                                                           tester_account = "XIAOMEI" )
        self.NORMAL_TOKEN_YAOYAO = self.__cal_different_account( ENV, self.LOGIN_TYPE_NORMAL,
                                                                 tester_account = "YAOYAO" )
        self.NORMAL_TOKEN_XIAOAI = self.__cal_different_account( ENV, self.LOGIN_TYPE_NORMAL,
                                                                 tester_account = "XIAOAI" )
        self.SUPPLIER_TOKEN = self.__cal_different_account( ENV, self.LOGIN_TYPE_SUPPLIER )
        self.MANAGER_TOKEN = self.__cal_different_account( ENV, self.LOGIN_TYPE_MANAGER )
        self.PMMANAGER_TOKEN = self.__cal_different_account( ENV, self.LOGIN_TYPE_PMMANAGER )
        self.STAFF_TOKEN = self.__cal_different_account( ENV, self.LOGIN_TYPE_STAFF )

    def __cal_different_account( self, env = ENV, login_type = "", tester_account = "default" ):
        '''
        生成账号
        :param env: 
        :param login_type: 
        :param tester_account: 
        :return: 
        '''
        accounts = ACCOUNTS
        if accounts:
            if tester_account == "default":  # 默认账号
                return self.cal_token( accounts[ env ][ login_type ][ "user_name" ],
                                       accounts[ env ][ login_type ][ "password" ], login_type, env )
            else:  # tester自己的账号，自己写的用例，用自己的token，例子 ：api_client.NORMAL_TOKEN_YAOYAO
                return self.cal_token(
                    accounts[ env ][ self.LOGIN_TYPE_NORMAL + "_{}".format( tester_account ) ][ "user_name" ],
                    accounts[ env ][ self.LOGIN_TYPE_NORMAL + "_{}".format( tester_account ) ][ "password" ],
                    login_type, env )

    @property
    def LOGIN_TYPE_NORMAL( self ):
        return self.__LOGIN_TYPE_NORMAL

    @property
    def LOGIN_TYPE_SUPPLIER( self ):
        return self.__LOGIN_TYPE_SUPPLIER

    @property
    def LOGIN_TYPE_MANAGER( self ):
        return self.__LOGIN_TYPE_MANAGER

    @property
    def LOGIN_TYPE_PMMANAGER( self ):
        return self.__LOGIN_TYPE_PMMANAGER

    @property
    def LOGIN_TYPE_STAFF( self ):
        return self.__LOGIN_TYPE_STAFF

    def cal_url( self, project_name, api_name, env = ENV ):
        '''
        生成最终请求的url
        :param env: 环境，beta、fix
        :param project_name:工程名称
        :param api_name:接口名
        :return:
        '''
        env_url = { "beta": "test", "fix": "fix", "stress": "stress" }
        if api_name.startswith( "/" ):
            api_name = api_name[ 1: ]
        return "http://" + env_url[ env ] + "." + project_name + "-api.hd/" + api_name

    def cal_token( self, username, password, login_type = "NORMAL", env = ENV ):
        '''
        生成token
        :param username: 用户名
        :param password: 密码
        :param login_type: 业主端：NORMAL，供应商：SUPPLIER，运营后台：MANAGER。物业后台：PMMANAGER。
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
                LogUtil().error( "生成NORMAL token出错！----" + traceback.format_exc() )
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
                LogUtil().error( "生成SUPPLIER token出错！----" + traceback.format_exc() )
        # 运营后台：MANAGER
        elif login_type == self.LOGIN_TYPE_MANAGER:
            params = { "username": username, "password": password, "systemType": 2 }
            url = self.cal_url( "sys-sso", "systemSso/loginSys", env )
            try:
                result = self.http_post( url, params, None, login_type = login_type )
                if result is not None:
                    return result[ "result" ]
            except:
                LogUtil().error( "生成MANAGER token出错！----" + traceback.format_exc() )
        # 物业后台：PMMANAGER
        elif login_type == self.LOGIN_TYPE_PMMANAGER:
            params = { "username": str( username ), "password": str( password ), "systemType": 1 }
            url = self.cal_url( "sys-sso", "systemSso/loginSys", env )
            try:
                result = self.http_post( url, params, None, login_type = login_type )
                if result is not None:
                    return result[ "result" ]
            except:
                LogUtil().error( "生成PMMANAGER token出错！----" + traceback.format_exc() )
        # 员工端：STAFF
        elif login_type == self.LOGIN_TYPE_STAFF:
            params = { "username": str( username ), "password": str( password ) }
            url = self.cal_url( "sys-sso", "systemSso/login", env )
            try:
                result = self.http_post( url, params, None, login_type = self.LOGIN_TYPE_NORMAL )
                if result is not None:
                    return result[ "result" ]
            except:
                LogUtil().error( "生成STAFF token出错！----" + traceback.format_exc() )

    def cal_signature( self, params ):
        '''
        生成MD5加密过的签名
        :param params: Dict格式
        :return:
        '''
        try:
            if params == None:
                params = { }
            if (isinstance( params, dict )):
                params = json.dumps( params, ensure_ascii = False, separators = (',', ':') )
                content = str( params ) + self.__APP_ID + self.__APP_SECURITY
                m = hashlib.md5()
                if (isinstance( content, str )):
                    m.update( content.encode( 'utf-8' ) )
                    return (m.hexdigest()).upper()
        except:
            LogUtil().error( "生成签名失败！----" + traceback.format_exc() )

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
            sha_result = hashlib.sha256( source_content ).hexdigest()
            if "AES" == crypto_type:
                key_length = 16
            elif "3DES" == crypto_type:
                key_length = 24
            else:
                return None
            return sha_result[ 0:key_length ]
        except:
            LogUtil().error( "生成密钥失败！----" + traceback.format_exc() )

    def encrypt( self, content, secret, crypto_type ):
        '''
        加密
        :param content: 待加密内容
        :param secret: 密钥
        :param crypto_type: 加密类型
        :return:
        '''
        if crypto_type == "AES":
            BLOCK_SIZE = 16
            pad = lambda s: s + (BLOCK_SIZE - len( s ) % BLOCK_SIZE) * chr(
                BLOCK_SIZE - len( s ) % BLOCK_SIZE )
            try:
                obj = AES.new( secret, AES.MODE_ECB )
                crypt = obj.encrypt( pad( content ) )
                return base64.b64encode( crypt ).decode( 'utf-8' )
            except:
                LogUtil().error( "AES加密失败！----" + traceback.format_exc() )
        elif crypto_type == "3DES":
            BLOCK_SIZE = 8
            pad = lambda s: s + (BLOCK_SIZE - len( s ) % BLOCK_SIZE) * chr(
                BLOCK_SIZE - len( s ) % BLOCK_SIZE )

            try:
                encryptor = DES3.new( secret, DES3.MODE_ECB )
                crypt = encryptor.encrypt( pad( content ) )
                return base64.b64encode( crypt ).decode( 'utf-8' )
            except:
                LogUtil().error( "3DES加密失败！----" + traceback.format_exc() )

    def decrypt( self, content, secret, crypto_type ):
        '''
        解密
        :param content: 待加密内容
        :param secret: 密钥
        :param crypto_type: 加密类型
        :return:
        '''
        if crypto_type == "AES":
            try:
                content = base64.b64decode( content )
                obj = AES.new( secret, AES.MODE_ECB )
                return obj.decrypt( content ).decode( 'utf-8' ).strip()
            except:
                LogUtil().error( "AES解密失败！----" + traceback.format_exc() )
        elif crypto_type == "3DES":
            try:
                content = base64.b64decode( content )
                obj = DES3.new( secret, DES3.MODE_ECB )
                return obj.decrypt( content ).decode( 'utf-8' ).strip()
            except:
                LogUtil().error( "3DES解密失败！----" + traceback.format_exc() )

    def http_post( self, url, params, token, login_type = "NORMAL", crypto_type = "3DES" ):
        '''
        http Post请求
        :param url: 请求url
        :param params: 请求参数，Dict类型
        :param login_type: token类型
        :param token: 登录的token
        :param crypto_type: 加密方式，
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
        signature = self.cal_signature( params )
        post_content = { "signature": signature, "params": params }
        if (isinstance( post_content, dict )):
            LogUtil().info( "请求入参：====>" + json.dumps( post_content, sort_keys = True,
                                                       ensure_ascii = False,
                                                       separators = (',', ':') ) )
            post_content = json.dumps( post_content, separators = (',', ':') )
            # 加密后的请求内容
            secret = self.cal_secret( token, crypto_type )
            payload = self.encrypt( post_content, secret, crypto_type )

            result = None
            # 发送HTTP Post请求
            try:
                response = requests.post( url, data = payload, headers = headers )
                # 解析HTTP响应
                try:
                    if (response.status_code == 200):
                        json_temp = json.loads( response.text )
                        if (json_temp[ "msgCode" ] == 200):
                            decrypt_result = self.decrypt( str( json_temp[ "data" ] ), secret, crypto_type )
                            s = re.compile( '[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]' ).sub( '', decrypt_result )
                            result = json.loads( s )
                            LogUtil().info( "解密结果：====>\n" + json.dumps( result, sort_keys = True,
                                                                         ensure_ascii = False,
                                                                         separators = (',', ':') ) )
                        else:
                            LogUtil().warning(
                                "warning的请求入参：====>\n" + url + "  " + json.dumps( params, sort_keys = True,
                                                                                  ensure_ascii = False,
                                                                                  separators = (',', ':') ) )
                            LogUtil().warning( "msgCode不等于200：====>" + str( json_temp ) )
                            return json_temp
                    else:
                        LogUtil().error(
                            "error的请求入参：====>\n" + url + "  " + json.dumps( params, sort_keys = True,
                                                                            ensure_ascii = False,
                                                                            separators = (',', ':') ) )
                        LogUtil().error( 'HTTP返回结果：=====>' + response.text )
                except:
                    LogUtil().error(
                        "error的请求入参：====>\n" + url + "  " + json.dumps( params, sort_keys = True,
                                                                        ensure_ascii = False,
                                                                        separators = (',', ':') ) )
                    LogUtil().error( "解析'{}'密文失败!----".format( crypto_type ) + traceback.format_exc() )
            except:
                LogUtil().error(
                    "error的请求入参：====>\n" + url + "  " + json.dumps( params, sort_keys = True,
                                                                    ensure_ascii = False,
                                                                    separators = (',', ':') ) )
                LogUtil().error( "http请求失败！----" + traceback.format_exc() )
            return result
        else:
            return "请求参数必须是Dict类型!"
