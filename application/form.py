from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField,HiddenField, BooleanField
from wtforms.validators import DataRequired,EqualTo
from hashlib import sha256
from .models import User

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField()

    def get_authenticated_user(self):
    	user = User.query.get(self.username.data)
    	if user is None:
    		return None
    	m = sha256()
    	m.update(self.password.data.encode())
    	passwd = m.hexdigest()
    	return user if passwd == user.password else None


class NewUserForm(FlaskForm):
    username = StringField("Nom d'utilisateur",validators=[DataRequired(message="Vous devez entrer un nom d'utilisateur")])
    password = PasswordField("Mot de passe", validators=[DataRequired(), EqualTo('pwconfirmation', message='Votre mot de passe ne correspond pas à la confirmation')])
    pwconfirmation = PasswordField("Confirmation", validators=[DataRequired(), EqualTo('pwconfirmation', message='La confirmation ne correspond pas à votre mot de passe')])
    spambox = BooleanField("Je souhaite recevoir les offres des partenaires de FL45K-MU51C", default="checked")
    next = HiddenField()
