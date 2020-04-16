#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os
import requests
import json
import logging
import logzero
import time
import copy
from redis import Redis
from logzero import logger
from logzero import setup_logger
from datetime import timedelta
from werkzeug.utils import secure_filename
from flask import Flask,make_response,request,redirect,url_for
from flask import Flask, session
from flask_session import Session
from flask_script import Manager
from flask import jsonify,Response,send_file
from flask import make_response, jsonify, Blueprint, abort
from configparser import ConfigParser
from flask import Flask, request
from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user,current_user
from flask_mail import Mail, Message
from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from flask_script import Manager
from config import *



logger = setup_logger(name="backend", logfile= logger_log_path, level=logging.INFO)

# Set a custom formatter
formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s')
logzero.formatter(formatter)

blue = Blueprint('app_page',__name__)



class Config(object):
      """配置参数"""
      SQLALCHEMY_DATABASE_URI = 'sqlite:///' + sqlite_path
      #设置sqlalchemy自动跟踪数据库
      SQLALCHEMY_TRACE_MODIFICATIONS = True





def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SESSION_KEY_PREFIX'] = 'flask'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 设置session的保存时间。
    manager = Manager(app)
    sess = Session(app)
    sess.init_app(app)
    app.debug = True
    return app


app = create_app()
app.debug = False
app.config.from_object(Config)


db = SQLAlchemy(app) #初始化数据库
db.create_all()




@app.route('/ping', methods=['GET'])
def ping():
    logger.info('ping')
    return 'ping ok'



@app.before_request
def before_request():
    logger.info('before_request ==>')



@app.route('/add',methods=['POST'])
def add():
    params = json.loads(request.get_data())
    logger.info(params)
    apiinfo = ApiInfo(**params)
    db.session.add(apiinfo)
    db.session.commit()
    return '保存数据成功 ==>'



@app.after_request
def after_request(response):
    logger.info('after_request ==>')
    result = copy.copy(response.response)
    try:
        if isinstance(result[0], bytes):
            result[0] = bytes.decode(result[0])
        logger.info('url:{} ,method:{},返回数据:{}'.format(request.url, request.method, json.loads(result[0])))
    except Exception as e:
        logger.info(e)
        logger.info('url:{} ,method:{}'.format(request.url, request.method))
    return response


@app.teardown_request
def teardown_request(exception):
    logger.info('teardown_request ==>')





class ApiInfo(db.Model):

    __tablename__ = 't_api_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interface_name = db.Column(db.String(300), unique=False)
    url = db.Column(db.String(300), unique=False)
    method = db.Column(db.String(300), unique=False)
    header = db.Column(db.String(300), unique=False)
    response = db.Column(db.String(300), unique=False)
    assert_params = db.Column(db.String(300), unique=False)
    issue = db.Column(db.String(300), unique=False)
    status_code = db.Column(db.String(300), unique=False)
    usd_time = db.Column(db.String(300), unique=False)
    time_stamp = db.Column(db.String(300), unique=False)


    def __init__(self, interface_name, url,method,header,response,assert_params,issue,status_code,usd_time,time_stamp):

        self.interface_name = interface_name
        self.url = url
        self.method = method
        self.header = header
        self.response = response
        self.assert_params = assert_params
        self.issue = issue
        self.status_code = status_code
        self.usd_time = usd_time
        self.time_stamp = time_stamp


db.create_all()

manager = Manager(app)
manager.add_command('clean', Clean())
manager.add_command('url', ShowUrls())
manager.add_command('server', Server(host=server_host,
                                     port=server_port,
                                     use_debugger=False
                                     )
                    )




@manager.command
def deploy():
    """Run deployment tasks."""
    pass


@manager.command
def myprint():
    logger.info('hello world...')


#创建数据库脚本
@manager.command
def create_db():
    db.create_all()


def start_manager():
    manager.run(default_command='server')


