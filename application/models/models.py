import yaml,os.path
from application.app import db
from flask-login import UserMixin

class User(db.Model,UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))

    def get_id(self):
        return self.username
