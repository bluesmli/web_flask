CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

import os,configparser


def getDburl():
    cf =configparser.ConfigParser()
    if os.getcwd().find("tmp")!=-1:
        path=os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + ".")+os.path.sep+"db.ini"
    else:
        path=os.getcwd()+"/db.ini"

    cf.read(path)
    dburi = cf.get("database", "dbhost")
    return dburi

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = getDburl()
SQLALCHEMY_TRACK_MODIFICATIONS=True