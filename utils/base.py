#!/usr/bin/env python
# coding=UTF-8
'''
 # Desc：
 # Author：TavisD 
 # Time：2017-7-13 14:01
 # Ver：V1.0
'''

import os
import sys

sys.path.append( os.path.dirname( os.path.abspath( __file__ ) ) )
from file_util import FileUtil


def __read_config( ):
    base_dir = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )
    settings_file = os.path.join( os.path.join( os.path.realpath( base_dir ), "config" ),
                                  "settings.yml" )  # 全局配置文件的绝对路径
    account_file = os.path.join( os.path.join( os.path.realpath( base_dir ), "config" ),
                                 "account.yml" )
    db_file = os.path.join( os.path.join( os.path.realpath( base_dir ), "config" ), "db.yml" )
    settings = FileUtil( ).connect_to( settings_file ).parsed_data
    accounts = FileUtil( ).connect_to( account_file ).parsed_data
    db = FileUtil( ).connect_to( db_file ).parsed_data
    ENV = settings[ "env" ]
    LOG_SWITCH = settings[ "log_switch" ]
    LOG_LEVEL = settings[ "log_level" ]
    PRINT_SWITCH = settings[ "print_switch" ]
    return ENV, LOG_SWITCH, accounts, db, LOG_LEVEL, PRINT_SWITCH


ENV, LOG_SWITCH, ACCOUNTS, DB, LOG_LEVEL, PRINT_SWITCH = __read_config( )
