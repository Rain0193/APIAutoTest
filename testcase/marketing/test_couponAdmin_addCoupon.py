#!/usr/bin/env python
# coding=UTF-8
'''
 # Desc：
 # Author：TavisD 
 # Time：2017-2-22 10:32
 # Ver：V1.0
'''
import os, pytest
from utils import api_client, file_util, gen_util, mysql_util

test_data, yml_file_path = file_util.get_test_data_by_name( os.path.abspath( __file__ ) )  # 获取测试数据、测试数据的文件名
url = api_client.cal_url( test_data[ "project_name" ], test_data[ "api_name" ] )  # 生成接口URL


######------------------------以上，每个py文件都一样。----------------------######


def test_add_business_coupon():
    '''
    创建业务券成功-基本流程
    :return:
    '''
    params = test_data[ "case1" ][ "params" ]
    mysql_util.update( test_data[ "case1" ][ "init_sql1" ] )
    mysql_util.query( test_data[ "case1" ][ "init_sql2" ] )
    if mysql_util.getRowCount():
        coupon_code_id = mysql_util.fetchOneRow()[ 0 ]
        delete_sql = test_data[ "case1" ][ "init_sql3" ]
        mysql_util.update( delete_sql.format( coupon_code_id ) )
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ] == True


def test_add_merchant_coupon():
    '''
    创建商家券成功-基本流程
    :return:
    '''
    params = test_data[ "case2" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ] == True


def test_add_diff_business_coupon():
    '''
    创建不同的业务券成功
    :return:
    '''
    params = test_data[ "case2" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ] == True
