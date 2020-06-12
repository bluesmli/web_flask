from flask import jsonify
from app import app
from flask_cors import cross_origin
from app.models import Project
from flask import request
from app.Utils.log import Logger
from app.Utils.timeUtils import format_time
from app.Utils.responseCode import *
from app.Utils.resObj import *
from app import db
import json

infolog = Logger(u'info.log', level=u'info')
errorlog = Logger(u'error.log', level=u'error')

@app.route('/')
@app.route('/index')
def index():
    return "hello world"


@app.before_request
def before_request():
    infolog.logger.info("请求地址------>{}".format(str(request.path)))
    infolog.logger.info("请求方法------>{}" .format(str(request.method)))
    infolog.logger.info("|------请求headers--start----|")
    infolog.logger.info(str(request.headers).rstrip())
    infolog.logger.info("|------请求headers--end------|")
    infolog.logger.info("GET参数------>{}".format(str(request.args)))
    infolog.logger.info("POST参数------{}".format(str(request.get_json())))




@app.route("/projects")
@cross_origin()
def projects():
    query,pagenum,pagesize=request.args.get("query"),request.args.get("pagenum"),request.args.get("pagesize")
    if query is None or query=='':
        prolist=Project.query.paginate(page=int(pagenum),per_page=int(pagesize)).items
    else:
        prolist = Project.query.filter_by(project_name=query).paginate(page=int(pagenum),per_page=int(pagesize)).items
    prodict=[]
    for pro in prolist:
        prodict.append(pro.as_dict())
    dics,prodics={},{}
    prodics["projects"],prodics["total"]=prodict,len(prodict)
    dics["code"],dics["message"],dics["data"]=200,"success",prodics
    return jsonify(dics)


@app.route("/allprojects",methods=['GET'])
@cross_origin()
def allprojects():
    prolist=Project.query.all()
    prodict=[]
    for pro in prolist:
        prodict.append(pro.as_dict())
    dics,prodics={},{}
    prodics["projects"],prodics["total"]=prodict,len(prodict)
    dics["code"],dics["message"],dics["data"]=200,"success",prodics
    return jsonify(dics)


@app.route("/addproject",methods=['POST'])
@cross_origin()
def addproject():
    data = request.get_data()
    json_re = json.loads(data)
    project_name,project_desc=json_re["project_name"],json_re["project_desc"]
    pro=Project(project_name=project_name,project_desc=project_desc,create_time=format_time(),update_time=format_time())
    db.session.add(pro)
    db.session.commit()
    reso = res(STATUS_OK, SUCCESS)
    return jsonSerialization(reso)

@app.route("/delproByid",methods=['POST'])
@cross_origin()
def delproByid():
    data = request.get_data()
    json_re = json.loads(data)
    id=json_re["id"]
    pro=Project.query.filter_by(id=id).first()
    db.session.delete(pro)
    db.session.commit()
    reso = res(STATUS_OK, SUCCESS)
    return jsonSerialization(reso)


@app.route("/getproByid",methods=['POST'])
@cross_origin()
def getproByid():
    data = request.get_data()
    json_re = json.loads(data)
    id=json_re["id"]
    pro=Project.query.filter_by(id=id).first()
    dics, prodics = {}, {}
    prodics["projects"]=pro.as_dict()
    dics['code'], dics['message'],dics["data"] = 200, '查询成功',prodics
    return jsonify(dics)



@app.route("/editProject",methods=['POST'])
@cross_origin()
def editProject():
    data = request.get_data()
    json_re = json.loads(data)
    id,project_name,project_desc=json_re["id"],json_re["project_name"],json_re["project_desc"]

    pro=Project.query.filter_by(id=id).first()
    pro.project_name=project_name
    pro.project_desc=project_desc
    db.session.commit()
    reso=res(STATUS_OK,SUCCESS)
    return jsonSerialization(reso)


'''
#################接口管理#################
'''


@app.route("/addapi",methods=['POST'])
@cross_origin()
def addapi():
    data = request.get_data()
    print(data)
    json_re = json.loads(data)
    print(json_re['body'])
    dics={}
    dics['code'], dics['message']= 200, '添加成功'
    return jsonify(dics)



















