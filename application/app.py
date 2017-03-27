import os.path
from flask import Flask
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__),p))

app = Flask(__name__)
app.debug = True
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
manager = Manager(app)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']=('sqlite:///'+mkpath('../tuto.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# app. config ['SECRET_KEY'] = "5598d6910d68379ae752d2dc58c919be"
