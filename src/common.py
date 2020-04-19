#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
工具类
"""

import time
import os
import json
import re
import urllib
import xlrd
import xlwt
import requests
from xlutils.copy import copy
from BeautifulSoup import BeautifulSoup
import platform
import datetime
from logzero import logger
from config import *



def record_time():
    def decorator(func):
        def wrapper(*args, **kw):
            logger.info('接口请求开始时间:{}'.format(datetime.datetime.now()))
            f = func(*args, **kw)
            logger.info('接口请求结束时间:{}'.format(datetime.datetime.now()))
            return f
        return wrapper
    return decorator



def save_request_log(file_path, result):
    """
    保存程序异常数据log日志
    :param file_ename: 文件名
    :param happen_time:发生时间
    :param error:具体错误信息
    :param url:错误url地址
    :return: 返回1,写入成功
    :return: 返回0,写入失败
    """

    is_success = False

    try:
        with open(file_path, 'a') as f:
            f.write(result)
            f.write('\n')
        return True
    except Exception as e:
        logger.error('保存{}失败!'.format(file_path))
        logger.error(e)
        return is_success


def save_error_log(file_path, happen_time, error, url):
    """
    保存程序异常数据log日志
    :param file_ename: 文件名
    :param happen_time:发生时间
    :param error:具体错误信息
    :param url:错误url地址
    :return: 返回1,写入成功
    :return: 返回0,写入失败
    """

    is_success = False

    try:
        with open(file_path, 'a') as f:
            f.write('发生时间: ' + happen_time + '\n')
            f.write('错误原因: ' + str(error) + '\n')
            f.write('接口地址: ' + url + '\n')
        return True
    except Exception as e:
        logger.error('保存{}失败!'.format(file_path))
        return is_success



def read_sheet(file_path, sheet_name):
    """
    读取excel文件某个sheet表的数据,把所有数据加到list中
    :param filepath: 文件名
    :param sheetname:sheet的名字
    :return: 返回list
    """

    is_success = False

    try:
        case_list = []
        # 文件位置
        excel_file = xlrd.open_workbook(file_path)
        # sheet名字
        sheet = excel_file.sheet_by_name(sheet_name)
        # 打印sheet的名称，行数，列数
        for index in range(sheet.nrows):
            if index != 0:
                case_list.append(sheet.row_values(index))
        return case_list
    except Exception, e:
        logger.error(e)
        return is_success


def read_excel(file_path):
    """
    读取excel文件,查找有几个sheet,加到list中
    :param filepath: 文件名
    :return: 返回list
    """
    try:
        sheetlist = []
        excel_file = xlrd.open_workbook(file_path)
        # print ExcelFile.sheet_names()
        for index in excel_file.sheet_names():
            if isinstance(index, unicode):
                sheetlist.append(index.encode('utf-8'))
        return sheetlist
    except Exception, e:
        logger.error(e)



def get_caases(file_path):
    """
    循环读取excel表中每个sheet表中的数据
    :param filepath: 文件名
    :return: 返回Caselist
    """
    case_list = []  # Case个数
    for sheet in read_excel(file_path):
        read_case_list = read_sheet(file_path, sheet)
        for case in read_case_list:
            case_list.append(case)
    return case_list



def write_excel(file_path):
    """
    xlrd的方式写入excel文件,
    返回所有sheet表的list
    :param filepath:
    :return:
    """
    rb = xlrd.open_workbook(file_path)
    # 通过sheet_by_index()获取的sheet没有write()方法
    wb = copy(rb)
    # 通过get_sheet()获取的sheet有write()方法
    ws = wb.get_sheet(0)
    ws.write(0, 0, 'changed!')
    wb.save(file_path)


def write_xlsx(file_path):
    """

    :param file_path:
    :return:
    """
    wbk = xlwt.Workbook()
    sheet = wbk.get_sheet('123')
    # sheet = wbk.add_sheet('test_sheet')
    sheet.write(1, 1, 'test text')
    wbk.save(file_path)






def update_version():
    """
    更新header请求中版本号或者URL参数中的版本号
    更新数据库中字段,不一定非要更新
    :return:
    """


# def get_version():
#     """
#     获取PC首页APP发布的最新版本号
#     :return 获取最新的版本号
#     """
#     appversion = '0.0.0'
#     try:
#         r = requests.get('http://down.58.com/updateInfo.html?PGTID=0d000000-0000-0134-fec3-8c87e95574a9&ClickID=2',
#                          verify=False, allow_redirects=True, timeout=TIMEOUT_R)
#         if r.status_code == 200 and r.content != None:
#             soup = BeautifulSoup(''.join(str(r.content)))
#             content_after = soup.findAll("div", {"class": "content-ver"})[0]
#             # 获取PC首页第一个版本号
#             soup_div = BeautifulSoup(str(content_after))
#             for k in soup_div.findAll('div'):
#                 if k.string != None:
#                     appversion = '\n'.join(k.string.split()).replace("\n", ",").split(u'版本')[0]
#                     # 得到版本号
#                     return str(appversion.encode('utf-8'))
#     except Exception as e:
#         return appversion


def get_version():
    return "9.9.9"



def parse_url(obj):
    """
    遍历解析json的每个url元素， 将url的加入到list中
    """
    json_string = json.dumps(obj)
    python_obj = json.loads(json_string)
    try:
        if isinstance(python_obj, dict):
            for key, value in python_obj.items():
                # print key,value
                if key != r'' and re.match(r'^(http|https)://.*', str(value)):
                    # print "PARSED URL:         %s，%s" % (key, value)
                    url = url_local_hander(value, city)
                    sublist.append(url)  # 未过滤重复的二级url
                    # print "FIND URL : " + value
                elif key == r'action' and re.match(r'^(wbmain)://.*', str(value)):
                    # print"ACTION_INFO :     %s, %s" % (value, type(value))
                    content = urllib.unquote(value)
                    get_protocol = content[content.find('{'): content.rfind('}') + len('}')]
                    json_str = str_to_json(get_protocol)
                    finderurl = parse_json(json_str)
                    if finderurl != r'':
                        url = url_local_hander(finderurl, city)
                        sublist.append(url)  # 未过滤重复的二级url
                # 再次迭代查找
                parse_url(value)

        elif isinstance(python_obj, (list, tuple)):
            for el in obj:
                parse_url(el)
    except Exception, e:
        logger.error(e)


def get_url_list(obj):
    """
    获取解析一级url后的所有二级url列表
    :param obj:json数据
    :return
    :exception 返回空列表
    """
    try:
        parse_url(obj)
        return sublist
    except Exception, e:
        logger.error(e)







def change_url_version(url, version):
    """
    替换url中参数部分的cversion和version
    :param url:请求地址
    :param version: 版本号
    :return 返回替换的version的url
    :return 返回不替换的url
    :exception 返回不替换的url
    """
    try:
        if 'cversion' in str(url) or 'version' in str(url):
            paramslist = []
            for s in str(url).split('?')[1].split('&'):
                if s.startswith('cversion'):
                    ns = s.replace(s, 'cversion=%s' % version)
                    paramslist.append(ns)
                elif s.startswith('version'):
                    ns = s.replace(s, 'version=%s' % version)
                    paramslist.append(ns)
                else:
                    paramslist.append(s)
            return '?'.join((str(url).split('?')[0], '&'.join(paramslist)))
            # 替换版本号的url
        else:
            return url
    except Exception, e:
        logger.error(e)
        return url


def url_local_hander(url, replaceto, str_default=r'@local@'):
    """ 替换url中native端自定义的变量 @local@ 为当前城市 """
    # print "this url  : %s " % url
    if url.find(str_default) != -1:
        url = url.replace(str_default, replaceto)
    # if DEBUG:
    #    print url
    return url


def json_to_str(json_str):
    """ python json/dict 数据机构转换为 str"""
    json_str = json.dumps(json_str)
    return json_str


def str_to_json(string):
    """ python str 数据机构转换为 json结构"""
    data = json.loads(string)
    return data


def parse_json(obj):
    """ 遍历解析json的每个url元素， 将url的值写入文件"""
    try:
        if isinstance(obj, dict):
            # print SUBURL
            for key, value in obj.items():
                # print key, value
                if re.match(r'.*(_url)$|^(url)$', key):
                    # print "[Deep find:] %s, %s" % (key, value)
                    return value
        elif isinstance(obj, (list, tuple)):
            for el in obj:
                # print el
                parse_json(el)
        return ''
    except Exception, e:
        # raise e
        print str(e)
        return ''


def app_version():
    """
    获取app版本号通过正则表达式方式
    :return:
    """
    try:
        res = requests.get('http://down.58.com/updateInfo.html?PGTID=0d000000-0000-01dd-c2e4-a823ef7f5166&ClickID=2')
        with open('pagehtml.txt', 'w+') as f:
            f.write(res.content)
    except ValueError:
        return 'page open error'
    # 读取response结果，正则匹配出version
    try:
        page_info = open('pagehtml.txt').read()
        regexpr = re.compile(r"<div class=\"content-ver\">(.*)版本")
        version = regexpr.findall(page_info)
        return version[0]
    except:
        return "did not get version"
    finally:
        pass




def is_windows_system():
    """
    获取当前windows平台
    :return:
    """
    return 'Windows' in platform.system()


def is_linux_system():
    """
     获取当前linux平台
    :return:
    """
    return 'Linux' in platform.system()



def get_current_time():
    """
    获取当前时间
    :return:
    """
    return time.strftime("%Y-%m-%d %H:%M:%S")