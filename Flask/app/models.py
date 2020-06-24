
from app import db
ROLE_USER = 0
ROLE_ADMIN = 1


class Project(db.Model):
    '''
    项目表
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name=db.Column(db.String(40))
    project_desc=db.Column(db.String(40))
    create_time=db.Column(db.DateTime)
    update_time=db.Column(db.DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class interfaces(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interface_name = db.Column(db.String(255))
    interface_url = db.Column(db.String(255))
    belong_project=db.Column(db.Integer)
    method=db.Column(db.String(255))
    interface_desc=db.Column(db.String(255))
    interface_header=db.Column(db.JSON)
    interface_body=db.Column(db.JSON)
    interface_param=db.Column(db.JSON)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class cases(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    belong_project = db.Column(db.Integer)
    case_desc=db.Column(db.String(255))
    interfaces=db.Column(db.String(255))
    case_name=db.Column(db.String(255))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    ispass=db.Column(db.String(255))
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class case_steps(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_id=db.Column(db.Integer)
    case_id=db.Column(db.Integer)
    assertion=db.Column(db.String(255))
    result=db.Column(db.String(5000))
    assertresult=db.Column(db.Integer)