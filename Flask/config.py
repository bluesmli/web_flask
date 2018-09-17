CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

import os,ConfigParser


def getDburl():
    cf =ConfigParser.ConfigParser()
    if os.getcwdu().find("tmp")!=-1:
        path=os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + ".")+os.path.sep+"db.ini"
    else:
        path=os.getcwd()+"/db.ini"
    print "  数据库路径",path
    cf.read(path)
    dburi = cf.get("database", "dbhost")
    print "数据库URL",dburi
    return dburi










basedir = os.path.abspath(os.path.dirname(__file__))
print basedir
SQLALCHEMY_DATABASE_URI = getDburl()
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS=True