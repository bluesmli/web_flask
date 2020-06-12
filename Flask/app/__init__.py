from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
#must after other definition
from app import views,models