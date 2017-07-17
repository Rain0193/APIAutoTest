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

def test_query_coupon_detail():
    '''
    正常查询优惠券详情
    :return:
    '''
    params = test_data[ "case1" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ][ "couponEntity" ][ "couponId" ] == test_data[ "case1" ][ "params" ][ "couponId" ]
