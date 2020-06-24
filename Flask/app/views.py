from flask import jsonify
from app import app
from flask_cors import cross_origin
from app.models import Project,interfaces,cases,case_steps
from flask import request
from app.Utils.log import Logger
from app.Utils.timeUtils import format_time
from app.Utils.responseCode import *
from app.Utils.resObj import *
from app.Utils.Requests import typetransfer,loadtype,getreq,post_json,postform
from app import db
import json
from app.Utils.sqlcollects import *
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
    json_re = json.loads(data)
    apiname,apidesc,apiurl,belongpro,requestway,headerinfo,body,parameters=json_re['apiname'],json_re['apidesc'],json_re['apiurl'],json_re['belongpro'],json_re['requestway'],json_re['headerinfo'], \
    json_re['body'],json_re['parameters']

    pro = Project.query.filter_by(project_name=belongpro).first()
    proid=pro.id
    dicheader={}
    #请求头转换json
    for i in headerinfo:
        dicheader[i['key']]= i['value']
    #参数转换为json
    parameters=typetransfer(parameters)

    #body 转换为json
    api=interfaces(interface_name = apiname,
                interface_url = apiurl,
                belong_project = proid,
                method = requestway,
                interface_desc = apidesc,
                interface_header =json.dumps(dicheader),
                interface_body = body,
                interface_param =json.dumps(parameters) ,
                create_time = format_time(),
                update_time = format_time())

    print(api.interface_header)
    print(api.interface_body)
    print(api.interface_param)

    db.session.add(api)
    db.session.commit()
    dics={}
    dics['code'], dics['message']= 200, '添加成功'
    return jsonify(dics)



@app.route("/editapi",methods=['POST'])
@cross_origin()
def editapi():
    data = request.get_data()
    json_re = json.loads(data)
    id,apiname,apidesc,apiurl,belongpro,requestway,headerinfo,body,parameters=json_re['id'],json_re['apiname'],json_re['apidesc'],json_re['apiurl'],json_re['belongpro'],json_re['requestway'],json_re['headerinfo'], \
    json_re['body'],json_re['parameters']

    pro = Project.query.filter_by(project_name=belongpro).first()
    proid=pro.id
    dicheader={}
    #请求头转换json
    for i in headerinfo:
        dicheader[i['key']]= i['value']
    #参数转换为json
    parameters=typetransfer(parameters)
    api = interfaces.query.filter_by(id=id).first()
    api.interface_name = apiname
    api.interface_url = apiurl
    api.belong_project = proid
    api.method = requestway
    api.interface_desc = apidesc
    print("dicheader---->",dicheader)
    print('header---->',json.dumps(dicheader))
    api.interface_header = json.dumps(dicheader)
    api.interface_body = body
    api.interface_param = json.dumps(parameters)
    api.update_time = format_time()
    print (api)

    db.session.commit()
    dics={}
    dics['code'], dics['message']= 200, '修改成功'
    return jsonify(dics)

@app.route("/apis")
@cross_origin()
def apis():
    query,pagenum,pagesize=request.args.get("query"),request.args.get("pagenum"),request.args.get("pagesize")
    if query is None or query=='':
        apis=interfaces.query.paginate(page=int(pagenum),per_page=int(pagesize)).items
    else:
        apis = interfaces.query.filter_by(interface_name=query).paginate(page=int(pagenum),per_page=int(pagesize)).items
    apili=[]
    for api in apis:
        pro=Project.query.filter_by(id=api.belong_project).first()
        apidict=api.as_dict()
        apidict['belong_project']=pro.project_name
        apili.append(apidict)
    dics,apidics={},{}
    apidics["apis"],apidics["total"]=apili,len(apili)
    dics["code"],dics["message"],dics["data"]=200,"success",apidics
    return jsonify(dics)

@app.route("/getapiBypro",methods=['POST'])
@cross_origin()
def getapiBypro():
    data = request.get_data()
    json_re = json.loads(data)
    project_name = json_re["project_name"]
    apilist=db.session.execute(apiByprosql.format(project_name)).fetchall()
    print(apilist)
    key_li=[]
    for api in apilist:
        dict = {}
        dict['apiname']=api[0]
        key_li.append(dict)
    dics={}
    dics["code"], dics["message"], dics["data"] = 200, "success", {"apis":key_li}
    return jsonify(dics)


@app.route("/getapiByid",methods=['POST'])
@cross_origin()
def getapiByid():
    data = request.get_data()
    json_re = json.loads(data)
    id=json_re["id"]
    api=interfaces.query.filter_by(id=id).first()
    #请求头信息
    headers=json.loads(api.interface_header)
    headerkey=None
    for i in headers.keys():
        headerkey=i
    header_dcit={
        "key": headerkey,
        "value":headers[headerkey]
    }
    headerinfo=[]
    headerinfo.append(header_dcit)
    dics, apidics = {}, {}
    apiser=api.as_dict()
    apiser['interface_header']=headerinfo

    #请求参数信息

    paramsinfo=[]
    params=json.loads(api.interface_param)
    for pa in params.keys():
        param_dcit = {
            "key": pa,
            "value": params[pa],
            "type":loadtype(params[pa])
        }
        paramsinfo.append(param_dcit)
    apiser['interface_param'] = paramsinfo
    apidics["apis"]=apiser
    dics['code'], dics['message'],dics["data"] = 200, '查询成功',apidics
    return jsonify(dics)


@app.route("/delapiByid",methods=['POST'])
@cross_origin()
def delapiByid():
    data = request.get_data()
    json_re = json.loads(data)
    id=json_re["id"]
    api=interfaces.query.filter_by(id=id).first()
    db.session.delete(api)
    db.session.commit()
    reso = res(STATUS_OK, SUCCESS)
    return jsonSerialization(reso)


@app.route("/cases")
@cross_origin()
def getcases():
    query,pagenum,pagesize=request.args.get("query"),request.args.get("pagenum"),request.args.get("pagesize")
    if query is None or query=='':
        caselist=cases.query.paginate(page=int(pagenum),per_page=int(pagesize)).items
    else:
        caselist = cases.query.filter_by(case_name=query).paginate(page=int(pagenum),per_page=int(pagesize)).items
    casedict=[]
    for ca in caselist:
        casedict.append(ca.as_dict())
    dics,casedics={},{}
    casedics["cases"],casedics["total"]=casedict,len(casedict)
    dics["code"],dics["message"],dics["data"]=200,"success",casedics
    return jsonify(dics)




@app.route("/saveSteps",methods=['POST'])
@cross_origin()
def saveStep():
    data = request.get_data()
    json_re = json.loads(data)
    caseid,steps=json_re["id"],json_re['steps']
    case = cases.query.filter_by(id=caseid).first()
    casesteps=case_steps.query.filter_by(case_id=caseid).all()
    ids=[]
    for li in steps:
        ids.append(li['id'])

    for s in steps:
        id,belongpro,api,code,message,data=s['id'],s['belongpro'],s['api'],s['code'],s['message'],s['data']
        belong_project=Project.query.filter_by(project_name=belongpro).first().id
        case.belong_project=belong_project
        #用例表修改项目名称
        db.session.commit()
        st=case_steps.query.filter_by(id=id).first()
        api_id = interfaces.query.filter_by(interface_name=api).first().id  # 接口唯一
        assertion = json.dumps({"code": code, "message": message, "data": data})
        if(st is  None):
            #添加
            step = case_steps(
                api_id=api_id,
                case_id=caseid,
                assertion=assertion
            )
            db.session.add(step)
            db.session.commit()
        else:
            #修改
            st.api_id = api_id
            st.case_id = caseid
            st.assertion = assertion
            db.session.commit()
    #删除
    for cast in casesteps:
        if(cast.id not in ids):
            db.session.delete(cast)
            db.session.commit()
    reso = res(STATUS_OK, SUCCESS)
    return jsonSerialization(reso)



@app.route("/getSteps",methods=['POST'])
@cross_origin()
def getSteps():
    data = request.get_data()
    json_re =json.loads(data)
    caseid= json_re["id"]
    print (caseid)
    case = cases.query.filter_by(id=caseid).first()
    #查询项目
    belongpro=Project.query.filter_by(id=case.belong_project).first().project_name
    steplist=case_steps.query.filter_by(case_id=caseid).all()
    steps=[]
    for i in steplist:
        id,api,code,message,data=i.id,interfaces.query.filter_by(id=i.api_id).first().interface_name,json.loads(i.assertion)['code'],json.loads(i.assertion)['message'],json.loads(i.assertion)['data']
        apidict={}
        apidict['id'],apidict['belongpro'],apidict['api'],apidict['code'],apidict['message'],apidict['data']=id,belongpro,api,code,message,data
        steps.append(apidict)
    reso = res(STATUS_OK, SUCCESS,steps)
    return jsonSerialization(reso)


@app.route("/debugCase",methods=['POST'])
@cross_origin()
def debugCase():
    data = request.get_data()
    json_re = json.loads(data)
    caseid = json_re["id"]
    stepilist = db.session.execute(reqinfosql.format(caseid)).fetchall()
    #运行
    cod, resp,resli=None,None,[]
    for st in stepilist:
        stepid,interface_url,interface_body,interface_param,method,assertion,assertresult,result,ispass,interface_header=st[0],st[1],st[2],st[3],st[4],st[5],st[6],st[7],st[8],st[9]
        if str(method).upper()=="GET":
            code,resp=getreq(interface_url,json.loads(interface_param),headers=json.loads(interface_header))
        elif str(method).upper()=="POST":
            header_dict=json.loads(json.loads(interface_header))      #header转换成字典
            interface_body = json.loads(json.loads(interface_body))   #body转换成字典
            code, resp ,runInfo=post_json(interface_url,interface_body,header_dict)

        #写入请求结果
        resli.append(runInfo)
        st=case_steps.query.filter_by(id=stepid).first()
        st.result=runInfo
        db.session.commit()
        #校验

    print(code, resp)
    reso = res(STATUS_OK, SUCCESS,resli)
    return jsonSerialization(reso)












