from flask_wtf.file import FileField, FileRequired
from hashlib import sha256
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, HiddenField, BooleanField, IntegerField, SelectMultipleField, \
	SubmitField
from wtforms.validators import DataRequired, EqualTo, Optional
from wtforms.widgets import ListWidget, CheckboxInput
from .models import User, Artiste, ajouter_artiste


################################ CODE EXTERNE ##################################

################################
# SOURCE : http://stackoverflow.com/questions/18188428/dynamic-forms-formsets-in-flask-wtforms
# NB : Pour l'implementation, d'autres extraits du code de cette page sont
# dans views.py et dans le template album-form.html. Les variables sont renommées
# mais l'idée de l'extrait reste la même
class MultiCheckboxField(SelectMultipleField):
	"""
	A multiple-select, except displays a list of checkboxes.

	Iterating the field will produce subfields, allowing custom rendering of
	the enclosed checkbox fields.
	"""
	widget = ListWidget(prefix_label=False)
	option_widget = CheckboxInput()


	# La méthode suivante est *temporaire*. Sans, le formulaire ne valide pas.
	def pre_validate(self, form):
		""" Desactive la pre validation """


################################

################################ FIN CODE EXTERNE ##################################

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
	username = StringField("Nom d'utilisateur",
						   validators=[DataRequired(message="Vous devez entrer un nom d'utilisateur")])
	password = PasswordField("Mot de passe", validators=[DataRequired(), EqualTo('pwconfirmation',
																				 message='Votre mot de passe ne correspond pas à la confirmation')])
	pwconfirmation = PasswordField("Confirmation", validators=[DataRequired(), EqualTo('pwconfirmation',
																					   message='La confirmation ne correspond pas à votre mot de passe')])
	spambox = BooleanField("Je souhaite recevoir les offres des partenaires de FL45K-MU51C", default="checked")
	next = HiddenField()


class AlbumForm(FlaskForm):

	def validate_genres(self, genres):
		return True

	album_id = HiddenField()
	title = StringField("Titre de l'album", validators=[DataRequired(message="Vous devez entrer un titre d'album")])
	releaseyear = IntegerField("Année de sortie", validators=[DataRequired(message="Vous devez entrer une année de sortie")])
	artist = StringField("Artiste", validators=[DataRequired(message="Vous devez entrer un nom d'artiste")])
	img = StringField('Chemin vers Image')
	genres = MultiCheckboxField(choices=[], coerce=int, validators=[Optional()])
	genre_add = StringField("Autre genre")
	submit_btn = SubmitField("Valider")
	next = HiddenField()

	def get_artist_id(self):
		"""
		retourne l'id_artiste d'un nouvel artiste
		créé en fonction de l'input utilisateur
		"""
		artiste = Artiste.query.filter_by(nom_artiste=self.artist.data).first()
		if artiste is None:
			new_artist = ajouter_artiste(self.artist.data)
		else:
			new_artist = artiste
		return new_artist.id_artiste

	def upload(self, request):
		""" Upload le fichier image du formulaire dans static/img """
		if self.data.img:
			image_data = request.FILES[self.img.name].read()

			from application.app import mkpath
			open(mkpath("static/img/" + self.img.data), 'w').write(image_data)




