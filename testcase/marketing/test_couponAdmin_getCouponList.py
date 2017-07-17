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

def test_query_with_default_params():
    '''
    默认参数查询管理列表
    :return:
    '''
    params = test_data[ "case1" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ][ "queryData" ][ "pageSize" ] == test_data[ "case1" ][ "params" ][ "pageSize" ]
    # 数据库结果条数与查询结果条数比较
    mysql_util.query( test_data[ "case1" ][ "verify_sql" ] )
    sql_result_count = mysql_util.fetchOneRow()[ 0 ]
    if sql_result_count > result[ "result" ][ "queryData" ][ "pageSize" ]:
        data_list_count = result[ "result" ][ "queryData" ][ "pageSize" ]
        assert data_list_count == result[ "result" ][ "queryData" ][ "pageSize" ]
    else:
        data_list_count = sql_result_count
        assert data_list_count == len( result[ "result" ][ "queryData" ][ "dataList" ] )


def test_query_approve_list_with_listType():
    '''
    使用listType查询审批列表
    :return:
    '''
    params = test_data[ "case2" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    # 数据库结果条数与查询结果条数比较
    mysql_util.query( test_data[ "case2" ][ "verify_total_count_sql" ] )
    total_count = mysql_util.fetchOneRow()[ 0 ]
    assert total_count == result[ "result" ][ "queryData" ][ "totalCount" ]

    mysql_util.query( test_data[ "case2" ][ "verify_been_approval_count_sql" ] )
    been_approval_count = mysql_util.fetchOneRow()[ 0 ]
    assert been_approval_count == result[ "result" ][ "approvalCount" ]

    mysql_util.query( test_data[ "case2" ][ "verify_not_approval_count_sql" ] )
    not_approval_count = mysql_util.fetchOneRow()[ 0 ]
    assert not_approval_count == result[ "result" ][ "notApprovalCount" ]


def test_pageSize_and_currentPage():
    '''
    pageSize&currentPage分页参数起作用
    :return:
    '''
    params = test_data[ "case3" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ][ "queryData" ][ "pageSize" ] == test_data[ "case3" ][ "params" ][ "pageSize" ]
    assert result[ "result" ][ "queryData" ][ "currPage" ] == test_data[ "case3" ][ "params" ][ "currentPage" ]


def test_CouponEntity_useScope():
    '''
    CouponEntity的useScope起作用
    :return:
    '''
    params = test_data[ "case4" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    mysql_util.query( test_data[ "case4" ][ "verify_sql" ] )
    total_count = mysql_util.fetchOneRow()[ 0 ]
    assert total_count == result[ "result" ][ "queryData" ][ "totalCount" ]


def test_CouponEntity_status():
    '''
    CouponEntity的status起作用
    :return:
    '''
    params = test_data[ "case5" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    mysql_util.query( test_data[ "case5" ][ "verify_sql" ] )
    total_count = mysql_util.fetchOneRow()[ 0 ]
    assert total_count == result[ "result" ][ "queryData" ][ "totalCount" ]


def test_CouponEntity_couponName():
    '''
    CouponEntity的couponName起作用
    :return:
    '''
    params = test_data[ "case6" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ][ "queryData" ][ "dataList" ][ 0 ][ "couponName" ] == \
           test_data[ "case6" ][ "params" ][ "param" ][
               "couponName" ]
    mysql_util.query( test_data[ "case6" ][ "verify_sql" ] )
    total_count = mysql_util.fetchOneRow()[ 0 ]
    assert result[ "result" ][ "queryData" ][ "totalCount" ] == total_count


def test_CouponEntity_couponName_not_exsit():
    '''
    CouponEntity的couponName不存在或错误
    :return:
    '''
    params = test_data[ "case7" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ][ "queryData" ][ "totalCount" ] == 0
    assert len( result[ "result" ][ "queryData" ][ "dataList" ] ) == 0


def test_CouponEntity_couponId():
    '''
    CouponEntity的couponId起作用
    :return:
    '''
    params = test_data[ "case8" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ][ "queryData" ][ "dataList" ][ 0 ][ "couponId" ] == \
           test_data[ "case8" ][ "params" ][ "param" ][ "couponId" ]


def test_CouponEntity_couponId_not_exist():
    '''
    CouponEntity的couponId不存在
    :return:
    '''
    params = test_data[ "case9" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ][ "queryData" ][ "totalCount" ] == 0
    assert len( result[ "result" ][ "queryData" ][ "dataList" ] ) == 0


def test_CouponEntity_not_exist():
    '''
    CouponEntity对应的查询参数，若不存在，则返回为空
    :return:
    '''
    params = test_data[ "case10" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ][ "queryData" ][ "totalCount" ] == 0
    assert len( result[ "result" ][ "queryData" ][ "dataList" ] ) == 0


def test_CouponEntity_combine_params():
    '''
    CouponEntity组合查询各参数
    :return:
    '''
    params = test_data[ "case11" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    mysql_util.query( test_data[ "case11" ][ "verify_sql" ] )
    total_count = mysql_util.fetchOneRow()[ 0 ]
    assert total_count == result[ "result" ][ "queryData" ][ "totalCount" ]


def test_CouponEntity_couponId_cannot_be_decimals():
    '''
    CouponEntity的couponId不能是小数
    :return:
    '''
    params = test_data[ "case12" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ][ "queryData" ][ "totalCount" ] == 0


def test_CouponEntity_couponId_cannot_be_string():
    '''
    CouponEntity的couponId不能是字符串
    :return:
    '''
    params = test_data[ "case13" ][ "params" ]
    result = api_client.http_post( url, params, api_client.MANAGER_TOKEN, api_client.LOGIN_TYPE_MANAGER )

    assert result[ "result" ][ "queryData" ][ "totalCount" ] == 0
