#!/usr/bin/env python
# -*- coding:utf-8 -*-


import time
import threading
import Queue
from logzero import logger
from src.common import *
from src.sendrequests import main_requests
import yaml
from src.server import *
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from src.esuntils import EsUntils
from src.config import *


EsUntils(es_index_name).create_index()
# 创建索引


def server_task():
    start_manager()


t = threading.Thread(target=server_task, name='ServerThread')
t.start()

time.sleep(lanuch_server_time)

logger.info("接口监控脚本 ==> 启动")
start_time = time.time()
start_timestamps = time.strftime("%Y-%m-%d %H:%M:%S")



def api_job(id='api_job'):
    """
    定时任务
    :param id:
    :return:
    """
    current_path = os.path.abspath(os.path.dirname(__file__))
    logger.info(current_path)
    with open(current_path + '/cases/' + 'case.yaml', 'r') as f:
        temp = yaml.load(f.read())
        for t in temp:
            main_requests(method=t['test']['request']['method'],
                          interface_name=t['test']['name'],
                          url=t['test']['request']['url'],
                          header=t['test']['request']['headers'],
                          params={},
                          assert_params={})

    end_time = time.time()
    diff = (end_time - start_time)
    endtime_stamps = time.strftime("%Y-%m-%d %H:%M:%S")
    import src.sendrequests
    logger.info("接口监控脚本 ==> 结束" + '\n' + '本次共监控接口 ==> {}个'.format(src.sendrequests.request_count))


scheduler = BlockingScheduler()
scheduler.add_job(api_job,args=['job_once_now',],trigger='interval',seconds=interval_time, id='my_job_id_test',)
scheduler.start()



os._exit(0)






