from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    password=StringField('password',validators=[DataRequired])

class registerForm(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    password=StringField('password',validators=[DataRequired])
    confirmpassword=StringField('password',validators=[DataRequired])

class user_editForm(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    password=StringField('password',validators=[DataRequired])
    userid=StringField('userid',validators=[DataRequired])

class usermanegeForm(FlaskForm):
    username=StringField('username',validators=[DataRequired()])

class project_editForm(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    status=StringField('status',validators=[DataRequired])
    id=StringField('id',validators=[DataRequired])

class projectsForm(FlaskForm):
    projectname=StringField('projectname',validators=[DataRequired()])


class interface_testForm(FlaskForm):
    interface_name=StringField('interface_name',validators=[DataRequired()])
    domain=StringField('domain',validators=[DataRequired()])
    parameter=StringField('parameter')
    port=StringField('port')
    URl=StringField('URl',validators=[DataRequired()])
    requestheader=StringField('requestheader',validators=[DataRequired()])
    transaction_way=StringField('transaction_way',validators=[DataRequired()])
    bool_redict=StringField('bool_redict',validators=[DataRequired()])
    ResponseHeader=StringField('ResponseHeader',validators=[DataRequired()])
    response=StringField('response',validators=[DataRequired()])

class interface_editForm(FlaskForm):
    interid=StringField('interid',validators=[DataRequired()])
    projectsName=StringField('projectsName',validators=[DataRequired()])
    InterfaceName=StringField('InterfaceName',validators=[DataRequired()])
    InterFaceUrl=StringField('InterFaceUrl',validators=[DataRequired()])
    param=StringField('param')
    way=StringField('way',validators=[DataRequired()])
    header=StringField('header')
    cookie=StringField('cookie')

class interface_serachForm(FlaskForm):
    projectname=StringField('projectname',validators=[DataRequired()])


class CaseForm(FlaskForm):
    Casename=StringField('Casename',validators=[DataRequired()])
    CaseDes=StringField('CaseDes',validators=[DataRequired()])
    projects=StringField('projects',validators=[DataRequired()])

class CaseInterFaceSaveForm(FlaskForm):
    URL=StringField('URL',validators=[DataRequired()])
    requestheader=StringField('requestheader')
    parameter=StringField('parameter')
    transaction_way=StringField('transaction_way')
    bool_redict=StringField('bool_redict')
    jurge=StringField('jurge')
    caseName=StringField('caseName')
    InterfaceName=StringField('InterfaceName')

class CaseSerachForm(FlaskForm):
    Casename=StringField('casename',validators=[DataRequired()])
