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

def test_query_coupon_detail( ):
    '''
    正常查询优惠券详情
    :return:
    '''
    params = test_data[ "case1" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ][ "couponEntity" ][ "couponId" ] == test_data[ "case1" ][ "params" ][ "couponId" ]
