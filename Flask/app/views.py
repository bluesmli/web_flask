#coding:utf-8
import  datetime

from flask import render_template, redirect, session, url_for, request, make_response

from app import app, db, models
from app.Utils.Requests import getReq,postReq
from form import LoginForm,registerForm,user_editForm,usermanegeForm,project_editForm,projectsForm,interface_testForm,interface_editForm
from models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html')


'''
-----用户管理------
'''
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    username=form.username.data
    form_password=form.password.data
    me=User.query.filter_by(user_name=username,password=form_password).first()
    if  request.method=='POST' and me:
            session["logged_in"] = True
            response=make_response(redirect(url_for('welcome',Name=username)))
            response.set_cookie("Name",username)
            return response
    else:
        return render_template('login.html')


@app.route('/register',methods = ['GET', 'POST'])
def register():
    form = registerForm()
    username=form.username.data
    password=form.password.data
    confirmpassword=form.confirmpassword.data
    me=User.query.filter_by(user_name=username).first()
    if  request.method=='POST':
        if me:
            return  render_template('login.html',form=form)
        elif password!=confirmpassword:
            print u'确认密码与输入密码不一致'
            return render_template('register.html')
        else:
            add=User(
              user_name=username,
              password=password,
              user_register_time=datetime.datetime.now()
            )
            db.session.add(add)
            db.session.commit()
            return  redirect(url_for('index'))
    return render_template('register.html')


@app.route('/welcome',methods=['GET', 'POST'])
def welcome():
    username=request.args['Name']
    if session["logged_in"]==True:
        return render_template("welcome.html",Name=username)


@app.route('/logout',methods=['GET','POST'])
def logout():
    if session["logged_in"]==True:
        session.pop('logged_in', None)
    return redirect(url_for('index'))

# @app.route('/userpage/<int:page>',methods=['GET','POST'])
@app.route('/userpage',methods=['GET','POST'])
def userpage():
    if session["logged_in"]==True:        
            pagination=models.User.query.paginate(int(request.args['page']), 13, False)
            user=pagination.items
            return render_template("user.html",users=user,pagination=pagination,Name=request.cookies['Name'])
    else:
        return redirect(url_for('index'))

@app.route('/usermanege',methods=['GET','POST'])
def usermanege():
    serach=''
    if session["logged_in"]==True:        
        if  request.method=='POST':
            form = usermanegeForm()
            username=form.username.data
            if username:
                pagination =User.query.filter_by(user_name=username).paginate(1, 13, False)
                users=pagination.items
                serach=True
            else:
                pagination =models.User.query.paginate(1, 13, False)
                users=pagination.items
            return render_template("user.html",
                                   users=users,
                                   Name=request.cookies['Name'],
                                   username=username,
                                   pagination=pagination,
                                   serach=serach)

        else:
            if str(request.url).find('page')==-1:
                pagination=models.User.query.paginate(1, 13, False)
                user=pagination.items
                return render_template("user.html",users=user,pagination=pagination,Name=request.cookies['Name'])
    else:
        return redirect(url_for('index'))

@app.route('/user_edit',methods=['GET','POST'])
@app.route('/user_edit/user_edit',methods=['GET','POST'])
def edit():
    form =user_editForm()
    username=form.username.data
    password=form.password.data
    uid=form.userid.data
    
    if session["logged_in"]==True :
        if request.method=='POST' and uid:
            me=User.query.filter_by(user_id=uid).first()
            me.user_name =username
            me.password=password
            db.session.commit()
        else:
            add=models.User(
              user_name=username,
              password=password,
              user_register_time= datetime.datetime.now()
            )
            db.session.add(add)
            db.session.commit()
        return redirect(url_for('usermanege'))
    return redirect(url_for('index'))


@app.route('/user_edit/<string:id>',methods=['GET','POST'])
def user_edit(id):
    me=User.query.filter_by(user_id=id).first()
    if session["logged_in"]==True:
        if me:
           return render_template("user_edit.html",Name=me.user_name,userid=id)
    return redirect(url_for('index'))


@app.route('/user_delete/<string:id>',methods=['GET','POST'])
def user_delete(id):
    user_id=id
    if session["logged_in"]==True:
        if user_id is not None and user_id!="":
             me=User.query.filter_by(user_id=user_id).first()
             if me:
                 db.session.delete(me)
                 db.session.commit()
             return redirect(url_for('usermanege'))
    return redirect(url_for('index'))


@app.route('/user_add',methods=['GET','POST'])
def user_add():
    if session["logged_in"]==True:
            return render_template("user_edit.html")
    return redirect(url_for('index'))


'''
-----项目管理------
'''

@app.route('/projects',methods=['GET','POST'])
def projects():
    if session["logged_in"]==True:
        if request.method=='POST':
            form = projectsForm()
            name=form.projectname.data
            print name,
            if name:
                pagination =models.Models.query.filter_by(name=name).paginate(1, 13, False)
                Models=pagination.items
                serach=True
            else:
                pagination =models.Models.query.paginate(1, 13, False)
                Models=pagination.items
            return render_template("projects.html",
                                   Models=Models,
                                   pagination=pagination,
                                   Name=request.cookies['Name'])
        else:
            if str(request.url).find('page')==-1:
                pagination=models.Models.query.paginate(1, 13, False)
                Models=pagination.items
                return render_template("projects.html",Models=Models,pagination=pagination,Name=request.cookies['Name'])
    else:
        return redirect(url_for('index'))

@app.route('/project_edit/<string:id>',methods=['GET','POST'])
def project_edit(id):
    me=models.Models.query.filter_by(id=id).first()
    if session["logged_in"]==True:
        if me:
           return render_template("project_edit.html",Name=me.name,id=id)
    return redirect(url_for('index'))

@app.route('/project_del/<string:id>',methods=['GET','POST'])
def project_del(id):
    pro_id=id
    if session["logged_in"]==True:
        if pro_id is not None and pro_id!="":
             me=models.Models.query.filter_by(id=pro_id).first()
             if me:
                 db.session.delete(me)
                 db.session.commit()
             return redirect(url_for('projects'))
    return redirect(url_for('index'))


@app.route('/project_edit',methods=['GET','POST'])
@app.route('/project_edit/project_edit',methods=['GET','POST'])
def projectsEdit():
    form =project_editForm()
    name=form.name.data

    status=form.status.data
    print name,status
    if status==u'未开始':
        status=0
    elif status==u'已开始':
        status=1
    elif status==u'测试中':
        status=2
    else:
        status=3
    print name,status
    id=form.id.data   
    if session["logged_in"]==True:
        if request.method=='POST' and id:
            me=models.Models.query.filter_by(id=id).first()
            me.name =name
            me.status=status
            db.session.commit()
        else:
            add=models.Models(
              name=name,
              status=status,
            )
            db.session.add(add)
            db.session.commit()
        return redirect(url_for('projects'))
    return redirect(url_for('index'))

@app.route('/project_page',methods=['GET','POST'])
def project_page():
    if session["logged_in"]==True:        
            pagination=models.Models.query.paginate(int(request.args['page']), 13, False)
            Models=pagination.items
            return render_template("projects.html",Models=Models,pagination=pagination,Name=request.cookies['Name'])
    else:
        return redirect(url_for('index'))



@app.route('/project_add',methods=['GET','POST'])
def project_add():
    if session["logged_in"]==True:
            return render_template("project_edit.html")
    return redirect(url_for('index'))


@app.route('/interfaces_test',methods=['GET','POST'])
def interfaces_test():
    if session.has_key('logged_in'):
        if session["logged_in"]==True:
            projects=models.Models.query.all()
            if request.method=='POST':
                #获取表单数据
                form=interface_testForm()
                bool_redict=form.bool_redict.data
                requestheader=form.requestheader.data
                url=form.URl.data
                transaction_way=form.transaction_way.data
                Param=form.parameter.data
                print bool_redict,url,Param
                #判断重定向
                redict=True if bool_redict==u'是' else False
                #根据获取到的数据设置请求头及cookie
                Head={}
                cookies={}
                if requestheader is not None and requestheader!='':
                     for head  in str(requestheader).split('\r\n'):
                         if head.split(':')[0]=='Cookie' and head.split(':')[1]:
                             if head.split(':')[1].find(';')==-1:
                                 cookies[head.split(':')[1].split('=')[0]]=head.split(':')[1].split('=')[1]
                             else:
                                 for ck in head.split(':')[1].split(';'):
                                     print ck
                                     if ck and ck!='':
                                        cookies[ck.split('=')[0].strip()]=ck.split('=')[1].strip()
                         else:
                             Head[head.split(':')[0]]=head.split(':')[1]
                print '请求头 headers:',Head
                print 'cookies:',cookies
                tmp=''
                #判断传输方式
                if transaction_way=='GET':
                    print  getReq(url,redict,Head,cookies)
                    content,headers,req=getReq(url,redict,Head,cookies)
                if transaction_way=='POST':
                    content,headers,req=postReq(url,Param,redict,Head,cookies)
                for k,v in headers.items():
                    tmp=tmp+k+'='+v+'\n'
                #print content,url,req.encoding
                return render_template('interface.html',
                                        Name=request.cookies['Name'],
                                        project=projects,
                                        response=content,
                                        headers=tmp,
                                        URL=url,
                                        requestheader=requestheader,
                                        p=Param)
            else:
                return render_template('interface.html',Name=request.cookies['Name'],project=projects)
    else:
        return redirect(url_for('index'))

'''
**************************************接口管理**********************************************
'''

@app.route('/interfacemanage',methods=['GET','POST'])

def interfacemanage():
    if session.has_key('logged_in'):
        if session["logged_in"]==True:
            if request.method=='POST':
                form=interface_editForm()
                projectsName='' if form.projectsName.data is None else form.projectsName.data
                InterfaceName='' if form.InterfaceName.data is None else form.InterfaceName.data
                InterFaceUrl='' if form.InterFaceUrl.data is None else form.InterFaceUrl.data
                param='' if form.param.data is None else form.param.data
                way='' if form.way.data is None else form.way.data
                header='' if form.header.data is None else form.header.data
                cookie='' if form.cookie.data is None else form.cookie.data

                add=models.Interfaces(
                  interface_name=InterfaceName,
                  interface_url=InterFaceUrl,
                  projects_name=projectsName,
                  interface_param=param,                                #接口参数
                  interface_way=way,                                 #方法
                  interface_header=header,                                 #头信息
                  interface_cookie=cookie

                )
                db.session.add(add)
                db.session.commit()
            pagination=models.Interfaces.query.paginate(1, 13, False)
            interfaces=pagination.items
            print interfaces
            return render_template("interfaceManage.html",
                                    interfaces=interfaces,
                                    pagination=pagination,
                                    Name=request.cookies['Name'])
    else:
        return redirect(url_for('index'))


@app.route('/interfacespage',methods=['GET','POST'])
def interfacespage():
    if session["logged_in"]==True:        
            pagination=models.Interfaces.query.paginate(int(request.args['page']), 13, False)
            interfaces=pagination.items
            return render_template("interfaceManage.html",
            	interfaces=interfaces,
            	pagination=pagination,
            	Name=request.cookies['Name'])

    else:
        return redirect(url_for('index'))

@app.route('/interface_add',methods=['GET','POST'])
def interface_add():
    if session["logged_in"]==True:
            return render_template("interface_edit.html")
    return redirect(url_for('index'))






















