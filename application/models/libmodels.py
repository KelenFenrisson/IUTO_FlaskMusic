from flask_login import UserMixin
from sqlalchemy import and_, text

from application import db, login_manager


@login_manager.user_loader
def load_user(username):
	return User.query.get(username)


class User(db.Model, UserMixin):
	username = db.Column(db.String(50), primary_key=True)
	password = db.Column(db.String(64))

	def get_id(self):
		return self.username


class Album_Genre(db.Model):
	id_album_genre = db.Column(db.Integer, primary_key=True)
	id_album = db.Column(db.Integer, db.ForeignKey("album.id_album"))
	nom_genre = db.Column(db.String, db.ForeignKey("genre.nom_genre"))
	album = db.relationship("Album", backref=db.backref("album_genre", lazy="dynamic"))
	genre = db.relationship("Genre", backref=db.backref("album_genre", lazy="dynamic"))


class Album(db.Model):
	id_album = db.Column(db.Integer, primary_key=True)
	titre_album = db.Column(db.String(50))
	annee_album = db.Column(db.Integer)
	img_album = db.Column(db.String(100))
	id_artiste = db.Column(db.Integer, db.ForeignKey("artiste.id_artiste"))
	artiste = db.relationship("Artiste", backref=db.backref("albums", lazy="dynamic"))

	def __repr__(self):
		return "<Album (%d) %s>" % (self.id_album, self.titre_album)


class Artiste(db.Model):
	id_artiste = db.Column(db.Integer, primary_key=True)
	nom_artiste = db.Column(db.String(100))

	def __repr__(self):
		return "<Artiste (%d) %s>" % (self.id_artiste, self.nom_artiste)


class Genre(db.Model):
	nom_genre = db.Column(db.String(100), primary_key=True)

	def __repr__(self):
		return "<Genre %s >" % self.nom_genre


def get_artistes():
	return Artiste.query.all()


def get_albums():
	return Album.query.all()


def get_albums_par_artiste(id_artiste):
	return Album.query.filter_by(id_artiste=id_artiste).all()


def get_albums_par_genre(nom_genre):
	genre = Genre.query.filter_by(nom_genre=nom_genre).first()
	albums = []
	for al_ge in genre.album_genre:
		albums.append(Album.query.get(al_ge.id_album))
	return albums


def get_genres():
	return Genre.query.all()


def ajouter_artiste(nomartiste):
	db.session.add(Artiste(nom_artiste=nomartiste))
	db.session.commit()
	return Artiste.query.filter(nom_artiste=nomartiste).first()


def ajouter_album(titre, annee, image, idartiste):
	db.session.add(Album(titre_album=titre, annee_album=annee, img_album=image, id_artiste=idartiste))
	db.session.commit()
	return Album.query.filter(and_(text("titre_album='{0}'".format(titre)), text("id_artiste='{0}'".format(idartiste)))).first()


def ajouter_genre(nomgenre):
	db.session.add(Genre(nom_genre=nomgenre))
	db.session.commit()
	return Genre.query.get(nomgenre)


def ajouter_album_genre(idalbum, nomgenre):
	db.session.add(Album_Genre(id_album=idalbum, nom_genre=nomgenre))
	db.session.commit()
	return Album_Genre.query.filter(and_(text("id_album={0}".format(idalbum)), text("nom_genre='{0}'".format(nomgenre)))).first()
