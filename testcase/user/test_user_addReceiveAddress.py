#!/usr/bin/env python
# coding=UTF-8
'''
 # Desc：
 # Author：TavisD 
 # Time：2017-2-22 10:32
 # Ver：V1.0
'''

import os
import sys
import pytest

sys.path.append( os.path.dirname( os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ) ) )
from utils.api_client import APIClient
from utils.file_util import FileUtil
from utils.mysql_util import MysqlUtil
from utils.gen_util import GenUtil

api_client = APIClient( )  # 接口核心类实例
file_util = FileUtil( )  # 文件类实例
mysql_util = MysqlUtil( )  # 操作数据库类实例
gen_util = GenUtil( )  # 生成测试数据类实例
test_data, yml_file_path = file_util.get_test_data_by_name( os.path.abspath( __file__ ) )  # 获取测试数据、测试数据的文件名
url = api_client.cal_url( test_data[ "project_name" ], test_data[ "api_name" ] )  # 生成接口URL


######------------------------以上，每个py文件都一样。----------------------######



def test_add_normal_address( ):  # 对应的测试数据的名字与它一样
    '''
    使用正常数据添加收货地址
    :return:
    '''
    params = test_data[ "case1" ][ "params" ]  # 入参
    result = api_client.http_post( url, params, api_client.NORMAL_TOKEN )  # 发送请求，并拿到返回值
    assert result[ "result" ][ "consignee" ] == test_data[ "case1" ][ "verify1" ]  # 断言校验
    assert result[ "result" ][ "mobile" ] == test_data[ "case1" ][ "verify2" ]  # 断言校验


# def test_add_normal_address( ):  # 对应的测试数据的名字与它一样
#     '''
#     使用正常数据添加收货地址
#     :return:
#     '''
#     # 当我们使用动态生成测试数据时：
#     # 1.把入参及对应的校验点改成动态生成的数据。
#     # 2.为了跟踪测试时用了什么测试数据，所以把测试数据保存下。
#     test_data[ "case1" ][ "verify1" ] = test_data[ "case1" ][ "params" ][ "model" ][
#         "consignee" ] = gen_util.gen_chinese_name( )
#     test_data[ "case1" ][ "params" ][ "model" ][ "mobile" ] = test_data[ "case1" ][ "verify2" ] = gen_util.gen_phones( )
#     file_util.save_test_data_by_name( yml_file_path, test_data )
#
#     params = test_data[ "case1" ][ "params" ]  # 入参
#     result = api_client.http_post( url, params, api_client.NORMAL_TOKEN )  # 发送请求，并拿到返回值
#     assert result[ "result" ][ "consignee" ] == test_data[ "case1" ][ "verify1" ]  # 断言校验
#     assert result[ "result" ][ "mobile" ] == test_data[ "case1" ][ "verify2" ]  # 断言校验


@pytest.mark.skip  # 若自动化时，觉得不需要该用例，可以跳过
def test_add_address_using_special_symbol( ):
    '''
    使用特殊符号、空格添加收货地址
    :return:
    '''
    params = test_data[ "case2" ][ "params" ]
    result = api_client.http_post( url, params, api_client.NORMAL_TOKEN )
    assert result[ "result" ] != None


# @pytest.mark.skip  # 若自动化时，觉得不需要该用例，可以跳过
def test_add_max_address( ):
    '''
    超出最大地址条数，手动测试后，自动化时只检验busCode，不校验条数。
    :return:
    '''
    params = test_data[ "case3" ][ "params" ]
    while True:
        result = api_client.http_post( url, params, api_client.NORMAL_TOKEN )
        if "busCode" in result.keys( ):
            assert result[ "busCode" ] == test_data[ "case3" ][ "verify" ]
            sql = test_data[ "case3" ][ "teardown" ]
            mysql_util.update( sql )
            break
        else:
            assert result[ "result" ] != None
