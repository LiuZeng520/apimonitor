#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
公共配置文件
"""


import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


city = 'bj'

TIMEOUT = 3  # 一级超时时间
TIMEOUT_R = (10, 10)

# TIMEOUT = 3  # 一级超时时间
# TIMEOUT_R = (50, 50)

# 测试失败类型定义
SUCC_ISSUE = u'请求正常'
FAILED_REQ = u'请求失败'
FAILED_OUT = u'请求超时'
FAILED_HARDOUT = u'请求严重超时'
FAILED_EXC = u'运行时异常'
FAILED_BAD = u'请求状态码'
ASSERT_BAD = u'断言失败'


Bad_URL = ''  # 请求失败的URL
index = ''  # 循环次数
DEBUG = False
DebugURL = ''
urllist = []
badlist = []
# 标识是否存在异常
hasError = False
# 标记是否超时
isTimeout = False
# 标识本次请求已经完成
hasRespond = False
# 标记JsonData是否可用
isAvailed = False
# 标记程序运行是否
hasException = False
# 404标记
isBadReq = False
# 失败的URL

total_low = 50
# 累计初级次数
total_medium = 70
# 累计中级次数
total_high = 90
# 累计高级次数

ADDUP = 5
# 连续报警次数


base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
error_log_path = base_path + '/logs/error.log'
requests_log_path = base_path + '/logs/requests.log'
logger_log_path = base_path + '/logs/logger.log'

sqlite_path = base_path + '/sqlite/api.sqlite'


total_low = 50
# 累计初级次数
total_medium = 70
# 累计中级次数
total_high = 90
# 累计高级次数

mail_sub = "线上接口异常报警"
mail_user = ''
mail_postfix = ''
mail_host = ''
mail_pass = ''


server_host = '127.0.0.1'
server_port = 5000

lanuch_server_time = 5

es_index_name = 'api_index'
es_server_host = '192.168.1.232'
es_server_port = 9200

mysql_connect = 'mysql://xxxx:xxxxx@49.234.104.160:3306/qacenter?charset=utf8mb4'

is_debug = True

interval_time = 10

