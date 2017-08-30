#coding:utf-8
from app import db
import datetime
ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    user_name = db.Column(db.String(64), unique = True)                     #用户名
    password = db.Column(db.String(64))                                     #密码
    # status=db.column(db.Integer)                                            #状态
    user_register_time=db.Column(db.DateTime)                               #注册时间
    def __init__(self,user_name,password,user_register_time):
        self.user_name = user_name
        self.password=password
        self.user_register_time=user_register_time


class Models(db.Model):
    id=db.Column(db.Integer, primary_key = True,autoincrement=True)
    name=db.Column(db.String(64), unique = True)                            #项目名称
    status = db.Column(db.Integer)                                          #状态

class Interfaces(db.Model):
    id=db.Column(db.Integer, primary_key = True,autoincrement=True)
    interface_name=db.Column(db.String(64), unique = True)                  #接口名称
    projects_name=db.Column(db.String(64))                                  #项目名称
    interface_url=db.Column(db.String(100))                                 #地址
    interface_param=db.Column(db.String(100))                                 #接口参数
    interface_way=db.Column(db.String(10))                                 #方法
    interface_header=db.Column(db.String(100))                                 #头信息
    interface_cookie=db.Column(db.String(100))                                 #cookie






