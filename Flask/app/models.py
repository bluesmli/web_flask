
from app import db
import datetime
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