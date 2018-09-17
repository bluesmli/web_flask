#coding:utf-8
from app import db
import datetime
ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    user_name = db.Column(db.String(64), unique = True)                     #用户名
    password = db.Column(db.String(64))                                     #密码
    user_register_time=db.Column(db.DateTime)                               #注册时间
    def __init__(self,user_name,password,user_register_time):
        self.user_name = user_name
        self.password=password
        self.user_register_time=user_register_time

class Models(db.Model):
    id=db.Column(db.Integer, primary_key = True,autoincrement=True)
    name=db.Column(db.String(64), unique = True)                            #项目名称
    status = db.Column(db.Integer)                                          #状态
    developer = db.Column(db.String(50))  # 用户名
    tester = db.Column(db.String(50))





class Interfaces(db.Model):
    id=db.Column(db.Integer, primary_key = True,autoincrement=True)
    interface_name=db.Column(db.String(64), unique = True)                  #接口名称
    projects_name=db.Column(db.String(64))                                  #项目名称
    interface_url=db.Column(db.String(100))                                 #url地址
    interface_param=db.Column(db.String(100))                               #接口参数
    interface_way=db.Column(db.String(10))                                  #方法
    interface_header=db.Column(db.String(100))                              #头信息
    interface_cookie=db.Column(db.String(100))                              #cookie
    Assertion=db.Column(db.String())
    caseName=db.Column(db.String(100))

class Case(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)    #用例ID
    CaseName=db.Column(db.String(64),unique=True)                   #用例名称
    CaseDesciption=db.Column(db.String(64))                         #用例描述
    ProjectsName=db.Column(db.String(64))                           #项目名称
    CaseUrl=db.Column(db.String(64))                                #case文件保存的路径
    CaseSatus=db.Column(db.Integer)                                 #case状态(None 未运行,0:失败,1:成功)
    RunDate=db.Column(db.DateTime)                                  #case运行时间
    #InterFaces=db.relationship('Interfaces', backref='interface_name', lazy=True)












