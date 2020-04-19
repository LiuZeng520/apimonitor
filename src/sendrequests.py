#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
请求类
"""

import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import time
import requests
import common
from config import *
from logzero import logger
import grequests
from esuntils import EsUntils


request_count = 0


def get_result(interface_name,url,method,header,response,assert_params,issue,status_code,usd_time,time_stamp):
    """
    :param interface_name:
    :param url:
    :param method:
    :param header:
    :param response:
    :param assert_params:
    :param issue:
    :param status_code:
    :param usd_time:
    :param time_stamp:
    :return:
    """

    return {
        'interface_name': interface_name,
        'url': url,
        'method': method,
        'header': header,
        'response': response,
        'assert_params': assert_params,
        'issue': issue,
        'status_code': str(status_code),
        'usd_time': str(usd_time),
        'time_stamp': time_stamp
        }




def common_requests(**kwargs):
    """
    # 封装通用get/post请求
    :param kwargs:
    :return:
    """
    try:
        url = kwargs['URL']
        header = kwargs['Header']
        params = kwargs['Params']
        Method = kwargs['Method']
        global req
        if Method == 'GET' and url != None:
            req = requests.get(url, headers=header, params=params, allow_redirects=False, verify=False,
                               timeout=TIMEOUT_R)
            logger.info("请求接口地址 ==> {}".format(req.url))

        elif Method == 'POST' and url != None:
            req = requests.post(url, headers=header, data=params, allow_redirects=False, verify=False,
                                timeout=TIMEOUT_R)
        else:
            logger.error("请求方法类型错误")

        logger.debug(req.json())
        return req.json()

    except Exception, e:
        logger.error("请求异常 ==> {}".format(e))
        return e


@common.record_time()
def main_requests(**kwargs):
    """
    封装一级接口请求的方法
    :param url: 请求接口地址
    :param Header: 请求头
    :param Params: 请求参数 或者 请求body
    :param Method: 请求类型
    :param Interface_name: 请求接口名字
    :return: 请求成功插入t_succurl表中
    :return: 请求失败插入t_errorurl表中
    """

    is_availed = False
    has_error = False
    has_respond = False
    has_exception = False
    is_availed = False
    response = {}
    result = {}
    req_url = ''
    issue = ''
    req_code = 0
    usd_time = 0
    time_stamp = ''
    req = ''

    global request_count


    try:

        url = kwargs['url']
        header = kwargs['header']
        params = kwargs['params']
        method = kwargs['method']
        interface_name = kwargs['interface_name']
        assert_params = kwargs['assert_params']

        r = requests.session()

        logger.info("请求接口 ==> {}".format(req_url))

        if method == 'get' or method == 'GET' and url != None:
            req = r.get(url, headers=header,params=params,allow_redirects=False, verify=False,
                               timeout=TIMEOUT_R)

        elif method == 'post' or method == 'POST' and url != None:
            req = r.post(url, headers=header, data=params, allow_redirects=False, verify=False,
                                timeout=TIMEOUT_R)

        request_count = request_count + 1
        req_code = req.status_code
        req_url = req.url
        time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        usd_time = float(str(req.elapsed).split(':')[-1])

        logger.info("当前请求次数 ==> {}".format(request_count))

        if req_code == 200 and usd_time < float(TIMEOUT):
            logger.info('正常请求 ==> ')
            try:
                try:
                    response = req.json()
                except Exception as e:
                    logger.error("获取接口响应异常 ==> {}".format(e))
                    response = {}

                issue = SUCC_ISSUE
                is_availed = True
                has_respond = True

                #TODO 增加接口断言

            except Exception as e:
                logger.error(e)
                common.save_error_log(error_log_path, common.get_current_time(), e, url)


        elif req_code == 200 and usd_time >= float(TIMEOUT):

            logger.info('请求超时 ==>')

            try:
                response = req.json()
            except Exception as e:
                logger.error("获取接口响应异常 ==> {}".format(e))
                response = {}

            issue = FAILED_OUT
            has_error = True


        elif req_code > 200:
            logger.info(' code码非200 ==>')
            issue = FAILED_BAD + str(req_code)
            has_error = True

    except Exception as e:

        logger.error("请求异常 ==> {}".format(e))
        common.save_error_log(error_log_path, common.get_current_time(), e, url)

        if 'Read timed out' in str(e):
            issue = FAILED_HARDOUT
            has_error = True


    finally:

        common.save_request_log(requests_log_path,json.dumps(result))
        result = get_result(interface_name, req_url, method, json.dumps(header), json.dumps(response),
                            json.dumps(assert_params), issue, req_code,usd_time,time_stamp)
        async_insert_result(result)
        common.sublist = []
        # 重置二级接口列表
        sub_url_list = common.get_url_list(response)

        if sub_url_list != None:

            for url in sub_url_list:
                logger.info("递归请求接口 ==> {}".format(url))
                sub_urllist = main_requests(method=method,
                                            interface_name=interface_name,
                                            url=url,
                                            header=header,
                                            params=params,
                                            assert_params=assert_params)






def async_insert_result(result):
    """
    异步请求
    :param result:
    :return:
    """
    req_list = [ grequests.post('http://{}:{}/add'.format(server_host,server_port),json=result)  ]
    res_list = grequests.map(req_list)
    logger.info('异步插入数据完成 ==> {}'.format(res_list[0].text))

    EsUntils(es_index_name).insert(result)






